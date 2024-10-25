documentation_content <- HTML('
<h2>Documentation</h2>

<div class="toc">
  <h3 class="open">1. Introduction to Meta-Mar</h3>
  <div class="content">
    <p>Meta-Mar is a user-friendly web application for conducting meta-analyses, developed on top of the powerful R packages \'meta\' (Schwarzer, 2007) and \'metafor\' (Viechtbauer, 2010). It provides an accessible interface for researchers to perform various types of meta-analyses without requiring extensive programming knowledge.</p>
    
    <p>Our goal is to democratize meta-analysis by offering an intuitive platform that guides users through the process, from data input to result interpretation. Meta-Mar supports a wide range of meta-analytic models and methods, making it suitable for researchers across various disciplines.</p>
    
    <p>Whether you\'re a seasoned meta-analyst or new to the field, Meta-Mar offers the flexibility and robustness needed for high-quality meta-analyses, all within a user-friendly web interface.</p>
  </div>

  <h3 class="closed">2. Meta-Analysis Tutorial</h3>
  <div class="content" style="display:none;">
    <h4>Step-by-Step Guide to Conducting a Meta-Analysis with Meta-Mar</h4>
    
    <h5>2.1 Choose Your Meta-Analysis Model</h5>
    <ul>
      <li>Continuous outcomes (metacont)</li>
      <li>Binary outcomes (metabin)</li>
      <li>Generic inverse variance / effect size (metagen)</li>
      <li>Correlations (metacor)</li>
    </ul>
    
    <h5>2.2 Prepare Your Data</h5>
    <p>Depending on your chosen model, prepare your data with the following essential variables:</p>
    <ul>
      <li>Continuous: studlab, n.e, mean.e, sd.e, n.c, mean.c, sd.c</li>
      <li>Binary: studlab, event.e, n.e, event.c, n.c</li>
      <li>Generic: studlab, TE, seTE</li>
      <li>Correlations: studlab, cor, n</li>
    </ul>
    <p>Additional variables for subgroup analysis (e.g., \'subgroup\') and meta-regression can be included.</p>
    
    <p> Variable Definitions </p>
<div>
  <p>Continuous Outcomes (metacont)</p>
  <p>Used for studies comparing means between two groups.</p>
  <ul>
    <li><strong>studlab:</strong> An optional vector with study labels.</li>
    <li><strong>n.e:</strong> Number of observations in experimental group.</li>
    <li><strong>mean.e:</strong> Estimated mean in experimental group.</li>
    <li><strong>sd.e:</strong> Standard deviation in experimental group.</li>
    <li><strong>n.c:</strong> Number of observations in control group.</li>
    <li><strong>mean.c:</strong> Estimated mean in control group.</li>
    <li><strong>sd.c:</strong> Standard deviation in control group.</li>
  </ul>
  <p><strong>Example:</strong> A meta-analysis of studies comparing a new diet (experimental) to a standard diet (control) on weight loss (in kg) after 6 months.</p>
  <div class="table-container">
    <table>
      <tr>
        <th>studlab</th>
        <th>n.e</th>
        <th>mean.e</th>
        <th>sd.e</th>
        <th>n.c</th>
        <th>mean.c</th>
        <th>sd.c</th>
      </tr>
      <tr><td>Smith et al., 2020</td><td>50</td><td>8.5</td><td>2.3</td><td>50</td><td>5.2</td><td>2.1</td></tr>
      <tr><td>Jones et al., 2019</td><td>45</td><td>7.8</td><td>2.5</td><td>48</td><td>5.5</td><td>2.2</td></tr>
      <tr><td>Brown et al., 2021</td><td>55</td><td>9.1</td><td>2.4</td><td>52</td><td>5.8</td><td>2.0</td></tr>
    </table>
  </div>

  <p>Binary Outcomes (metabin)</p>
  <p>Used for studies comparing event rates between two groups.</p>
  <ul>
    <li><strong>studlab:</strong> An optional vector with study labels.</li>
    <li><strong>event.e:</strong> Number of events in experimental group.</li>
    <li><strong>n.e:</strong> Number of observations in experimental group.</li>
    <li><strong>event.c:</strong> Number of events in control group.</li>
    <li><strong>n.c:</strong> Number of observations in control group.</li>
  </ul>
  <p><strong>Example:</strong> A meta-analysis of studies comparing a new drug (experimental) to a placebo (control) on heart attack prevention over 5 years.</p>
  <div class="table-container">
    <table>
      <tr>
        <th>studlab</th>
        <th>event.e</th>
        <th>n.e</th>
        <th>event.c</th>
        <th>n.c</th>
      </tr>
      <tr><td>Johnson et al., 2018</td><td>15</td><td>500</td><td>30</td><td>500</td></tr>
      <tr><td>Lee et al., 2019</td><td>12</td><td>450</td><td>25</td><td>450</td></tr>
      <tr><td>Garcia et al., 2020</td><td>18</td><td>550</td><td>35</td><td>550</td></tr>
    </table>
  </div>

  <p>Generic Inverse Variance / Effect Size (metagen)</p>
  <p>Used when only effect sizes and their standard errors are available.</p>
  <ul>
    <li><strong>studlab:</strong> An optional vector with study labels.</li>
    <li><strong>TE:</strong> Estimated treatment effect (e.g., log odds ratio, mean difference).</li>
    <li><strong>seTE:</strong> Standard error of the treatment estimate.</li>
  </ul>
  <p><strong>Example:</strong> A meta-analysis of studies reporting the effect of a new educational program on standardized test scores, using Cohen\'s d as the effect size.</p>
  <div class="table-container">
    <table>
      <tr>
        <th>studlab</th>
        <th>TE</th>
        <th>seTE</th>
      </tr>
      <tr><td>Wilson et al., 2017</td><td>0.45</td><td>0.12</td></tr>
      <tr><td>Taylor et al., 2018</td><td>0.38</td><td>0.10</td></tr>
      <tr><td>Martinez et al., 2019</td><td>0.52</td><td>0.11</td></tr>
    </table>
  </div>

  <p>Correlations (metacor)</p>
  <p>Used for meta-analysis of correlation coefficients.</p>
  <ul>
    <li><strong>studlab:</strong> An optional vector with study labels.</li>
    <li><strong>cor:</strong> Correlation coefficient.</li>
    <li><strong>n:</strong> Sample size.</li>
  </ul>
  <p><strong>Example:</strong> A meta-analysis of studies examining the correlation between hours of sleep and academic performance in college students.</p>
  <div class="table-container">
    <table>
      <tr>
        <th>studlab</th>
        <th>cor</th>
        <th>n</th>
      </tr>
      <tr><td>Chen et al., 2019</td><td>0.35</td><td>200</td></tr>
      <tr><td>Patel et al., 2020</td><td>0.42</td><td>180</td></tr>
      <tr><td>Kim et al., 2021</td><td>0.38</td><td>220</td></tr>
    </table>
  </div>
</div>
    
    <h5>2.3 Upload Your Data</h5>
    <p>Use the file upload feature to import your prepared dataset (CSV or Excel format).</p>
    
    <h5>2.4 Select Summary Measure</h5>
    <ul>
      <li>Continuous: "MD" (Mean Difference), "SMD" (Standardized Mean Difference), "ROM" (Ratio of Means)</li>
      <li>Binary: "OR" (Odds Ratio), "RR" (Risk Ratio), "RD" (Risk Difference)</li>
      <li>Generic: Any of the above, plus "HR" (Hazard Ratio), "IRR" (Incidence Rate Ratio), etc.</li>
      <li>Correlations: "ZCOR" (Fisher\'s z-transformed), "COR" (untransformed)</li>
    </ul>
    
    <h5>2.5 Choose Pooling Method</h5>
    <p>Fixed-effect methods:</p>
    <ul>
      <li>Mantel-Haenszel (for binary outcomes)</li>
      <li>Peto (for binary outcomes with rare events)</li>
      <li>Inverse Variance (for all types)</li>
      <li>Hedges\' g, Cohen\'s d, Glass\' delta (for continuous outcomes)</li>
    </ul>
    <p>Random-effects methods:</p>
    <ul>
      <li>DerSimonian-Laird</li>
      <li>Restricted Maximum Likelihood (REML)</li>
      <li>Paule-Mandel</li>
      <li>Maximum Likelihood (ML)</li>
      <li>Sidik-Jonkman</li>
      <li>Hedges</li>
      <li>Empirical Bayes (EB)</li>
      <li>Hunter-Schmidt</li>
    </ul>
    
    <h5>2.6 Select Additional Analysis Options</h5>
    <ul>
      <li>Method for estimating between-study variance (τ²)</li>
      <li>Method for calculating confidence intervals for random effects estimate</li>
      <li>Ad hoc variance correction for Hartung-Knapp method</li>
      <li>Method for calculating prediction intervals</li>
      <li>Method for calculating confidence intervals for τ²</li>
    </ul>
    
    <h5>2.7 Run Analysis and Interpret Results</h5>
    <p>After setting all parameters, run the analysis. Review the following outputs:</p>
    <ul>
      <li>Forest Plot (with options for different visualization standards: RevMan5, BMJ, JAMA, IQWiG5, IQWiG6, geneexpr, meta4)</li>
      <li>Heterogeneity statistics</li>
      <li>Publication bias assessment</li>
      <li>Subgroup analysis (if applicable)</li>
      <li>Meta-regression results (if applicable)</li>
    </ul>
    
    <h5>2.8 Additional Analyses</h5>
    <p>Conduct sensitivity analyses or additional tests as needed:</p>
    <ul>
      <li>Publication bias tests (e.g., Egger\'s test, trim-and-fill)</li>
      <li>Influence diagnostics</li>
      <li>Cumulative meta-analysis</li>
    </ul>
    
    <h5>2.9 Generic Inverse Variance / Effect Size (metagen) Analysis</h5>
    <p>This analysis is based on effect sizes and their standard errors. It can be used for various types of outcomes:</p>
    <ul>
      <li>Continuous outcomes: Use standardized mean differences or mean differences with their standard errors</li>
      <li>Binary outcomes: Use log odds ratios, log risk ratios, or risk differences with their standard errors</li>
      <li>Time-to-event outcomes: Use log hazard ratios with their standard errors</li>
    </ul>
    <p>This flexibility makes the generic inverse variance method suitable for a wide range of meta-analytic scenarios.</p>
  </div>

  <h3 class="closed">3. Data Structure Scenarios</h3>
  <div class="content" style="display:none;">
    <h4>Example Data Structures for Different Meta-Analysis Models</h4>
    
    <h5>3.1 Continuous Outcomes (metacont)</h5>
    <div class="table-container">
    <table>
      <tr>
        <th>studlab</th>
        <th>n.e</th>
        <th>mean.e</th>
        <th>sd.e</th>
        <th>n.c</th>
        <th>mean.c</th>
        <th>sd.c</th>
        <th>subgroup</th>
        <th>age</th>
        <th>duration</th>
        <th>quality</th>
      </tr>
      <tr><td>Study 1</td><td>50</td><td>10.5</td><td>2.3</td><td>50</td><td>8.9</td><td>2.1</td><td>A</td><td>45.2</td><td>12</td><td>High</td></tr>
      <tr><td>Study 2</td><td>45</td><td>11.2</td><td>2.5</td><td>48</td><td>9.1</td><td>2.2</td><td>B</td><td>42.8</td><td>10</td><td>Medium</td></tr>
      <tr><td>Study 3</td><td>55</td><td>10.8</td><td>2.4</td><td>52</td><td>9.0</td><td>2.0</td><td>A</td><td>47.5</td><td>14</td><td>High</td></tr>
      <tr><td>Study 4</td><td>48</td><td>10.9</td><td>2.2</td><td>51</td><td>9.2</td><td>2.3</td><td>C</td><td>44.1</td><td>11</td><td>Low</td></tr>
      <tr><td>Study 5</td><td>52</td><td>11.0</td><td>2.6</td><td>49</td><td>8.8</td><td>2.0</td><td>B</td><td>46.3</td><td>13</td><td>Medium</td></tr>
    </table>
    </div>
    
    <h5>3.2 Binary Outcomes (metabin)</h5>
    <div class="table-container">
    <table>
      <tr>
        <th>studlab</th>
        <th>event.e</th>
        <th>n.e</th>
        <th>event.c</th>
        <th>n.c</th>
        <th>subgroup</th>
        <th>year</th>
        <th>region</th>
        <th>risk</th>
      </tr>
      <tr><td>Study 1</td><td>15</td><td>100</td><td>10</td><td>100</td><td>B</td><td>2015</td><td>Europe</td><td>Low</td></tr>
      <tr><td>Study 2</td><td>20</td><td>110</td><td>12</td><td>105</td><td>A</td><td>2016</td><td>North America</td><td>Medium</td></tr>
      <tr><td>Study 3</td><td>18</td><td>95</td><td>11</td><td>98</td><td>C</td><td>2014</td><td>Asia</td><td>High</td></tr>
      <tr><td>Study 4</td><td>22</td><td>120</td><td>14</td><td>115</td><td>B</td><td>2017</td><td>Europe</td><td>Medium</td></tr>
      <tr><td>Study 5</td><td>16</td><td>105</td><td>9</td><td>102</td><td>A</td><td>2015</td><td>South America</td><td>Low</td></tr>
    </table>
    </div>
    
    <h5>3.3 Generic Inverse Variance / Effect Size (metagen)</h5>
    <div class="table-container">
    <table>
      <tr>
        <th>studlab</th>
        <th>TE</th>
        <th>seTE</th>
        <th>subgroup</th>
        <th>sample_size</th>
        <th>intervention_type</th>
        <th>follow_up</th>
      </tr>
      <tr><td>Study 1</td><td>0.5</td><td>0.1</td><td>C</td><td>200</td><td>Drug A</td><td>6</td></tr>
      <tr><td>Study 2</td><td>0.4</td><td>0.12</td><td>B</td><td>180</td><td>Drug B</td><td>12</td></tr>
      <tr><td>Study 3</td><td>0.6</td><td>0.09</td><td>A</td><td>220</td><td>Drug A</td><td>9</td></tr>
      <tr><td>Study 4</td><td>0.45</td><td>0.11</td><td>C</td><td>190</td><td>Drug C</td><td>8</td></tr>
      <tr><td>Study 5</td><td>0.55</td><td>0.08</td><td>B</td><td>210</td><td>Drug B</td><td>10</td></tr>
    </table>
    </div>
    
    <h5>3.4 Correlations (metacor)</h5>
    <div class="table-container">
    <table>
      <tr>
        <th>studlab</th>
        <th>cor</th>
        <th>n</th>
        <th>subgroup</th>
        <th>age_group</th>
        <th>measure_type</th>
        <th>reliability</th>
      </tr>
      <tr><td>Study 1</td><td>0.45</td><td>100</td><td>A</td><td>Adult</td><td>Self-report</td><td>0.85</td></tr>
      <tr><td>Study 2</td><td>0.52</td><td>95</td><td>B</td><td>Adolescent</td><td>Interview</td><td>0.88</td></tr>
      <tr><td>Study 3</td><td>0.48</td><td>110</td><td>A</td><td>Adult</td><td>Observation</td><td>0.82</td></tr>
      <tr><td>Study 4</td><td>0.50</td><td>105</td><td>C</td><td>Elderly</td><td>Self-report</td><td>0.86</td></tr>
      <tr><td>Study 5</td><td>0.47</td><td>98</td><td>B</td><td>Adult</td><td>Interview</td><td>0.84</td></tr>
    </table>
    </div>
  </div>
</div>

<script>
document.querySelectorAll(\'.toc h3\').forEach(item => {
  item.addEventListener(\'click\', event => {
    event.target.classList.toggle(\'open\');
    event.target.classList.toggle(\'closed\');
    event.target.nextElementSibling.style.display = event.target.classList.contains(\'open\') ? \'block\' : \'none\';
  })
});
</script>
')
