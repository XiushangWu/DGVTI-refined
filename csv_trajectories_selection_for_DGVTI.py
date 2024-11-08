import os
import pandas as pd
from shapely.geometry import Point, Polygon
import argparse

# Define the boundary as a polygon
boundary_coords = [
    (9.4257695, 57.9407115),  # Upper left
    (11.8354331, 57.9407115),  # Upper right
    (11.8354331, 56.5932447),  # Lower right
    (9.4257695, 56.5932447),  # Lower left
    (9.4257695, 57.9407115)  # Closing the polygon
]
boundary_polygon = Polygon(boundary_coords)


# Function to check if any point in the dataframe is within the boundary
def contains_points_in_boundary(df, boundary_polygon):
    for _, row in df.iterrows():
        point = Point(row['Longitude'], row['Latitude'])
        if boundary_polygon.contains(point):
            return True
    return False


def main(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all CSV files in the directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_dir, file_name)

            # Load CSV file
            df = pd.read_csv(file_path)

            # Check if the dataframe contains any points within the boundary
            if 'Longitude' in df.columns and 'Latitude' in df.columns:
                if contains_points_in_boundary(df, boundary_polygon):
                    # Save the file to the output directory if it has points within the boundary
                    df.to_csv(os.path.join(output_dir, file_name), index=False)

    print("Filtering complete. Selected files are saved in the output directory.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter trajectory CSV files by geographic boundary")
    parser.add_argument('--input_dir', type=str,
                        default=r'G:\AIS_Project1\AIS_Data_Class_A\10_ship_type\aisdk-2024-10-31\Cargo',
                        help="Directory containing CSV files")
    parser.add_argument('--output_dir', type=str,
                        default=r'G:\AIS_Project1\AIS_Data_Class_A\10_ship_type\aisdk-2024-10-31\Cargo_csv_selected',
                        help="Directory to save selected CSV files")

    args = parser.parse_args()
    main(args.input_dir, args.output_dir)

# python script_name.py --input_dir "your_input_path" --output_dir "your_output_path"