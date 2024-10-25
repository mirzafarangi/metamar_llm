"""
Enhanced Claude integration handler for Meta-Mar
"""

from anthropic import Anthropic
from typing import Dict, Any, Optional
from ..config.settings import settings
import logging
import json

logger = logging.getLogger(__name__)

class ClaudeHandler:
    """Handles interactions with Claude API"""
    
    def __init__(self):
        """Initialize Claude handler with settings"""
        self.client = Anthropic()
        self.settings = settings.llm_settings['claude']
    
    def generate_report(
        self,
        meta_analysis_results: Dict[str, Any],
        analysis_type: str,
        meta_settings: Dict[str, Any],
        custom_instructions: Optional[str] = None
    ) -> str:
        """
        Generate meta-analysis report using Claude
        
        Args:
            meta_analysis_results: Dictionary containing meta-analysis results
            analysis_type: Type of meta-analysis ('continuous', 'binary', 'generic', 'correlation')
            meta_settings: Meta-analysis settings used
            custom_instructions: Optional additional instructions
            
        Returns:
            str: Generated report text
        """
        try:
            prompt = self._create_prompt(
                meta_analysis_results,
                analysis_type,
                meta_settings,
                custom_instructions
            )
            
            message = self.client.messages.create(
                model=self.settings['model'],
                max_tokens=self.settings['max_tokens'],
                messages=[{"role": "user", "content": prompt}]
            )
            
            return message.content[0].text
            
        except Exception as e:
            logger.error(f"Error generating Claude report: {str(e)}")
            raise
    
    def _create_prompt(
        self,
        results: Dict[str, Any],
        analysis_type: str,
        meta_settings: Dict[str, Any],
        custom_instructions: Optional[str]
    ) -> str:
        """Create structured prompt for Claude"""
        
        type_specific_guidance = {
            'continuous': {
                'focus': "mean differences and standardized effects",
                'key_metrics': "means, standard deviations, and standardized differences",
                'interpretation': "magnitude and direction of continuous outcomes"
            },
            'binary': {
                'focus': "event rates and risk measures",
                'key_metrics': "event counts, risk ratios, and odds ratios",
                'interpretation': "relative and absolute risk differences"
            },
            'generic': {
                'focus': "generic effect sizes",
                'key_metrics': "standardized effects and variance measures",
                'interpretation': "effect size magnitude and precision"
            },
            'correlation': {
                'focus': "correlation patterns",
                'key_metrics': "correlation coefficients and Fisher's z-values",
                'interpretation': "strength and direction of relationships"
            }
        }
        
        guidance = type_specific_guidance.get(analysis_type, {})
        
        prompt = f"""As a meta-analysis expert, analyze these {analysis_type} meta-analysis results.

Study Focus: {guidance.get('focus')}
Key Metrics: {guidance.get('key_metrics')}
Interpretation Focus: {guidance.get('interpretation')}

Analysis Configuration:
- Summary Measure: {meta_settings['summary_measure']}
- Model Type: {meta_settings['pooling_method']}
- Heterogeneity Estimator: {meta_settings['tau2_estimator']}
- Confidence Interval Method: {meta_settings['ci_method']}

Please provide a comprehensive analysis including:

1. Effect Size Analysis:
   - Pooled effect estimation
   - Confidence intervals interpretation
   - Clinical/practical significance assessment
   - Effect size context in the field

2. Heterogeneity Evaluation:
   - I² statistic interpretation
   - τ² estimation and meaning
   - Q-test results analysis
   - Sources of heterogeneity discussion

3. Model Assessment:
   - Model selection justification
   - Sensitivity considerations
   - Prediction intervals
   - Model assumptions review

4. Publication Bias Analysis:
   - Funnel plot assessment
   - {meta_settings['publication_bias_method']} test results
   - Small-study effects evaluation
   - Publication bias impact

5. Clinical/Practical Implications:
   - Main findings summary
   - Practice recommendations
   - Implementation considerations
   - Research gaps identification

Results for Analysis:
{json.dumps(results, indent=2)}"""

        if custom_instructions:
            prompt += f"\n\nAdditional Analysis Instructions:\n{custom_instructions}"
            
        return prompt