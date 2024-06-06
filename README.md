# LIDARGO_samples
This repo hosts sample files from AWAKEN generated thorough the LIDARGO package described in this [document](https://github.com/StefanoWind/LIDARGO_samples/blob/main/docs/240502_LIDARGO.pdf), and a code to read them.

Data files are stored in separate public an propietary folders. All users will have access to the public data at [link](https://app.box.com/s/egvd3vdxd2gevsqgcnoxwuvpkjdvpsl5) while proprietary files (nacelle lidar data streams) are available at this [link](https://nrel.app.box.com/folder/265053402407) only to the CRADA signers (please ask permission to stefano.letizia@nrel.gov). 

Data include:
- b0-level files, which are standardized and quality-controlled using LIDARGO
- c0-level files (nacelle lidars only), which are spatial statistics calculated through the Barnes-scheme-based [LiSBOA](https://amt.copernicus.org/articles/14/2065/2021/) approach embedded in LIDARGO
- figures describing the data standardization and quality control for b0 files
- figures showing the wind statitics for c0 files
  
Test_lidar_b0.py can be used to read b0 files and plot overall radial wind speed field, individual realization of the scans, and distrubution of QC flags within the scanning volume. For testing the b0 data, download them and copy them into the data folder indicated as "source" and run Test_lidar_b0.py with one of the suggested wildcard names. The code will only process the first file if the wildcard has multiple matches.

c0 files have a simpler formatting and the variables can be plotted directly after reading the netCDF files.

The scan schedule for the nacelle lidars at AWAKEN in 2023 is shown below:

![Scan schedule of nacelle-mpunted scanning lidars at AWAKEN in 2023](https://github.com/StefanoWind/LIDARGO_samples/blob/main/docs/AWAKEN_nacelle_lidars_2023.jpg)
