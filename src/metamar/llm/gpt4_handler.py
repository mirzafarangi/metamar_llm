"""
Enhanced GPT-4 integration handler for Meta-Mar
"""

from openai import OpenAI
from typing import Dict, Any, Optional
from ..config.settings import settings
import logging
import json

logger = logging.getLogger(__name__)

class GPT4Handler:
    """Handles interactions with GPT-4 API"""
    
    def __init__(self):
        """Initialize GPT-4 handler with settings"""
        self.client = OpenAI()
        self.settings = settings.llm_settings['gpt4']
    
    def generate_report(
        self,
        meta_analysis_results: Dict[str, Any],
        analysis_type: str,
        meta_settings: Dict[str, Any],
        custom_instructions: Optional[str] = None
    ) -> str:
        """
        Generate meta-analysis report using GPT-4
        
        Args:
            meta_analysis_results: Dictionary containing meta-analysis results
            analysis_type: Type of meta-analysis ('continuous', 'binary', 'generic', 'correlation')
            meta_settings: Meta-analysis settings used
            custom_instructions: Optional additional instructions
            
        Returns:
            str: Generated report text
        """
        try:
            messages = self._create_messages(
                meta_analysis_results,
                analysis_type,
                meta_settings,
                custom_instructions
            )
            
            response = self.client.chat.completions.create(
                model=self.settings['model'],
                messages=messages,
                temperature=self.settings['temperature'],
                max_tokens=self.settings['max_tokens']
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating GPT-4 report: {str(e)}")
            raise
    
    def _create_messages(
        self,
        results: Dict[str, Any],
        analysis_type: str,
        meta_settings: Dict[str, Any],
        custom_instructions: Optional[str]
    ) -> list:
        """Create structured messages for GPT-4"""
        
        # Base system prompt for different analysis types
        type_specific_instructions = {
            'continuous': "Focus on mean differences, standardized effects, and heterogeneity.",
            'binary': "Focus on event rates, risk ratios/odds ratios, and number needed to treat.",
            'generic': "Focus on the specific effect size measure and its interpretation.",
            'correlation': "Focus on correlation strengths, Fisher's z-transformation, and relationship patterns."
        }
        
        base_prompt = f"""You are a meta-analysis expert. You will analyze results from a {analysis_type} meta-analysis.

Analysis Settings:
- Summary Measure: {meta_settings['summary_measure']}
- Model Type: {meta_settings['pooling_method']}
- Heterogeneity Estimator: {meta_settings['tau2_estimator']}
- Confidence Interval Method: {meta_settings['ci_method']}

{type_specific_instructions.get(analysis_type, '')}

Provide a comprehensive analysis including:
1. Main Effect Analysis:
   - Effect size interpretation
   - Confidence intervals
   - Statistical significance
   - Clinical/practical significance

2. Heterogeneity Assessment:
   - I² interpretation
   - τ² estimation
   - Q-statistic results
   - Between-study variance analysis

3. Model Assessment:
   - Model choice justification
   - Sensitivity considerations
   - Prediction intervals interpretation

4. Publication Bias:
   - Funnel plot asymmetry
   - Bias test results ({meta_settings['publication_bias_method']})
   - Small-study effects

5. Practical Implications:
   - Key findings
   - Clinical/practical relevance
   - Limitations
   - Recommendations"""

        if custom_instructions:
            base_prompt += f"\n\nAdditional Instructions:\n{custom_instructions}"

        return [
            {"role": "system", "content": base_prompt},
            {"role": "user", "content": (
                f"Please analyze these meta-analysis results:\n"
                f"{json.dumps(results, indent=2)}"
            )}
        ]