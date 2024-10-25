"""
Tests for LLM handlers and report generation
"""

import pytest
from metamar.llm.gpt4_handler import GPT4Handler
from metamar.llm.claude_handler import ClaudeHandler
from metamar.llm.report_generator import ReportGenerator
from metamar.config.settings import settings
import json
from datetime import datetime

@pytest.fixture
def sample_meta_results():
    """Sample meta-analysis results for testing"""
    return {
        "effect_size": 0.45,
        "ci_lower": 0.32,
        "ci_upper": 0.58,
        "p_value": 0.001,
        "heterogeneity": {
            "i2": 75.5,
            "tau2": 0.15,
            "q_statistic": 45.6,
            "q_p_value": 0.001
        },
        "k": 15,
        "total_n": 1200
    }

@pytest.fixture
def meta_settings():
    """Sample meta-analysis settings"""
    return {
        "summary_measure": "SMD",
        "pooling_method": "Random",
        "tau2_estimator": "REML",
        "ci_method": "classic",
        "publication_bias_method": "Egger"
    }

class TestGPT4Handler:
    """Test GPT-4 handler functionality"""
    
    def test_initialization(self):
        """Test handler initialization"""
        handler = GPT4Handler()
        assert handler.settings == settings.llm_settings['gpt4']
    
    def test_report_generation(self, sample_meta_results, meta_settings):
        """Test GPT-4 report generation"""
        handler = GPT4Handler()
        report = handler.generate_report(
            sample_meta_results,
            "continuous",
            meta_settings
        )
        assert isinstance(report, str)
        assert len(report) > 0
        
        # Check for key components
        assert "effect size" in report.lower()
        assert "heterogeneity" in report.lower()
        assert "confidence interval" in report.lower()

class TestClaudeHandler:
    """Test Claude handler functionality"""
    
    def test_initialization(self):
        """Test handler initialization"""
        handler = ClaudeHandler()
        assert handler.settings == settings.llm_settings['claude']
    
    def test_report_generation(self, sample_meta_results, meta_settings):
        """Test Claude report generation"""
        handler = ClaudeHandler()
        report = handler.generate_report(
            sample_meta_results,
            "continuous",
            meta_settings
        )
        assert isinstance(report, str)
        assert len(report) > 0
        
        # Check for key components
        assert "effect size" in report.lower()
        assert "heterogeneity" in report.lower()
        assert "confidence interval" in report.lower()

class TestReportGenerator:
    """Test report generator functionality"""
    
    def test_initialization(self):
        """Test generator initialization"""
        generator = ReportGenerator()
        assert isinstance(generator.gpt4, GPT4Handler)
        assert isinstance(generator.claude, ClaudeHandler)
    
    def test_comparative_report(self, sample_meta_results, meta_settings):
        """Test comparative report generation"""
        generator = ReportGenerator()
        comparison = generator.generate_comparative_report(
            sample_meta_results,
            "continuous",
            meta_settings
        )
        
        # Check structure
        assert "timestamp" in comparison
        assert "analysis_type" in comparison
        assert "settings_used" in comparison
        assert "gpt4" in comparison
        assert "claude" in comparison
        
        # Check content
        assert isinstance(comparison["gpt4"]["report"], str)
        assert isinstance(comparison["claude"]["report"], str)
        assert comparison["gpt4"]["time"] > 0
        assert comparison["claude"]["time"] > 0
        
        # Check metrics
        metrics = comparison["comparison_metrics"]
        assert "length_comparison" in metrics
        assert "section_coverage" in metrics
        
    def test_invalid_settings(self, sample_meta_results):
        """Test handling of invalid settings"""
        generator = ReportGenerator()
        invalid_settings = {
            "summary_measure": "INVALID",
            "pooling_method": "INVALID"
        }
        
        with pytest.raises(ValueError):
            generator.generate_comparative_report(
                sample_meta_results,
                "continuous",
                invalid_settings
            )