**DGVTI-Refined: Historical AIS Trajectory Data Imputation**

This project focuses on refining the imputation algorithm for missing positional reports in vessel trajectories, known as "Depth Map Enhanced Graph for Vessel Trajectory Imputation" (DGVTI). The algorithm was originally proposed by two colleagues from the Computer Science department at Aalborg University.

The Jupyter notebook, "Missing Scenarios Mimic.ipynb," utilizes 25 CSV files stored in the folder: "C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\25 Chosen Perfect Trajectory Data". These files are used to simulate missing data by removing certain instances, mimicking three missing data patterns described in the paper "DGVTI: Depth-Map Enhanced Graph Imputation for Vessel Trajectories":

The **single_random_generator.py** script reads data from 25 CSV files stored in the folder: "C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\25 Chosen Perfect Trajectory Data". It creates a single large missing gap in the data to evaluate the performance of the DGVTI algorithm in scenarios where the trajectory contains one significant gap.

The **multiple_random_generator.py** script processes the same 25 CSV files and introduces multiple midsize missing gaps to test the DGVTI algorithm's performance under conditions where the trajectory features several gaps of moderate size.

The **realistic_frequency_random_generator.py** script generates missing gaps based on realistic transmission frequencies, also using the same 25 CSV files. These gaps simulate realistic conditions derived from the expected transmission rates of Class A vessels under various movement scenarios. 

**For example:** vessels anchored or moored transmit position reports every 3 minutes, while those traveling at 0-14 knots transmit every 10 seconds, with increased frequency (every 3.33 seconds) during course changes.Vessels exceeding 23 knots may transmit as frequently as every 2 seconds.By replicating these transmission patterns, the study simulates realistic data gaps, allowing for the evaluation of the DGVTI algorithm’s ability to handle incomplete data. This approach is crucial for assessing the algorithm’s performance in comparison to other imputation methods.








Single Missing Pattern: A single large gap within the trajectory.
Multiple Missing Pattern: Several mid-sized gaps dividing the trajectory into multiple disconnected parts.
Realistic Frequency Missing Pattern: Refers to a scenario designed to simulate the realistic patterns of missing Automatic Identification System (AIS) data, specifically when vessel position reports are not received at the expected intervals. These missing patterns are meant to reflect real-world conditions where AIS data might be incomplete due to several causes such as signal interference, system malfunctions, or manual switch-offs.




The next step is to extract all CSV files containing "perfect" trajectories, meaning those without missing values in the attributes "longitude," "latitude," and "draught." It’s important to emphasize that having no missing values for "longitude" and "latitude" alone does not guarantee a perfect trajectory without positional gaps. Missing data gaps can still occur due to prolonged AIS communication failures. Additionally, it's crucial to ensure that the extracted CSV files have no missing values for "draught." This is because, during the sea depth grid construction in the data preparation stage, missing sea depth grid cells are filled with the maximum draught values from neighboring vessel samples around the centroid of the grid cell. This ensures the depth map remains complete and consistent for the subsequent graph construction stage.


