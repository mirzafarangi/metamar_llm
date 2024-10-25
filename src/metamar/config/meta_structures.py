"""
Meta-analysis data structure definitions and validations
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class MetaAnalysisStructure:
    """Defines required columns and validations for different meta-analysis types"""
    required_columns: List[str]
    optional_columns: List[str]
    data_types: Dict[str, str]
    validations: Dict[str, Any]

class MetaStructures:
    """Configuration for different meta-analysis data structures"""
    
    CONTINUOUS = MetaAnalysisStructure(
        required_columns=['studlab', 'n.e', 'mean.e', 'sd.e', 'n.c', 'mean.c', 'sd.c'],
        optional_columns=['subgroup', 'year', 'age'],
        data_types={
            'n.e': 'numeric', 'mean.e': 'numeric', 'sd.e': 'numeric',
            'n.c': 'numeric', 'mean.c': 'numeric', 'sd.c': 'numeric'
        },
        validations={
            'n.e': lambda x: x > 0,
            'n.c': lambda x: x > 0,
            'sd.e': lambda x: x >= 0,
            'sd.c': lambda x: x >= 0
        }
    )
    
    CONTINUOUS_MEDIAN = MetaAnalysisStructure(
        required_columns=['studlab', 'n.e', 'median.e', 'q1.e', 'q3.e', 
                         'n.c', 'median.c', 'q1.c', 'q3.c'],
        optional_columns=['subgroup', 'year', 'age'],
        data_types={
            'n.e': 'numeric', 'median.e': 'numeric', 
            'q1.e': 'numeric', 'q3.e': 'numeric',
            'n.c': 'numeric', 'median.c': 'numeric',
            'q1.c': 'numeric', 'q3.c': 'numeric'
        },
        validations={
            'n.e': lambda x: x > 0,
            'n.c': lambda x: x > 0,
            'q1.e': lambda x, row: x <= row['median.e'],
            'q3.e': lambda x, row: x >= row['median.e'],
            'q1.c': lambda x, row: x <= row['median.c'],
            'q3.c': lambda x, row: x >= row['median.c']
        }
    )
    
    BINARY = MetaAnalysisStructure(
        required_columns=['studlab', 'event.e', 'n.e', 'event.c', 'n.c'],
        optional_columns=['subgroup', 'cluster', 'rho'],
        data_types={
            'event.e': 'numeric', 'n.e': 'numeric',
            'event.c': 'numeric', 'n.c': 'numeric'
        },
        validations={
            'event.e': lambda x, row: 0 <= x <= row['n.e'],
            'event.c': lambda x, row: 0 <= x <= row['n.c'],
            'n.e': lambda x: x > 0,
            'n.c': lambda x: x > 0
        }
    )
    
    GENERIC = MetaAnalysisStructure(
        required_columns=['studlab', 'TE', 'seTE'],
        optional_columns=['lower', 'upper', 'pval', 'df', 'subgroup'],
        data_types={
            'TE': 'numeric', 'seTE': 'numeric'
        },
        validations={
            'seTE': lambda x: x > 0
        }
    )
    
    CORRELATION = MetaAnalysisStructure(
        required_columns=['studlab', 'cor', 'n'],
        optional_columns=['subgroup'],
        data_types={
            'cor': 'numeric', 'n': 'numeric'
        },
        validations={
            'cor': lambda x: -1 <= x <= 1,
            'n': lambda x: x > 0
        }
    )

# Model settings configuration
META_SETTINGS = {
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