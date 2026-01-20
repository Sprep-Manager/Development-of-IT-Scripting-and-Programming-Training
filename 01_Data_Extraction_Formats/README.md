# Module 2: Climate Data Formats & Integration

This directory covers **Lecture 10: Heterogeneous Data Integration**. It demonstrates how to handle and merge different climate data formats common in NMHSs operations.

## 📂 Contents

* **`merge_station_grid_data.py`**: A Python script that integrates Station data (CSV) with Gridded Model/Satellite data (NetCDF).

## 🛠️ Key Concepts

1.  **Reading Heterogeneous Formats**:
    * **CSV**: Used for observational station data (Point data).
    * **NetCDF (`.nc`)**: Used for satellite, reanalysis, or climate model data (Grid data).
2.  **Spatial Extraction**:
    * Using `xarray.sel(method='nearest')` to find the grid point corresponding to a specific station's latitude/longitude.
3.  **Time Series Merging**:
    * Aligning datasets based on timestamps using `pandas.merge`.

## 🚀 How to Run

```bash
# Ensure you have the required libraries installed
pip install pandas xarray netCDF4 numpy

# Run the integration script
python merge_station_grid_data.py
