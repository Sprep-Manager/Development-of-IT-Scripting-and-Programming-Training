# ==========================================
# [Automated Reporting] Monthly Climate Summary
# Module 6 Lec 26: Generating & Distributing PDF/HTML
# ==========================================

# 1. 라이브러리 로드 (없으면 설치 필요)
if (!require("rmarkdown")) install.packages("rmarkdown")
if (!require("ggplot2")) install.packages("ggplot2")
if (!require("dplyr")) install.packages("dplyr")

library(rmarkdown)
library(ggplot2)
library(dplyr)

# ==========================================
# [Step 1] Create RMarkdown Template dynamically
# (실습 편의를 위해 .Rmd 파일을 코드로 생성합니다)
# ==========================================
report_filename <- "monthly_climate_report.Rmd"

rmd_content <- '
---
title: "Monthly Climate Analysis Report"
author: "Automated System (ClimSA)"
date: "`r Sys.Date()`"
output: html_document
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = FALSE, warning = FALSE, message = FALSE)
library(ggplot2)
