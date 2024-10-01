import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
from geopy.distance import geodesic

# User-defined parameters for missing gaps

# Single large gap parameters
gap_size_km_single = 100  # Size of the single large gap in kilometers
gap_start_single = 0.5  # Start position of the large gap within the trajectory (as a percentage of total points)

# Multiple small gaps parameters
gap_size_km_multiple = 60  # Size of each small gap in kilometers
num_gaps_multiple = 5  # Number of small gaps
gap_start_locations_multiple = [0.2, 0.4, 0.6, 0.7, 0.8]  # Start positions of the small gaps as percentages

# Realistic frequency pattern parameters
gap_size_km_realistic_large = 50  # Size of each large gap for realistic frequency pattern
num_large_gaps_realistic = 3  # Number of large gaps for realistic frequency pattern
gap_start_locations_realistic_large = [0.6, 0.75, 0.9]  # Start positions of large gaps as percentages

gap_size_km_realistic_small = 5  # Size of each small gap for realistic frequency pattern
num_small_gaps_realistic = 50  # Number of small gaps for realistic frequency pattern
gap_start_locations_realistic_small = [
    0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19,
    0.2,
    0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29, 0.3, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39,
    0.4,
    0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49, 0.5
]  # Start positions of small gaps as percentages

# Define the input and output folders
input_folder = r"C:/Users/HU84VR/Downloads/AIS Project1/Test Trajectories for AIS 20240831//25 chosen perfect trajectory data"
output_single_folder = r"C:/Users/HU84VR/Downloads/AIS Project1/Test Trajectories for AIS 20240831/data_single"
output_multiple_folder = r"C:/Users/HU84VR/Downloads/AIS Project1/Test Trajectories for AIS 20240831/data_multiple"
output_realistic_folder = r"C:/Users/HU84VR/Downloads/AIS Project1/Test Trajectories for AIS 20240831/data_realistic_frequency"
output_plot_folder = r"/Users/HU84VR/Downloads/AIS Project1/Test Trajectories for AIS 20240831/plots"

# Define the paths to the output plot folders
single_plot_folder_path = os.path.join(output_plot_folder, "plots_single")
multiple_plot_folder_path = os.path.join(output_plot_folder, "plots_multiple")
realistic_frequency_plot_folder_path = os.path.join(output_plot_folder, "plots_realistic_frequency")

# Create output directories if they don't exist
os.makedirs(output_single_folder, exist_ok=True)
os.makedirs(output_multiple_folder, exist_ok=True)
os.makedirs(output_realistic_folder, exist_ok=True)
os.makedirs(single_plot_folder_path, exist_ok=True)
os.makedirs(multiple_plot_folder_path, exist_ok=True)
os.makedirs(realistic_frequency_plot_folder_path, exist_ok=True)


# Function to calculate the distance between two points using the geodesic formula
def calculate_distance(lat1, lon1, lat2, lon2):
    return geodesic((lat1, lon1), (lat2, lon2)).kilometers


# Function to find the number of points to remove based on a given gap size in kilometers
def calculate_points_to_remove(df, gap_size_km):
    total_distance = 0
    points_to_remove = 0

    for i in range(1, len(df)):
        total_distance += calculate_distance(
            df.iloc[i - 1]['Latitude'], df.iloc[i - 1]['Longitude'],
            df.iloc[i]['Latitude'], df.iloc[i]['Longitude']
        )
        if total_distance >= gap_size_km:
            points_to_remove = i
            break

    return points_to_remove


# Function to convert a percentage into a starting index for a DataFrame
def get_start_index_from_percentage(df, percentage):
    return int(percentage * len(df))


# Function to check if a range of indices overlaps with any existing ranges
def check_overlap(existing_ranges, new_range):
    for existing_range in existing_ranges:
        if (new_range[0] <= existing_range[1]) and (new_range[1] >= existing_range[0]):
            return True
    return False


