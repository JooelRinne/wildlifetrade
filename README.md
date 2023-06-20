# Online wildlife trade data collection and processing tool
Tool for scraping websites trading wildlife species and processing the scraped data.



## 1. Preparation

The data collection from a website is done using web-crawling framework ScraPy. Before using the Wildlife trade data collector, user should familiarise themself with Python, ScraPy and web scraping using CSS-selectors in general. We suggest using virtual environment, such as Conda, to ensure that your project has all the required dependencies and to avoid conflicts between other Python projects. This code was tested using Python version 3.11.3 and ScraPy version 2.9.0 on Windows and Ubuntu.

Steps:
1. Create a new conda virtual environment using a supported Python 3 version. Replace "myenv" with the name of your choice.
   ```ruby
   conda create --name myenv python=3
   ```
2. Activate the environment.
   ```ruby
   conda activate myenv
   ```
3. Copy the code to your personal drive to a location of your choice. Using git:
   ```ruby
   git clone https://github.com/JooelRinne/wildlifetrade.git
   ```
4. Navigate to the "wildlifetrade" folder you just copied.
      ```ruby
   cd wildlifetrade
   ```
5. Install the required dependencies.
   ```ruby
   pip install -r requirements.txt
   ```
   
## 2. Data collection
Steps:
1. Navigate to the "wildlifetrade/Data_collection/scraper/config" directory on your drive.
2. Open the "config.py" file and fill the variables in the file with CSS-selectors, links and other information based on the website you want to scrape. Follow the annotations in the file.
   
   SelectorGadget is a useful tool for determining the right CSS-selectors. It is available as an extension for Google Chrome:
https://chrome.google.com/webstore/detail/selectorgadget/mhjhnkcfbdhnjickkkdbjoemdmbfginb

4. Navigate to the "wildlifetrade/Data_collection" directory in terminal and run the script with
   ```ruby
   scrapy crawl scraper
   ```
5. If everything is set up correctly, the scraped information is stored in a SQLite database saved to the "wildlifetrade/Data_collection" folder.

To be noted:
- You can change the name of the SQLite database and the tables of the database in the "pipelines.py" file. There you can also choose if a new table is created once you run the crawler. At first run this variable has to be True. Note that the database and table names must correspond to the names in the script "Data_processing/matches.py" used in the Data processing phase.
- New website can be scraped by removing the previous websites config file from the "config" folder and replacing it with the config file of the next website.

------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 3. Data processing

The data processing finds matches from the scraped data to the keywords listed in the file "Data_processing/keywords.csv". Then it extracts information from the matching data entries.

Steps:
1. Download spacy language model by running the command below in your terminal. Note that spacy must be installed before loading the model. 
   ```ruby
   python -m spacy download en_core_web_sm
   ```
2. Navigate to the "wildlifetrade/Data_processing" folder.
3. Insert your SQLite database of scraped data entries from the "wildlifetrade/Data_collection" folder to the "wildlifetrade/Data_processing" folde.
4. The .csv files in the folder can be modified depending on the wildlife studied .
  - "keywords.csv" consists of all keywords which are searched from the scraped data. Make sure you allocate the keywords to a species in the "reptilesynonyms.csv" file. 
  - "reptilesynonyms.csv" consists of synonyms of each species studied. First column indicates the scientific name of the species and rest of the columns are synonyms for the species. Make sure that the keywords in the "keywords.csv" file are allocated to a species in this file. 
  - "seller_or_buyer.csv" consists of synonyms of keywords indicating intent of the trade. Synonyms can be added under each column and new columns can be added.
  - "currency_symbols.csv" consists of symbols of currencies and their corresponding abbreviations.
  - "locationlist.csv" is an empty file which can be used to manually list locations under country names, if the geocoder used in the script does not find a location automatically. The first row should consist of the country names and the locations should be listed under the responding country.
    
5. Before runnning the processing algorithms, make sure that the names of your database and the table where your data is located are the same in Data_processing/matches.py file as the database and table names you used for storing the data in the Data_collection/pipelines.py file.  
    
6. Run the all processing algorithms from the masterscript.
   ```ruby
   python processor.py
   ```
   OR<br>
   
   Run each script separately. The script must be run in the right order, because the result of the    previous script is used in the following script:
   ```ruby
   python matches.py
   python species.py
   python trader_information.py
   python locations.py
   ``` 
7. The results are saved into "results.csv" file.
------------------------------------------------------------------------------------------------------------------------------------------------------------------

## 4. Accuracy assessment

The accuracy of the data procssing is assessed with two scripts "filteringaccuracy.py" and "processingaccuracy".

### 1. Filtering accuracy

"filteringaccuracy.py" creates accuracy assessment reports of the filterin phase done in the "matches.py" script of the data processing phase. 

Steps
1. Navigate to the wildlifetrade/Accuracy_assessment" folder.
2. Insert your SQLite database containing the scraped data entries to the "wildlifetrade/Accuracy_assessment" folder which contains the "filteringaccuracy.py" script.
3. Edit the "filteringaccuracy.py" script and make sure that
   - The variable "data_selection" is set as True.
   - The variable "accuracy_assessment" is set as False.
   - The variable "db" corresponds to the name of your SQLite database.
   - The variable "tb" corresponds to the name of your SQLite database table name.
     
4. Select the sample size of your assessement data (number of data entries) by setting the "sample_size" variable (for example 100).
5. Run the "filteringaccuracy.py" script. Six .csv files are created, two of each website type. The files have as many randomly selected data entries from the database as defined by the "sample_size" variable.
   ```ruby
   python filteringaccuracy.py
   ```
6. Review the .csv files manually. Insert new column "filtered" to the files and mark the entries that should be filtered (include species you are searching) with "y" and the entries that should be filtered with "n" as done in the example .csv file  "forum_revieweddata.csv".  
7. Name the reviewed .csv files same way as they are refered in the "filteringaccuracy.py" script.
8. Edit the "filteringaccuracy.py" script again and make sure that this time the variable "data_selection" is False and "accuracy_assessment" is True.
9. The script produces accuracy_assessment reports including accuracies and omission and commission errors for each six reviewed data sets.

-----

### 2. Processing accuracy

"processingaccuracy.py" creates accuracy assessment reports of the rest of the processing phase done by the rest of the scripts. 

Steps
1. Navigate to the wildlifetrade/Accuracy_assessment" folder.
2. Make sure that the resulting .csv file from the "matches.py" script, namely the "matches.csv" is in the same folder as the "processingaccuracy.py" script.
3. Edit the "processingaccuracy.py" script and make sure that the variable "data_selection" is True and "accuracy_assessment" is False.
4. Select the sample size of your assessement data (number of data entries) by setting the "sample_size" variable (for example 100).
5. Run the "processingaccuracy.py" script. Two .csv files are created, validation and test data sets. The files have as many randomly selected data entries from the database as defined by the "sample_size" variable.
6. Review the .csv files manually. Review the generated .csv files manually by determining the right data fields (Species_r, Quantity_r, Price_r, Currency_r, Location_r and Intent_r) as done in the example .csv file "processing_validationdata_reviewed". Leave the field empty if the information is not found from the data entry. If the whole data entry should not be included write "NO" to each of the reviewed columns "ending with _r".
7. Name the reviewed .csv files same way as they are refered in the "processingaccuracy.py" script.
8. Edit the "processingaccuracy.py" script again and make sure that this time the variable "data_selection" is False and "accuracy_assessment" is True.
9. The script produces accuracy_assessment reports including accuracies of each data field reviewed. 


