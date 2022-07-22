# Data_Processing_for_Integration
Processing of Supplier's Product Data: Pre-Processing, Normalisation, Integration 

Load, process and integrate product data to target format

Running "Data_Processing.py" will take "supplier_car.json" as the input and process it producing the output "Onedot-Data_Analyst_Remote_Task.xlsx"

"supplier_car.json": list of car data with different attributes that need to be matched to the darget data format

"Data_Processing.py": 
  - reads in the json file and turns it into a Pandas dataframe
  - Pivots the dataframe to have one row per car (based on ID) with all attributes
  - Normalises the data
  - Integrates it into the target data format
  - outputs an Excel file with the processes product data
  
"Onedot-Data_Analyst_Remote_Task.xlsx": Excel file that contains processes data
