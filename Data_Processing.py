#!/usr/bin/env python
# coding: utf-8
import numpy as np
import pandas as pd
import json


# Pre-processing

# open the json file and read it into dataframe
list_sup = []
with open('supplier_car.json') as f:
    for obj in f:
        dic = json.loads(obj)
        list_sup.append(dic)
df_sup = pd.DataFrame(list_sup)

# standardise zero values with 'NaN'
df_sup = df_sup.replace('null', np.NaN)
df_sup = df_sup.replace('None', np.NaN)

# change data such that attributes are written as colums
df_att = df_sup.pivot(values='Attribute Values',
                      index=['ID', 'MakeText', 'TypeName', 'TypeNameFull', 'ModelText', 'ModelTypeText'],
                      columns='Attribute Names').reset_index()

## Export to excel
df_att.to_excel('Onedot-Data_Analyst_Remote_Task.xlsx', sheet_name='Pre-Processing', index=False)


# Normalisation

df_norm = df_att

# turn ConsumptionTotal into numeric values with new column for unit
# this will allow to check if all the units are the same and would allow for comparison of numeric consumption values
df_norm[['ConsumptionTotal', 'ConsumptionTotalUnit']] = df_norm['ConsumptionTotalText'].str.split(' ', 1, expand=True)

df_norm['ConsumptionTotal'] = df_norm['ConsumptionTotal'].apply(pd.to_numeric, errors='coerce')
# the same could be done with 'Co2EmissionText'

# normalise all string values to be fully lower case to avoid differences from cases
str_cols = ['MakeText','TypeName','TypeNameFull','ModelText','ModelTypeText','BodyColorText','BodyTypeText','City',
            'ConditionTypeText','DriveTypeText','FuelTypeText','InteriorColorText','Properties','TransmissionTypeText']

for col in str_cols:
    df_norm[col] = df_norm[col].str.lower()

## Write to Excel
with pd.ExcelWriter('Onedot-Data_Analyst_Remote_Task.xlsx', engine="openpyxl", mode='a') as writer:
    df_norm.to_excel(writer, sheet_name='Normalisation', index=False)


# Integration

# a lot of columns are not in the target data and are would get dropped from the table (example of a few here)
# however, there are also values in the target data that are not here which cannot be inferred from this data either
df_int = df_norm.drop(['ID', 'TypeNameFull', 'TypeName', 'Properties'],
                      axis=1)

# integrate 'milage' column with 'milage_unit'  
df_int['milage_unit'] = 'kilometer'
df_int.rename(columns={'Km':'milage'}, inplace=True)

# add column for country (all cities are in Switzerland)
df_int['country'] = 'CH'

# they are all cars
df_int['type'] = 'car'
# it is unclear if the month and year of first registration is the same as the month and year of manufacturing

# match dataframe to target data format
df_int.rename(columns = {'MakeText':'make',  'BodyColorText':'color', 
                         'ConditionTypeText':'condition', 'City':'city', 'ModelTypeText':'model_variant', 
                         'ModelText':'model', 'BodyTypeText':'carType', 'Co2EmissionText':'Co2Emission'},
              inplace = True)

## Export to Excel
with pd.ExcelWriter('Onedot-Data_Analyst_Remote_Task.xlsx', engine="openpyxl", mode='a') as writer:
    df_int.to_excel(writer, sheet_name='Integration', index=False)
