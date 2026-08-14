import os
import csv
import numpy as np
import pandas as pd
from osgeo import gdal

# =========================
# USER INPUT
# =========================


# ---  RAINFALL INPACT ---
# Activate or deactivate the inputs based on the output to get.

input_folder = r"C:\\DoD_1cm_nodetrended_z" #for the DoD normal
output_folder = r"C:\\DoD_values_output_z"
lod_path = r"C:\\limit_of_detection_z.csv"


# ----- ANIMAL IMPACT ---
#input_folder = r"C:\\DoD_1cm_animals effect_z"
#output_folder = r"C:\\Animal_disturbance_csv_z"
#lod_path = r"C:\\LoD_animalsDoD_z.csv"



# create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Read the LoD file

lod_df = pd.read_csv(lod_path)

# Create dictionary for the LoD 
# Expected columns: DoD, DoD_name, "LoD (m)", "LoD(95%)"
lod_dict = dict(zip(lod_df["DoD_name"], lod_df["LoD (m)"]))
lod95_dict = dict(zip(lod_df["DoD_name"], lod_df["LoD(95%)"]))

# This will collect one row per raster (whole-DoD summary), used to build the
# mean/range of % area above LoD vs LoD(95%) for the results-section comparison.
summary_rows = []

for filename in os.listdir(input_folder):
    if not filename.lower().endswith((".tif", ".tiff")):
        continue

    raster_name = os.path.splitext(filename)[0]

    if raster_name not in lod_dict:
        print(f"LoD not found for {raster_name}, skipping.")
        continue

    lod_value = lod_dict[raster_name]
    lod95_value = lod95_dict[raster_name]

    raster_path = os.path.join(input_folder, filename)
    csv_path = os.path.join(output_folder, raster_name + ".csv")

    ds = gdal.Open(raster_path)
    band = ds.GetRasterBand(1)
    nodata = band.GetNoDataValue()

    arr = band.ReadAsArray().astype(float)

    if nodata is not None:
        #arr[arr >= 3.4e+38] = np.nan# in my DEM, no data are usually this large number.
        # Other option to deal with 'no data if that doesn't work:
        arr[np.isclose(arr, nodata)] = np.nan
    arr = np.flipud(arr) #N.B: this makes the row 1 being the upslope, and the last row downslope. Without this, it will be the opposite

    n_rows, n_cols = arr.shape

    results = []
    
    # running totals across the whole raster, for the whole-DoD summary row
    total_valid = 0
    total_above_lod = 0
    total_above_lod95 = 0

    # =========================
    # ROW-WISE ANALYSIS
    # =========================

    for row in range(n_rows):

        row_data = arr[row, :]
        valid_data = row_data[~np.isnan(row_data)]
        n_valid = len(valid_data)
        
        # ---- ORIGINAL VALUES ----
        pos_vals = valid_data[valid_data > 0]
        neg_vals = valid_data[valid_data < 0]

        sum_pos = np.sum(pos_vals) #sum of cells with positive values (m)
        sum_neg = np.sum(neg_vals)
        n_pix_pos = len(pos_vals)
        n_pix_neg = len(neg_vals)
        net_val = (sum_pos + sum_neg)#Sum of vertical changes across all pixels in the row
        mean_surf_change = net_val/n_valid if n_valid > 0 else np.nan # The 'if' has been added in a second moment. 
        
        # Calculate area (m2)
        pixel_area = 0.01 * 0.01  # 1 cm resolution in meters
        area_pos = n_pix_pos * pixel_area
        area_neg = n_pix_neg * pixel_area
        
        # Calculate volume
        vol_pos = sum_pos * pixel_area
        vol_neg = sum_neg * pixel_area
        vol_net = (sum_pos + sum_neg) * pixel_area #How much sediment was eroded/deposited in this cross-slope band

        # ---- LoD (1 sigma) FILTERED VALUES ----
        above_lod_mask = np.abs(valid_data) >= lod_value
        above_lod_vals = valid_data[above_lod_mask]

        n_pix_above_LoD = len(above_lod_vals)
        if n_valid > 0:
            perc_area_above_LoD = (n_pix_above_LoD / n_valid) * 100
        else:
            perc_area_above_LoD = np.nan

        pos_lod_vals = above_lod_vals[above_lod_vals > 0]
        neg_lod_vals = above_lod_vals[above_lod_vals < 0]

        sum_pos_LoD = np.sum(pos_lod_vals)
        sum_neg_LoD = np.sum(neg_lod_vals)
        
        # Volumes(LoD filtered)
        vol_pos_LoD = sum_pos_LoD * pixel_area
        vol_neg_LoD = sum_neg_LoD * pixel_area
        vol_net_LoD = (sum_pos_LoD + sum_neg_LoD) * pixel_area
        
        # ---- LoD (95%) FILTERED VALUES ----
        
        above_lod95_mask = np.abs(valid_data) >= lod95_value
        above_lod95_vals = valid_data[above_lod95_mask]
 
        n_pix_above_LoD95 = len(above_lod95_vals)
        perc_area_above_LoD95 = (n_pix_above_LoD95 / n_valid) * 100 if n_valid > 0 else np.nan
 
        pos_lod95_vals = above_lod95_vals[above_lod95_vals > 0]
        neg_lod95_vals = above_lod95_vals[above_lod95_vals < 0]
 
        sum_pos_LoD95 = np.sum(pos_lod95_vals)
        sum_neg_LoD95 = np.sum(neg_lod95_vals)
 
        vol_pos_LoD95 = sum_pos_LoD95 * pixel_area
        vol_neg_LoD95 = sum_neg_LoD95 * pixel_area
        vol_net_LoD95 = (sum_pos_LoD95 + sum_neg_LoD95) * pixel_area
        
        
        # RESULTS

        results.append([
            row + 1,
            sum_pos,
            sum_neg,
            n_pix_pos,
            n_pix_neg,
            net_val,
            mean_surf_change,
            area_pos,
            area_neg,
            vol_pos,
            vol_neg,
            vol_net,
            n_pix_above_LoD,
            perc_area_above_LoD,
            sum_pos_LoD,
            sum_neg_LoD,
            vol_pos_LoD,
            vol_neg_LoD,
            vol_net_LoD,
            n_pix_above_LoD95,
            perc_area_above_LoD95,
            sum_pos_LoD95,
            sum_neg_LoD95,
            vol_pos_LoD95,
            vol_neg_LoD95,
            vol_net_LoD95
        ])
        
        total_valid += n_valid
        total_above_lod += n_pix_above_LoD
        total_above_lod95 += n_pix_above_LoD95

    # =========================
    # WRITE CSV per row
    # =========================

    with open(csv_path, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "row_id",
            "sum_pos (m)",
            "sum_neg (m)",
            "n_pix_pos",
            "n_pix_neg",
            "sum_surf_change (m)",# total sum of positive and negative
            "mean_surf_change_row (m)",# tot sum pf positive and negative but divided by pixels
            "area_pos (m2)",
            "area_neg (m2)",
            "vol_pos_m3",
            "vol_neg_m3",
            "vol_net_m3",
            "n_pix_above_LoD",
            "perc_area_above_LoD",
            "sum_pos_LoD",
            "sum_neg_LoD",
            "vol_pos_LoD_m3",
            "vol_neg_LoD_m3",
            "vol_net_LoD_m3",
            "n_pix_above_LoD95",
            "perc_area_above_LoD95",
            "sum_pos_LoD95",
            "sum_neg_LoD95",
            "vol_pos_LoD95_m3",
            "vol_neg_LoD95_m3",
            "vol_net_LoD95_m3"
        ])
        writer.writerows(results)
        
        # whole-DoD (all rows combined) % area above threshold, for the summary table
    perc_area_above_LoD_total = (total_above_lod / total_valid) * 100 if total_valid > 0 else np.nan
    perc_area_above_LoD95_total = (total_above_lod95 / total_valid) * 100 if total_valid > 0 else np.nan
 
    summary_rows.append([
        raster_name,
        lod_value,
        lod95_value,
        total_valid,
        perc_area_above_LoD_total,
        perc_area_above_LoD95_total,
    ])

    print(f"Processed: {filename}")
    
# =========================
# WRITE WHOLE-DoD SUMMARY CSV
# (one row per DoD: use this to report mean/range of % area above
#  LoD vs LoD(95%) across all DoDs in the results section)
# =========================
 
 # Summary for RAINFALL IMPACT
summary_path = os.path.join(r"C:\\LoD_vs_LoD95_summary_excel_z.csv")

#Summary for ANIMAL IMPACT
#summary_path = os.path.join(r"C:\\LoD_vs_LoD95_summary_ANIMALS_z.csv")

with open(summary_path, mode="w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "raster_name",
        "LoD_m",
        "LoD95_m",
        "n_valid_pixels",
        "perc_area_above_LoD",
        "perc_area_above_LoD95",
    ])
    writer.writerows(summary_rows)
 
print(f"Summary written to: {summary_path}")

print("All rasters processed.")
