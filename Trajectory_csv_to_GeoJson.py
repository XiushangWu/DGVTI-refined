# import pandas as pd
# from shapely.geometry import LineString, Point, mapping
# import json
# import argparse
# import os
#
# def trajectory_to_geojson(data, mmsi_column='MMSI', timestamp_column='# Timestamp',
#                           lat_column='Latitude', lon_column='Longitude',
#                           draught_column='Draught', cog_column='COG',
#                           nav_status_column='Navigational status'):
#     # Filter data to include only relevant columns and drop rows with missing values in key columns
#     data_filtered = data[[timestamp_column, mmsi_column, lat_column, lon_column,
#                           draught_column, cog_column, nav_status_column]].dropna()
#
#     # Check if data_filtered is empty
#     if data_filtered.empty:
#         print("Warning: No valid data in this file after filtering. Skipping this file.")
#         return None  # Return None to indicate no GeoJSON could be generated
#
#     # Convert columns to appropriate types for JSON serialization
#     data_filtered[mmsi_column] = data_filtered[mmsi_column].astype(str)
#     data_filtered[timestamp_column] = data_filtered[timestamp_column].astype(str)
#     data_filtered[draught_column] = data_filtered[draught_column].astype(float)
#     data_filtered[cog_column] = data_filtered[cog_column].astype(float)
#     data_filtered[nav_status_column] = data_filtered[nav_status_column].astype(str)
#
#     # Create Points for each trajectory record with attributes
#     points = []
#     for _, row in data_filtered.iterrows():
#         point = Point(row[lon_column], row[lat_column])
#         # Store attributes with each point
#         point_attr = {
#             "type": "Feature",
#             "geometry": mapping(point),
#             "properties": {
#                 "MMSI": row[mmsi_column],
#                 "timestamp": row[timestamp_column],
#                 "draught": row[draught_column],
#                 "cog": row[cog_column],
#                 "navigation_status": row[nav_status_column]
#             }
#         }
#         points.append(point_attr)
#
#     # Create a LineString from Points (ignoring attributes at LineString level)
#     coordinates = [(p['geometry']['coordinates'][0], p['geometry']['coordinates'][1]) for p in points]
#     line = LineString(coordinates)
#
#     # Convert to GeoJSON format
#     geojson = {
#         "type": "FeatureCollection",
#         "features": [
#             {
#                 "type": "Feature",
#                 "geometry": mapping(line),
#                 "properties": {"MMSI": data_filtered[mmsi_column].iloc[0]}  # Assume MMSI is consistent
#             },
#             *points  # Add individual points with attributes
#         ]
#     }
#
#     return geojson
#
#
# def process_directory(input_dir, output_dir):
#     # Traverse the input directory and process each CSV file
#     for root, _, files in os.walk(input_dir):
#         for file in files:
#             if file.endswith(".csv"):
#                 # Determine input and output paths
#                 input_file = os.path.join(root, file)
#
#                 # Replicate folder structure in the output directory
#                 relative_path = os.path.relpath(root, input_dir)
#                 output_folder = os.path.join(output_dir, relative_path)
#                 os.makedirs(output_folder, exist_ok=True)
#
#                 # Set output file path with .geojson extension
#                 output_file = os.path.join(output_folder, file.replace(".csv", ".geojson"))
#
#                 # Load the CSV file
#                 data = pd.read_csv(input_file)
#
#                 # Convert to GeoJSON
#                 geojson_output = trajectory_to_geojson(data)
#
#                 # Skip if no valid GeoJSON was generated
#                 if geojson_output is None:
#                     print(f"Skipping {input_file} due to insufficient data.")
#                     continue
#
#                 # Save the GeoJSON file
#                 with open(output_file, "w") as f:
#                     json.dump(geojson_output, f, indent=2)
#
#                 print(f"Processed {input_file} -> {output_file}")
#
#
# def main():
#     # Set up argument parsing
#     parser = argparse.ArgumentParser(
#         description="Convert multiple AIS trajectory CSV files to GeoJSON in nested folders.")
#     parser.add_argument("input_dir", type=str, help="Path to the root input directory containing CSV files.")
#     parser.add_argument("output_dir", type=str, help="Path to the root output directory for GeoJSON files.")
#
#     args = parser.parse_args()
#
#     # Process the directory
#     process_directory(args.input_dir, args.output_dir)
#
#
# if __name__ == "__main__":
#     main()

