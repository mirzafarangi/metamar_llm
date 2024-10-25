"""
Helper functions for Meta-Mar
"""

from typing import Dict, Any
import pandas as pd
import logging

logger = logging.getLogger(__name__)

def format_results(results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format meta-analysis results for LLM processing
    
    Args:
        results: Raw meta-analysis results
        
    Returns:
        Dict: Formatted results
    """
    try:
        formatted = {
            "model_type": results.get("model_type", "Not specified"),
            "effect_size": {
                "value": results.get("effect_size", "Not available"),
                "ci_lower": results.get("ci_lower"),
                "ci_upper": results.get("ci_upper")
            },
            "heterogeneity": {
                "i2": results.get("i2"),
                "q_statistic": results.get("q"),
                "tau2": results.get("tau2")
            },
            "studies": {
                "count": results.get("k"),
                "total_sample": results.get("n")
            }
        }
        
        return formatted
        
    except Exception as e:
        logger.error(f"Error formatting results: {str(e)}")
        raise

def validate_data(data: pd.DataFrame, analysis_type: str) -> bool:
    """
    Validate data for meta-analysis
    
    Args:
        data: Input DataFrame
        analysis_type: Type of meta-analysis
        
    Returns:
        bool: True if valid, raises ValueError if not
    """
    try:
        # Check required columns
        required_columns = {
            'continuous': ['studlab', 'n.e', 'mean.e', 'sd.e', 'n.c', 'mean.c', 'sd.c'],
            'binary': ['studlab', 'event.e', 'n.e', 'event.c', 'n.c'],
            'correlation': ['studlab', 'cor', 'n']
        }
        
        if analysis_type not in required_columns:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
            
        missing_cols = set(required_columns[analysis_type]) - set(data.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Check data types and ranges
        if analysis_type == 'continuous':
            numeric_cols = ['n.e', 'mean.e', 'sd.e', 'n.c', 'mean.c', 'sd.c']
            for col in numeric_cols:
                if not pd.to_numeric(data[col],