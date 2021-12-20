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
    raw_data = pd.read_csv('database.csv')

    forum_validationdata = raw_data.query("websitetype == 'forum'").sample(n = sample_size)
    marketplace_validationdata = raw_data.query("websitetype == 'marketplace' or websitetype == 'other'").sample(n = sample_size)
    shop_validationdata = raw_data.query("websitetype == 'shop'").sample(n = sample_size)

    forum_testdata = raw_data.query("websitetype == 'forum'").sample(n = sample_size)
    marketplace_testdata = raw_data.query("websitetype == 'marketplace' or websitetype == 'other'").sample(n  = sample_size)
    shop_testdata = raw_data.query("websitetype == 'shop'").sample(n = sample_size)


    forum_validationdata.to_csv('forum_validationdata.csv')
    marketplace_validationdata.to_csv('marketplace_validationdata.csv')
    shop_validationdata.to_csv('shop_validationdata.csv')
    forum_testdata.to_csv('forum_testdata.csv')
    marketplace_testdata.to_csv('marketplace_testdata.csv')
    shop_testdata.to_csv('shop_testdata.csv')


if accuracy_assessment:
    # Read reviewed validation and test data sets
    forum_validationdata_r = pd.read_csv('forum_revieweddata.csv')
    forum_testdata_r = pd.read_csv('forum_revieweddata_test.csv')

    marketplace_validationdata_r = pd.read_csv('marketplace_revieweddata.csv')
    marketplace_testdata_r = pd.read_csv('marketplace_revieweddata_test.csv')

    shop_validationdata_r = pd.read_csv('shop_revieweddata.csv')
    shop_testdata_r = pd.read_csv('shop_revieweddata_test.csv')

    # Read reviewed positive match data set
    positive = pd.read_csv('positivematch_accuracy_reviewed.csv')

    # Read the filtered data by filtering algorithm
    filtered_df = pd.read_csv('matches.csv')


    filtered_df['original_datarow'] = filtered_df['original_datarow'].astype(str)
    # Calculate overall accuracies and omission and comission errors for filtered data from validation data and test datasets

    # Select the validation or test data sets used as reference 
    # reference_datasets = [positive]
    reference_datasets = [forum_validationdata_r, forum_testdata_r, marketplace_validationdata_r, marketplace_testdata_r, shop_validationdata_r, shop_testdata_r, positive]

    for dataset in reference_datasets:
        dataset['match_filtered'] = [[]] * dataset.shape[0]

    number = 1
    for dataset in reference_datasets:
        for index, row in dataset.iterrows():
            search = str(row['original_datarow'])
            filtered = filtered_df.apply(lambda x: 'y' if re.fullmatch(search, x['original_datarow']) else None, axis=1) 
            # print(filtered)
            no_nones = filter(None.__ne__, filtered)
            filtered = list(no_nones)
            # print(filtered)

            if filtered:
                dataset.loc[index, 'match_filtered'] = 'y'
            else:
                dataset.loc[index, 'match_filtered'] = 'n'

        dataset.to_csv(str(number) + '_results.csv')

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
        df.to_csv(str(number) + '_accuracyreport.csv')
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