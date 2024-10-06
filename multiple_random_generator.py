import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import geopandas as gpd
import contextily as ctx
import random

# Define directories
input_dir = r"C:\\Users\\HU84VR\\Downloads\\AIS Project1\\Test Trajectories for AIS 20240831\\25 chosen perfect trajectory data"
output_dir = r"C:\\Users\\HU84VR\\Downloads\\AIS Project1\\Test Trajectories for AIS 20240831\\data_multiple"
plots_dir = r"C:\\Users\\HU84VR\\Downloads\\AIS Project1\\Test Trajectories for AIS 20240831\\plots\\plots_multiple"

# Create output directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)

# Generate NUM_GAPS and MIN_GAP_THRESHOLD dynamically
NUM_GAPS = random.randint(2, 50)
# The larger the NUM_GAPS, the smaller the MIN_GAP_THRESHOLD, and vice versa
MIN_GAP_THRESHOLD = float(200000 - (190000 * (NUM_GAPS / 50)))


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

# Function to create multiple gaps in a trajectory
def create_gaps(data, num_gaps):
    # Calculate total trajectory length
    total_length_of_trajectory = data['distance'].sum()

    # Split the total length into equal segments for each gap
    segment_length = total_length_of_trajectory / num_gaps

    # List to store the removed segments
    gaps = []

    # Create each gap within its respective segment
    for i in range(num_gaps):
        # Define the start and end of the current segment
        segment_start = i * segment_length
        segment_end = (i + 1) * segment_length

        # Dynamically reduce the gap threshold if necessary
        current_gap_threshold = MIN_GAP_THRESHOLD
        while segment_end - segment_start < current_gap_threshold:
            current_gap_threshold *= 0.5

        # Generate a random start location within the segment
        gap_start_location = np.random.uniform(segment_start, segment_end - current_gap_threshold)

        # Set the gap length to fit within the segment
        gap_length = np.random.uniform(current_gap_threshold, segment_end - gap_start_location)

        # Append the gap details to the list
        gaps.append((gap_start_location, gap_start_location + gap_length))

    # Remove the rows that fall within the gaps
    cumulative_distance = data['distance'].cumsum().reindex(data.index)
    for gap_start, gap_end in gaps:
        # data = data[(cumulative_distance < gap_start) | (cumulative_distance > gap_end)]
        data = data.loc[(cumulative_distance < gap_start) | (cumulative_distance > gap_end)]

    return data



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

            # Create gaps in the trajectory
            data_with_gaps_removed = create_gaps(data, NUM_GAPS)

            # Save the updated dataframe to a new CSV file with "_multiple_gaps" suffix
            output_file_path = os.path.join(output_dir, filename.replace(".csv", "_multiple_gaps.csv"))
            data_with_gaps_removed.to_csv(output_file_path, index=False)

            # Plotting the trajectory
            fig, ax = plt.subplots(figsize=(10, 10))

            # Convert data to GeoDataFrame for plotting
            gdf = gpd.GeoDataFrame(
                data_with_gaps_removed,
                geometry=gpd.points_from_xy(data_with_gaps_removed['Longitude'], data_with_gaps_removed['Latitude']),
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