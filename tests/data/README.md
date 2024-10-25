# Meta-Mar Test Data Documentation

## Overview
This directory contains test data files for validating Meta-Mar's functionality across different types of meta-analyses.

## Data Structure

### Continuous Outcome Data
Location: `continuous/`

#### example1.csv
Basic mean difference structure:
- studlab: Study identifier
- n.e: Sample size (experimental group)
- mean.e: Mean (experimental group)
- sd.e: Standard deviation (experimental group)
- n.c: Sample size (control group)
- mean.c: Mean (control group)
- sd.c: Standard deviation (control group)
- subgroup: Optional subgroup identifier
- year: Publication year

#### example2.xlsx
Extended structure with median/IQR:
- studlab: Study identifier
- n.e: Sample size (experimental)
- median.e: Median (experimental)
- q1.e: First quartile (experimental)
- q3.e: Third quartile (experimental)
- n.c: Sample size (control)
- median.c: Median (control)
- q1.c: First quartile (control)
- q3.c: Third quartile (control)

### Binary Outcome Data
Location: `binary/`

#### example1.csv
Basic binary outcome structure:
- studlab: Study identifier
- event.e: Events in experimental group
- n.e: Total sample (experimental)
- event.c: Events in control group
- n.c: Total sample (control)
- subgroup: Optional subgroup identifier

#### example2.xlsx
Extended binary structure:
- Additional fields:
  * cluster: Cluster identifier
  * rho: Intracluster correlation
  * year: Publication year
  * quality: Study quality score

### Correlation Data
Location: `correlation/`

#### example1.csv
Basic correlation structure:
- studlab: Study identifier
- cor: Correlation coefficient
- n: Sample size
- subgroup: Optional subgroup identifier

#### example2.xlsx
Extended correlation structure:
- Additional fields:
  * year: Publication year
  * quality: Study quality
  * measure_type: Correlation measure type

## Data Validation Rules

### Continuous Data
- n.e, n.c > 0
- sd.e, sd.c ≥ 0
- q1 < median < q3

### Binary Data
- 0 ≤ events ≤ n
- n.e, n.c > 0

### Correlation Data
- -1 ≤ cor ≤ 1
- n > 0

## Usage Examples
```python
from metamar.utils.data_loader import DataLoader

# Load continuous data
loader = DataLoader()
cont_data = loader.load_file("continuous/example1.csv", "continuous")

# Load binary data
bin_data = loader.load_file("binary/example1.csv", "binary")

# Load correlation data
cor_data = loader.load_file("correlation/example1.csv", "correlation")
```

## Adding New Test Data
1. Follow the structure patterns above
2. Include relevant metadata columns
3. Validate against requirements
4. Update this documentation