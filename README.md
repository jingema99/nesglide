# Midjourney_processing.ipynb:
Preprocessing script for the Midjourney dataset.


# DiffusionDB_processing.ipynb:
Preprocessing script for the DiffusionDB dataset.


# SAC_processing.ipynb:
Preprocessing script for the SAC dataset.


# LAION_processing.ipynb:
Preprocessing script for the LAION dataset.


# Midjourney_First_order_analysis.ipynb:
This script must be run after you have preprocessed the Midjourney dataset. Before running this script, please change the path in the first cell to the path to the preprocessed Midjourney dataset. Running this script will perform first-order analysis on the Midjourney dataset, and then plot the top 50 most frequent terms and the distribution of term frequency. The script will also save a csv file containing all terms in the Midjourney dataset sorted by term frequency in descending order.


# DiffusionDB_First_order_analysis.ipynb:
Works the same as Midjourney_First_order_analysis.ipynb, but for the DiffusionDB dataset.


# SAC_First_order_analysis.ipynb：
Works the same as Midjourney_First_order_analysis.ipynb, but for the SAC dataset.


# Midjourney_Second_order_analysis.ipynb：
This script must be run after you have preprocessed the Midjourney dataset. Before running this script, please change the path in the first cell to the path to the preprocessed Midjourney dataset. Running this script will perform second-order analysis on the Midjourney dataset, and then print the top 50 most frequent term pairs and the distribution of term frequency. The script will also save a csv file containing all term pairs in the Midjourney dataset sorted by term frequency in descending order.


# DiffusionDB_Second_order_analysis.ipynb:
Works the same as Midjourney_Second_order_analysis.ipynb, but for the DiffusionDB dataset.


# SAC_Second_order_analysis.ipynb:
Works the same as Midjourney_Second_order_analysis.ipynb, but for the SAC dataset.


# Midjourney_reweighting.ipynb:
This script must be run after you have preprocessed the Midjourney dataset and have run both Midjourney_First_order_analysis.ipynb and Midjourney_Second_order_analysis.ipynb. Before running this script, please change the paths in the first two cells to the paths to the csv files with all terms and term pairs in Midjourney. Running this script will perform chi-square reweighting on the top 10, 000 term pairs from the Midjourney dataset, and then print the top 50 most significant term pairs. The script will also save a csv file containing the top 10, 000 term pairs in the Midjourney dataset sorted by chi-square scores in descending order. In addition, this script can also perform other reweighting algorithms on the term pairs, such as PMI, t-test, etc. These results are not included in the paper and are for reference only.


# DiffusionDB_reweighting.ipynb:
Works the same as Midjourney_reweighting.ipynb, but for the DiffusionDB dataset.


# SAC_reweighting.ipynb:
Works the same as Midjourney_reweighting.ipynb, but for the SAC dataset.


# Analysis.ipynb
For query-level and session-level analysis, please run this script. Before running, make sure you have preprocessed the dataset. Functions called in scripts are defined in scripts.py and utils.py.
