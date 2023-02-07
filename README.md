# Midjourney Processing
## Preprocessing script for the Midjourney dataset.

# DiffusionDB Processing
## Preprocessing script for the DiffusionDB dataset.

# SAC Processing
## Preprocessing script for the SAC dataset.

# LAION Processing
## Preprocessing script for the LAION dataset.

# Midjourney First-order Analysis
## This script must be run after preprocessing the Midjourney dataset. 
## Before running, change the path in the first cell to the path to the preprocessed Midjourney dataset. 
## The script will perform first-order analysis on the Midjourney dataset, plot the top 50 most frequent terms, 
## and the distribution of term frequency. The script will also save a CSV file containing all terms sorted by term frequency in descending order.

# DiffusionDB First-order Analysis
## Works the same as Midjourney_First_order_analysis, but for the DiffusionDB dataset.

# SAC First-order Analysis
## Works the same as Midjourney_First_order_analysis, but for the SAC dataset.

# Midjourney Second-order Analysis
## This script must be run after preprocessing the Midjourney dataset.
## Before running, change the path in the first cell to the path to the preprocessed Midjourney dataset. 
## The script will perform second-order analysis on the Midjourney dataset, print the top 50 most frequent term pairs, 
## and the distribution of term frequency. The script will also save a CSV file containing all term pairs sorted by term frequency in descending order.

# DiffusionDB Second-order Analysis
## Works the same as Midjourney_Second_order_analysis, but for the DiffusionDB dataset.

# SAC Second-order Analysis
## Works the same as Midjourney_Second_order_analysis, but for the SAC dataset.

# Midjourney Reweighting
## This script must be run after preprocessing the Midjourney dataset and running both Midjourney_First_order_analysis and Midjourney_Second_order_analysis.
## Before running, change the paths in the first two cells to the paths to the CSV files with all terms and term pairs in Midjourney. 
## The script will perform chi-square reweighting on the top 10,000 term pairs and print the top 50 most significant term pairs. 
## The script will also save a CSV file containing the top 10,000 term pairs sorted by chi-square scores in descending order. 
## It can also perform other reweighting algorithms, such as PMI and t-test, but these results are not included in the paper and are for reference only.

# DiffusionDB Reweighting
## Works the same as Midjourney_reweighting, but for the DiffusionDB dataset.

# SAC Reweighting
## Works the same as Midjourney_reweighting, but for the SAC dataset.

# Analysis
## For query-level and session-level analysis, run this script. 
## Make sure to preprocess the dataset first. Functions used in scripts are defined in scripts.py and utils.py.