# import pandas as pd
# from shapely.geometry import LineString, Point, mapping
# import json
# import argparse
# import os
#
#
# def trajectory_to_geojson(data, mmsi_column='MMSI', timestamp_column='# Timestamp',
#                           lat_column='Latitude', lon_column='Longitude',
#                           draught_column='Draught', cog_column='COG',
#                           nav_status_column='Navigational status'):
#     # Filter data to include only relevant columns and drop rows with missing values in key columns
#     data_filtered = data[[timestamp_column, mmsi_column, lat_column, lon_column,
#                           draught_column, cog_column, nav_status_column]].dropna()
#
#     # Ensure there are at least two points to form a LineString
#     if len(data_filtered) < 2:
#         print("Warning: No valid data in this file after filtering. Skipping this file.")
#         return None
#
#     # Convert columns to string or float types where needed for JSON serialization
#     data_filtered[mmsi_column] = data_filtered[mmsi_column].astype(str)
#     data_filtered[timestamp_column] = data_filtered[timestamp_column].astype(str)
#     data_filtered[draught_column] = data_filtered[draught_column].astype(float)
#     data_filtered[cog_column] = data_filtered[cog_column].astype(float)
#     data_filtered[nav_status_column] = data_filtered[nav_status_column].astype(str)
#
#     # Create Points for each trajectory record with attributes
#     points = []
#     for _, row in data_filtered.iterrows():
#         point = Point(row[lon_column], row[lat_column])
#         # Store attributes with each point
#         point_attr = {
#             "type": "Feature",
#             "geometry": mapping(point),
#             "properties": {
#                 "MMSI": row[mmsi_column],
#                 "timestamp": row[timestamp_column],
#                 "draught": row[draught_column],
#                 "cog": row[cog_column],
#                 "navigation_status": row[nav_status_column]
#             }
#         }
#         points.append(point_attr)
#
#     # Create a LineString from Points (ignoring attributes at LineString level)
#     coordinates = [(p['geometry']['coordinates'][0], p['geometry']['coordinates'][1]) for p in points]
#     line = LineString(coordinates)
#
#     # Convert to GeoJSON format
#     geojson = {
#         "type": "FeatureCollection",
#         "features": [
#             {
#                 "type": "Feature",
#                 "geometry": mapping(line),
#                 "properties": {"MMSI": data_filtered[mmsi_column].iloc[0]}  # Assume MMSI is consistent
#             },
#             *points  # Add individual points with attributes
#         ]
#     }
#
#     return geojson
#
#
# def process_directory(input_dir, output_dir):
#     # Traverse the input directory and process each CSV file
#     for root, _, files in os.walk(input_dir):
#         for file in files:
#             if file.endswith(".csv"):
#                 # Determine input and output paths
#                 input_file = os.path.join(root, file)
#
#                 # Replicate folder structure in the output directory
#                 relative_path = os.path.relpath(root, input_dir)
#                 output_folder = os.path.join(output_dir, relative_path)
#                 os.makedirs(output_folder, exist_ok=True)
#
#                 # Set output file path with .geojson extension
#                 output_file = os.path.join(output_folder, file.replace(".csv", ".geojson"))
#
#                 # Load the CSV file
#                 data = pd.read_csv(input_file)
#
#                 # Convert to GeoJSON
#                 geojson_output = trajectory_to_geojson(data)
#
#                 # Only save if geojson_output is valid
#                 if geojson_output is not None:
#                     with open(output_file, "w") as f:
#                         json.dump(geojson_output, f, indent=2)
#                     print(f"Processed {input_file} -> {output_file}")
#                 else:
#                     print(f"Skipping {input_file} due to insufficient data.")
#
#
# def main():
#     # Set up argument parsing
#     parser = argparse.ArgumentParser(
#         description="Convert multiple AIS trajectory CSV files to GeoJSON in nested folders.")
#     parser.add_argument("input_dir", type=str, help="Path to the root input directory containing CSV files.")
#     parser.add_argument("output_dir", type=str, help="Path to the root output directory for GeoJSON files.")
#
#     args = parser.parse_args()
#
#     # Process the directory
#     process_directory(args.input_dir, args.output_dir)
#
#
# if __name__ == "__main__":
#     main()

