# =======================================================
# SPREP ClimSA Training - R Environment Setup Script
# =======================================================

# List of required packages for the training
packages <- c(
  "rmarkdown",  # For automated reporting (Module 6)
  "ggplot2",    # For visualization (Module 4)
  "dplyr",      # For data manipulation
  "knitr",      # Dependency for rmarkdown
  "ncdf4"       # For NetCDF data handling (Module 2)
)

# Identify missing packages
new_packages <- packages[!(packages %in% installed.packages()[,"Package"])]

# Install missing packages
if(length(new_packages)) {
  message("🚀 Installing missing packages: ", paste(new_packages, collapse = ", "))
  install.packages(new_packages, repos = "http://cran.us.r-project.org")
} else {
  message("✅ All required packages are already installed.")
}

message("🎉 R Environment Setup Complete!")
