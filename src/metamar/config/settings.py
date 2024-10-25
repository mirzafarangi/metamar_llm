"""
Configuration management for Meta-Mar LLM
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class LLMConfig:
    """LLM configuration settings"""
    model: str
    temperature: float
    max_tokens: int
    timeout: int

@dataclass
class APIConfig:
    """API configuration settings"""
    retry_attempts: int
    retry_delay: int
    batch_size: int
    rate_limit: int

@dataclass
class MetaAnalysisConfig:
    """Meta-analysis configuration settings"""
    visualization_style: str
    summary_measure: str
    pooling_method: str
    tau2_estimator: str
    ci_method: str
    hartung_knapp_adjustment: str
    prediction_interval_method: str
    tau2_ci_method: str
    publication_bias_method: str

@dataclass
class ShinyConfig:
    """Shiny app configuration settings"""
    port: int
    host: str
    max_upload_size: int

class Settings:
    """Configuration manager for Meta-Mar LLM"""
    
    # Valid meta-analysis settings
    VALID_SETTINGS = {
        'visualization_styles': [
            'RevMan5', 'BMJ', 'JAMA', 'IQWiG5', 
            'IQWiG6', 'geneexpr', 'meta4'
        ],
        'summary_measures': {
            'continuous': ['MD', 'SMD', 'ROM'],
            'binary': ['OR', 'RR', 'RD'],
            'generic': ['MD', 'SMD', 'ROM', 'OR', 'RR', 'RD', 'HR', 'IRR'],
            'correlation': ['ZCOR', 'COR']
        },
        'pooling_methods': {
            'fixed_effect': {
                'binary': ['MH', 'Peto', 'Inverse'],
                'continuous': ['Inverse', 'Hedges', 'Cohen', 'Glass']
            },
            'random_effects': [
                'REML', 'PM', 'DL', 'ML', 'HS', 'SJ', 'HE', 'EB'
            ]
        },
        'tau2_estimators': [
            'REML', 'PM', 'DL', 'ML', 'HS', 'SJ', 'HE', 'EB'
        ],
        'ci_methods': {
            'random_effects': ['classic', 'HK', 'KR'],
            'hartung_knapp_adjustments': ['', 'se', 'IQWiG6', 'ci']
        },
        'prediction_intervals': {
            'methods': ['HTS', 'HK', 'KR', 'NNF', 'S'],
            'adjustments': ['', 'se']
        },
        'tau2_ci_methods': ['J', 'BJ', 'QP', 'PL', ''],
        'publication_bias_methods': [
            'Begg', 'Egger', 'Thompson', 'Harbord', 'Deeks'
        ]
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize settings manager
        
        Args:
            config_dir: Optional custom config directory path
        """
        self.config_dir = Path(config_dir) if config_dir else Path(__file__).parents[3] / 'config'
        self.env = os.getenv('METAMAR_ENV', 'development')
        self._load_config()
        
    def _load_config(self):
        """Load configuration from YAML files"""
        try:
            # Load general configuration
            config_path = self.config_dir / f'config.{self.env}.yml'
            if not config_path.exists():
                config_path = self.config_dir / 'config.yml'
            
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
            
            # Load logging configuration
            log_path = self.config_dir / 'logging.yml'
            with open(log_path, 'r') as f:
                self.logging_config = yaml.safe_load(f)
                
            # Initialize configuration objects
            self._initialize_configs()
            
        except Exception as e:
            logger.error(f"Error loading configuration: {str(e)}")
            raise
    
    def _initialize_configs(self):
        """Initialize configuration dataclass objects"""
        # LLM Configurations
        self.gpt4_config = LLMConfig(
            model=self.config['llm']['gpt4']['model'],
            temperature=self.config['llm']['gpt4']['temperature'],
            max_tokens=self.config['llm']['gpt4']['max_tokens'],
            timeout=self.config['llm']['gpt4']['timeout']
        )
        
        self.claude_config = LLMConfig(
            model=self.config['llm']['claude']['model'],
            temperature=self.config['llm']['claude']['temperature'],
            max_tokens=self.config['llm']['claude']['max_tokens'],
            timeout=self.config['llm']['claude']['timeout']
        )
        
        # API Configuration
        self.api_config = APIConfig(
            retry_attempts=self.config['api']['retry_attempts'],
            retry_delay=self.config['api']['retry_delay'],
            batch_size=self.config['api']['batch_size'],
            rate_limit=self.config['api']['rate_limit']
        )
        
        # Meta-analysis Configuration
        self.meta_config = MetaAnalysisConfig(
            visualization_style=self.config['meta_analysis']['visualization_style'],
            summary_measure=self.config['meta_analysis']['summary_measure'],
            pooling_method=self.config['meta_analysis']['pooling_method'],
            tau2_estimator=self.config['meta_analysis']['tau2_estimator'],
            ci_method=self.config['meta_analysis']['ci_method'],
            hartung_knapp_adjustment=self.config['meta_analysis']['hartung_knapp_adjustment'],
            prediction_interval_method=self.config['meta_analysis']['prediction_interval_method'],
            tau2_ci_method=self.config['meta_analysis']['tau2_ci_method'],
            publication_bias_method=self.config['meta_analysis']['publication_bias_method']
        )
        
        # Shiny Configuration
        self.shiny_config = ShinyConfig(
            port=self.config['shiny']['port'],
            host=self.config['shiny']['host'],
            max_upload_size=self.config['shiny']['max_upload_size']
        )
    
    def validate_meta_settings(self, analysis_type: str) -> bool:
        """
        Validate meta-analysis settings for given analysis type
        
        Args:
            analysis_type: Type of meta-analysis ('continuous', 'binary', 'generic', 'correlation')
            
        Returns:
            bool: True if settings are valid
        """
        try:
            # Check visualization style
            if self.meta_config.visualization_style not in self.VALID_SETTINGS['visualization_styles']:
                raise ValueError(f"Invalid visualization style: {self.meta_config.visualization_style}")
            
            # Check summary measure
            valid_measures = self.VALID_SETTINGS['summary_measures'][analysis_type]
            if self.meta_config.summary_measure not in valid_measures:
                raise ValueError(f"Invalid summary measure for {analysis_type}: {self.meta_config.summary_measure}")
            
            # Check pooling method
            if analysis_type == 'binary':
                valid_methods = self.VALID_SETTINGS['pooling_methods']['fixed_effect']['binary']
            elif analysis_type == 'continuous':
                valid_methods = self.VALID_SETTINGS['pooling_methods']['fixed_effect']['continuous']
            else:
                valid_methods = ['Inverse']
                
            if self.meta_config.pooling_method not in valid_methods:
                raise ValueError(f"Invalid pooling method for {analysis_type}: {self.meta_config.pooling_method}")
            
            # Check other settings
            if self.meta_config.tau2_estimator not in self.VALID_SETTINGS['tau2_estimators']:
                raise ValueError(f"Invalid τ² estimator: {self.meta_config.tau2_estimator}")
                
            if self.meta_config.ci_method not in self.VALID_SETTINGS['ci_methods']['random_effects']:
                raise ValueError(f"Invalid CI method: {self.meta_config.ci_method}")
                
            if self.meta_config.hartung_knapp_adjustment not in self.VALID_SETTINGS['ci_methods']['hartung_knapp_adjustments']:
                raise ValueError(f"Invalid Hartung-Knapp adjustment: {self.meta_config.hartung_knapp_adjustment}")
                
            return True
            
        except Exception as e:
            logger.error(f"Meta-analysis settings validation error: {str(e)}")
            return False
    
    @property
    def llm_settings(self) -> Dict[str, Any]:
        """Get LLM-specific settings"""
        return {
            'gpt4': {
                'model': self.gpt4_config.model,
                'temperature': self.gpt4_config.temperature,
                'max_tokens': self.gpt4_config.max_tokens,
                'timeout': self.gpt4_config.timeout
            },
            'claude': {
                'model': self.claude_config.model,
                'temperature': self.claude_config.temperature,
                'max_tokens': self.claude_config.max_tokens,
                'timeout': self.claude_config.timeout
            }
        }
    
    @property
    def meta_settings(self) -> Dict[str, Any]:
        """Get meta-analysis settings"""
        return {
            'visualization_style': self.meta_config.visualization_style,
            'summary_measure': self.meta_config.summary_measure,
            'pooling_method': self.meta_config.pooling_method,
            'tau2_estimator': self.meta_config.tau2_estimator,
            'ci_method': self.meta_config.ci_method,
            'hartung_knapp_adjustment': self.meta_config.hartung_knapp_adjustment,
            'prediction_interval_method': self.meta_config.prediction_interval_method,
            'tau2_ci_method': self.meta_config.tau2_ci_method,
            'publication_bias_method': self.meta_config.publication_bias_method
        }
    
    def get_valid_settings(self, analysis_type: str) -> Dict[str, List[str]]:
        """Get valid settings for analysis type"""
        return {
            'visualization_styles': self.VALID_SETTINGS['visualization_styles'],
            'summary_measures': self.VALID_SETTINGS['summary_measures'][analysis_type],
            'pooling_methods': (
                self.VALID_SETTINGS['pooling_methods']['fixed_effect'].get(
                    analysis_type, ['Inverse']
                )
            ),
            'tau2_estimators': self.VALID_SETTINGS['tau2_estimators'],
            'ci_methods': self.VALID_SETTINGS['ci_methods']['random_effects'],
            'hartung_knapp_adjustments': self.VALID_SETTINGS['ci_methods']['hartung_knapp_adjustments'],
            'prediction_interval_methods': self.VALID_SETTINGS['prediction_intervals']['methods'],
            'tau2_ci_methods': self.VALID_SETTINGS['tau2_ci_methods'],
            'publication_bias_methods': self.VALID_SETTINGS['publication_bias_methods']
        }

# Create singleton instance
settings = Settings()

# Usage example
if __name__ == "__main__":
    # Print current meta-analysis settings
    print("Meta-Analysis Settings:", settings.meta_settings)
    
    # Get valid settings for continuous outcome
    print("\nValid Settings for Continuous Outcome:")
    print(settings.get_valid_settings('continuous'))
    
    # Validate settings for binary outcome
    print("\nValidating Binary Outcome Settings:")
    print(settings.validate_meta_settings('binary'))