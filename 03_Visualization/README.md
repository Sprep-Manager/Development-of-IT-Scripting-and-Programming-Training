# Module 4: Climate Data Visualization

This directory focuses on **Lecture 18 & 19**, demonstrating how to create professional climate maps using Python's `Cartopy` and `Matplotlib` libraries.

## 📂 Contents

* **`plot_spatial_map.py`**: A script that generates a spatial map visualizing **Temperature (Scalar)** and **Wind (Vector)** fields over the Pacific region.

## 🛠️ Key Concepts

1.  **Map Projections (`Cartopy`)**:
    * Using `ccrs.PlateCarree(central_longitude=180)` to center the map on the Pacific Ocean, which is critical for SPREP member states.
2.  **Scalar Visualization (Contourf)**:
    * Plotting temperature fields using filled contours (`contourf`) with a diverging colormap (`RdYlBu_r`).
3.  **Vector Visualization (Quiver)**:
    * Overplotting wind arrows (`quiver`) to show atmospheric circulation patterns.
4.  **Map Features**:
    * Adding standard geographic features: Coastlines, Borders, Land/Ocean colors, and Gridlines.

## 🚀 How to Run

> **Prerequisite**: This script requires `cartopy`, which is best installed via Conda.

```bash
# Recommended installation via Conda
conda install -c conda-forge cartopy matplotlib numpy

# Run the visualization script
python plot_spatial_map.py
