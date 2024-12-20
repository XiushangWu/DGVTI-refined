**DGVTI-Refined: Historical AIS Trajectory Data Imputation**

This project focuses on refining the imputation algorithm for missing positional reports in vessel trajectories, known as "Depth Map Enhanced Graph for Vessel Trajectory Imputation" (DGVTI). The algorithm was originally proposed by two colleagues from the Computer Science department at Aalborg University.

The Jupyter notebook, "Missing Scenarios Mimic.ipynb," utilizes 6 CSV files stored in the folder: "C:\Users\HU84VR\Downloads\AIS_Project1\DGVTI_Test_Trajectories\trajectory_data_csv". These files are used to simulate missing data by removing certain instances, mimicking three missing data patterns described in the paper "DGVTI: Depth-Map Enhanced Graph Imputation for Vessel Trajectories":

The **single_random_generator_parsed.py** script processes data from 6 CSV files located in the folder: "C:\Users\HU84VR\Downloads\AIS_Project1\DGVTI_Test_Trajectories". It introduces a single large missing gap in the trajectory to assess the DGVTI algorithm's performance in scenarios with a significant gap. The script starts by setting a minimum threshold for the gap length, which is randomly generated between 50 km and 200 km, as defined by the variable **MIN_GAP_THRESHOLD = random.uniform(50000, 200000)**. If the total length of the trajectory is insufficient to create a gap of this size, the minimum threshold is repeatedly reduced by half (multiplied by 0.5) until the generated gap length, determined by **single_gap_length = np.random.uniform(current_gap_threshold, remaining_trajectory_length)**, fits within the available trajectory length. This approach ensures that a gap can be created even for shorter trajectories.
 
The **multiple_random_generator_parsed.py** script processes the same 6 CSV files and introduces multiple midsize missing gaps to test the DGVTI algorithm's performance under conditions where the trajectory features several gaps of moderate size. Similartly, it introduces multiple midsized missing gaps in the trajectory to assess the DGVTI algorithm's performance in scenarios with several midsized gaps. The script starts by setting a minimum threshold for the each gap length, which is randomly generated between 10 km and 200 km. The number of these gaps range from 2 to 50.

**Generate NUM_GAPS and MIN_GAP_THRESHOLD dynamically**
NUM_GAPS = random.randint(2, 50)
**The larger the NUM_GAPS, the smaller the MIN_GAP_THRESHOLD, and vice versa
**MIN_GAP_THRESHOLD = float(200000 - (190000 * (NUM_GAPS / 50)))

If the total length of the trajectory is insufficient to create a these gaps, the minimum threshold is repeatedly reduced by half (multiplied by 0.5) until the generated gap length, determined by **#gap_length = np.random.uniform(current_gap_threshold, segment_end - gap_start_location)**, fits within the available trajectory length. This approach ensures that all gap can be created without overlaping each other even for shorter trajectories.

The **combined_random_generator_parsed.py** script generates missing gaps based on realistic transmission frequencies, using the same 6 CSV files. These gaps simulate conditions that reflect the expected transmission rates of Class A vessels under various movement scenarios. This script combines both the single large gap and multiple smaller gaps, creating a more complex and realistic pattern of missing data. This approach is designed to mimic real-world scenarios where trajectories may experience both significant and minor gaps, offering a more comprehensive evaluation of the DGVTI algorithm’s performance under varied missing data conditions.

**For example:** vessels anchored or moored transmit position reports every 3 minutes, while those traveling at 0-14 knots transmit every 10 seconds, with increased frequency (every 3.33 seconds) during course changes.Vessels exceeding 23 knots may transmit as frequently as every 2 seconds.By replicating these transmission patterns, the study simulates realistic data gaps, allowing for the evaluation of the DGVTI algorithm’s ability to handle incomplete data. This approach is crucial for assessing the algorithm’s performance in comparison to other imputation methods.

**The examples of how to use the above 3 scripts are outlined in the 3 scripts uasge examples.txt, please check that.**

**Single Missing Pattern:** A single large gap within the trajectory.
**Multiple Missing Pattern:** Several mid-sized gaps dividing the trajectory into multiple disconnected parts.
**Combined (realistic frequency) Missing Pattern:** Refers to a scenario designed to simulate the realistic patterns of missing Automatic Identification System (AIS) data, specifically when vessel position reports are not received at the expected intervals. These missing patterns are meant to reflect real-world conditions where AIS data might be incomplete due to several causes such as signal interference, system malfunctions, or manual switch-offs. More specifically, the length of these missing gaps vary significantly from each other. So there are several large gaps and small gaps exist within the trajectory.

The next step is to extract all CSV files containing "perfect" trajectories, meaning those without missing values in the attributes "longitude," "latitude," and "draught." It’s important to emphasize that having no missing values for "longitude" and "latitude" alone does not guarantee a perfect trajectory without positional gaps. Missing data gaps can still occur due to prolonged AIS communication failures. Additionally, it's crucial to ensure that the extracted CSV files have no missing values for "draught." This is because, during the sea depth grid construction in the data preparation stage, missing sea depth grid cells are filled with the maximum draught values from neighboring vessel samples around the centroid of the grid cell. This ensures the depth map remains complete and consistent for the subsequent graph construction stage.

In order to make the model performance test valid. The script "**MMSI_ship_type_classification.py**" is used to extract all the trajectories from the data downloaded from the https://web.ais.dk/aisdata/. And the extracted trajectory data are classified into different categories based on the attribute "Ship type".

In addition, inorder to show the original trajectory on the QGIS, where we can compare the original trajectory, trajectory with manually created missing gaps and the imputed trajectory from DGVTI, the script **Trajectory_csv_to_GeoJson.py** is created and uploaded. The users can use it to convert the extracted csv trajectory for each MMSI into a GeoJson format. 

And the script **csv_trajectories_selection_for_DGVTI.py** is uploaded in order to  include only trajectories that overlap the 3 by 3 Skagen imputation graph, where we can check the performance of the 3 by 3 Skagen graph imputation on the trajectories that traverse the 3 by 3 graph.


