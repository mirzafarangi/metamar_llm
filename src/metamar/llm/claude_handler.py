from anthropic import Anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ClaudeHandler:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    def generate_report(self, model_settings_summary, meta_summary):
        """Generate a report using Claude"""
        try:
            message = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[
                    {
                        "role": "user",
                        "content": self._create_prompt(model_settings_summary, meta_summary)
                    }
                ]
            )
            return message.content[0].text
        except Exception as e:
            return f"An error occurred: {str(e)}"
    
    def _create_prompt(self, model_settings_summary, meta_summary):
        """Create the prompt for Claude"""
        return f"""
        Generate a report for a meta-analysis based on the following information:
        
        Model Settings:
        {model_settings_summary}
        
        Meta-Analysis Summary:
        {meta_summary}
        
        Please provide a comprehensive analysis including:
        1. Detailed results interpretation
        2. Heterogeneity assessment
        3. Publication bias analysis
        4. Practical implications
        """