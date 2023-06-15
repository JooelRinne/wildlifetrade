import numpy as np
from numpy.core.numeric import NaN
import pandas as pd
import re
import sqlite3
from sqlalchemy import create_engine

# Choose which functions the script will run by writing True or False after the variable
# Data selection randomly sleects the data entries from raw data to data sets 
# sample_size determines how many data entries are chosen per data set
data_selection = True
sample_size = 100

# Accuracy assessments compares a reviewed data sets to data processed by scripts 
accuracy_assessment = True


if data_selection:
    # Loads data
    # If data in .csv:
    raw_data = pd.read_csv('database.csv')

    # If data in .db:
    # db = 'database.db'
    # data = sqlite3.connect(db)
    # raw_data = pd.read_sql_query('SELECT * FROM data_table', data)

    # Selects training data sets based on website type
    forum_trainingdata = raw_data.query("websitetype == 'forum'").sample(n = sample_size)
    marketplace_trainingdata = raw_data.query("websitetype == 'marketplace' or websitetype == 'other'").sample(n = sample_size)
    shop_trainingdata = raw_data.query("websitetype == 'shop'").sample(n = sample_size)

    # Selects test data sets based on website type
    forum_testdata = raw_data.query("websitetype == 'forum'").sample(n = sample_size)
    marketplace_testdata = raw_data.query("websitetype == 'marketplace' or websitetype == 'other'").sample(n  = sample_size)
    shop_testdata = raw_data.query("websitetype == 'shop'").sample(n = sample_size)

    # Saves created data sets as .csv files
    forum_trainingdata.to_csv('forum_validationdata.csv')
    marketplace_trainingdata.to_csv('marketplace_validationdata.csv')
    shop_trainingdata.to_csv('shop_validationdata.csv')
    forum_testdata.to_csv('forum_testdata.csv')
    marketplace_testdata.to_csv('marketplace_testdata.csv')
    shop_testdata.to_csv('shop_testdata.csv')


if accuracy_assessment:
    # Reads reviewed training and test data sets
    forum_trainingdata_r = pd.read_csv('forum_revieweddata.csv')
    forum_testdata_r = pd.read_csv('forum_revieweddata_test.csv')

    marketplace_trainingdata_r = pd.read_csv('marketplace_revieweddata.csv')
    marketplace_testdata_r = pd.read_csv('marketplace_revieweddata_test.csv')

    shop_trainingdata_r = pd.read_csv('shop_revieweddata.csv')
    shop_testdata_r = pd.read_csv('shop_revieweddata_test.csv')

    # Reads reviewed positive match data set
    positive = pd.read_csv('positivematch_accuracy_reviewed.csv')

    # Reads the filtered data by filtering algorithm
    filtered_df = pd.read_csv('matches.csv')
    filtered_df['original_datarow'] = filtered_df['original_datarow'].astype(str)


    # Select the training or test data sets used as reference 
    reference_datasets = [forum_trainingdata_r, forum_testdata_r, marketplace_trainingdata_r, marketplace_testdata_r, shop_trainingdata_r, shop_testdata_r, positive]
    # reference_datasets = [positive]

    for dataset in reference_datasets:
        dataset['match_filtered'] = [[]] * dataset.shape[0]

    # Calculates overall accuracies and omission and comission errors for filtered data from training data and test data sets
    number = 1
    for dataset in reference_datasets:
        for index, row in dataset.iterrows():
            search = str(row['original_datarow'])
            filtered = filtered_df.apply(lambda x: 'y' if re.fullmatch(search, x['original_datarow']) else None, axis=1) 

            no_nones = filter(None.__ne__, filtered)
            filtered = list(no_nones)


            if filtered:
                dataset.loc[index, 'match_filtered'] = 'y'
            else:
                dataset.loc[index, 'match_filtered'] = 'n'

        # Saves results to a .csv file
        dataset.to_csv(str(number) + '_results.csv')


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
        df.to_csv(str(number) + '_accuracyreport.csv')
        number += 1


