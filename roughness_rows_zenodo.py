import os
import csv
import numpy as np
import pandas as pd
from osgeo import gdal

# =========================
# USER INPUT
# =========================

input_folder = r"W:\\Roughness_1cm_detrend_z"
output_folder = r"W:\\Roughness_rows_z"
lod_path = r"W:\\limit_of_detection_z.csv"

# create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)





for filename in os.listdir(input_folder):
    if not filename.lower().endswith((".tif", ".tiff")):
        continue

    raster_name = os.path.splitext(filename)[0]



    raster_path = os.path.join(input_folder, filename)
    csv_path = os.path.join(output_folder, raster_name + ".csv")

    ds = gdal.Open(raster_path)
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()

    arr = band.ReadAsArray().astype(float)

    if nodata is not None:
        arr[arr == nodata] = np.nan
        arr = np.flipud(arr) #N.B: this makes the row 1 being the upslope, and the last row downslope. Without this, it will be the opposite

    n_rows, n_cols = arr.shape

    results = []


    # =========================
    # ROW-WISE ANALYSIS
    # =========================
    

    for row in range(n_rows):

        row_data = arr[row, :]
        valid_data = row_data[~np.isnan(row_data)]
        n_valid = len(valid_data)

        # ---- ORIGINAL VALUES ----
        
        sum_pos = np.sum(valid_data)
        
        #Sum of vertical changes across all pixels in the row
        mean_surf_change = sum_pos/n_valid 
        
    

        results.append([
            row + 1,
            sum_pos,
            
            mean_surf_change,
            
    ])

    # =========================
    # WRITE CSV
    # =========================

    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "row_id",
            "sum_roughness (m)",
            
            "mean_surf_change_row (m)",# tot sum pf positive and negative but divided by pixels

        ])
        writer.writerows(results)

    print(f"Processed: {filename}")

print("All rasters processed.")
    
    
    