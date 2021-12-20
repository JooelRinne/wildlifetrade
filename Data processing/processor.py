#!/usr/bin/env python3

# Choose which scripts to run:
# Previous script has to be have run before next script can be run
find_matches = True
find_species = True
find_trader_information = True
find_locations = True

# Filters matches from the raw data of scraped data entries
if find_matches:
    print('Processing: matches.py')
    import matches

# Finds and names the species from the filtered data
if find_species:
    print('Processing: species.py')
    import species

# Finds information on quantities, prices, currency and trader intent from the filtered data 
if find_trader_information:
    print('Processing: quantities_prices.py')
    import trader_information

# Finds the location of the data entry
if find_locations:    
    print('Processing: locations.py')
    import locations