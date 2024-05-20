# LIDARGO_samples
This repo hosts sample files from AWAKEN generated thorough the LIDARGO package.

Test_lidar_b0.py can be used to read standardized and quality-controlled (b0) files and plot overall radial wind speed field, individual realization of the scans, and distrubution of QC flags within the scanning volume.

Data are stored in separate public an propietary folders. All users will have access to the public data while propietary files (nacelle lidar data streams) are available at this [link](https://nrel.app.box.com/folder/264604405404) only to the CRADA signers. For testing propietary data, simply download and copy them into the dedicated data folder of this repo.

Data include:
- b0-level files, which are standardized and quality-controlled using the LIDARGO package also described in the 240502_LIDARGO.pdf
- c0-level files (nacelle lidars only), which are spatial statistics caclculated through the Barnes-scheme-based [LiSBOA](https://amt.copernicus.org/articles/14/2065/2021/) approach
- figures describing the data standardization and quality control for b0 files
- figures showing the wind statitics for c0 files

The 
