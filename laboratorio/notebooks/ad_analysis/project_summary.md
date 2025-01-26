<project_summary>
The purpose of this project is to develop a Python program that processes data from .xlsx files, generates visualizations (heatmaps and radar graphs), and provides insights based on the data analysis. The program aims to automate the data processing and visualization tasks, making it easier to analyze and interpret the evaluation results of individuals across different competencies.
Key functions implemented so far:

Loading and processing data from .xlsx files:

The program reads data from .xlsx files using the pandas library.
It processes the data by discarding specified columns and removing accents from column names and values based on the configuration settings.
The processed data is then converted to JSON format for further analysis.


Generating heatmaps:

The program generates heatmaps for each competency defined in the configuration file.
It filters the data for the current competency and corresponding assessors.
The heatmap visualizes the scores given by assessors for each objective question related to the competency.
The heatmap is formatted according to the settings specified in the configuration file.
The generated heatmap is saved as an image file in the output folder.


Generating radar graph:

The program generates a radar graph that provides an overview of the average scores for each competency.
It calculates the averages of the assessors' scores and the self-assessment scores for each competency.
The radar graph is created using the settings specified in the configuration file.
The generated radar graph is saved as an image file in the output folder.



Specific requirements and considerations:

The program should be configurable using a YAML configuration file (competencias.yaml) that specifies the competencies, questions, assessor categories, and formatting settings for the visualizations.
The program should handle missing or inconsistent data gracefully and provide informative error messages.
The generated visualizations should be saved in a specified output folder with appropriate file names.
The program should provide a user-friendly interface for inputting the .xlsx file name and generating the visualizations.
The program should be modular and extensible, allowing for easy addition of new functionalities or modifications to existing ones.

In the previous session, we focused on implementing the data loading, processing, and accent removal functionalities. We also discussed the structure and content of the YAML configuration file and how it should be used to parameterize the program's behavior.
The next steps would be to implement the heatmap and radar graph generation functions, integrate them with the data processing pipeline, and ensure that the program generates the desired visualizations based on the configuration settings.
</project_summary>