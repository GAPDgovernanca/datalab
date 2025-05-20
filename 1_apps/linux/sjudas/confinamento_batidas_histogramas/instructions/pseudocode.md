# Updated Pseudocode for Batch Data Analysis Application using Streamlit

## 1. **Import Dependencies**

- Import necessary libraries:
  - `streamlit as st`: User interface components.
  - `pandas as pd`: Data manipulation.
  - `numpy as np`: Mathematical operations for numerical data.
  - `matplotlib.pyplot as plt`: Plotting histograms.
  - `yaml`: Configuration loading from YAML.
  - `pytz`: Timezone management.
  - `openpyxl`: Handling Excel files.
  - `logging`: Add for detailed debugging and error reporting.
  - Remove unused imports, e.g., `textwrap`.

## 2. **Load Configuration**

- Function: `read_config(config_file="config.yaml")`
  - Load configuration from the YAML file.
  - **Improve Error Handling**: Add detailed logging for both `FileNotFoundError` and `YAMLError`.
  - Return a dictionary with the following sections:
    - **Excel Column Mapping (`excel_columns`)**: Maps column names in the dataset, including a review to **handle duplicated columns** (`PREVISTO (KG).1`, `REALIZADO (KG).1`) by utilizing only the unique and necessary columns.
    - **Analysis Parameters (`analysis`)**: Sets default weights, tolerance thresholds, outlier parameters, and smoothing factors (`fator_suavizacao`, `peso_desvio`).
    - **UI Configuration (`ui`)**: Defines text, titles, and labels for the user interface.
    - **Visualization Settings (`visualization`)**: Adjust grid lines, color thresholds, and legend settings.
    - **Export Settings (`export`)**: Defines formats for image and CSV exports, and adds options for **multiple formats** like Excel for better accessibility.
    - **Timezone (`timezone`)**: Configures the timezone for timestamps (e.g., `America/Sao_Paulo`).

## 3. **Load and Process Data**

- Function: `load_and_process_data(uploaded_file)`
  - Accept an Excel file uploaded by the user.
  - Process the file by:
    1. **Skipping Rows**: Skip rows as configured in the `config.yaml` file (parameter: `skip_rows`).
    2. **Column Validation**: Ensure all required columns (as defined in `excel_columns`) are present in the file.
    3. **Convert 'DATA' Column to Datetime**: Use `pandas.to_datetime()` to handle date formats.
    4. **Numeric Conversion**: Convert columns like `'PREVISTO (KG)'`, `'REALIZADO (KG)'`, and `'DIFERENÇA (%)'` to numeric, handling `NaN` values.
    5. **Treat Missing Values**: Add a step to **replace or drop `NaN` values** based on `config.yaml`.
  - Handle errors if the file structure is invalid or columns are missing, and log errors for better debugging.
  - Return the processed DataFrame or an error message.

## 4. **Column Identification**

- Function: `find_correct_columns(df, config)`
  - Identify and validate the required columns (`PREVISTO (KG)`, `REALIZADO (KG)`, `DIFERENÇA (%)`, etc.) in the dataset.
  - Match column names from the Excel file to those specified in the configuration.
  - Return a dictionary with column indices or raise an error if columns are missing.

## 5. **Weighted Average Calculation**

- Function: `calculate_weighted_average_with_weights(df, pesos_relativos, config)`
  - Steps:
    1. **Numeric Conversion**: Convert columns like `PREVISTO (KG)` and `REALIZADO (KG)` to numeric.
    2. **Map Relative Weights**: Apply relative weights (`PESO RELATIVO`) to the `TIPO` column as per user input.
    3. **Calculate Adjusted Planned Quantity**: Multiply the planned quantity (`PREVISTO (KG)`) by the relative weight (`PESO RELATIVO`).
    4. **Calculate Desvio Normalizado**: Calculate the normalized deviation using the mean and standard deviation, applying the `fator_suavizacao` and `peso_desvio` as configured.
    5. **Calculate Contribution**: Multiply the absolute percentage difference by the adjusted planned quantity, considering the smoothing factor (`fator_suavizacao`).
    6. **Group by 'COD. BATIDA'**: Calculate the weighted average for each batch (`COD. BATIDA`).
    7. **Error Handling**: Add **detailed logs** for missing essential columns or calculation issues.
  - Return a DataFrame containing the calculated weighted averages per batch.

## 6. **Outlier Removal**

