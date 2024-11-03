# import pandas as pd
# import os
# import argparse
#
#
# def process_ais_data(input_csv, output_directory):
#     # Load data
#     data = pd.read_csv(input_csv)
#
#     # Check for necessary columns
#     if 'MMSI' not in data.columns or 'Ship type' not in data.columns:
#         raise ValueError("The input CSV must contain 'MMSI' and 'Ship type' columns.")
#
#     # Get unique MMSI values
#     unique_mmsi = data['MMSI'].unique()
#
#     # Iterate through each MMSI and save to separate CSV files
#     for mmsi in unique_mmsi:
#         mmsi_data = data[data['MMSI'] == mmsi]
#         ship_type = mmsi_data['Ship type'].iloc[0]  # Get the Ship type for the MMSI
#
#         # Define the ship type directory path
#         ship_type_dir = os.path.join(output_directory, str(ship_type))
#         os.makedirs(ship_type_dir, exist_ok=True)  # Create directory if it doesn't exist
#
#         # Define the output file path with the desired format
#         mmsi_file_path = os.path.join(
#             ship_type_dir,
#             f"aisdk-2024-10-01_Class_A_MMSI_{mmsi}.csv"
#         )
#
#         # Save the MMSI data to the CSV file
#         mmsi_data.to_csv(mmsi_file_path, index=False)
#         print(f"Data has been successfully processed and saved to: {ship_type_dir}")
#
#     print(f"Data has been successfully processed and saved to: {output_directory}")
#
#
# if __name__ == "__main__":
#     # Set up argument parsing
#     parser = argparse.ArgumentParser(description="Process AIS data based on MMSI and ship type.")
#     parser.add_argument("input_csv", type=str, help="Path to the input CSV file.")
#     parser.add_argument("output_directory", type=str, help="Path to the output directory for classified CSV files.")
#
#     # Parse the arguments
#     args = parser.parse_args()
#
#     # Run the main function with parsed arguments
#     process_ais_data(args.input_csv, args.output_directory)

import pandas as pd
import os
import argparse
import glob


def process_ais_data(input_csv, output_directory):
    # Load data
    data = pd.read_csv(input_csv)

    # Check for necessary columns
    if 'MMSI' not in data.columns or 'Ship type' not in data.columns:
        raise ValueError("The input CSV must contain 'MMSI' and 'Ship type' columns.")

    # Extract base filename (without extension) to use in the output structure
    base_filename = os.path.splitext(os.path.basename(input_csv))[0]

    # Get unique MMSI values
    unique_mmsi = data['MMSI'].unique()

    # Iterate through each MMSI and save to separate CSV files
    for mmsi in unique_mmsi:
        mmsi_data = data[data['MMSI'] == mmsi]
        ship_type = mmsi_data['Ship type'].iloc[0]  # Get the Ship type for the MMSI

        # Define the ship type directory path within the base output directory
        ship_type_dir = os.path.join(output_directory, base_filename, str(ship_type))
        os.makedirs(ship_type_dir, exist_ok=True)  # Create directory if it doesn't exist

        # Define the output file path with the desired format
        mmsi_file_path = os.path.join(
            ship_type_dir,
            f"{base_filename}_MMSI_{mmsi}.csv"
        )

        # Save the MMSI data to the CSV file
        mmsi_data.to_csv(mmsi_file_path, index=False)
        print(f"Data has been successfully processed and saved to: {ship_type_dir}")

    print(f"Data for '{input_csv}' has been successfully processed and saved to: {output_directory}")


def process_all_files_in_directory(input_directory, output_directory):
    # Loop through all CSV files in the input directory
    csv_files = glob.glob(os.path.join(input_directory, "*.csv"))
    for csv_file in csv_files:
        process_ais_data(csv_file, output_directory)


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process multiple AIS CSV files by MMSI and ship type.")
    parser.add_argument("input_directory", type=str, help="Path to the input directory containing CSV files.")
    parser.add_argument("output_directory", type=str, help="Path to the output directory for classified CSV files.")

    # Parse the arguments
    args = parser.parse_args()

    # Run the main function to process all files in the directory
    process_all_files_in_directory(args.input_directory, args.output_directory)
