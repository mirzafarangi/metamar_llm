library(shiny)
library(meta)
library(readxl)
library(ggplot2)
library(dplyr)
library(metafor)
library(DT)
library(reticulate)


use_condaenv("ruckizucki", required = TRUE)

# Use reticulate to source the Python script
source_python("gpt_report.py")
# Source the documentation content
source("documentation_content.R")

ui <- fluidPage(
  tags$head(
    tags$style(HTML('
    
    .toc h3 { cursor: pointer; padding: 10px; background-color: #f0f0f0; margin: 5px 0; }
    .toc h3::before { content: "▶ "; }
    .toc h3.open::before { content: "▼ "; }
    .toc h3.open { background-color: #e0e0e0; }
    .content { margin-left: 20px; padding: 10px; border-left: 2px solid #ddd; }
    .table-container { width: 100%; overflow-x: auto; }
    table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; white-space: nowrap; }
    th { background-color: #f2f2f2; }
    tr:nth-child(even) { background-color: #f9f9f9; }
    .toc h4, .toc h5 { margin-top: 15px; margin-bottom: 10px; }
    .toc ul { padding-left: 20px; }
    '))
  ),
  titlePanel("Meta-Analysis App"),
  sidebarLayout(
    sidebarPanel(
      fileInput("file", "Upload Excel or CSV File", accept = c(".xlsx", ".csv")),
      selectInput("model", "Choose the Meta-Analysis Model",
                  choices = c("Continuous outcome" = "metacont",
                              "Binary outcome" = "metabin",
                              "Generic inverse variance (effect size)" = "metagen",
                              "Correlations" = "metacor")),
      uiOutput("sm_ui"),
      uiOutput("smd_method_ui"),
      uiOutput("pooling_method_ui"),
      selectInput("method.tau", "τ² Estimator (estimates the between-study variance)",
                  choices = c("REML: Restricted maximum-likelihood (Viechtbauer, 2005)" = "REML",
                              "PM: Paule-Mandel (Paule and Mandel, 1982)" = "PM",
                              "DL: DerSimonian-Laird (DerSimonian and Laird, 1986)" = "DL",
                              "ML: Maximum-likelihood (Viechtbauer, 2005)" = "ML",
                              "HS: Hunter-Schmidt (Hunter and Schmidt, 2015)" = "HS",
                              "SJ: Sidik-Jonkman (Sidik and Jonkman, 2005)" = "SJ",
                              "HE: Hedges (Hedges and Olkin, 1985)" = "HE",
                              "EB: Empirical Bayes (Morris, 1983)" = "EB"),
                  selected = "REML"),
      selectInput("method.random.ci", "Select the Method for Calculating Confidence Intervals for the Random Effects Estimate",
                  choices = c("Based on standard normal quantile (classic)" = "classic",
                              "Hartung-Knapp method" = "HK",
                              "Kenward-Roger method (only available with REML)" = "KR")),
      conditionalPanel(
        condition = "input.method.random.ci == 'HK'",
        selectInput("adhoc.hakn.ci", "Choose Ad Hoc Variance Correction for Hartung-Knapp Method",
                    choices = c("No correction" = "",
                                "Use variance correction if HK standard error is smaller" = "se",
                                "Use variance correction if HK CI is narrower" = "IQWiG6",
                                "Use wider CI of classic and HK" = "ci"))
      ),
      selectInput("method.predict", "Select the Method for Calculating Prediction Intervals",
                  choices = c("Based on t-distribution (HTS)" = "HTS",
                              "Hartung-Knapp method (HK)" = "HK",
                              "Kenward-Roger method (KR)" = "KR",
                              "Bootstrap approach (NNF)" = "NNF",
                              "Based on standard normal quantile (S)" = "S")),
      conditionalPanel(
        condition = "input.method.predict == 'HK'",
        selectInput("adhoc.hakn.pi", "Choose Ad Hoc Variance Correction for Prediction Intervals",
                    choices = c("No correction" = "",
                                "Use variance correction" = "se"))
      ),
      selectInput("method.tau.ci", "Select the Method for Calculating Confidence Intervals for τ²",
                  choices = c("Jackson method" = "J",
                              "Biggerstaff and Jackson method" = "BJ",
                              "Q-Profile method" = "QP",
                              "Profile-Likelihood method (only for three-level meta-analysis)" = "PL",
                              "No confidence interval" = "")),
      
      actionButton("run", "Run Analysis")
    ),
    mainPanel(
      tabsetPanel(id = "tabs",
                  tabPanel("Documentation",
                           documentation_content
                            ),
                  tabPanel("Data Summary", 
                           DTOutput("data_table"),
                           uiOutput("data_summary")
                  ),
                  tabPanel("Meta-Analysis Summary", 
                           verbatimTextOutput("ma_summary")),
                  tabPanel("Plots",
                           tabsetPanel(
                             tabPanel("Forest Plot", 
                                      selectInput("forest_settings", "Choose Forest Plot Settings",
                                                  choices = c("Default", "RevMan5", "BMJ", "JAMA", "IQWiG5", "IQWiG6", "geneexpr", "meta4")),
                                      plotOutput("forest_plot_common", height = "800px"),
                                      br(),
                                      plotOutput("forest_plot_random", height = "800px")),
                             tabPanel("Funnel Plot", plotOutput("funnel_plot", height = "600px")),
                             tabPanel("Other Plots",
                                      selectInput("other_plot", "Select Plot Type",
                                                  choices = c("Galbraith Plot", "L'Abbe Plot", "Baujat Plot", "Bubble Plot")),
                                      HTML("<p><strong>Galbraith Plot:</strong> Shows the relationship between precision and effect size.</p>
                                 <p><strong>L'Abbe Plot:</strong> Compares event rates in treatment and control groups (for binary outcomes).</p>
                                 <p><strong>Baujat Plot:</strong> Identifies studies that contribute to heterogeneity.</p>
                                 <p><strong>Bubble Plot:</strong> Visualizes meta-regression results.</p>"),
                                      plotOutput("other_plot", height = "600px"))
                           )),
                  tabPanel("Meta-Regression", 
                           p("Meta-regression is used to explore the relationship between study-level covariates and effect sizes. For all models, you'll need to add one or more covariates to your existing data structure. These covariates can be continuous or categorical."),
                           uiOutput("metareg_vars"),
                           verbatimTextOutput("metareg_summary")),
                  tabPanel("Bias Analysis", 
                           h4("Test for funnel plot asymmetry"),
                           verbatimTextOutput("bias_analysis"),
                           br(),
      
                           selectInput("fsn_method", "File Drawer Analysis (fail-safe N) Method",
                                       choices = c("Rosenthal", "Orwin", "Rosenberg")),
                           verbatimTextOutput("fsn_analysis")),
                  tabPanel("Report Generator",
                           br(),
                           actionButton("generate_report", "Generate Comprehensive Report"),
                           br(),
                           uiOutput("gpt_report")
                  
                  )
      )
    )
  )
)

server <- function(input, output, session) {
  create_link <- function(text, tab) {
    sprintf("<a href='#' onclick='$(\"a[data-value=%s]\").tab(\"show\");'>%s</a>", tab, text)
  }
  data <- reactive({
    req(input$file)
    ext <- tools::file_ext(input$file$datapath)
    
    tryCatch(
      {
        if(ext == "csv") {
          read.csv(input$file$datapath)
        } else if(ext == "xlsx") {
          read_excel(input$file$datapath)
        } else {
          stop("Unsupported file format")
        }
      },
      error = function(e) {
        showNotification(HTML("Error reading file. Please make sure it's a valid CSV or Excel file."), type = "error")
        return(NULL)
      }
    )
  })
  
  validate_data <- reactive({
    req(data())
    req(input$model)
    
    required_cols <- switch(input$model,
                            "metacont" = c("studlab", "n.e", "mean.e", "sd.e", "n.c", "mean.c", "sd.c"),
                            "metabin" = c("studlab", "event.e", "n.e", "event.c", "n.c"),
                            "metagen" = c("studlab", "TE", "seTE"),
                            "metacor" = c("studlab", "cor", "n"))
    
    missing_cols <- setdiff(required_cols, names(data()))
    
    if(length(missing_cols) > 0) {
      showNotification(HTML(paste0("It seems your data structure doesn't match this analysis. For the selected model (", input$model, "), the data structure should be: ", paste(required_cols, collapse=", "), ". Please make sure your data is structured in line with the <a href='#' onclick='$(\"a[data-value=Documentation]\").tab(\"show\");'>Documentation</a>.")), type = "error", duration = NULL)
      return(NULL)
    }
    
    return(data())
  })
  
  output$sm_ui <- renderUI({
    choices <- switch(input$model,
                      "metacont" = c("Mean Difference (MD)" = "MD",
                                     "Standardized Mean Difference (SMD)" = "SMD",
                                     "Ratio of Means (ROM)" = "ROM"),
                      "metabin" = c("Odds Ratio (OR)" = "OR",
                                    "Risk Ratio (RR)" = "RR",
                                    "Risk Difference (RD)" = "RD"),
                      "metagen" = c("Mean Difference (MD)" = "MD",
                                    "Standardized Mean Difference (SMD)" = "SMD",
                                    "Ratio of Means (ROM)" = "ROM",
                                    "Odds Ratio (OR)" = "OR",
                                    "Risk Ratio (RR)" = "RR",
                                    "Risk Difference (RD)" = "RD",
                                    "Hazard Ratio (HR)" = "HR",
                                    "Incidence Rate Ratio (IRR)" = "IRR"),
                      "metacor" = c("Fisher's z-transformed correlation (ZCOR)" = "ZCOR",
                                    "Untransformed correlation (COR)" = "COR"))
    selectInput("sm", "Summary measure used for pooling of studies", choices = choices)
  })
  
  output$smd_method_ui <- renderUI({
    if (input$sm == "SMD") {
      selectInput("smd_method", "SMD method",
                  choices = c("Hedges' g" = "Hedges",
                              "Cohen's d" = "Cohen",
                              "Glass' delta" = "Glass"))
    }
  })
  
  output$pooling_method_ui <- renderUI({
    if (input$model == "metabin") {
      selectInput("pooling_method", "Method for pooling studies",
                  choices = c("Mantel-Haenszel" = "MH",
                              "Inverse Variance" = "Inverse",
                              "Peto" = "Peto"))
    } else {
      selectInput("pooling_method", "Method for pooling studies",
                  choices = c("Inverse Variance" = "Inverse"),
                  selected = "Inverse")
    }
  })
  
  meta_analysis <- eventReactive(input$run, {
    req(validate_data())
    
    meta_func <- switch(input$model,
                        "metacont" = metacont,
                        "metabin" = metabin,
                        "metagen" = metagen,
                        "metacor" = metacor)
    
    analysis_data <- validate_data()
    
    args <- list(sm = input$sm,
                 method.tau = input$method.tau,
                 method.random.ci = input$method.random.ci,
                 adhoc.hakn.ci = input$adhoc.hakn.ci,
                 method.predict = input$method.predict,
                 adhoc.hakn.pi = input$adhoc.hakn.pi,
                 method.tau.ci = input$method.tau.ci,
                 method.bias = input$method.bias)
    
    if (input$model == "metabin") {
      args$method <- input$pooling_method
    }
    
    if (input$model == "metacont" && input$sm == "SMD") {
      args$method.smd <- input$smd_method
    }
    
    tryCatch({
      result <- do.call(meta_func, c(args, as.list(analysis_data)))
      
      # Ensure all columns from the original data are included in the meta-analysis object
      result$data <- analysis_data
      
      result
    }, error = function(e) {
      showNotification(HTML(paste0("Error in meta-analysis: ", e$message, ". Please make sure your data is structured in line with the <a href='#' onclick='$(\"a[data-value=Documentation]\").tab(\"show\");'>Documentation</a>.")), type = "error", duration = NULL)
      return(NULL)
    })
  })
  
  output$data_table <- renderDT({
    req(input$file)
    datatable(data(), options = list(pageLength = 10, scrollX = TRUE))
  })
  
  output$data_summary <- renderUI({
    if(is.null(input$file)) {
      HTML(paste0(
        "<div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 5px;'>",
        "<h4>No data uploaded yet</h4>",
        "<p>To get started:</p>",
        "<ol style='text-align: left; display: inline-block;'>",
        "<li>Upload your data</li>",
        "<li>Set the model</li>",
        "<li>Run the analysis</li>",
        "</ol>",
        "<p>Or take a moment to review the ", create_link("documentation", "Documentation"), " for guidance.</p>",
        "</div>"
      ))
    } else {
      verbatimTextOutput("data_summary_text")
    }
  })
  
  output$data_summary_text <- renderPrint({
    req(input$file)
    summary(data())
  })
  output$ma_summary <- renderPrint({
    req(meta_analysis())
    if (!is.null(meta_analysis()$subgroup)) {
      summary(meta_analysis(), subgroup = TRUE)
    } else {
      summary(meta_analysis())
    }
  })
  
  output$forest_plot_common <- renderPlot({
    req(meta_analysis())
    if(input$forest_settings != "Default") {
      settings.meta(input$forest_settings)
    }
    forest(meta_analysis(), common = TRUE, random = FALSE, 
           main = "Common Effect Model Forest Plot")
  })
  
  output$forest_plot_random <- renderPlot({
    req(meta_analysis())
    if(input$forest_settings != "Default") {
      settings.meta(input$forest_settings)
    }
    forest(meta_analysis(), common = FALSE, random = TRUE, 
           main = "Random Effects Model Forest Plot")
  })
  
  output$funnel_plot <- renderPlot({
    req(meta_analysis())
    funnel(meta_analysis())
  })
  
  output$other_plot <- renderPlot({
    req(meta_analysis())
    switch(input$other_plot,
           "Galbraith Plot" = radial(meta_analysis()),
           "L'Abbe Plot" = {
             if(input$model == "metabin") {
               labbe(meta_analysis())
             } else {
               plot(NULL, xlab="", ylab="", main="L'Abbe plot only available for binary outcomes")
             }
           },
           "Baujat Plot" = baujat(meta_analysis()),
           "Bubble Plot" = {
             tryCatch({
               mr <- metareg(meta_analysis(), ~year)
               bubble(mr)
             }, error = function(e) {
               plot(NULL, xlab="", ylab="", main="Bubble plot not available (meta-regression error)")
             })
           })
  })
  
  output$metareg_vars <- renderUI({
    req(data())
    basic_vars <- switch(input$model,
                         "metacont" = c("studlab", "n.e", "mean.e", "sd.e", "n.c", "mean.c", "sd.c"),
                         "metabin" = c("studlab", "event.e", "n.e", "event.c", "n.c"),
                         "metagen" = c("studlab", "TE", "seTE"),
                         "metacor" = c("studlab", "cor", "n"))
    
    additional_vars <- setdiff(names(data()), basic_vars)
    
    if (length(additional_vars) > 0) {
      checkboxGroupInput("metareg_vars", "Choose variables for meta-regression:",
                         choices = additional_vars,
                         selected = NULL)
    } else {
      helpText("No additional variables available for meta-regression.")
    }
  })
  
  output$metareg_vars <- renderUI({
    req(data())
    basic_vars <- switch(input$model,
                         "metacont" = c("studlab", "n.e", "mean.e", "sd.e", "n.c", "mean.c", "sd.c"),
                         "metabin" = c("studlab", "event.e", "n.e", "event.c", "n.c"),
                         "metagen" = c("studlab", "TE", "seTE"),
                         "metacor" = c("studlab", "cor", "n"))
    
    additional_vars <- setdiff(names(data()), basic_vars)
    
    if (length(additional_vars) > 0) {
      checkboxGroupInput("metareg_vars", "Choose variables for meta-regression:",
                         choices = additional_vars,
                         selected = NULL)
    } else {
      helpText("No additional variables available for meta-regression.")
    }
  })
  
  output$metareg_summary <- renderPrint({
    req(meta_analysis())
    req(input$metareg_vars)
    
    if (length(input$metareg_vars) > 0) {
      formula <- as.formula(paste("~", paste(input$metareg_vars, collapse = " + ")))
      tryCatch({
        mr <- metareg(meta_analysis(), formula)
        summary(mr)
      }, error = function(e) {
        showNotification(HTML(paste0("Meta-regression error: ", e$message, ". Please make sure your data is structured in line with the <a href='#' onclick='$(\"a[data-value=Documentation]\").tab(\"show\");'>Documentation</a>.")), type = "error", duration = NULL)
        return(NULL)
      })
    } else {
      cat("No variables selected for meta-regression.")
    }
  })
  
  output$bias_analysis <- renderPrint({
    req(meta_analysis())
    
    tryCatch({
      tf <- trimfill(meta_analysis())
      summary(tf)
    }, error = function(e) {
      showNotification(HTML(paste0("Error in trim and fill analysis: ", e$message, ". Please make sure your data is structured in line with the <a href='#' onclick='$(\"a[data-value=Documentation]\").tab(\"show\");'>Documentation</a>.")), type = "error", duration = NULL)
      return(NULL)
    })
  })
  
  output$fsn_analysis <- renderPrint({
    req(meta_analysis())
    tryCatch({
      # Extract effect sizes and standard errors from the meta-analysis object
      TE <- meta_analysis()$TE
      seTE <- meta_analysis()$seTE
      
      # Run fail-safe N analysis
      fsn_result <- fsn(TE, seTE, type = input$fsn_method)
      print(fsn_result)
    }, error = function(e) {
      showNotification(HTML(paste0("Error in fail-safe N analysis: ", e$message, ". Please make sure your data is structured in line with the <a href='#' onclick='$(\"a[data-value=Documentation]\").tab(\"show\");'>Documentation</a>.")), type = "error", duration = NULL)
      return(NULL)
    })
  })
  
  model_settings_summary <- reactive({
    req(input$model, input$sm, input$method.tau, input$method.random.ci,
        input$method.predict, input$method.tau.ci)
    
    paste(
      "Model Type:", input$model,
      "\nSummary Measure:", input$sm,
      "\nτ² Estimator:", input$method.tau,
      "\nRandom Effects CI Method:", input$method.random.ci,
      "\nPrediction Interval Method:", input$method.predict,
      "\nτ² CI Method:", input$method.tau.ci,
      if (!is.null(input$smd_method)) paste("\nSMD Method:", input$smd_method),
      if (!is.null(input$pooling_method)) paste("\nPooling Method:", input$pooling_method),
      if (!is.null(input$adhoc.hakn.ci)) paste("\nHartung-Knapp Correction:", input$adhoc.hakn.ci),
      if (!is.null(input$adhoc.hakn.pi)) paste("\nPrediction Interval Correction:", input$adhoc.hakn.pi)
    )
  })
  
  meta_summary <- reactive({
    req(meta_analysis())
    
    ma_summary <- capture.output(summary(meta_analysis()))
    bias_summary <- capture.output({
      print(trimfill(meta_analysis()))
      print(fsn(meta_analysis()$TE, meta_analysis()$seTE, type = input$fsn_method))
    })
    
    paste(
      "Meta-Analysis Summary:",
      paste(ma_summary, collapse = "\n"),
      "\n\nBias Analysis:",
      paste(bias_summary, collapse = "\n")
    )
  })
  
  observeEvent(input$generate_report, {
    
    report <- generate_report(model_settings_summary(), meta_summary())
    
    output$loading <- renderUI(NULL)
    
    output$gpt_report <- renderUI({
      tags$div(
        class = "content",
        style = "margin-top: 20px; padding: 20px; background-color: #f8f9fa; border-radius: 5px;",
        HTML(markdown::markdownToHTML(text = report, fragment.only = TRUE))
      )
    })
  })
}

shinyApp(ui, server)