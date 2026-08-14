###############################

SOIL SURFACE CHANGES ANALYSIS - first submission version 

###############################

MANUSCRIPT TITLE - FIRST SUBMISSION VERSION
How terrestrial bioturbators affect soil surface changes and water infiltration patterns - A high resolution mesocosm study on earthworms and mole interaction 

AUTHORS
Marta Loreggian1,2, Jantiene Baartman1*, Loes van Schaik1, Sebastián Bravo-Peña1,  Coen Ritsema1, Annegret Larsen2*
1 Soil Physics and Land Management Group, Department of Environmental Sciences, Wageningen University & Research, P.O. Box 47, 6708PB, Wageningen, The Netherlands
2Soil Geography and Landscape Group, Department of Environmental Sciences, Wageningen University & Research, P.O. Box 47, 6708PB, Wageningen, The Netherlands
* Author contributed in equal way.

CORRESPONDING AUTHOR 
marta.loreggian@wur.nl


ABSTRACT
Animal bioturbation shapes terrestrial landscapes by altering water infiltration, storage, and soil surface dynamics. While moles (Talpa europaea) construct surface mounds and extensive tunnels, their primary prey - earthworm (i.e., Lumbricus terrestris) - simultaneously engineer deep burrow networks. Despite their interaction, the combined impact of these organisms as soil hydro-physical engineers remains poorly understood.
To address this, we conducted a densely monitored mesocosm experiment (single box, W=0.5 m, L=2 m, H= 1 m), sequentially increasing bioturbation complexity across three treatments: bare soil (B), earthworms only (EW), and earthworms plus mole (EW+M). Ten rainfall events were applied at a constant intensity of 0.8 mm min⁻¹. Photogrammetry was performed before and after each event to quantify surface roughness and soil redistribution. Spatiotemporal soil moisture was monitored through 24 TEROS 10 sensors installed following a 3-dimension grid at 5, 15, 30, and 60 cm depths. 
Results indicate that: (i) EW activity promoted fast infiltration to deeper soil layers, with response times of 39, 74, and 231 min at 15, 30, and 60 cm depth, respectively  (the shortest of all treatments), and the steepest wetting-front slopes (Smax up to 29.8 × 10⁻⁴ cm³cm⁻³min⁻¹ at 30 cm), indicative of preferential flow; (ii) mole activity increased surface roughness upslope by up to 511% relative to bare soil (vs. 110% for EW downslope), reflecting contrasting, species-specific spatial strategies — mole effects concentrated upslope, earthworm effects diffuse and downslope-oriented; and (iii) despite this pronounced surface disturbance (~4500 cm³ of soil excavated by the mole), deep-layer moisture response in EW+M remained close to EW levels (Δ ≈ 0.25 cm³cm⁻³ at 60 cm), with water storage instead concentrated near the surface (0–10 cm) 24 h after events. These results suggest that mole burrowing reorganizes the surface without proportionally enhancing deep infiltration. Additionally, high earthworm escape rates following mole introduction likely altered hydrological processes.

DOI: https://doi.org/10.5281/zenodo.21932478

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



