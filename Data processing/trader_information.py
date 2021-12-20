#!/usr/bin/env python3

# Imports necessary libraries
import numpy as np
from numpy.core.numeric import True_
import pandas as pd
import re
import spacy


# Defines quantity function
def def_quantity(cell, quantity_found):
    quantity_cell = cell.split()
    # Does not match to numerical values that indicate date or time 
    no_dates = list(filter(lambda x: not re.match('^(?:(?:[0-9]{1,4}[:\/x-]){1,2}[0-9]{1,4}|am|pm)$', x), quantity_cell))
    numbers_joined = ''.join(no_dates)
    numbers_strings = re.findall(r'\d+', numbers_joined)
    numbers = [int(n) for n in numbers_strings]
    numbers = [n for n in numbers if n < 100]
    summed = sum(numbers)
    if numbers and summed < 1000:
        df.loc[index, 'Quantity'] = summed
        quantity_found = True
    return quantity_found

# Reads the results from previous script "species.py"
df = pd.read_csv('reptiles_found.csv')
df.fillna('')

# Reads the necessary .csv files
currency_list = pd.read_csv('currency_symbols.csv')
synonyms = pd.read_csv('reptilesynonyms.csv')
synonyms = synonyms.fillna('')
seller_buyer = pd.read_csv('seller_or_buyer.csv')

# Creates a list of the currency symbols
currency_symbols = currency_list.Symbol.to_list()



# Creates new data columns needed
df['Quantity'] = [[]] * df.shape[0]
df['Quantity_found_from'] = [[]] * df.shape[0]
df['Price'] = [[]] * df.shape[0]
df['Currency'] = [[]] * df.shape[0] 
df['Intent'] = [[]] * df.shape[0]
df['Intent_found_from'] = [[]] * df.shape[0]
df['Intent_match'] = [[]] * df.shape[0]
df['Seller_id'] = [[]] * df.shape[0]

# Chooses language for SpaCy
nlp = spacy.load('en_core_web_sm')

# Removes NaN values
df = df.fillna('')
df = df.replace(r'\s',' ', regex=True) 


sellers = []

# Iterrates over each data entry
for index, row in df.iterrows():
    quantity_found = False
    description = row['description']

    # Tries to find quantity information from df['quantity'] column
    if row['quantity']:
        quantity_found = def_quantity(row['quantity'], quantity_found)
        if quantity_found:
            df.loc[index, 'Quantity_found_from'] = 'quantity'

    # Finds price information from df['price'] column
    if row['price']:
        price_cell = row['price']
        price_list = re.findall(r'\d+(?:[,.]\d+)*', price_cell)
        price_cell_str = str(price_cell)

        # If price is found from df['price'] column adds the price numerical value to df['Price'] column
        if len(price_list) > 0:
            if "," and "." in price_list[0]:
                price = price_list[0].replace(',','')
            else:
                price = price_list[0].replace(',', '.')
            df.loc[index, 'Price'] = price
        
        # Finds if currency any currency symbol is found from the df['price'] column
        currency = [symbol for symbol in currency_symbols if(str(symbol) in price_cell_str)]

        # If currency symbol is found saves the corresponding currency code to df['Currency'] colu,m
        if len(currency) > 0:
            currency_symb = currency[0]
            currency_code = currency_list.loc[currency_list['Symbol'] == currency_symb, 'Code'].iloc[0]
            df.loc[index, 'Currency'] = currency_code
    
    intent_found = False
    # Columns from which advertisement's intent will be searched from
    intent_columns = ['intent', 'reptile', 'description']

    # Searches the columns until inten is found
    for search_column in intent_columns:
        if not intent_found:
            for col in seller_buyer.columns:
                for i, r in seller_buyer.iterrows():
                    if not intent_found:
                        intent = re.findall(str(r[col]), str(row[search_column]), re.IGNORECASE)
                        if intent != '[]' and intent:
                            # print('col: ' + col)
                            # print('r[col]: ' + r[col])
                            # print('row[search_column]): ' + row[search_column])
                            # print('search_column: ' + search_column)
                            df.loc[index, 'Intent'] = col
                            df.loc[index, 'Intent_found_from'] = search_column
                            df.loc[index, 'Intent_match'] = str(r[col])
                            intent_found = True

    # If intent is not found from columns listed in "intent_columns" df['Price'] is searched
    if not intent_found:
        # If price is defined the intent of the advertisement is to sell
        if row['Price']:
            df.loc[index, 'Intent'] = 'Seller'
            intent_found = True

    # Still, if intent is not found df['comments'] column is searched
    if not intent_found:
        for col in seller_buyer.columns:
            for i, r in seller_buyer.iterrows():
                if not intent_found:
                    intent = re.findall(str(r[col]), str(row['comments']), re.IGNORECASE)
                    if intent != '[]' and intent:
                        df.loc[index, 'Intent'] = col
                        df.loc[index, 'Intent_found_from'] = search_column
                        df.loc[index, 'Intent_match'] = str(r[col])
                        intent_found = True

    # Turns seller name into id number 
    if row['seller']:
        seller_name = row['seller'][0:8]
        seller = seller_name.strip()

    if seller not in sellers:
        sellers.append(seller)
    
    if row['seller']:
        df.loc[index, 'Seller_id'] = sellers.index(seller)


# Saves to file
df.to_csv('quantitiesdone.csv')
