#!/usr/bin/env python3

# Imports necessary libraries
import numpy as np
from numpy.core.numeric import True_
import pandas as pd
import re
import spacy
from forex_python.converter import CurrencyRates
import datetime


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
df['Price_euro'] = [[]] * df.shape[0] 
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

        # If currency symbol is found saves the corresponding currency code to df['Currency'] column
        if len(currency) > 0:
            currency_symb = currency[0]
            currency_code = currency_list.loc[currency_list['Symbol'] == currency_symb, 'Code'].iloc[0]
            df.loc[index, 'Currency'] = currency_code

            # If timestamp is found finds values for year, month and day and then fetches the right rate from forex from that day, converts price to euros and stores to df['Price_euro'] column
            timestamp_cell = df.loc[index, 'timestamp']
            print(timestamp_cell)
            year = re.findall(r'.*([1-3][0,9][0-9]{2})', timestamp_cell)
            if year: 
                year = year[0]
            if not year:
                year = re.findall(r'.*([.][0,1,2][0-9])', timestamp_cell)
                if year:
                    year = str(year[0]).replace('.', '20') 
            print(year)

            month = re.findall(r'.*([.][0,1][0-9][.])', timestamp_cell)
            if month:
                month = str(month[0]).replace('.','')

            if not month:
                month = re.findall(r'.*([" "][1-9]{1,2}[[/])', timestamp_cell)
                if month:
                    month = str(month[0]).replace('/','')

            if not month:
                months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                months_regexp = '|'.join(months)
                month = re.findall(months_regexp, timestamp_cell)
                if month:
                    month = months.index(month[0]) + 1
            
            day = re.findall(r'.*([" "][0-9]{1,2}[.])', timestamp_cell)
            
            if day: 
                day = str(day[0]).replace('.','')

            if not day:
                day = re.findall(r'.*([" "][0-9]{1,2}[,])', timestamp_cell)

                if day: 
                    day = str(day[0]).replace(',','')
            if not day:
                day = re.findall(r'.*([/][0-9]{1,2}[/])', timestamp_cell)

                if day: 
                    day = str(day[0]).replace('/','')

            print(month)
            print(day)
            if year and month and day: 
                dt = datetime.datetime(int(year), int(month), int(day))
            elif year and month:
                dt = datetime.datetime(int(year), int(month), 1)
            elif year:
                dt = datetime.datetime(int(year), 1, 1)
            else:
                acquired = df.loc[index, 'acquired'].split('-')
                dt = datetime.datetime(int(acquired[0]), int(acquired[1]), int(acquired[2]))
            
            
            df.loc[index, 'Price_euro'] = float(df.loc[index, 'Price']) * CurrencyRates().get_rate(currency_code, 'EUR', dt)
        
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
