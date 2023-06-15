# Online wildlife trade data collection and processing tool
Tool for scraping websites trading wildlife species and processing the scraped data.

## 1. Data collection

The data collection from a website is done using web-crawling framework ScraPy version 2.4.1. Before using the Wildlife trade data collector user should familiarise themself with Python annd ScraPy and web scraping using CSS-selectors in general. We suggest using virtual environment, such as Conda, to ensure that your project has all the required dependencies and to avoid conflicts between other Python projects.

Steps
1. Start a new virtual environment, using a Python version 3.6 or higher
   Conda:
   ```
   conda create env --name myenv python=3.6
   ```
3. Follow the installation and set up insctuctions 
4. After the ScraPy framework is set up, replace the spider Python file in "spiders" folder with the "scraper.py" Python file in "Data collection/spiders"
5. Replace files "items.py", "middlewares.py", "pipelines,py" and "settings.py" in your ScraPy framework's "scraper" folder with the same files from "Data collection"
6. Add a folder named "config" to your Scrapy framework's "scraper" folder
7. Add "config.py" file from "Data collection" to your Scrapy framework's newely generated "scraper/config" folder
8. Fill the "config.py" file with CSS-selectors, links and other information based on the website you want to scrape
9. Run the scraper in terminal with "scrapy crawl scraper.py" command
10. If everything is set up correctly, the scraped information is stored in a SQLite database saved to your ScraPy Framework folder
11. A new website can be scraped by removing the previous websites config file from the "config" folder and replacing it wit the config file of the next website

------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 2. Data processing

The data processing filters data enries from a data set that include keywords listed in a seperate file. Then it extracts information from the selected data entries

Steps
1. Download the "Data processing" folder to your environment
2. Insert your SQLite database of scraped data entries to the "Data processing" folder
3. The .csv files in the folder can be modified depending on the wildlife studied 
  - "keywords.csv" consists of all keywords which are searched from the scraped data. Data entries including the keywords are filtereded to be processed               further.
  - "reptilesynonyms.csv" consists of synonyms of each species studied. First column indicates the scientific name of the species and rest of the columns are         synonyms for the species.
  - "seller_or_buyer.csv" consists of synonyms fo keywords indicating intent of the trade. Synonyms can be added under each column and new columns can be             added.
  - "currency_symbols.csv" consists of symbolsof currencies and their corresponding abbreviations.
  - "locationlist.csv" consists of columns of country names. Under each country name are names of locations that are located in that country.
4. Run the all processing algorithms from the masterscript "processor.py" or
5. Run each script separately. The scripts have to be run in order descripted in the "Flowchart.png" file.

------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 3. Accuracy assessment

The accuracy of the data procssing is assessed with two scripts "filteringaccuracy.py" and "processingaccuracy".

1. Filtering accuracy

"filteringaccuracy.py" creates accuracy assessment reports of the filterin phase done in the "matches.py" script of the data processing phase. 

Steps
1. Insert your SQLite database of scraped data entries to the same folder as the "filteringaccuracy.py" script
2. Edit the "filteringaccuracy.py" script and make sure that the variable "data_selection" is True and "accuracy_assessment" is False.
3. Select the sample size of your assessement data (number of data entries) by setting the "sample_size" variable to for example 100
4. Run the "filteringaccuracy.py" script. Six .csv files are created, two of each website type. The files have as many randomly selected data entries from the database as defined by the "sample_size" variable.
5. Review the .csv files manually. Insert new column "filtered" to the files and mark the entries that should be filtered (include species you are searching) with "y" and the entries that should be filtered with "n" as done in the example .csv file  "forum_revieweddata.csv".  
6. Name the reviewed .csv files same way as they are refered in the "filteringaccuracy.py" script
7. Edit the "filteringaccuracy.py" script again and make sure that this time the variable "data_selection" is False and "accuracy_assessment" is True.
8. The script produces accuracy_assessment reports including accuracies and omission and commission errors for each six reviewed data sets.

-----

2. Processing accuracy

"processingaccuracy.py" creates accuracy assessment reports of the rest of the processing phase done by the rest of the scripts. 

Steps
1. Make sure that the resulting .csv file from the "matches.py" script, namely the "matches.csv" is in the same folder as the "processingaccuracy.py" script
2. Edit the "processingaccuracy.py" script and make sure that the variable "data_selection" is True and "accuracy_assessment" is False.
3. Select the sample size of your assessement data (number of data entries) by setting the "sample_size" variable to for example 100
4. Run the "processingaccuracy.py" script. Two .csv files are created, validation and test data sets. The files have as many randomly selected data entries from the database as defined by the "sample_size" variable.
5. Review the .csv files manually. Review the generated .csv files manually by determining the right data fields (Species_r, Quantity_r, Price_r, Currency_r, Location_r and Intent_r) as done in the example .csv file "processing_validationdata_reviewed". Leave the field empty if the information is not found from the data entry. If the whole data entry should not be included write "NO" to each of the reviewed columns "ending with _r"
6. Name the reviewed .csv files same way as they are refered in the "processingaccuracy.py" script
7. Edit the "processingaccuracy.py" script again and make sure that this time the variable "data_selection" is False and "accuracy_assessment" is True.
8. The script produces accuracy_assessment reports including accuracies of each data field reviewed. 


