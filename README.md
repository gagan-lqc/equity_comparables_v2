# Company Competitor Analysis
## Overview
This repository contains code and data used for conducting competitor analysis for both public and private companies. The analysis includes scraping company data, extracting features, and finding similar companies based on various criteria such as industry, region, and vertical.

## Requirements
Python 3.10.12
Libraries:
- beautifulsoup4==4.12.3
- guidance==0.1.13
- pandas==2.2.2
- regex==2023.12.25
- requests==2.31.0
- sentence-transformers==2.6.1
- tqdm==4.66.2

## Files
* inference.ipynb: Jupyter notebook containing the code for conducting inference on private companies, extracting features, and finding similar companies.
* processing.py: Python script containing functions for processing URLs and extracting company information.
* generate_features.py: Python script containing functions for generating features from company data.
* models.py: Python script containing functions for initializing machine learning models.
* fetch_comparables.py: Python script containing functions for finding similar companies.
* public_company_features_final.csv: CSV file containing features of public companies.
* snp_public_companies_final.csv: CSV file containing filtered public company data.
* private_companies.csv: CSV file containing data of private companies.
* region_mapping.json: JSON file containing mapping of regions to stock exchanges.

## Usage
* Setup Environment: Ensure you have Python installed along with the required dependencies listed in requirements.txt.
* Run inference.ipynb: Open the Jupyter notebook inference.ipynb and execute the cells to conduct inference on private companies, extract features, and find similar companies.
* Review Results: Review the generated README.md file to see the analysis results including similar companies for each private company.

## Contributors
@Gagandeep Kamra
@Victor Arshavskiy
