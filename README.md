**DGVTI-Refined: Historical AIS Trajectory Data Imputation**

This project focuses on refining the imputation algorithm for missing positional reports in vessel trajectories, known as "Depth Map Enhanced Graph for Vessel Trajectory Imputation" (DGVTI). The algorithm was originally proposed by two colleagues from the Computer Science department at Aalborg University.

The Jupyter notebook, "Missing Scenarios Mimic.ipynb," utilizes 25 CSV files stored in the folder: "C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\25 Chosen Perfect Trajectory Data". These files are used to simulate missing data by removing certain instances, mimicking three missing data patterns described in the paper "DGVTI: Depth-Map Enhanced Graph Imputation for Vessel Trajectories":

**single_random_generator.py**, this script is used to read and create one single large missing gap within the data from the 25 CSV files stored in the folder: "C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\25 Chosen Perfect Trajectory Data", the processed data with one large single missing gap is used to check the performance of DGVTI algorithm performance under scenario where the trajectory exhibit one single lager missing gap pattern.
**multiple_random_generator.py**, this script is used to read and create multiple midzise missing gaps within the data from the 25 CSV files stored in the folder: "C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\25 Chosen Perfect Trajectory Data", the processed data with multiple midzise missing gaps is used to check the performance of DGVTI algorithm performance under scenario where the trajectory exhibit one multiple midzise missing gaps pattern.
**realistic_frequency_random_generator**.py, this script is used to read and create realistic frequency missing gaps within the data from the 25 CSV files stored in the folder: "C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\25 Chosen Perfect Trajectory Data", data the processed data with realistic frequency missing gaps is used to check the performance of DGVTI algorithm performance under scenario where the trajectory exhibit realistic frequency missing gaps pattern. This realistic frequency of missing data is derived based on the transmission rates expected from Class A vessels under different conditions of movement. The paper describes how these vessels transmit position reports at varying frequencies based on factors like speed, course changes, and whether the vessel is stationary or moving. 
For instance: 
When the vessel is anchored or moored, the transmission frequency is every 3 minutes.
For vessels moving at speeds between 0 and 14 knots, the reports are transmitted every 10 seconds, but when changing course, it increases to every 3.33 seconds.
At higher speeds (above 23 knots), the frequency of transmission can be as short as 2 seconds.
By replicating these transmission rates, the study models missing data to reflect realistic conditions where expected reports may be absent. This is crucial for evaluating how the proposed imputation method handles incomplete data compared to other methods








Single Missing Pattern: A single large gap within the trajectory.
Multiple Missing Pattern: Several mid-sized gaps dividing the trajectory into multiple disconnected parts.
Realistic Frequency Missing Pattern: Refers to a scenario designed to simulate the realistic patterns of missing Automatic Identification System (AIS) data, specifically when vessel position reports are not received at the expected intervals. These missing patterns are meant to reflect real-world conditions where AIS data might be incomplete due to several causes such as signal interference, system malfunctions, or manual switch-offs.




The next step is to extract all CSV files containing "perfect" trajectories, meaning those without missing values in the attributes "longitude," "latitude," and "draught." It’s important to emphasize that having no missing values for "longitude" and "latitude" alone does not guarantee a perfect trajectory without positional gaps. Missing data gaps can still occur due to prolonged AIS communication failures. Additionally, it's crucial to ensure that the extracted CSV files have no missing values for "draught." This is because, during the sea depth grid construction in the data preparation stage, missing sea depth grid cells are filled with the maximum draught values from neighboring vessel samples around the centroid of the grid cell. This ensures the depth map remains complete and consistent for the subsequent graph construction stage.


