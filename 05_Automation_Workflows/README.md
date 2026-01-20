# Module 6: Automation of Climate Workflows

This directory corresponds to **Lecture 26 & 27**, focusing on automating the entire analysis pipeline from data processing to reporting.

## 📂 Contents

* **`generate_report.R`**: An R script using **R Markdown** to dynamically generate HTML/PDF climate reports.
* **`run_daily_analysis.sh`**: A **Bash shell script** that orchestrates the execution of Python (QC) and R (Reporting) scripts, logging the results.

## 🛠️ Key Concepts

1.  **Reproducible Reporting (R Markdown)**:
    * Mixing code and narrative text to create automated documents.
    * The script generates a `Monthly_Climate_Report.html` containing charts and summary statistics.
2.  **Pipeline Orchestration (Shell)**:
    * Using bash scripts to chain multiple tasks (Python -> R).
    * **Error Handling**: Checking exit codes (`$?`) to stop the pipeline if a step fails.
    * **Logging**: Redirecting outputs (`>> automation.log`) for monitoring.
3.  **Scheduling (Cron)**:
    * Automating the execution using the OS scheduler.

## 🚀 How to Run

### 1. Generate Report Manually
```bash
# Requires R and rmarkdown package
Rscript generate_report.R
