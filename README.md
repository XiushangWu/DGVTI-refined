**DGVTI-Refined: Historical AIS Trajectory Data Imputation**

This project focuses on refining the imputation algorithm for missing positional reports in vessel trajectories, known as "Depth Map Enhanced Graph for Vessel Trajectory Imputation" (DGVTI). The algorithm was originally proposed by two colleagues from the Computer Science department at Aalborg University.

The Jupyter notebook, "Missing Scenarios Mimic.ipynb," utilizes 25 CSV files stored in the folder: "C:\Users\HU84VR\Downloads\AIS Project1\Test Trajectories for AIS 20240831\25 Chosen Perfect Trajectory Data". These files are used to simulate missing data by removing certain instances, mimicking three missing data patterns described in the paper "DGVTI: Depth-Map Enhanced Graph Imputation for Vessel Trajectories":

Single Missing Pattern: A single large gap within the trajectory.
Multiple Missing Pattern: Several mid-sized gaps dividing the trajectory into multiple disconnected parts.
Realistic Frequency Missing Pattern: Large gaps in specific sections where positional reports are completely missing, alongside frequent small gaps that indicate brief, minor interruptions in otherwise frequent reports.
The simulated data is stored in three folders—single, multiple, and realistic_frequency—each containing CSV files that reflect the respective missing pattern. The notebook also generates and saves trajectory plots for each missing pattern in a folder named "plots."




