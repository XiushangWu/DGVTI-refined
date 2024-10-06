
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import geopandas as gpd
import contextily as ctx
import random

# Directories
input_dir = r"C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\25 chosen perfect trajectory data"
output_dir = r"C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\data_realistic_frequency"
plots_dir = r"C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\plots\plots_realistic_frequency"

# Create output directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

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

# Introduce gaps in the trajectory
def create_gaps(data, num_large_gaps, num_small_gaps):
    total_rows = len(data)
    
    # Creating large gaps
    for _ in range(num_large_gaps):
        start_idx = random.randint(0, total_rows // 2)
        end_idx = start_idx + random.randint(500, 1000)  # Large gap (range of 500-1000 points)
        data = data.drop(data.index[start_idx:end_idx])

    # Creating small gaps
    for _ in range(num_small_gaps):
        start_idx = random.randint(0, total_rows - 100)
        end_idx = start_idx + random.randint(50, 100)  # Small gap (range of 50-100 points)
        data = data.drop(data.index[start_idx:end_idx])

    return data.reset_index(drop=True)

# Get global bounds for all the data
global_min_lat, global_max_lat, global_min_lon, global_max_lon = get_global_bounds(input_dir)

# Parameters for gaps
NUM_LARGE_GAPS = random.randint(2, 4)
NUM_SMALL_GAPS = random.randint(5, 10)

# Process each file in the directory
for filename in os.listdir(input_dir):
    if filename.endswith(".csv"):
        try:
            print(f"Processing: {filename}")
            
            # Load the trajectory data
            file_path = os.path.join(input_dir, filename)
            data = pd.read_csv(file_path)
            
            # Create gaps
            data_with_gaps = create_gaps(data, NUM_LARGE_GAPS, NUM_SMALL_GAPS)

            # Save the updated dataframe to a new CSV file
            output_file_path = os.path.join(output_dir, filename.replace(".csv", "_gaps.csv"))
            data_with_gaps.to_csv(output_file_path, index=False)

            # Plotting the trajectory
            fig, ax = plt.subplots(figsize=(10, 10))

            # Convert data to GeoDataFrame for plotting
            gdf = gpd.GeoDataFrame(
                data_with_gaps,
                geometry=gpd.points_from_xy(data_with_gaps['Longitude'], data_with_gaps['Latitude']),
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
            plot_file_path = os.path.join(plots_dir, filename.replace(".csv", "_trajectory.png"))
            plt.savefig(plot_file_path)

            # Close the plot to free up memory
            plt.close()

            print(f"Successfully processed: {filename}")

        except Exception as e:
            print(f"Error processing file {filename}: {e}")
