# Meta-Mar LLM Enhanced

## Overview
Meta-Mar LLM Enhanced is an AI-powered meta-analysis service that combines statistical meta-analysis with advanced AI interpretation capabilities. This project enhances the traditional meta-analysis process by integrating GPT-4 and Claude for more structuralized result interpretation and reporting.

## Key Features
- Meta-analysis calculation and visualization
- AI-powered result interpretation using:
  * GPT-4 for detailed statistical explanations
  * Claude for comparative analysis
- Interactive R Shiny web interface
- Comprehensive statistical reporting
- Publication bias assessment
- Heterogeneity analysis

## Tech Stack
- **R**: Statistical computing and Shiny web interface
- **Python**: AI integration and backend processing
- **AI Models**: OpenAI GPT-4, Anthropic Claude
- **Frameworks**: LangChain for AI integration

## Installation

### Prerequisites
- R (>= 4.0.0)
- Python (>= 3.10)
- Conda or Miniconda

### Setup
1. Clone the repository
```bash
git clone [your-repository-url]
cd metamar_llm
```

2. Create and activate Python environment
```bash
conda create -n metamar_llm python=3.10
conda activate metamar_llm
pip install -r requirements.txt
```

3. Configure environment variables
- Copy `.env.example` to `.env`
- Add your API keys:
  * OPENAI_API_KEY
  * ANTHROPIC_API_KEY

4. Install R dependencies
```R
install.packages(c("shiny", "meta", "metafor", "dplyr", "ggplot2"))
```

## Project Structure
```
metamar_llm/
├── src/            # Python source code
├── tests/          # Test files
├── notebooks/      # Jupyter notebooks for development
├── config/         # Configuration files
├── docs/           # Documentation
└── shiny/          # R Shiny application
```

## Usage
1. Start the Shiny application
2. Upload your meta-analysis data
3. Configure analysis parameters
4. Run analysis
5. Get AI-enhanced interpretation

## Development Status
🚧 Currently under active development

## Contributing
Issues and pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgments
- Original Meta-Mar project contributors
- R meta-analysis community
- OpenAI and Anthropic for AI capabilities