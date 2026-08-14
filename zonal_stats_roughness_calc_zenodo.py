import os
import csv
import numpy as np
from qgis.core import QgsRasterLayer, QgsRasterBandStats
from osgeo import gdal

# Here adjust the folder where the input files are positioned
dem_folder = r"W:\ESG\DOW_SLM\PhD_projects\Marta_Loreggian\DEM_1cm"#folder of the 1cm DEMs
rough_folder = r"W:\ESG\DOW_SLM\PhD_projects\Marta_Loreggian\Roughness\Roughness_1cm_detrend"#folder with 1cm detrended roughness calculated
output_csv = r"W:\ESG\DOW_SLM\PhD_projects\Marta_Loreggian\Spatial_analysis_py\mesocosm_spatial_analysis\roughness_raster_statistics.csv"#output raster. Use as input the one previously calculated
band = 1

# Call the raster path
def raster_to_array(path):
    ds = gdal.Open(path)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray().astype(float)
    nodata = band.GetNoDataValue()
    if nodata is not None:
        arr[arr == nodata] = np.nan
    return arr

results = []

for dem_file in os.listdir(dem_folder):
    if not dem_file.lower().endswith(".tif"):
        continue

    # Expecting: 1cm_{run_name}.tif
    if not dem_file.startswith("1cm_"):
        continue

    run_name = dem_file.replace("1cm_", "").replace(".tif", "")

    dem_path = os.path.join(dem_folder, dem_file)

    rough_file = f"Rough_1cm_Detrended_{run_name}.tif" #this is the name of the .tif in the folder of the detrnded rasters
    rough_path = os.path.join(rough_folder, rough_file)

    if not os.path.exists(rough_path):
        print(f"Missing roughness raster for run: {run_name}")
        continue

# Load raster arrays
    dem_arr = raster_to_array(dem_path)
    rough_arr = raster_to_array(rough_path)

    # Elevation quantiles (relative elevation)
    q33, q66 = np.nanpercentile(dem_arr, [33.33, 66.66])

    # Masks: meaning divide in three equal zones my whole raster
    foot_mask = dem_arr <= q33
    middle_mask = (dem_arr > q33) & (dem_arr <= q66)
    upper_mask = dem_arr > q66

    # Standard deviations of roughness
    sd_foot = np.nanstd(rough_arr[foot_mask])
    sd_middle = np.nanstd(rough_arr[middle_mask])
    sd_upper = np.nanstd(rough_arr[upper_mask])

    #mean of roughness

    average_foot = np.nanmean(rough_arr[foot_mask])
    average_middle = np.nanmean(rough_arr[middle_mask])
    average_upper = np.nanmean(rough_arr[upper_mask])

    # Whole-raster statistics (QGIS-native)
    rough_layer = QgsRasterLayer(rough_path, rough_file)
    provider = rough_layer.dataProvider()
    stats = provider.bandStatistics(band, QgsRasterBandStats.All)

    results.append([
        rough_file,
        stats.minimumValue*1000,
        stats.mean*1000,
        stats.maximumValue*1000,
        stats.stdDev*1000,
        sd_upper*1000,
        sd_middle*1000,
        sd_foot*1000,
        average_upper*1000,
        average_middle*1000,
        average_foot*1000
    ])

# Write CSV
with open(output_csv, "w", newline="") as f: #this part overwrites the prvious csv I had, but adding noew columns
    writer = csv.writer(f)
    writer.writerow([
        "filename",
        "minimum (mm)",
        "mean(mm)",
        "maximum(mm)",
        "standard_deviation(mm)",
        "SD_up(mm)",
        "SD_middle(mm)",
        "SD_foot(mm)",
        "mean_up (mm)",
        "mean_middle (mm)",
        "mean_foot (mm)"
    ])
    writer.writerows(results)

print("new CSV successfully written.")