import pandas as pd
from shapely.geometry import LineString, Point, mapping
import json
import argparse
import os


def trajectory_to_geojson(data, mmsi_column='MMSI', timestamp_column='# Timestamp',
                          lat_column='Latitude', lon_column='Longitude',
                          draught_column='Draught', cog_column='COG',
                          nav_status_column='Navigational status'):
    # Filter out rows with missing latitude or longitude only
    data_filtered = data.dropna(subset=[lat_column, lon_column])

    # Convert columns to string or float types where needed for JSON serialization
    data_filtered[mmsi_column] = data_filtered[mmsi_column].astype(str)
    data_filtered[timestamp_column] = data_filtered[timestamp_column].astype(str)
    data_filtered[draught_column] = data_filtered[draught_column].astype(float)
    data_filtered[cog_column] = data_filtered[cog_column].astype(float)
    data_filtered[nav_status_column] = data_filtered[nav_status_column].astype(str)

    # Create Points for each trajectory record with attributes
    points = []
    for _, row in data_filtered.iterrows():
        if pd.notna(row[lat_column]) and pd.notna(row[lon_column]):  # Check for valid coordinates
            point = Point(row[lon_column], row[lat_column])
            # Store attributes with each point
            point_attr = {
                "type": "Feature",
                "geometry": mapping(point),
                "properties": {
                    "MMSI": row[mmsi_column],
                    "timestamp": row[timestamp_column],
                    "draught": row[draught_column],
                    "cog": row[cog_column],
                    "navigation_status": row[nav_status_column]
                }
            }
            points.append(point_attr)

    # Ensure there are at least two points for creating a LineString
    if len(points) < 2:
        print("Not enough valid data points to form a LineString.")
        return None

    # Create a LineString from Points
    coordinates = [(p['geometry']['coordinates'][0], p['geometry']['coordinates'][1]) for p in points]
    line = LineString(coordinates)

    # Convert to GeoJSON format
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": mapping(line),
                "properties": {"MMSI": data_filtered[mmsi_column].iloc[0]}  # Assume MMSI is consistent
            },
            *points  # Add individual points with attributes
        ]
    }
    return geojson

def process_directory(input_dir, output_dir):
    # Traverse the input directory and process each CSV file
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".csv"):
                # Determine input and output paths
                input_file = os.path.join(root, file)

                # Replicate folder structure in the output directory
                relative_path = os.path.relpath(root, input_dir)
                output_folder = os.path.join(output_dir, relative_path)
                os.makedirs(output_folder, exist_ok=True)

                # Set output file path with .geojson extension
                output_file = os.path.join(output_folder, file.replace(".csv", ".geojson"))

                # Load the CSV file
                data = pd.read_csv(input_file)

                # Convert to GeoJSON
                geojson_output = trajectory_to_geojson(data)

                # Check if conversion was successful (enough points to form a LineString)
                if geojson_output:
                    # Save the GeoJSON file
                    with open(output_file, "w") as f:
                        json.dump(geojson_output, f, indent=2)
                    print(f"Processed {input_file} -> {output_file}")
                else:
                    print(f"Skipped {input_file} due to insufficient valid data points.")


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Convert multiple AIS trajectory CSV files to GeoJSON in nested folders.")
    parser.add_argument("input_dir", type=str, help="Path to the root input directory containing CSV files.")
    parser.add_argument("output_dir", type=str, help="Path to the root output directory for GeoJSON files.")

    args = parser.parse_args()

    # Process the directory
    process_directory(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()

# python Trajectory_csv_to_GeoJson.py G:\AIS_Project1\AIS_Data_Class_A\10_ship_type\aisdk-2024-10-03\Cargo G:\AIS_Project1\AIS_Data_Class_A\10_ship_type\aisdk-2024-10-03\Cargo_GeoJson
