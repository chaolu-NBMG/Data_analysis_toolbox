# -*- coding: utf-8 -*-
"""
Created on Thu May  2 11:36:19 2024

@author: chaolu
"""
import pandas as pd
import os

# Uncomment the line below to use the current working directory
# path = '.'

# Uncomment and modify the line below to specify a different directory
path = r'C:\Users\chaolu\Project folder\INGENIOUS\Dixie Valley\Dixie Valley Excel\Final version'

# Get the list of all CSV files in the specified directory
csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]

# Check if "Combined output.csv" already exists in the directory
if "Combined output.csv" in csv_files:
    print("Warning: 'Combined output.csv' already exists in the directory. "
          "Please remove or rename the existing file before running the script.")
else:
    print("No 'Combined output.csv' file found in the directory. It is safe to proceed with the script.")
    # Check the number of CSV files found
    num_files = len(csv_files)
    
    # Ensure there is at least one CSV file
    if num_files == 0:
        raise ValueError("No CSV files found in the directory: " + path)
    else:
        print(f"Total CSV files found: {num_files}")
    
    # List CSV files if 10 or fewer are found
    if num_files <= 10:
        print("Listing CSV files:")
        for file in csv_files:
            print(file)
         
    # Read the first file to get the column names
    first_file = pd.read_csv(os.path.join(path, csv_files[0]))
    
    # Initialize a list to store dataframes, starting with the first file
    df_list = [first_file]
    
    # Read remaining files using the column names from the first file and skip the header
    for file in csv_files[1:]:
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path, names=first_file.columns, header=0)
        df_list.append(df)
    
    # Concatenate all dataframes
    final_df = pd.concat(df_list, ignore_index=True)
    
    # Save the concatenated dataframe to a new CSV file
    output_file_path = os.path.join(path, 'Combined output.csv')
    final_df.to_csv(output_file_path, index=False)
    print("Combined output saved to:", output_file_path)

