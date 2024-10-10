import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import geopandas as gpd
import contextily as ctx
import random
import argparse

# Set up argparse to parse NUM_LARGE_GAPS, NUM_SMALL_GAPS, LARGE_GAP_THRESHOLD, and SMALL_GAP_THRESHOLD
parser = argparse.ArgumentParser(description="Process AIS trajectories with specified gap settings.")
parser.add_argument("--num_large_gaps", type=int, default=random.randint(1, 4),
                    help="Number of large gaps to create in the larger part of the trajectory.")
parser.add_argument("--num_small_gaps", type=int, default=random.randint(10, 20),
                    help="Number of small gaps to create in the smaller part of the trajectory.")
parser.add_argument("--large_gap_threshold", type=float, default=random.uniform(100000, 200000),
                    help="Threshold for large gaps (default: random between 100000 and 200000 meters).")
parser.add_argument("--small_gap_threshold", type=float, default=random.uniform(10000, 20000),
                    help="Threshold for small gaps (default: random between 10000 and 20000 meters).")
parser.add_argument("--input_dir", type=str, required=True,
                    help="Directory containing input CSV files with AIS trajectories.")
parser.add_argument("--output_data_dir", type=str, required=True,
                    help="Directory to save output CSV files after processing.")
parser.add_argument("--output_plots_dir", type=str, required=True,
                    help="Directory to save output plots.")
args = parser.parse_args()

# Assign parsed values to variables
NUM_LARGE_GAPS = args.num_large_gaps
NUM_SMALL_GAPS = args.num_small_gaps
LARGE_GAP_THRESHOLD = args.large_gap_threshold
SMALL_GAP_THRESHOLD = args.small_gap_threshold
input_dir = args.input_dir
output_data_dir = args.output_data_dir
output_plots_dir = args.output_plots_dir

# Verbose output (for informational purposes)
print(f"Number of large gaps: {NUM_LARGE_GAPS}")
print(f"Number of small gaps: {NUM_SMALL_GAPS}")
print(f"Large gap threshold set to: {LARGE_GAP_THRESHOLD}")
print(f"Small gap threshold set to: {SMALL_GAP_THRESHOLD}")
print(f"Input directory: {input_dir}")
print(f"Output data directory: {output_data_dir}")
print(f"Output plots directory: {output_plots_dir}")

# Define directories (these remain hardcoded as per your specification)
# input_dir = r"C:/Users/HU84VR/Downloads/AIS Project1/Test Trajectories for AIS 20240831/25 chosen perfect trajectory data"
# output_data_dir = r"C:/Users/HU84VR/Downloads/AIS Project1/Test Trajectories for AIS 20240831/data_realistic_frequency"
# output_plots_dir = r"C:/Users/HU84VR/Downloads/AIS Project1/Test Trajectories for AIS 20240831/plots/plots_realistic_frequency"

# Create output directories if they don't exist
os.makedirs(output_data_dir, exist_ok=True)
os.makedirs(output_plots_dir, exist_ok=True)


# Function to calculate distance between two geographical points using geopy
def haversine_distance(lat1, lon1, lat2, lon2):
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    return geodesic(point1, point2).meters


# Function to get the geographical extents (min/max lat/lon) across all files
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


# Function to split the trajectory based on location point
def split_trajectory(data):
    total_length_of_trajectory = data['distance'].sum()
    split_point = np.random.uniform(0.3, 0.7) * total_length_of_trajectory
    cumulative_length = data['distance'].cumsum()

    # Split the data based on the chosen split point
    larger_part = data[cumulative_length >= split_point]
    smaller_part = data[cumulative_length < split_point]

    return larger_part, smaller_part


# Function to create gaps in a trajectory with dynamic thresholds and update mechanism
def create_gaps(data, num_gaps, gap_threshold):
    gaps = []
    total_length = data['distance'].sum()
    segment_length = total_length / num_gaps

    for i in range(num_gaps):
        segment_start = i * segment_length
        segment_end = (i + 1) * segment_length

        current_gap_threshold = gap_threshold
        while segment_end - segment_start < current_gap_threshold:
            current_gap_threshold *= 0.5

        gap_start_location = np.random.uniform(segment_start, segment_end - current_gap_threshold)
        gap_length = np.random.uniform(current_gap_threshold, segment_end - gap_start_location)
        gaps.append((gap_start_location, gap_start_location + gap_length))

    cumulative_distance = data['distance'].cumsum().reindex(data.index)
    for gap_start, gap_end in gaps:
        data = data.loc[(cumulative_distance < gap_start) | (cumulative_distance > gap_end)]

    return data


# Process each file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        try:
            print(f"Processing file: {filename}")

            file_path = os.path.join(input_dir, filename)
            data = pd.read_csv(file_path)

            data['distance'] = np.nan
            for i in range(1, len(data)):
                lat1, lon1 = data.loc[i - 1, 'Latitude'], data.loc[i - 1, 'Longitude']
                lat2, lon2 = data.loc[i, 'Latitude'], data.loc[i, 'Longitude']
                data.loc[i, 'distance'] = haversine_distance(lat1, lon1, lat2, lon2)

            larger_part, smaller_part = split_trajectory(data)

            # Apply large and small gaps creation
            larger_part_with_gaps = create_gaps(larger_part, NUM_LARGE_GAPS, LARGE_GAP_THRESHOLD)
            smaller_part_with_gaps = create_gaps(smaller_part, NUM_SMALL_GAPS, SMALL_GAP_THRESHOLD)

            combined_data = pd.concat([smaller_part_with_gaps, larger_part_with_gaps])
            output_file_path = os.path.join(output_data_dir, filename.replace(".csv", "_gaps_combined.csv"))
            combined_data.to_csv(output_file_path, index=False)

            fig, ax = plt.subplots(figsize=(10, 10))
            gdf = gpd.GeoDataFrame(
                combined_data,
                geometry=gpd.points_from_xy(combined_data['Longitude'], combined_data['Latitude']),
                crs="EPSG:4326"
            )

            gdf.plot(ax=ax, label="Trajectory", color="blue", markersize=5, linewidth=1)
            ax.set_xlim(global_min_lon, global_max_lon)
            ax.set_ylim(global_min_lat, global_max_lat)
            ctx.add_basemap(ax, crs='EPSG:4326', source=ctx.providers.OpenStreetMap.Mapnik)

            start_point = gdf.iloc[0].geometry
            end_point = gdf.iloc[-1].geometry
            ax.scatter([start_point.x], [start_point.y], color="green", s=100, label="Start Point")
            ax.scatter([end_point.x], [end_point.y], color="red", s=100, label="End Point")

            plt.title(f"Trajectory Plot - {filename}")
            plt.legend()
            plot_file_path = os.path.join(output_plots_dir, filename.replace(".csv", "_trajectory.png"))
            plt.savefig(plot_file_path)
            plt.close()

            print(f"Successfully processed: {filename}")

        except Exception as e:
            print(f"Error processing file {filename}: {e}")
