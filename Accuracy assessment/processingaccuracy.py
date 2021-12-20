import numpy as np
from numpy.core.numeric import NaN
import pandas as pd
import re
import sqlite3
from sqlalchemy import create_engine


# load the data
# db = 'reptilesales2.db'
# data = sqlite3.connect(db)
# raw_data = pd.read_sql_query('SELECT * FROM reptiles_tb', data)

data_selection = False
accuracy_assessment = True
sample_size = 100

if data_selection:
    raw_data = pd.read_csv('matches.csv')

    processing_validationdata = raw_data.sample(n = sample_size)
    processing_testdata = raw_data.sample(n = sample_size)

    processing_validationdata .to_csv('processing_validationdata .csv')
    processing_testdata.to_csv('processing_testdata.csv')


if accuracy_assessment:
    # Read reviewed validation and test data sets
    validationdata_r = pd.read_csv('processing_validationdata_reviewed.csv')
    testdata_r = pd.read_csv('processing_testdata_reviewed.csv')

    # Read the filtered data by filtering algorithm
    processed_df = pd.read_csv('locationsdone.csv')
    processed_df['original_datarow'] = processed_df['original_datarow'].astype(str)
    # Calculate overall accuracies and omission and comission errors for filtered data from validation data and test datasets

    # Select the validation or test data sets used as reference 
    reference_datasets = [validationdata_r, testdata_r]


    for dataset in reference_datasets:
        dataset['Species_correct'] = [[]] * dataset.shape[0]
        dataset['Quantity_correct'] = [[]] * dataset.shape[0]
        dataset['Price_correct'] = [[]] * dataset.shape[0]
        dataset['Currency_correct'] = [[]] * dataset.shape[0]
        dataset['Location_correct'] = [[]] * dataset.shape[0]
        dataset['Intent_correct'] = [[]] * dataset.shape[0]

    script_cells = ['Species', 'Quantity', 'Price', 'Currency', 'Intent']
    reviewed_cells = ['Species_r', 'Quantity_r', 'Price_r', 'Currency_r', 'Intent_r']
    comparison_cells = ['Species_correct', 'Quantity_correct', 'Price_correct', 'Currency_correct', 'Intent_correct']

    number = 1
    original_datarow = 0
    for dataset in reference_datasets:
        for index, row in dataset.iterrows():
            for i, r in processed_df.iterrows():
                if str(float(row['original_datarow'])) == str(float(r['original_datarow'])):
                    if str(original_datarow) != str(r['original_datarow']):
                        for cell in script_cells:
                            if (str(row[cell + '_r']) == 'nan' and str(r[cell]) == '[]'):
                                dataset.loc[index, cell + '_correct'] = ''
                            elif (str(row[cell + '_r']) == 'NO' and str(r[cell]) == '[]'):
                                dataset.loc[index, cell + '_correct'] = ''
                            elif str(r[cell]) in str(row[cell + '_r']):
                                dataset.loc[index, cell + '_correct'] = 'y'
                            else:
                                dataset.loc[index, cell + '_correct'] = 'n'

                        if (str(row['Location_r']) == 'nan' and str(r['location_spacy']) == '[]'):
                            dataset.loc[index, 'Location_correct'] = ''
                        elif (str(row['Location_r']) == 'NO' and str(r['location_spacy']) == '[]'):
                            dataset.loc[index, 'Location_correct'] = ''                                                            
                        elif str(row['Location_r']) in str(r['location_spacy']):
                            dataset.loc[index, 'Location_correct'] = 'y'
                        else:
                            dataset.loc[index, 'Location_correct'] = 'n'
                                                                         
                        original_datarow = r['original_datarow']


        dataset.to_csv(str(number) + '_processingresults.csv')

        df = pd.DataFrame(index=[
            'Species_y',
            'Species_n',
            'Accuracy_species',
            'Quantity_y',
            'Quantity_n',
            'Accuracy_quantity',
            'Price_y',
            'Price_n',
            'Accuracy_price',
            'Currency_y',
            'Currency_n',
            'Accuracy_currency',
            'Location_y',
            'Location_n', 
            'Accuracy_location',
            'Intent_y',
            'Intent_n',
            'Accuracy_intent',
            'Total_y',
            'Total_n', 
            'Overall_accuracy_all'],  
            columns=['total'])

        species_y = 0
        species_n = 0
        
        quantity_y = 0
        quantity_n = 0

        price_y = 0
        price_n = 0

        currency_y = 0
        currency_n = 0

        location_y = 0
        location_n = 0

        intent_y = 0
        intent_n = 0

        for index, row in dataset.iterrows():
            if dataset.iloc[index]['Species_correct'] == 'y':
                species_y += 1
            elif (str(dataset.iloc[index]['Species_r']) == 'NO' 
            and str(dataset.iloc[index]['Species_correct']) == '[]'):
                None    
            elif dataset.iloc[index]['Species_correct'] == '':
                None
            else:
                species_n += 1
            
            if dataset.iloc[index]['Quantity_correct'] == 'y':
                quantity_y += 1
            elif (str(dataset.iloc[index]['Species_r']) == 'NO' 
            and str(dataset.iloc[index]['Quantity_correct']) == '[]'):
                None
            elif dataset.iloc[index]['Quantity_correct'] == '':
                None           
            else:
                quantity_n += 1

            if dataset.iloc[index]['Price_correct'] == 'y':
                price_y += 1
            elif (str(dataset.iloc[index]['Species_r']) == 'NO' 
            and (dataset.iloc[index]['Price_correct']) == '[]'):
                None
            elif dataset.iloc[index]['Price_correct'] == '':
                None     
            else:
                price_n += 1

            if dataset.iloc[index]['Currency_correct'] == 'y':
                currency_y += 1
            elif (str(dataset.iloc[index]['Species_r']) == 'NO' 
            and str(dataset.iloc[index]['Currency_correct']) == '[]'):
                None
            elif dataset.iloc[index]['Currency_correct'] == '':
                None     
            else:
                currency_n += 1
            
            if dataset.iloc[index]['Location_correct'] == 'y':
                location_y += 1
            elif (str(dataset.iloc[index]['Species_r']) == 'NO' 
            and str(dataset.iloc[index]['Location_correct']) == '[]'):
                None
            elif dataset.iloc[index]['Location_correct'] == '':
                None     
            else:
                location_n += 1

            if dataset.iloc[index]['Intent_correct'] == 'y':
                intent_y += 1
            elif (str(dataset.iloc[index]['Intent_r']) == 'NO' 
            and  str(dataset.iloc[index]['Intent_correct']) == '[]'):
                None
            elif dataset.iloc[index]['Intent_correct'] == '':
                None     
            else:
                intent_n += 1                   
                
        df.loc['Species_y', 'total'] = species_y
        df.loc['Species_n', 'total'] = species_n
        df.loc['Quantity_y', 'total'] = quantity_y
        df.loc['Quantity_n', 'total'] = quantity_n
        df.loc['Price_y', 'total'] = price_y
        df.loc['Price_n', 'total'] = price_n
        df.loc['Currency_y', 'total'] = currency_y
        df.loc['Currency_n', 'total'] = currency_n
        df.loc['Location_y', 'total'] = location_y
        df.loc['Location_n', 'total'] = location_n
        df.loc['Intent_y', 'total'] = intent_y
        df.loc['Intent_n', 'total'] = intent_n

        species_total = species_y + species_n
        df.loc['Accuracy_species', 'total'] = species_y / species_total

        quantity_total = quantity_y + quantity_n
        df.loc['Accuracy_quantity', 'total'] = quantity_y / quantity_total

        price_total = price_y + price_n
        df.loc['Accuracy_price', 'total'] = price_y / price_total        

        currency_total = currency_y + currency_n
        df.loc['Accuracy_currency', 'total'] = currency_y / currency_total

        location_total = location_y + location_n
        df.loc['Accuracy_location', 'total'] = location_y / location_total

        intent_total = intent_y + intent_n
        df.loc['Accuracy_intent', 'total'] = intent_y / intent_total


        total_y = species_y + quantity_y + price_y + currency_y + location_y + intent_y
        df.loc['Total_y', 'total'] = total_y

        total_n = species_n + quantity_n + price_n + currency_n + location_n + intent_n
        df.loc['Total_n', 'total'] = total_n

        total = total_y + total_n
        df.loc['Overall_accuracy_all', 'total'] = total_y / total

        df.to_csv(str(number) + '_processingaccuracyreport.csv')
        number += 1

# for index, row in websitetypes.iterrows():
#     df['websitetype'] = df.apply(lambda x: row['type'] if re.findall(row['abbreviation'], x['source'], re.IGNORECASE | re.MULTILINE | re.DOTALL) else x['websitetype'], axis=1) 
#     break

# # for index, row in df.iterrows():
# #     for i, website in websitetypes.iterrows():
# #         source = str(df['source'])
# #         abbreviation = str(website['abbreviation'])

# #         if source.find(abbreviation) != -1:
# #             row['websitetype'] = website['type']





# df['original_datarow'] = np.arange(len(df))

# engine = create_engine('sqlite://', echo=False)
# df.to_sql('reptilesales', con=engine)
# df.to_csv('database.csv')
# print(df.head())