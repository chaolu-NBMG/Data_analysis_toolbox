# -*- coding: utf-8 -*-
"""
Created on Sun May 12 17:15:28 2024

@author: chao lu
"""
# 1. Load the original dataset
import pandas as pd
import os
# Uncomment and modify the line below to specify a different directory
path = r'C:\Users\chaolu\workspace\time series data'
filename = 'weather_data_utf8.csv'
target_file = os.path.join(path, filename)
# Read the target file
df = pd.read_csv(target_file)


# 2. Identify and Handle Inconsistent Timestamps
# Convert 'Date/Time' to datetime, manually adding the year 2023
df['Date/Time'] = pd.to_datetime(df['Date/Time'].apply(lambda x: x + ', 2023'), format='%b %d, %I:%M %p, %Y')
# Round each timestamp to the nearest 5 minutes and identify which are on a 5-minute mark
df['Rounded Time'] = df['Date/Time'].dt.round('5min')
df_on_interval = df[df['Rounded Time'] == df['Date/Time']]
# Identify the start and end time
start_time = df_on_interval['Date/Time'].min()
end_time = df_on_interval['Date/Time'].max()
# Generate the expected sequence of 5-minute intervals from minimum to the maximum time in your DataFrame
expected_times = pd.date_range(start=start_time, end=end_time, freq='5min')
# Filter out any timestamps that do not fall on the exact 5-minute marks from the expected times
df_clean = df[df['Date/Time'].isin(expected_times)]
# Find all entries that are not in the expected time sequence
num_inconsistent = len(df) - len(df_clean)
print(f"Total number of inconsistent format rows: {num_inconsistent}")
print("Dealing method: Entire row remove")


# 3. Remove Duplicates
# Check for duplicates based on 'Date/Time' and sort by 'Date/Time' to keep the latest record
df_clean = df_clean.sort_values(by='Date/Time', ascending=True)
duplicates_before = df_clean.duplicated(subset=['Date/Time'], keep=False)
num_duplicates = duplicates_before.sum()
# Remove duplicates, keeping the last occurrence
df_clean = df_clean.drop_duplicates(subset=['Date/Time'], keep='last')
# Report the number of duplicates and the handling method
print(f"Total number of duplicate rows: {num_duplicates}")
print("Dealing method: Retain the latest record for duplicates")


# 4. Handle missing timestamps
# Generate a DataFrame with the complete range of expected timestamps
all_times = pd.DataFrame(expected_times, columns=['Date/Time'])
df_final = pd.merge(all_times, df_clean, on='Date/Time', how='left')
# Identify missing timestamps, Check which of these timestamps are not present in df_clean
missing_timestamps = all_times[~all_times['Date/Time'].isin(df_clean['Date/Time'])]
num_missing_timestamps = len(missing_timestamps)
print(f"Number of missing timestamps: {num_missing_timestamps}")
# Handle filling for specific columns
columns_to_fill = ['Temp_C', 'Dew_Point_C', 'RH']  # Example columns
# Loop through each column to apply different filling strategies
for column in df_final.columns:
    if column in columns_to_fill:
        # Apply the mean of the nearest entries for filling
        df_final[column] = df_final[column].interpolate(method='linear', limit_direction='both', limit_area='inside')
    else:
        # Leave other columns with missing data as NaN
        if column not in ['Date/Time']:
            df_final[column] = df_final[column]  # This is effectively a no-op
# Print statement to reflect the actual data handling method and the columns affected
print("Dealing method: Apply linear interpolation to fill missing values in specified columns: " + ', '.join(columns_to_fill))


# 5. Save the Final Cleaned Data
# Removing the 'Rounded Time' column from df_final
df_final = df_final.drop(columns=['Rounded Time'])
# Specify the output file path for the cleaned data
output_file_path = os.path.join(path, 'df_final.csv')
# Save the cleaned time series data to a CSV file without the index
df_final.to_csv(output_file_path, index=False, encoding='ISO-8859-1')
# df_final.to_csv(output_file_path, index=False)
# Confirm that the file has been saved successfully
print("Cleaned time series data saved to:", output_file_path)
