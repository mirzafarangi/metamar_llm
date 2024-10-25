"""
Test suite for Meta-Mar
"""

from pathlib import Path

# Get test data directory
TEST_DATA_DIR = Path(__file__).parent / "data"

def get_test_file_path(analysis_type: str, filename: str) -> Path:
    """Get path to test data file"""
    return TEST_DATA_DIR / analysis_type / filename