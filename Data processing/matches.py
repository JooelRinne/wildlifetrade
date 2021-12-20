#!/usr/bin/env python3

# Import necessary libraries
import numpy as np
import pandas as pd
import re
import sqlite3



# Prepares keyword list:
# Reads them from the file
keywords = pd.read_csv('keywords.csv')['Keyword'].to_list()

# Create a regular expression that combines the keywords in one search phrase
keyword_regexp = '|'.join(  # | == OR in regular expressions
    [
        keyword.replace(' ', '.*?')  # change spaces to “match any character(s) (non-greedily)”
        for keyword in keywords
    ]
)

# Load scraped data from the SQLite database
db = 'reptilesales.db'
data = sqlite3.connect(db)

df = pd.read_sql_query('SELECT * FROM reptiles_tb', data)

# Creates 'original_datarow' column used later
df['original_datarow'] = np.arange(len(df))

# Creates list of text columns that might include species names. These columns are searched for matches to the keywords in the keywords list
columns_to_match_to_keywords = [
    'source',
    'reptile',
    'description',
    'comments',
    'location',
    'other',
    'image',
    'seller',
    'commenter',
    'intent'
]


# Creates empty data fields for matching parts in the data entries and for the keywords matchin them
df['matches'] = [[]] * df.shape[0]
df['keywords'] = [[]] * df.shape[0]


# Tries to match each column to the regular expression
# and adds the matches to df['matches']

for column in columns_to_match_to_keywords:
    df['matches'] += (
        df[column]
        .fillna('') 
        .str
        .findall(keyword_regexp, re.IGNORECASE | re.MULTILINE | re.DOTALL)
    )

# Cleans duplicates
# (if same keyword matched more than one column)
#  and joins into comma-separated string
df['matches'] = df['matches'].apply(lambda x: ',  '.join(set(x)))

df['matches'].replace('', float('NaN'), inplace=True)
df.dropna(subset = ['matches'], inplace=True)

# If strings in a matching text are less then 31 characters apart the keyword is saved
for keyword in keywords:
    keyword_regex = keyword.replace(' ', '.{0,30}?')
    keyword_regex_rest = keyword.replace(' ', '.{31, 10000}?')
    df['keywords'] = df.apply(lambda x: x['keywords'] + [keyword] if re.findall(keyword_regex, x['matches'], re.IGNORECASE | re.MULTILINE | re.DOTALL) else x['keywords'], axis=1) 
    
df['keywords'] = df['keywords'].apply(lambda x: ',  '.join(set(x)))

# If df['keywords'] column is empty drops the data entry
df['keywords'].replace('', float('NaN'), inplace=True)
df.dropna(subset = ['keywords'], inplace=True)

# Saves the results to a .csv file
df.to_csv('matches.csv')