# Function to apply missing data scenarios based on user-defined parameters
def apply_reduction_methods(df, file_name):
    length = len(df)

    # Extract the MMSI number from the DataFrame (assuming the MMSI column exists)
    try:
        mmsi_number = str(df['MMSI'].iloc[0])  # Assuming MMSI is the same for all rows in the file
    except KeyError:
        print(f"MMSI column not found in {file_name}. Skipping this file.")
        return

    # Store applied gap ranges to avoid overlaps
    applied_ranges = []

    # Single large gap reduction
    points_to_remove_single = calculate_points_to_remove(df, gap_size_km_single)
    start_idx_large = get_start_index_from_percentage(df, gap_start_single)
    end_idx_large = min(start_idx_large + points_to_remove_single, len(df))  # Ensure end_idx is within bounds

    if not check_overlap(applied_ranges, (start_idx_large, end_idx_large)):
        indices_to_remove_large = list(range(start_idx_large, end_idx_large))
        df_single_gap = df.drop(indices_to_remove_large).reset_index(drop=True)
        applied_ranges.append((start_idx_large, end_idx_large))
    else:
        df_single_gap = df.copy()  # No gap applied if it overlaps

    # Multiple gap reduction
    df_multiple_gap = df.copy()
    applied_ranges_multiple = []
    for gap_start_percentage in gap_start_locations_multiple:
        points_to_remove_multiple = calculate_points_to_remove(df_multiple_gap, gap_size_km_multiple)
        start_idx = get_start_index_from_percentage(df_multiple_gap, gap_start_percentage)
        end_idx = min(start_idx + points_to_remove_multiple, len(df_multiple_gap))  # Ensure end_idx is within bounds

        if not check_overlap(applied_ranges_multiple, (start_idx, end_idx)):
            df_multiple_gap.drop(
                df_multiple_gap.index[start_idx:end_idx],
                inplace=True
            )
            df_multiple_gap.reset_index(drop=True, inplace=True)
            applied_ranges_multiple.append((start_idx, end_idx))

    # Realistic frequency reduction
    df_realistic_frequency = df.copy()
    applied_ranges_realistic = []

    # Large gaps for realistic frequency pattern
    for gap_start_percentage in gap_start_locations_realistic_large:
        points_to_remove_realistic_large = calculate_points_to_remove(
            df_realistic_frequency, gap_size_km_realistic_large
        )
        start_idx_large_realistic = get_start_index_from_percentage(
            df_realistic_frequency, gap_start_percentage
        )
        end_idx_large_realistic = min(start_idx_large_realistic + points_to_remove_realistic_large,
                                      len(df_realistic_frequency))  # Ensure end_idx is within bounds

        if not check_overlap(applied_ranges_realistic, (start_idx_large_realistic, end_idx_large_realistic)):
            df_realistic_frequency.drop(
                df_realistic_frequency.index[
                start_idx_large_realistic:end_idx_large_realistic
                ],
                inplace=True
            )
            df_realistic_frequency.reset_index(drop=True, inplace=True)
            applied_ranges_realistic.append((start_idx_large_realistic, end_idx_large_realistic))

    # Small gaps for realistic frequency pattern
    for gap_start_percentage in gap_start_locations_realistic_small:
        points_to_remove_realistic_small = calculate_points_to_remove(
            df_realistic_frequency, gap_size_km_realistic_small
        )
        start_idx_small_realistic = get_start_index_from_percentage(
            df_realistic_frequency, gap_start_percentage
        )
        end_idx_small_realistic = min(start_idx_small_realistic + points_to_remove_realistic_small,
                                      len(df_realistic_frequency))  # Ensure end_idx is within bounds

        if not check_overlap(applied_ranges_realistic, (start_idx_small_realistic, end_idx_small_realistic)):
            df_realistic_frequency.drop(
                df_realistic_frequency.index[
                start_idx_small_realistic:end_idx_small_realistic
                ],
                inplace=True
            )
            df_realistic_frequency.reset_index(drop=True, inplace=True)
            applied_ranges_realistic.append((start_idx_small_realistic, end_idx_small_realistic))

    # Define the new filenames based on the MMSI number and the scenario type
    single_gap_file_name = f"AIS data of MMSI {mmsi_number} Class A_single gap.csv"
    multiple_gaps_file_name = f"AIS data of MMSI {mmsi_number} Class A_multiple gaps.csv"
    realistic_frequency_file_name = f"AIS data of MMSI {mmsi_number} Class A_realistic_frequency.csv"

    # Save the files to the corresponding folders
    df_single_gap.to_csv(os.path.join(output_single_folder, single_gap_file_name), index=False)
    df_multiple_gap.to_csv(os.path.join(output_multiple_folder, multiple_gaps_file_name), index=False)
    df_realistic_frequency.to_csv(os.path.join(output_realistic_folder, realistic_frequency_file_name), index=False)


# Function to calculate the bounding box (extent) for the plots
def get_bounding_box(folder_path):
    min_lat, max_lat = float('inf'), -float('inf')
    min_lon, max_lon = float('inf'), -float('inf')

    # Loop through all CSV files and calculate the bounding box
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            data = pd.read_csv(file_path)
            if 'Latitude' in data.columns and 'Longitude' in data.columns:
                min_lat = min(min_lat, data['Latitude'].min())
                max_lat = max(max_lat, data['Latitude'].max())
                min_lon = min(min_lon, data['Longitude'].min())
                max_lon = max(max_lon, data['Longitude'].max())

    return [min_lon, max_lon, min_lat, max_lat]


