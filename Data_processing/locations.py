#!/usr/bin/env python3

"""Search locations in text form and convert them to geographic coordinates
"""
from numpy.core.numeric import NaN
import spacy
import geocoder
import re
import pandas as pd
from collections import Counter

# Choose language
nlp = spacy.load('en_core_web_sm')

# Read data
df = pd.read_csv('quantitiesdone.csv')
locationlist = pd.read_csv('locationlist.csv')

# Add new location columns
df['location_spacy'] = [[]] * df.shape[0]  # empty list​
df['location_osm'] = [[]] * df.shape[0]
df['coordinates'] = [[]] * df.shape[0]
df['lat'] = [[]] * df.shape[0]
df['lon'] = [[]] * df.shape[0]
df['location_found_from'] = [[]] * df.shape[0]
df['location_match'] = [[]] * df.shape[0]

# Remove NaN values
df = df.fillna('')
df = df.replace(r'\s',' ', regex=True) 

# Column names from which location is searched
location_columns = ['location', 'description', 'reptile']

# Iterating trough dataframe rows
for index, row in df.iterrows():
    location_found = False
    location = str(df.iloc[index]['location'])
    # Uses Natural language processing to find location entities from the location column
    doc = nlp(location)
    for ent in doc.ents:
        if not location_found:
        # If an entity is geographic find it's coordinates from osm with geocoder and add them to data
            if ent.label_ == 'GPE':
                df.at[index, 'location_spacy'] = doc
                osm = geocoder.osm(str(ent))
                df.at[index, 'location_osm'] = osm
                if osm.country is not None:
                    country_osm = geocoder.osm(osm.country)
                    if country_osm.latlng is not None:
                        df.at[index, 'coordinates'] = country_osm.latlng
                        df.at[index, 'Country'] = country_osm.country
                        df.at[index, 'lat'] = float(country_osm.latlng[0])
                        df.at[index, 'lon'] = float(country_osm.latlng[1])
                df.loc[index, 'location_found_from'] = 'location'
                location_found = True
            # if ent.label_ == 'GPE':
            #     df.at[index, 'location_spacy'] = doc
            #     osm = geocoder.osm(str(ent))
            #     df.at[index, 'location_osm'] = osm
            #     if osm.latlng is not None:
            #         df.at[index, 'coordinates'] = osm.latlng
            #         df.at[index, 'country'] = osm.country
            #         df.at[index, 'lat'] = float(osm.latlng[0])
            #         df.at[index, 'lon'] = float(osm.latlng[1])
            #     df.loc[index, 'location_found_from'] = 'location'
            #     df.loc[index, 'location_match'] = str(row['location'])
            #     
  
    # If location is not found search keywords from locationlist matching text in df
    if not location_found:
        for search_column in location_columns:
            if not location_found:
                for col in locationlist.columns:
                    if not location_found:
                        for i, r in locationlist.iterrows():
                            if not location_found:
                                location = re.findall(str(r[col]), str(row[search_column]), re.IGNORECASE)
                                if location != '[]' and str(r[col]) != 'nan' and location:
                                    df.loc[index, 'location_spacy'] = col
                                    osm = geocoder.osm(str(ent))
                                    df.at[index, 'location_osm'] = osm
                                    if osm.country is not None:
                                        country_osm = geocoder.osm(osm.country)
                                        if country_osm.latlng is not None:
                                            df.at[index, 'coordinates'] = country_osm.latlng
                                            df.at[index, 'Country'] = country_osm.country
                                            df.at[index, 'lat'] = float(country_osm.latlng[0])
                                            df.at[index, 'lon'] = float(country_osm.latlng[1])    

                                    df.loc[index, 'location_found_from'] = search_column
                                    df.loc[index, 'location_match'] = str(r[col])
                                    location_found = True
                    

# Drop any data entries that dont have species information (These should not exist anymore at this point)
df['Species'].replace('', float('NaN'), inplace=True)
df.dropna(subset = ['Species'], inplace=True)


#Remove duplicates, where Seller_id, location, quantity, price, currency, intent and species are indentical
df['Seller_id'] = df['Seller_id'].astype(str)
df['location_spacy'] = df['location_spacy'].astype(str)

df_noseller_id = df[df['Seller_id']=='[]']
df_withseller_id = df[df['Seller_id']!='[]']


subset_columns = ['Species', 'Quantity', 'Price', 'Currency', 'Intent', 'Seller_id', 'location_spacy']

non_empty_columns = df_withseller_id[subset_columns].apply(lambda x: sum(item != '[]' for item in x), axis=1)

# Determine how many of the columns has to have data so the deduplication is taken into consideration
# How many empty columns is allowed? Enter here:
empty_columns = 0

# Create a mask to identify rows that match the condition of empty columns allowed
condition = non_empty_columns >= len(subset_columns) - empty_columns

# Perform deduplication only on rows that satisfy the condition
deduplicated_df = df_withseller_id[condition].drop_duplicates(subset=subset_columns)

# Combine the deduplicated rows with the rows that don't meet the condition
df_withseller_id = pd.concat([deduplicated_df, df_withseller_id[~condition]])


# Combine rows with seller id and rest of the roews
df = pd.concat([df_withseller_id, df_noseller_id])

# Drop columns that might have personal information
columns = df[['original_datarow', 'Species', 'Quantity', 'Price', 'Currency', 'Intent', 'Seller_id', 'Country', 'lat', 'lon']]

new_df = columns.copy()
# Saves to file
new_df.to_csv("results.csv")
