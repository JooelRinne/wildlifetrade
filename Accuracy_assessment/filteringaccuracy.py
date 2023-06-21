import pandas as pd
import re
import sqlite3
import glob

# Choose which functions the script will run by writing True or False after the variable
# Data selection randomly sleects the data entries from raw data to data sets 
data_selection = False

# Accuracy assessments compares a reviewed data sets to data processed by scripts 
accuracy_assessment = True

# Name of the database and the data table
db = 'wildlifetrade.db'
tb = 'reptiles_tb'

# Sample size determines how many data entries are chosen per data set
sample_size = 1

if data_selection:
    # Loads data
    # If data in .csv:
    #raw_data = pd.read_csv('database.csv')

    # If data in .db:
    data = sqlite3.connect(db)
    raw_data = pd.read_sql_query(f'SELECT * FROM {tb}', data)

    # Selects training data sets based on website type
    website_types = raw_data['website_type'].to_list()
    dataframes = {}

    for website_type in website_types:
        try:        
            dataframes[website_type + '_trainingdata'] = raw_data.query(f"website_type == '{website_type}'").sample(n = sample_size)
            dataframes[website_type + '_testdata'] = raw_data.query(f"website_type == '{website_type}'").sample(n = sample_size)
        except:
            print(f'Could not find enough rows of the website type: {website_type} to create training data ')

    # Saves created data sets as .csv files
    for key, df in dataframes.items():
        df['original_datarow'] = df.index
        filename = f'{key}.csv'
        df.to_csv(filename, index=False)


if accuracy_assessment:
    # Reads reviewed training and test data sets
    file_pattern = '*reviewed.csv*' # Pattern to match filenames
    
    csv_files = glob.glob(f'{file_pattern}')

    # Filter out files containing the word 'processing'
    csv_files = [file for file in csv_files if 'processing' not in file]

    dataframes = {}

    for file in csv_files:
        filename = file.split('/')[-1]  # Extract the filename from the file path
        df = pd.read_csv(file)  # Read the CSV file into a DataFrame
        dataframes[filename] = df  # Add the DataFrame to the dictionary

    # Reads the filtered data by filtering algorithm
    filtered_df = pd.read_csv('matches.csv')
    filtered_df['original_datarow'] = filtered_df['original_datarow'].astype(str)

    # Calculates overall accuracies and omission and comission errors for filtered data from training data and test data sets
    number = 1
    for key, dataset in dataframes.items():
        dataset['match_filtered'] = [[]] * dataset.shape[0]
        for index, row in dataset.iterrows():
            search = str(row['original_datarow'])
            filtered = filtered_df.apply(lambda x: 'y' if re.fullmatch(search, x['original_datarow']) else None, axis=1) 

            filtered = list(filter(lambda x: x is not None, filtered))

            if filtered:
                dataset.loc[index, 'match_filtered'] = 'y'
            else:
                dataset.loc[index, 'match_filtered'] = 'n'

        # Saves results to a .csv file
        filename = key[:-4]
        dataset.to_csv(f'{filename}_results.csv')


        # Creates accuracy reports for each data set
        df = pd.DataFrame(index=['filtered_y','filtered_n', 'total', 'overall_accuracy', 'filtered_omission_error', 'unfiltered_omission_error', 'filtered_commission_error', 'unfiltered_commission_error'], columns=['reference_y','reference_n', 'total'])

        filtered_y_reference_y = 0
        filtered_y_reference_n = 0
        filtered_n_reference_n = 0
        filtered_n_reference_y = 0
        for index, row in dataset.iterrows():
            if dataset.iloc[index]['filtered'] == 'y' and dataset.iloc[index]['match_filtered'] == 'y':
                filtered_y_reference_y += 1
            
            if dataset.iloc[index]['filtered'] == 'y' and dataset.iloc[index]['match_filtered'] == 'n':
                filtered_n_reference_y += 1

            if dataset.iloc[index]['filtered'] == 'n' and dataset.iloc[index]['match_filtered'] == 'n':
                filtered_n_reference_n += 1

            if dataset.iloc[index]['filtered'] == 'n' and dataset.iloc[index]['match_filtered'] == 'y':
                filtered_y_reference_n += 1        
                
        df.loc['filtered_y', 'reference_y'] = filtered_y_reference_y
        df.loc['filtered_y', 'reference_n'] = filtered_y_reference_n
        df.loc['filtered_n', 'reference_n'] = filtered_n_reference_n
        df.loc['filtered_n', 'reference_y'] = filtered_n_reference_y

        filtered_y_total = filtered_y_reference_y + filtered_y_reference_n
        df.loc['filtered_y', 'total'] = filtered_y_total
        filtered_n_total = filtered_n_reference_n + filtered_n_reference_y
        df.loc['filtered_n', 'total'] = filtered_n_total
        total_reference_y = filtered_y_reference_y + filtered_n_reference_y
        df.loc['total', 'reference_y'] = total_reference_y
        total_reference_n = filtered_n_reference_n + filtered_y_reference_n
        df.loc['total', 'reference_n'] = total_reference_n
        total_total = filtered_y_reference_y + filtered_y_reference_n + filtered_n_reference_n +filtered_n_reference_y
        df.loc['total', 'total'] = total_total

        if total_total != 0:
            df.loc['overall_accuracy', 'reference_y'] = (filtered_y_reference_y + filtered_n_reference_n)/total_total
        if total_reference_y != 0:    
            df.loc['filtered_omission_error', 'reference_y'] = filtered_n_reference_y/total_reference_y
        if total_reference_n != 0:
            df.loc['unfiltered_omission_error', 'reference_y'] = filtered_y_reference_n/total_reference_n
        if filtered_y_total != 0:
            df.loc['filtered_commission_error', 'reference_y'] = filtered_y_reference_n/filtered_y_total
        if filtered_n_total != 0:
            df.loc['unfiltered_commission_error', 'reference_y'] = filtered_n_reference_y/filtered_n_total
        
        # Saves data sets as .csv file
        df.to_csv(f'{filename}_accuracyreport.csv')
        