# Function to extract MMSI from the filename (assuming the filename includes MMSI)
def extract_mmsi_from_filename(filename):
    parts = filename.split(" ")
    for i, part in enumerate(parts):
        if part == 'MMSI' and i + 1 < len(parts):
            mmsi = parts[i + 1]
            if mmsi.isdigit() and len(mmsi) == 9:
                return mmsi
    return "unknown_MMSI"


# Function to plot and save trajectory with start (green), end (red) points, and smaller blue points for the rest
def plot_and_save_trajectory_with_map(csv_path, save_path, title, bbox, pattern_type):
    data = pd.read_csv(csv_path)
    mmsi_number = extract_mmsi_from_filename(title)

    # Ensure the columns for latitude and longitude exist
    if 'Latitude' in data.columns and 'Longitude' in data.columns:
        # Create a plot with a map background and fixed size (4:3 aspect ratio)
        fig, ax = plt.subplots(figsize=(8, 6), dpi=200)  # 8x6 inches at 200 DPI (4:3 ratio)

        # Extract the start, end, and middle points
        start_point = data.iloc[0]  # First row (start point)
        end_point = data.iloc[-1]  # Last row (end point)
        middle_points = data.iloc[1:-1]  # All other points

        # Plot the remaining points (blue) with reduced size
        ax.scatter(middle_points['Longitude'], middle_points['Latitude'], c='blue', s=1, label='Middle Points')

        # Plot the start point (green)
        ax.scatter(start_point['Longitude'], start_point['Latitude'], c='green', s=100, label='Start Point')

        # Plot the end point (red)
        ax.scatter(end_point['Longitude'], end_point['Latitude'], c='red', s=100, label='End Point')

        # Set the aspect ratio and labels
        ax.set_aspect('equal')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title(f'Trajectory: {title}')

        # Apply the bounding box to ensure all plots have the same region
        ax.set_xlim(bbox[0], bbox[1])
        ax.set_ylim(bbox[2], bbox[3])

        # Add OpenStreetMap tiles using contextily
        ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)

        # Define the filename based on the pattern type
        if pattern_type == "single":
            save_file_name = f"Trajectory of MMSI_{mmsi_number}_single_gap.png"
        elif pattern_type == "multiple":
            save_file_name = f"Trajectory of MMSI_{mmsi_number}_multiple_gap.png"
        elif pattern_type == "realistic":
            save_file_name = f"Trajectory of MMSI_{mmsi_number}_realistic_frequency_gap.png"
        else:
            save_file_name = f"Trajectory of MMSI_{mmsi_number}_unknown_pattern.png"

        # Save the plot with the appropriate filename
        save_file_path = os.path.join(save_path, save_file_name)
        plt.savefig(save_file_path)
        plt.close()  # Close the figure after saving to avoid display


# Function to plot and save all trajectories from a directory with a map background
def plot_and_save_all_trajectories_from_folder_with_map(folder_path, save_folder_path, bbox, pattern_type):
    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)  # Create the directory if it doesn't exist
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            plot_and_save_trajectory_with_map(file_path, save_folder_path, filename, bbox, pattern_type)


# Process each CSV file in the input folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        file_path = os.path.join(input_folder, file_name)
        df = pd.read_csv(file_path)
        apply_reduction_methods(df, file_name)

print("AIS Data reduction complete.")

# Calculate the bounding box across all the data to ensure uniformity in the plotted region
bbox_single = get_bounding_box(output_single_folder)
bbox_multiple = get_bounding_box(output_multiple_folder)
bbox_realistic = get_bounding_box(output_realistic_folder)

# Plot and save all trajectories from the 'single' folder with a map background
plot_and_save_all_trajectories_from_folder_with_map(output_single_folder, single_plot_folder_path, bbox_single,
                                                    "single")

# Plot and save all trajectories from the 'multiple' folder with a map background
plot_and_save_all_trajectories_from_folder_with_map(output_multiple_folder, multiple_plot_folder_path, bbox_multiple,
                                                    "multiple")

# Plot and save all trajectories from the 'realistic_frequency' folder with a map background
plot_and_save_all_trajectories_from_folder_with_map(
    output_realistic_folder, realistic_frequency_plot_folder_path, bbox_realistic, "realistic"
)

print("AIS Data plotting and saving complete.")
