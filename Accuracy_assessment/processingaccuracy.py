import pandas as pd

# Choose which functions the script will run by writing True or False after the variable
# Data selection randomly sleects the data entries from raw data to data sets 
# sample_size determines how many data entries are chosen per data set
data_selection = False
sample_size = 1

# Accuracy assessments compares a reviewed data sets to data processed by scripts 
accuracy_assessment = True

if data_selection:
    # Loads data
    raw_data = pd.read_csv('matches.csv')
    
    raw_data['Species_r'] = [''] * raw_data.shape[0]
    raw_data['Quantity_r'] = [''] * raw_data.shape[0]
    raw_data['Price_r'] = [''] * raw_data.shape[0]
    raw_data['Currency_r'] = [''] * raw_data.shape[0]
    raw_data['Intent_r'] = [''] * raw_data.shape[0]
    raw_data['Location_r'] = [''] * raw_data.shape[0]

    # Selects training and validation data sets
    processing_trainingdata = raw_data.sample(n = sample_size)
    processing_testdata = raw_data.sample(n = sample_size)

    # Saves created data sets as .csv files
    processing_trainingdata.to_csv('processing_trainingdata.csv')
    processing_testdata.to_csv('processing_testdata.csv')

# Calculates overall accuracies for each data field for processed data from training data and test data sets
if accuracy_assessment:
    # Reads reviewed training and test data sets
    trainingdata_r = pd.read_csv('processing_trainingdata_reviewed.csv')
    testdata_r = pd.read_csv('processing_testdata_reviewed.csv')

    # Reads the data processed by the processing algorithms
    processed_df = pd.read_csv('results.csv')
    processed_df['original_datarow'] = processed_df['original_datarow'].astype(str)
    # Calculate overall accuracies and omission and comission errors for filtered data from validation data and test datasets

    # Select the training or test data sets used as reference 
    reference_datasets = [trainingdata_r, testdata_r]
    datasets_names = ['trainingdata', 'testdata']


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

    original_datarow = 0
    for dataset, name in zip(reference_datasets, datasets_names):
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

                        if (str(row['Location_r']) == 'nan' and str(r['Country']) == '[]'):
                            dataset.loc[index, 'Location_correct'] = ''
                        elif (str(row['Location_r']) == 'NO' and str(r['Country']) == '[]'):
                            dataset.loc[index, 'Location_correct'] = ''                                                            
                        elif str(row['Location_r']) in str(r['Country']):
                            dataset.loc[index, 'Location_correct'] = 'y'
                        else:
                            dataset.loc[index, 'Location_correct'] = 'n'
                                                                         
                        original_datarow = r['original_datarow']


        dataset.to_csv(f'{name}__processingresults.csv')

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
        if species_total != 0:
            df.loc['Accuracy_species', 'total'] = species_y / species_total
        else:
            df.loc['Accuracy_species', 'total'] = 'NaN'

        quantity_total = quantity_y + quantity_n
        if quantity_total  != 0:
            df.loc['Accuracy_quantity', 'total'] = quantity_y / quantity_total
        else: 
            df.loc['Accuracy_quantity', 'total'] = 'NaN'

        price_total = price_y + price_n
        if price_total != 0:
            df.loc['Accuracy_price', 'total'] = price_y / price_total        
        else:
            df.loc['Accuracy_price', 'total'] = 'NaN'

        currency_total = currency_y + currency_n
        if currency_total != 0:
            df.loc['Accuracy_currency', 'total'] = currency_y / currency_total
        else:
            df.loc['Accuracy_currency', 'total'] = 'NaN'

        location_total = location_y + location_n
        if location_total != 0:
            df.loc['Accuracy_location', 'total'] = location_y / location_total
        else:
            df.loc['Accuracy_location', 'total'] = 'NaN'

        intent_total = intent_y + intent_n
        if intent_total != 0:
            df.loc['Accuracy_intent', 'total'] = intent_y / intent_total
        else:
            df.loc['Accuracy_intent', 'total'] = 'NaN'

        total_y = species_y + quantity_y + price_y + currency_y + location_y + intent_y
        df.loc['Total_y', 'total'] = total_y

        total_n = species_n + quantity_n + price_n + currency_n + location_n + intent_n
        df.loc['Total_n', 'total'] = total_n

        total = total_y + total_n

        if total != 0:
            df.loc['Overall_accuracy_all', 'total'] = total_y / total
        else:
            df.loc['Overall_accuracy_all', 'total'] = 'NaN'

        df.to_csv(f'{name}_processingaccuracyreport.csv')
