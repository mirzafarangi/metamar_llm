"""
Tests for data loading and validation
"""

import pytest
import pandas as pd
from metamar.utils.data_loader import MetaAnalysisDataLoader
from pathlib import Path
import numpy as np

@pytest.fixture
def data_loader():
    """Create data loader instance"""
    return MetaAnalysisDataLoader()

@pytest.fixture
def sample_continuous_data():
    """Create sample continuous outcome data"""
    return pd.DataFrame({
        'studlab': ['Study1', 'Study2', 'Study3'],
        'n.e': [50, 60, 55],
        'mean.e': [10.5, 11.2, 10.8],
        'sd.e': [2.1, 2.3, 2.0],
        'n.c': [48, 62, 53],
        'mean.c': [9.8, 10.5, 10.1],
        'sd.c': [2.0, 2.2, 1.9],
        'subgroup': ['A', 'B', 'A'],
        'year': [2018, 2019, 2020]
    })

@pytest.fixture
def sample_binary_data():
    """Create sample binary outcome data"""
    return pd.DataFrame({
        'studlab': ['Study1', 'Study2', 'Study3'],
        'event.e': [15, 20, 18],
        'n.e': [100, 110, 95],
        'event.c': [10, 12, 11],
        'n.c': [100, 105, 98],
        'subgroup': ['A', 'B', 'A']
    })

@pytest.fixture
def sample_correlation_data():
    """Create sample correlation data"""
    return pd.DataFrame({
        'studlab': ['Study1', 'Study2', 'Study3'],
        'cor': [0.45, 0.52, 0.48],
        'n': [100, 95, 110],
        'subgroup': ['A', 'B', 'A']
    })

class TestMetaAnalysisDataLoader:
    """Test data loader functionality"""
    
    def test_load_continuous_data(self, data_loader, tmp_path):
        """Test loading continuous outcome data"""
        # Create test file
        test_file = tmp_path / "test_continuous.csv"
        pd.DataFrame({
            'studlab': ['Test1'],
            'n.e': [50],
            'mean.e': [10.5],
            'sd.e': [2.1],
            'n.c': [48],
            'mean.c': [9.8],
            'sd.c': [2.0]
        }).to_csv(test_file, index=False)
        
        # Load and verify
        data = data_loader.load_data(test_file, 'continuous')
        assert isinstance(data, pd.DataFrame)
        assert all(col in data.columns for col in [
            'studlab', 'n.e', 'mean.e', 'sd.e', 'n.c', 'mean.c', 'sd.c'
        ])
    
    def test_load_binary_data(self, data_loader, tmp_path):
        """Test loading binary outcome data"""
        # Create test file
        test_file = tmp_path / "test_binary.csv"
        pd.DataFrame({
            'studlab': ['Test1'],
            'event.e': [15],
            'n.e': [100],
            'event.c': [10],
            'n.c': [100]
        }).to_csv(test_file, index=False)
        
        # Load and verify
        data = data_loader.load_data(test_file, 'binary')
        assert isinstance(data, pd.DataFrame)
        assert all(col in data.columns for col in [
            'studlab', 'event.e', 'n.e', 'event.c', 'n.c'
        ])
    
    def test_data_validation(self, data_loader, sample_continuous_data, tmp_path):
        """Test data validation"""
        # Create invalid data
        invalid_data = sample_continuous_data.copy()
        invalid_data.loc[0, 'sd.e'] = -1  # Invalid negative SD
        
        test_file = tmp_path / "test_invalid.csv"
        invalid_data.to_csv(test_file, index=False)
        
        # Check validation
        with pytest.raises(ValueError):
            data_loader.load_data(test_file, 'continuous')
    
    def test_missing_columns(self, data_loader, tmp_path):
        """Test handling of missing required columns"""
        # Create incomplete data
        incomplete_data = pd.DataFrame({
            'studlab': ['Test1'],
            'n.e': [50]  # Missing other required columns
        })
        
        test_file = tmp_path / "test_incomplete.csv"
        incomplete_data.to_csv(test_file, index=False)
        
        # Check validation
        with pytest.raises(ValueError):
            data_loader.load_data(test_file, 'continuous')
    
    def test_numeric_validation(self, data_loader, tmp_path):
        """Test numeric data validation"""
        # Create data with non-numeric values
        invalid_numeric = pd.DataFrame({
            'studlab': ['Test1'],
            'n.e': ['not_a_number'],
            'mean.e': [10.5],
            'sd.e': [2.1],
            'n.c': [48],
            'mean.c': [9.8],
            'sd.c': [2.0]
        })
        
        test_file = tmp_path / "test_numeric.csv"
        invalid_numeric.to_csv(test_file, index=False)
        
        # Check validation
        with pytest.raises(ValueError):
            data_loader.load_data(test_file, 'continuous')
    
    def test_correlation_bounds(self, data_loader, tmp_path):
        """Test correlation coefficient bounds validation"""
        # Create data with invalid correlation
        invalid_correlation = pd.DataFrame({
            'studlab': ['Test1'],
            'cor': [1.5],  # Invalid correlation > 1
            'n': [100]
        })
        
        test_file = tmp_path / "test_correlation.csv"
        invalid_correlation.to_csv(test_file, index=False)
        
        # Check validation
        with pytest.raises(ValueError):
            data_loader.load_data(test_file, 'correlation')