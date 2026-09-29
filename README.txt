###############################

SOIL SURFACE CHANGES ANALYSIS - first submission version 

###############################

MANUSCRIPT TITLE

Dual-species bioturbation shapes soil surface dynamics and water infiltration: a high-resolution mesocosm experiment on earthworm-mole interaction


AUTHORS
Marta Loreggian1,2, Jantiene Baartman1*, Loes van Schaik1, Sebastián Bravo-Peña1,  Coen Ritsema1, Annegret Larsen2*
1 Soil Physics and Land Management Group, Department of Environmental Sciences, Wageningen University & Research, P.O. Box 47, 6708PB, Wageningen, The Netherlands
2Soil Geography and Landscape Group, Department of Environmental Sciences, Wageningen University & Research, P.O. Box 47, 6708PB, Wageningen, The Netherlands
* Author contributed in equal way.

CORRESPONDING AUTHOR 
marta.loreggian@wur.nl


ABSTRACT
Terrestrial bioturbators act as key soil hydro-physical engineers, yet how interacting species such as the earthworm Lumbricus terrestris and the mole Talpa europaea alter infiltration and surface change remains poorly quantified. In a densely monitored laboratory mesocosm (0.9 m³, 10% slope), we applied ten rainfall events (0.8 mm min⁻¹) across three sequential states: bare soil (B), earthworms only (EW), and earthworms plus mole (EW+M), combining event-based photogrammetry (1 cm DEM resolution) with minute-resolution soil moisture monitoring at four depths (24 sensors , 5, 15, 30 and 60 cm depth). Earthworms produced the fastest infiltration of all treatments and the steepest wetting fronts (Smax up to 29.8 × 10⁻⁴ cm³cm⁻³min⁻¹ at 30 cm). Mole tunnelling excavated ~4500 cm³ of soil and increased upslope surface roughness by up to 511% relative to bare soil. The fractions of water stored and drained did not differ among treatments, but its vertical distribution did: earthworms promoted deep drainage along the slope (45–90 cm), whereas combined mole–earthworm activity retained water near the surface (0–10 cm) and in deep galleries while bypassing intermediate depths. This study demonstrates that high-resolution spatial monitoring of species interactions is essential to identify surface–subsurface hydrological impact of bioturbation activity. However, upscaling these insights requires long-term, landscape-scale monitoring to unravel the complex co-evolution of soil-hydrological processes and bioturbator behaviour.



PROGRAMS
Python and Jupyter Notebook, version 3.12.4.
QGIS version 3.28.8



ENVIRONMENTS
spatial_analysis.yml # to run all the surface changes analysis Jupiter Notebooks. The .py files are meant to be run directly in QGIS



LICENSE
Data: CC BY-NC

Code: Apache-2.0 

FOLDER CONTENT

In this folder there are all input and output files and codes use to prepare the data and analyze them.
At the beginning of each Jupiter Notebook or python code, there is a list of libraries and input data used to run the code. 
The libraries are present in the environment, therefore set that environment as Kernel in the Jupiter Notebook.
When importing the data in the laptop, adjust documents paths with the path where the folder has been imported.



WORKFLOW:

we suggest to import first the DEMs in QGIS, and set the local coordinate system using the code provided in QGIS_local_coordinates_z. 
Then, run the .py files in the QGIS python interface. The Jupiter Notebook can be run as last.

CODES:

- soil_transport_zenodo.py:
 The code is meant to be run directly in QGIS python interface. It is used to calculate for both rainfall DEMs and animals DEMs:

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


Input files: 
folders: DoD_1cm_nodetrended_z, DoD_1cm_animals effect_z
limit of detection csv:limit_of_detection_z.csv,LoD_animalsDoD_z.csv

- roughness_rows_zenodo.py:
 The code is meant to be run directly in QGIS python interface. It is used for calculating surface roughness values by rows

Input file: Roughness_1cm_detrend_z
Limit of detection csv: limit_of_detection_z.csv

- Surface analysis_zenodo.ipynb: 
This is the only Jupiter Notebook. It is used to the general plots visualization and subsidence analysis.  



