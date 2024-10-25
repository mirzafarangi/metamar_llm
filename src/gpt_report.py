from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def generate_report(model_settings_summary, meta_summary):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""
    Generate a report for a meta-analysis based on the following information:
    
    Model Settings:
    {model_settings_summary}
    
    Meta-Analysis Summary:
    {meta_summary}
    
    The report should include two parts:
    1. A detailed comprehensive report of the model setting summary, meta-analysis results, bias analysis (including funnel plot asymmetry and file drawer (fail-safe N) analysis), and if aplicable reports of subgroup analysis. Note these reports should not just include the summaries but also the meaning of them, discussion and interpretation of them and Potential limitations of the analysis
    2 . Plots and Their Interpretation: forest plots (for fixed and random effects models), funnel plot, Galbraith Plot, L'Abbe Plot, Baujat Plot, Bubble Plot, Box plot for subgroup-effect size. --- for each plot give two infos: -Explain each plot shows what and -how to interprete them.  
    For example, this could be only an example of a good report --- Meta-Analysis Report
1. Model Setting Summary
Model Settings:
Model Type: metacont
Summary Measure: Mean Difference (MD)
τ² Estimator: Restricted Maximum Likelihood (REML)
Random Effects CI Method: classic
Prediction Interval Method: Hartung-Knapp correction applied
τ² CI method: Jackson method (J)
Pooling Method: Inverse variance method
Meta-Analysis Summary:
A comprehensive meta-analysis was conducted on 20 studies with a total of 6896 observations (3425 experimental and 3471 control subjects). The primary findings are as follows:

Overall Effects:
Common Effect Model:

Mean Difference (MD): 1.9479, 95% CI [1.8675; 2.0282], z = 47.52, p < 0.0001.
Interpretation: On average, the experimental group shows a significantly higher outcome compared to the control group, with a mean difference of approximately 1.95. This result is statistically significant.
Random Effects Model:

Mean Difference (MD): 1.6589, 95% CI [-0.3074; 3.6253], z = 1.65, p = 0.0982.
Interpretation: The random effects model indicates a potentially meaningful effect size that is not statistically significant. The broad confidence interval signifies high variability among studies.
Prediction Interval:
Prediction Interval: [-7.9731; 11.2909].
Interpretation: This interval implies that future studies could result in mean differences falling anywhere between -7.97 and 11.29, illustrating considerable uncertainty.
Quantifying Heterogeneity:
Tau-squared (τ²): 20.0126, 95% CI [8.4755; 37.9933] — indicates substantial variability across studies.
tau: 4.4735, 95% CI [2.9113; 6.1639].
I²: 99.7% — suggests almost complete heterogeneity.
H-value: 17.24 (indicating a substantial degree of heterogeneity).
Test of Heterogeneity:
Q: 5649.81 with 19 degrees of freedom, p < 0.0001.
Interpretation: There is significant heterogeneity among the study results, justifying the use of a random effects model.
Subgroup Analysis:
Conducted under both common and random effects models, grouped by different subcategories (A, B, C).
Common Effect Model Results:
Subgroup A: MD = 2.8680 [2.6679; 3.0680]
Subgroup B: MD = 1.3582 [1.2481; 1.4683]
Subgroup C: MD = 2.4884 [2.3432; 2.6336]
Significant differences found (Q = 244.66, p < 0.0001) indicate that the effects of treatment differ significantly across subgroups.
Random Effects Model Results:
Subgroup comparisons showed no significant differences (Q = 0.62, p = 0.7316).
Bias Analysis:
Funnel Plot Asymmetry:
Number of studies: k = 22 (with 2 added studies).
Random effects model estimate: MD = 2.2542, 95%-CI [0.2979; 4.2105], p = 0.0239.
Prediction Interval: [-7.7065; 12.2148].
Interpretation: Suggests potential publication bias may exist, but further analysis is needed.
Fail-Safe N Calculation:
Using Rosenthal’s methodology, the fail-safe N is calculated as 1833. This means that an additional 1833 studies showing no effect would be required to overturn the significance of the results.

Potential Limitations:
High degree of heterogeneity suggests that study populations or methodologies differ, which can influence the generalizability of the results.
A failure to address potential publication and reporting biases could skew understanding.
2. Plots and Their Interpretation
2.1 Forest Plots
What It Shows: Forest plots illustrate the estimated mean differences with confidence intervals for each study and the overall meta-analysis.
Interpretation: Points outside the confidence interval line (typically a vertical line at zero) indicate statistical significance.
2.2 Funnel Plot
What It Shows: A funnel plot assesses bias by plotting study effect sizes against their variances.
Interpretation: An asymmetric funnel suggests potential publication bias, while a symmetrical funnel indicates reasonable confidence in the collected studies.
2.3 Galbraith Plot
What It Shows: It illustrates the relationship between the observed study outcomes and their standard errors to assess heterogeneity.
Interpretation: Studies falling outside the expected confidence interval bands indicate potential outliers or high influence on the overall effects.
2.4 L’Abbe Plot
What It Shows: A L’Abbe plot depicts the relationship between event rates in the experimental and control groups.
Interpretation: A line of equality indicates that the experimental and control groups have equivalent responses. Deviations indicate differences in efficacy or effect size.
2.5 Baujat Plot
What It Shows: Displays the influence of individual studies on the overall heterogeneity.
Interpretation: Studies that significantly affect heterogeneity will appear in extremes, indicating their disproportionate impact on the aggregate findings.
2.6 Bubble Plot
What It Shows: Shows effect sizes of studies, with bubble size representing sample size.
Interpretation: Larger bubbles suggest more robust conclusions from those studies, while smaller studies are more prone to sampling error.
2.7 Box Plot for Subgroup-effect Size
What It Shows: Illustrates the distribution of effect sizes within each subgroup.
Interpretation: Boxes indicate interquartile ranges, with whiskers denoting variability outside the upper and lower quartiles. Observing overlaps and gaps can inform on subgroup performance.--- But this is only for a specific scenario and an example for you to get the idea. ---

    Please provide a well-structured and detailed report.
    """
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a meta-analysis report generator assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    print("GPT report generator function is ready to use in your R Shiny app.")