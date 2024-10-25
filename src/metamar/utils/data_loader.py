"""
Enhanced data loading with meta-analysis structure validation
"""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Union, Optional
import logging
from ..config.meta_structures import MetaStructures, META_SETTINGS

logger = logging.getLogger(__name__)

class MetaAnalysisDataLoader:
    """Enhanced data loader for meta-analysis"""
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).parents[3] / "tests" / "data"
        self.structures = MetaStructures()
    
    def load_data(
        self,
        file_path: Union[str, Path],
        analysis_type: str,
        structure_type: str = 'basic'
    ) -> pd.DataFrame:
        """
        Load and validate meta-analysis data
        
        Args:
            file_path: Path to data file
            analysis_type: Type of meta-analysis ('continuous', 'binary', 'generic', 'correlation')
            structure_type: Data structure variant ('basic', 'median', 'range' for continuous)
            
        Returns:
            pd.DataFrame: Validated data frame
        """
        try:
            # Load data
            data = self._read_file(file_path)
            
            # Get appropriate structure
            structure = self._get_structure(analysis_type, structure_type)
            
            # Validate structure
            self._validate_structure(data, structure)
            
            # Validate data types and values
            self._validate_data(data, structure)
            
            return data
            
        except Exception as e:
            logger.error(f"Error loading meta-analysis data: {str(e)}")
            raise
    
    def _read_file(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """Read data file"""
        file_path = Path(file_path)
        if file_path.suffix == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
    
    def _get_structure(self, analysis_type: str, structure_type: str) -> MetaAnalysisStructure:
        """Get appropriate data structure"""
        structure_map = {
            'continuous': {
                'basic': self.structures.CONTINUOUS,
                'median': self.structures.CONTINUOUS_MEDIAN
            },
            'binary': {'basic': self.structures.BINARY},
            'generic': {'basic': self.structures.GENERIC},
            'correlation': {'basic': self.structures.CORRELATION}
        }
        
        if analysis_type not in structure_map:
            raise ValueError(f"Unknown analysis type: {analysis_type}")
            
        if structure_type not in structure_map[analysis_type]:
            raise ValueError(f"Unknown structure type: {structure_type} for {analysis_type}")
            
        return structure_map[analysis_type][structure_type]
    
    def _validate_structure(self, data: pd.DataFrame, structure: MetaAnalysisStructure):
        """Validate data structure"""
        missing_cols = set(structure.required_columns) - set(data.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
    
    def _validate_data(self, data: pd.DataFrame, structure: MetaAnalysisStructure):
        """Validate data types and values"""
        for col, dtype in structure.data_types.items():
            try:
                data[col] = pd.to_numeric(data[col])
            except:
                raise ValueError(f"Column {col} must be numeric")
        
        for col, validation in structure.validations.items():
            if 'row' in validation.__code__.co_varnames:
                mask = ~data.apply(lambda row: validation(row[col], row), axis=1)
            else:
                mask = ~data[col].apply(validation)
            
            if mask.any():
                invalid_rows = data.index[mask].tolist()
                raise ValueError(f"Validation failed for {col} in rows: {invalid_rows}")

    def get_available_settings(self, analysis_type: str) -> Dict[str, Any]:
        """Get available settings for analysis type"""
        return {
            'summary_measures': META_SETTINGS['summary_measures'][analysis_type],
            'pooling_methods': META_SETTINGS['pooling_methods'],
            'tau2_estimators': META_SETTINGS['tau2_estimators'],
            'ci_methods': META_SETTINGS['ci_methods'],
            'prediction_intervals': META_SETTINGS['prediction_intervals'],
            'tau2_ci_methods': META_SETTINGS['tau2_ci_methods'],
            'publication_bias_methods': META_SETTINGS['publication_bias_methods']
        }