"""
Enhanced report generator combining multiple LLM outputs for Meta-Mar
"""

from typing import Dict, Any, Optional, Tuple
from .gpt4_handler import GPT4Handler
from .claude_handler import ClaudeHandler
from ..config.settings import settings
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generates and compares reports from multiple LLMs"""
    
    def __init__(self):
        """Initialize handlers for different LLMs"""
        self.gpt4 = GPT4Handler()
        self.claude = ClaudeHandler()
        
    def generate_comparative_report(
        self,
        meta_analysis_results: Dict[str, Any],
        analysis_type: str,
        meta_settings: Optional[Dict[str, Any]] = None,
        custom_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comparative analysis from multiple LLMs
        
        Args:
            meta_analysis_results: Dictionary containing meta-analysis results
            analysis_type: Type of meta-analysis
            meta_settings: Optional custom meta-analysis settings
            custom_instructions: Optional additional instructions
            
        Returns:
            Dict containing both reports and comparison metrics
        """
        try:
            # Use provided settings or get defaults
            analysis_settings = meta_settings or settings.meta_settings
            
            # Validate settings for analysis type
            if not settings.validate_meta_settings(analysis_type):
                raise ValueError(f"Invalid meta-analysis settings for {analysis_type}")
            
            # Generate reports from both models
            gpt4_report, gpt4_time = self._generate_gpt4_report(
                meta_analysis_results,
                analysis_type,
                analysis_settings,
                custom_instructions
            )
            
            claude_report, claude_time = self._generate_claude_report(
                meta_analysis_results,
                analysis_type,
                analysis_settings,
                custom_instructions
            )
            
            # Prepare comparison results
            comparison = {
                "timestamp": datetime.now().isoformat(),
                "analysis_type": analysis_type,
                "settings_used": analysis_settings,
                "input_data": meta_analysis_results,
                "gpt4": {
                    "report": gpt4_report,
                    "time": gpt4_time
                },
                "claude": {
                    "report": claude_report,
                    "time": claude_time
                },
                "comparison_metrics": self._compare_reports(
                    gpt4_report,
                    claude_report,
                    analysis_type
                )
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error generating comparative report: {str(e)}")
            raise
    
    def _generate_gpt4_report(
        self,
        results: Dict[str, Any],
        analysis_type: str,
        meta_settings: Dict[str, Any],
        custom_instructions: Optional[str]
    ) -> Tuple[str, float]:
        """Generate report using GPT-4"""
        start_time = datetime.now()
        report = self.gpt4.generate_report(
            results,
            analysis_type,
            meta_settings,
            custom_instructions
        )
        time_taken = (datetime.now() - start_time).total_seconds()
        return report, time_taken
    
    def _generate_claude_report(
        self,
        results: Dict[str, Any],
        analysis_type: str,
        meta_settings: Dict[str, Any],
        custom_instructions: Optional[str]
    ) -> Tuple[str, float]:
        """Generate report using Claude"""
        start_time = datetime.now()
        report = self.claude.generate_report(
            results,
            analysis_type,
            meta_settings,
            custom_instructions
        )
        time_taken = (datetime.now() - start_time).total_seconds()
        return report, time_taken
    
    def _compare_reports(
        self,
        gpt4_report: str,
        claude_report: str,
        analysis_type: str
    ) -> Dict[str, Any]:
        """Compare reports from different models"""
        
        # Basic comparison metrics
        basic_metrics = {
            "length_comparison": {
                "gpt4_length": len(gpt4_report),
                "claude_length": len(claude_report)
            },
            "section_coverage": self._analyze_section_coverage(
                gpt4_report,
                claude_report
            )
        }
        
        # Analysis type specific metrics
        type_specific_metrics = self._get_type_specific_metrics(
            gpt4_report,
            claude_report,
            analysis_type
        )
        
        return {**basic_metrics, **type_specific_metrics}
    
    def _analyze_section_coverage(
        self,
        gpt4_report: str,
        claude_report: str
    ) -> Dict[str, Dict[str, bool]]:
        """Analyze which sections are covered in each report"""
        key_sections = [
            "effect size",
            "heterogeneity",
            "confidence interval",
            "publication bias",
            "clinical implications"
        ]
        
        return {
            "gpt4": {
                section: section.lower() in gpt4_report.lower()
                for section in key_sections
            },
            "claude": {
                section: section.lower() in claude_report.lower()
                for section in key_sections
            }
        }
    
    def _get_type_specific_metrics(
        self,
        gpt4_report: str,
        claude_report: str,
        analysis_type: str
    ) -> Dict[str, Any]:
        """Get analysis type specific comparison metrics"""
        # Add specific metrics based on analysis type
        metrics = {}
        
        if analysis_type == 'continuous':
            metrics["effect_size_reporting"] = {
                "gpt4_includes_standardized": "standardized mean" in gpt4_report.lower(),
                "claude_includes_standardized": "standardized mean" in claude_report.lower()
            }
        elif analysis_type == 'binary':
            metrics["risk_reporting"] = {
                "gpt4_includes_nnt": "number needed to treat" in gpt4_report.lower(),
                "claude_includes_nnt": "number needed to treat" in claude_report.lower()
            }
        
        return metrics