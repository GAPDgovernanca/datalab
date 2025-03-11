## Updated Instructions for the Data Analysis Application with Streamlit

### **Primary Requirements**:

1. **Dependencies**:

   - Utilize libraries `pandas`, `numpy`, `matplotlib`, `streamlit`, `pyyaml`, `openpyxl` for Excel handling, and `logging` for debugging.
   - Include additional libraries such as `datetime`, `io`, `base64`, `pytz` for specific functionalities.
   - **Remove unnecessary libraries** like `textwrap`.
   - Add `logging` for **detailed error reporting** and debugging.

2. **Configuration Management via YAML**:

   - **Refine Configuration**: Manage settings through an external YAML file (`config.yaml`) with enhanced descriptions.
   - The YAML file should include:
     - **Excel Column Mapping** (`excel_columns`): Handle duplicated columns (`PREVISTO (KG).1`, `REALIZADO (KG).1`) by retaining only unique columns to improve data handling.
     - **Analysis Settings** (`analysis`): Define weights, tolerance thresholds, outlier parameters, smoothing factors (`fator_suavizacao`, `peso_desvio`), and **missing value handling strategies**.
     - **User Interface Settings** (`ui`): Configure interface titles, labels, and other UI elements.
     - **Visualization Settings** (`visualization`): Enhance settings for histogram visualization, color thresholds, legends, and layout.
     - **Export Settings** (`export`): Define export formats, including options like Excel, and **add flexibility for exporting as PDF**.
     - **Timezone (`timezone`)**: Specify `America/Sao_Paulo` for all timestamps.

3. **Function to Load and Process Data**:

   - Function: `load_and_process_data(uploaded_file)`
     - Loads an Excel file (`.xlsx`) and processes it according to the YAML configuration.
     - **Enhance Missing Value Handling**: Add a step to either replace or remove `NaN` values based on configuration.
     - Return a processed DataFrame or **log detailed error messages** if validation fails.

4. **Column Identification**:

   - Function: `find_correct_columns(df, config)`
     - **Improve Column Validation**: Log missing or misconfigured columns for better debugging and data integrity.
     - Return a dictionary of column indices.

5. **Calculation of Weighted Average with Relative Weights**:

   - Function: `calculate_weighted_average_with_weights(df, pesos_relativos, config)`
     - Convert columns to numeric and compute absolute percentage differences.
     - **Improve Weight Mapping**: Apply user-defined weights (`PESO RELATIVO`) to the `TIPO` column, providing clearer messages in case of errors or data issues.
     - Compute the normalized deviation using the mean and standard deviation, applying the smoothing factors (`fator_suavizacao`, `peso_desvio`).
     - Group by 'COD. BATIDA' and compute the weighted average for each batch.
     - **Use detailed logging** for data issues or missing columns.

6. **Outlier Removal**:

   - Function: `remove_outliers_from_df(df, column)`
     - Utilize the IQR method for outlier detection.
     - **Log the number of outliers removed** to ensure transparency in data processing.
     - Return the filtered DataFrame.

7. **Data Filtering**:

   - Function: `filter_data(df, operadores, alimentos, dietas, start_date, end_date)`
     - Filters based on the user input (date range, operators, foods, diets).
     - **Improve Date Filtering**: Allow configurable default start and end dates through `config.yaml`.
     - Return the filtered DataFrame.

8. **Histogram Creation and Customization**:

   - Function: `create_histogram(df, start_date, end_date, remove_outliers, pesos_relativos, config)`
     - Remove outliers based on IQR if specified.
     - **Refine Color Thresholds**: Improve color coding for histograms to clearly represent percentage differences.
     - Include a legend, grid lines, vertical lines for tolerance, and **add a Weights Table** next to the histogram.
     - Return the created figure.

9. **Saving Histograms and Statistics**:

   - Function: `save_histogram_as_image(fig)`
     - Save the histogram in PNG format and generate a download link.
     - **Consider additional export formats (e.g., PDF)** for enhanced user experience.

   - Function: `save_statistics_as_csv(stats_df)`
     - Save statistics as CSV and generate a download link.
     - Add support for **multiple file formats**, like Excel, for tabular data.

10. **User Interface with Streamlit**:

    - Function: `main()`
      - Configure the Streamlit page with appropriate title and layout.
      - Divide the UI into **two columns** for inputs and results.
      - **Enhance User Input Flexibility**:
        - Add sliders for adjusting relative weights for food types (`TIPO`).
        - Add **sliders for smoothing parameters** (`fator_suavizacao`, `peso_desvio`) for fine-tuning analysis.
        - Multiselect inputs for selecting operators, foods, diets, and date range.
        - Checkbox for enabling/disabling outlier removal.
      - Upon clicking the "Generate" button:
        1. Load and filter data.
        2. Calculate weighted averages.
        3. Generate histogram.
        4. Display histogram and provide download links for both statistics and images.

11. **Timezone Configuration**:

    - Ensure all generated timestamps are formatted according to the Brasília timezone (`pytz`).

12. **Function Calls**:

    - Ensure that the `main()` function is called with:
      ```python
      if __name__ == "__main__":
          main()
      ```

### **Running the Application**:

Use the command below to run the application:

```bash
streamlit run batidas.py
```

### **GitHub Commands**

Use the following commands to commit and push updates to GitHub:

```bash
git status
git add applications/sjudas/app_batidas/instructions/Entendendo\ os\ Pesos\ Relativos\ no\ Controle\ de\ Dietas.html
git add applications/sjudas/app_batidas/instructions/formula_calculo.tex
git add applications/sjudas/app_batidas/instructions/instructions_for_app_batidas.md
git add applications/sjudas/app_batidas/instructions/pseudocode.md
git commit -m "Updated version of batidas app"
git push origin master
```

### **Virtual Environment Activation**

Activate the virtual environment before running:

```bash
workon batidas
```

Deactivate the virtual environment after you are done:

```bash
deactivate
```