- Function: `remove_outliers_from_df(df, column)`
  - Identify and remove outliers using the Interquartile Range (IQR) method:
    1. Calculate the IQR (Q3 - Q1).
    2. Define upper and lower bounds (Q1 - 1.5 * IQR, Q3 + 1.5 * IQR).
    3. Remove rows with values outside these bounds.
  - **Log outlier removal**: Log the number of rows removed as outliers for reference.
  - Return the cleaned DataFrame.

## 7. **Data Filtering**

- Function: `filter_data(df, operadores, alimentos, dietas, start_date, end_date)`
  - Filter the dataset based on:
    1. **Date Range**: Filter rows within the selected `start_date` and `end_date`.
    2. **Operators** (`OPERADOR`): Select only the operators chosen by the user.
    3. **Foods** (`ALIMENTO`): Select specific food types defined by the user.
    4. **Diets** (`NOME`): Filter data based on selected diets.
  - Return the filtered DataFrame.

## 8. **Histogram Creation and Customization**

### a. **Create Histogram**

- Function: `create_histogram(df, start_date, end_date, remove_outliers, pesos_relativos, config)`
  - Steps:
    1. **Remove Outliers**: Optionally remove outliers based on the IQR method.
    2. **Define Bins**: Use the Freedman-Diaconis rule to calculate histogram bin width.
    3. **Color Bars**: Color the histogram bars based on percentage difference thresholds defined in `config.yaml`.
    4. **Add Vertical Line**: Add a dashed vertical line at the tolerance limit for visual reference.
    5. **Add Legend**: Include a **legend** to explain the color coding.
    6. **Footer**: Add analysis details like date range, number of batches, and the current timestamp.
    7. **Weights Table**: Display the relative weights for each food type next to the histogram.
  - Return the created figure.

## 9. **Statistics Calculation and Export**

### a. **Create Statistics DataFrame**

- Function: `create_statistics_dataframe(weighted_average_df, remove_outliers=False, config=None)`
  - Calculate key statistics:
    1. **Mean and Median**: Calculate the mean and median of the percentage differences.
    2. **Count in Ranges**: Count how many percentage differences fall within predefined ranges (e.g., 3%-5%, 5%-7%, >7%).
  - Return a DataFrame with the statistics.

### b. **Save Histogram as Image**

- Function: `save_histogram_as_image(fig)`
  - Save the generated histogram as a PNG image using a BytesIO buffer.
  - Encode the image in Base64 format and return a downloadable HTML link.

### c. **Save Statistics as CSV**

- Function: `save_statistics_as_csv(stats_df)`
  - Save the calculated statistics as a CSV file.
  - Encode the file in Base64 format and return a downloadable HTML link.

## 10. **User Interface with Streamlit**

### a. **UI Layout and Inputs**

- Set up the Streamlit interface with a "wide" layout:
  1. **File Uploader**: Allow the user to upload an Excel file (`.xlsx` format).
  2. **Sliders for Relative Weights**: Add sliders for adjusting relative weights, defined in `config.yaml`, allowing real-time updates to the analysis based on user inputs.
  3. **Sliders for Smoothing Factors**: Allow adjustment of `fator_suavizacao` and `peso_desvio` via sliders, giving users control over the influence of extreme values.
  4. **Multiselect Inputs**: Provide options for selecting operators, foods, diets, and a date range.
  5. **Outlier Removal Checkbox**: Add a checkbox to enable or disable outlier removal.
  6. **Generate Button**: Add a "Generate" button to trigger the data analysis.

## 11. **Execution Flow**

### a. **Main Function**

- Function: `main()`
  - Load configurations from `config.yaml`.
  - Handle file upload and data processing.
  - Display filters and inputs to the user:
    - Sliders for adjusting relative weights and smoothing parameters.
    - Date range, operators, foods, and diets for filtering.
  - When the user clicks "Generate":
    1. Load and filter data.
    2. Calculate weighted averages.
    3. Generate and display the histogram.
    4. Display key statistics and allow for downloading the histogram and statistics.

### b. **Program Entry Point**

- Ensure the `main()` function is called when the script runs:
  
  ```python
  if __name__ == "__main__":
      main()
  ```

## 12. **Timezone Handling**

- Use the timezone setting defined in `config.yaml` (`America/Sao_Paulo`) to manage timestamps for exported files and footers on the histogram.

## 13. **Application Execution**

- Run the Streamlit application with the following command:
  
  ```bash
  streamlit run batidas.py
  ```
