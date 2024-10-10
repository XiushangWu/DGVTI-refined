import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import geopandas as gpd
import contextily as ctx
import random
import argparse

# Set up argparse
parser = argparse.ArgumentParser(description="Process AIS trajectories with a specified gap threshold.")
parser.add_argument("--min_gap_threshold", type=float, default=random.uniform(50000, 200000),
                    help="Initial minimum gap threshold (default: random between 50,000 and 200,000)")
parser.add_argument("--input_dir", type=str, required=True,
                    help="Directory containing input CSV files with AIS trajectories.")
parser.add_argument("--output_data_dir", type=str, required=True,
                    help="Directory to save output CSV files after processing.")
parser.add_argument("--output_plots_dir", type=str, required=True,
                    help="Directory to save output plots.")
args = parser.parse_args()

# Assign the parsed value to MIN_GAP_THRESHOLD
MIN_GAP_THRESHOLD = args.min_gap_threshold  # Random float between 50,000 and 200,000'
input_dir = args.input_dir
output_data_dir = args.output_data_dir
output_plots_dir = args.output_plots_dir

# Define directories
# input_dir = r"C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\25 chosen perfect trajectory data"
# output_data_dir = r"C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\data_single"
# output_plots_dir = r"C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\plots\plots_single"

# Verbose output (for debugging or informational purposes)
print(f"Minimum gap threshold set to: {MIN_GAP_THRESHOLD}")
print(f"Input directory: {input_dir}")
print(f"Output data directory: {output_data_dir}")
print(f"Output plots directory: {output_plots_dir}")

# Create output directories if they don't exist
os.makedirs(output_data_dir, exist_ok=True)
os.makedirs(output_plots_dir, exist_ok=True)

# Function to calculate distance between two geographical points using geopy
def haversine_distance(lat1, lon1, lat2, lon2):
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    return geodesic(point1, point2).meters

# Get the geographical extents (min/max lat/lon) across all files
def get_global_bounds(input_dir):
    min_lat, max_lat = np.inf, -np.inf
    min_lon, max_lon = np.inf, -np.inf
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            data = pd.read_csv(file_path)
            min_lat = min(min_lat, data['Latitude'].min())
            max_lat = max(max_lat, data['Latitude'].max())
            min_lon = min(min_lon, data['Longitude'].min())
            max_lon = max(max_lon, data['Longitude'].max())
    return min_lat, max_lat, min_lon, max_lon

# Get global bounds for all the data
global_min_lat, global_max_lat, global_min_lon, global_max_lon = get_global_bounds(input_dir)

# Process each file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        try:
            print(f"Processing file: {filename}")

            # Load the CSV file
            file_path = os.path.join(input_dir, filename)
            data = pd.read_csv(file_path)

            # Calculate distances between consecutive points
            data['distance'] = np.nan
            for i in range(1, len(data)):
                lat1, lon1 = data.loc[i-1, 'Latitude'], data.loc[i-1, 'Longitude']
                lat2, lon2 = data.loc[i, 'Latitude'], data.loc[i, 'Longitude']
                data.loc[i, 'distance'] = haversine_distance(lat1, lon1, lat2, lon2)

            # Calculate total trajectory length
            total_length_of_trajectory = data['distance'].sum()

            # Initialize the gap threshold with the standard minimum threshold
            current_gap_threshold = MIN_GAP_THRESHOLD

            # Adjust the minimum gap length if the trajectory is smaller than the gap
            while total_length_of_trajectory < current_gap_threshold:
                current_gap_threshold *= 0.5
                print(f"Adjusting minimum gap threshold to {current_gap_threshold / 1000} km for {filename}")

            # Regenerate start location until enough space for the adjusted gap
            while True:
                # Generate random start location
                single_gap_start_location = np.random.uniform(0, 1)
                remaining_trajectory_length = total_length_of_trajectory * (1 - single_gap_start_location)

                # Check if remaining trajectory can accommodate the adjusted gap
                if remaining_trajectory_length >= current_gap_threshold:
                    break  # Valid start location, break out of the loop

            # Generate gap length (between the adjusted gap threshold and the remaining trajectory length)
            single_gap_length = np.random.uniform(current_gap_threshold, remaining_trajectory_length)

            # Find the start and end points of the gap based on the percentage of the trajectory
            cumulative_distance = data['distance'].cumsum()
            gap_start_distance = single_gap_start_location * total_length_of_trajectory
            gap_end_distance = gap_start_distance + single_gap_length

            # Remove the rows that fall within the gap
            data_with_gap_removed = data[(cumulative_distance < gap_start_distance) | (cumulative_distance > gap_end_distance)]

            # Save the updated dataframe to a new CSV file with "_single_gap" suffix
            output_file_path = os.path.join(output_data_dir, filename.replace(".csv", "_single_gap.csv"))
            data_with_gap_removed.to_csv(output_file_path, index=False)

            # Plotting the trajectory
            fig, ax = plt.subplots(figsize=(10, 10))

            # Convert data to GeoDataFrame for plotting
            gdf = gpd.GeoDataFrame(
                data_with_gap_removed,
                geometry=gpd.points_from_xy(data_with_gap_removed['Longitude'], data_with_gap_removed['Latitude']),
                crs="EPSG:4326"
            )

            # Plot the trajectory with smaller markersize
            gdf.plot(ax=ax, label="Trajectory", color="blue", markersize=5, linewidth=1)

            # Set the x and y limits to the global bounds (fixed map region)
            ax.set_xlim(global_min_lon, global_max_lon)
            ax.set_ylim(global_min_lat, global_max_lat)

            # Add map basemap
            ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)

            # Highlight the start and end points
            start_point = gdf.iloc[0].geometry
            end_point = gdf.iloc[-1].geometry
            ax.scatter([start_point.x], [start_point.y], color="green", s=100, label="Start Point")
            ax.scatter([end_point.x], [end_point.y], color="red", s=100, label="End Point")

            # Add labels and legend
            plt.title(f"Trajectory Plot - {filename}")
            plt.legend()

            # Save the plot
            plot_file_path = os.path.join(output_plots_dir, filename.replace(".csv", "_trajectory.png"))
            plt.savefig(plot_file_path)

            # Close the plot to free up memory
            plt.close()

            print(f"Successfully processed: {filename}")
# print("Done")
        except Exception as e:
            print(f"Error processing file {filename}: {e}")