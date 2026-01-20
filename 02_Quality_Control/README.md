# Module 3: Data Quality Control & Cleaning

This directory corresponds to **Lecture 11 & 12**, focusing on cleaning raw meteorological data. It demonstrates how to detect errors, handle outliers, and fill missing gaps using Python.

## 📂 Contents

* **`qc_outlier_check.py`**: A robust script that implements a multi-stage QC pipeline (Physical limits + Statistical checks + Interpolation).

## 🛠️ QC Pipeline Overview

The script processes data through the following stages, simulating a real-world operational workflow:

### 1. Physical Limit Check (Lec 11)
Checks if the data values are within physically possible ranges.
* **Temperature**: Must be between -50°C and +50°C. Values like `-100.0` or `999.9` (error codes) are flagged.
* **Precipitation**: Must be ≥ 0mm. Negative values (e.g., `-5.0`) are removed.

### 2. Statistical Outlier Detection (Lec 11)
Uses **Z-Score** to identify values that deviate significantly from the mean (e.g., $|Z| > 3$).
* Helps filter out spikes that pass the physical check but are statistically improbable (e.g., sudden 45°C in winter).

### 3. Missing Data Interpolation (Lec 12)
Fills the gaps created by missing observations or removed bad data.
* **Temperature**: Uses `linear interpolation` as temperature changes continuously.
* **Precipitation**: Uses `forward fill` (or 0) as rain is discontinuous.

## 🚀 How to Run

```bash
# Ensure pandas and numpy are installed
pip install pandas numpy

# Run the QC pipeline
python qc_outlier_check.py
