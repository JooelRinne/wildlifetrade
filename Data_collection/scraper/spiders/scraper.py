# import necessary libraries 
import scrapy
import os
import importlib.util
from ..items import ScraperItem
from datetime import date

# Spider class
class ScraperSpider(scrapy.Spider):
    name = 'scraper'
    # Reads the config files from the folder path. Insert path to folder where config.py is located
    config_path = os.path.abspath('../Data_collection/scraper/config/')
    config = os.listdir(config_path)
    config.remove('__pycache__')
    config.remove('__init__.py')
    # Reads the config file and imports all variables from it
    path_name = os.path.join(config_path, config[0])

    spec = importlib.util.spec_from_file_location('Config', path_name)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)        
    pages, category_card, category_card_2, inner_page_href, item_card, first_page_fields, inner_page_fields, type_in_fields, next_page_href, starting_page, last_page, paging_interval, paging_string_1, paging_string_2 = foo.Config().config()
    start_urls = pages
    page = starting_page

    # Connects to the webpage
    def parse(self, response):
        inner_page_hrefs = ScraperSpider.inner_page_href
        # If the webpage has inner levels to be scraped: 
        if len(inner_page_hrefs) > 0:
            page_no = 1
            # Creates variable names for all the inner page links
            for page in inner_page_hrefs:
                globals()["inner_page_href_" + str(page_no)] = page
                page_no += 1

        # If the webpage has one or less inner levels to be scraped and no categories:
        if len(inner_page_hrefs) <= 1 and ScraperSpider.category_card is None:
            # Yields the request to inner level function
            yield response.follow(response.request.url, callback=self.parse_first_level)
        # If more than one inner levels need to be scraped:
        else:
            # Finds the link to each category with CSS selector
            category_card = ScraperSpider.category_card
            category = response.css(category_card)
            # If two inner levels need to be scraped
            if len(inner_page_hrefs) <= 2: 
                for link in category:
                    # Reads the first level link
                    inner_page = link.css(inner_page_href_1).get()
                    # Yields the request to first level function
                    yield response.follow(inner_page, callback=self.parse_first_level)
            # If more than two inner levels need to be scraped
            else:
                for link in category:
                    # Reads the first level link
                    inner_page = link.css(inner_page_href_1).get()
                    # Yields the request to category level function
                    yield response.follow(inner_page, callback=self.parse_category)

    # This function is needed if there are more than two levels of links to be followed             
    def parse_category(self, response):
            # Read the second category
            category_card_2 = ScraperSpider.category_card_2
            category = response.css(category_card_2)
            for link in category:
                # Get the category address with CSS selector
                inner_page = link.css(inner_page_href_2).get()
                # Yeild to inner level function
                yield response.follow(inner_page, callback=self.parse_first_level)

    # Inner level scraper function. 
    # This is the level on the website where items for sales are listed.
    # Some of the information scraped might be found from this level, some from deeper level
    # behind a link.        
    def parse_first_level(self, response):
        # Read the item card CSS selector
        item_card = ScraperSpider.item_card
        # Reads the address to next page. Used if paging is needed-
        next_page_href = ScraperSpider.next_page_href
        # List of the addressess of the sales ite# if __name__ == '__main__':
#     process = CrawlerProcess()
#     process.crawl(ScraperSpider)
#     process.start()ms on the page
        items_for_sale = response.css(item_card)

        # Iterates trough the items for sale on the page
        for item in items_for_sale:
            # Reads which data fields are scraped from this level
            first_page_fields = ScraperSpider.first_page_fields.copy()
            # Reads the CSS selectors for fields that are scraped from this level
            for key in first_page_fields:
                # Scrapes information on fields that are scraped from this level
                if first_page_fields[key] is not None:
                    first_page_fields[key] = [''.join(item.css(first_page_fields[key]).extract())]
            
            # Reads the link to the page on which the specific information of the sales link is located
            # The variable name depends on the number of the levels already followed.
            if len(ScraperSpider.inner_page_href) == 1 and ScraperSpider.category_card is None:
                    inner_page = item.css(inner_page_href_1).get()
            elif len(ScraperSpider.inner_page_href) == 2:                    
                    inner_page = item.css(inner_page_href_2).get()
            elif len(ScraperSpider.inner_page_href) == 3:
                    inner_page = item.css(inner_page_href_3).get()                    
            # If no inner page links are provieded
            # Scrapes information from this level if no inner level information is needed to be scraped
            else:
                inner_page = None
                items = ScraperItem()
                items['acquired'] = [str(date.today())]
                items['source'] = [response.request.url]
                for key in first_page_fields:
                    if first_page_fields[key] is not None:
                        items[key] = first_page_fields[key]
                    else:
                        items[key] = ['']
                type_in_fields = ScraperSpider.type_in_fields.copy()
                for key in type_in_fields:
                    if type_in_fields[key] is not None:
                        items[key] = type_in_fields[key]       
                yield items

            # If there is an inner level to be scraped (for example specific information behind a link in a sales item card)
            if inner_page is not None:
                # Yields to lowest level scraper
                yield response.follow(inner_page, meta=first_page_fields, callback=self.parse_items)

        # If more than one page of sales items is listed = paging is needed
        # If Next page link available:
        if next_page_href is not None:
            next_page = response.css(next_page_href).get()
        # if not:
        else:
            next_page = None

        # If next page link available follows the link and beings the scraper process again
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_first_level)
        
        # if next page link is not available but paging is needed the next page link is solved with following script
        if next_page_href is 'paging':            
            if ScraperSpider.page == ScraperSpider.starting_page:
                next_page = response.request.url + ScraperSpider.paging_string_1 + str(ScraperSpider.page) + ScraperSpider.paging_string_2
            else:
                index = response.request.url.find(ScraperSpider.paging_string_1) 
                current_page = response.request.url[:index]
                next_page = current_page + ScraperSpider.paging_string_1 + str(ScraperSpider.page) + ScraperSpider.paging_string_2
                
            if ScraperSpider.page <= ScraperSpider.last_page:
                try:
                    ScraperSpider.page += ScraperSpider.paging_interval
                    yield response.follow(next_page, callback = self.parse_first_level)
                except:
                    ScraperSpider.page = 2
                    pass
            else:
                ScraperSpider.page = 2



    # Function to scrape information form the lowest level and parse all scraped infromation together into a scraped data entity
    def parse_items(self, response):
        # Creates a scraper item (used to parse all scpared information into a data entry)
        items = ScraperItem()
        # Copies the lists of css selectors of different data fields
        inner_page_fields = ScraperSpider.inner_page_fields.copy()
        type_in_fields = ScraperSpider.type_in_fields.copy()

        # Inserts automatically filled fields of the data entry
        items['acquired'] = [str(date.today())]
        items['source'] = [response.request.url]

        # Deletes fields that are unwanted
        meta = response.meta        
        del meta['depth']
        del meta['download_timeout']
        del meta['download_slot']
        del meta['download_latency']

        # Copies information scraped from upper levels (first_level_fields) to the scraper item
        for key in meta:
            if meta[key] is not None:
                items[key] = meta[key]
            else: 
                items[key] = ['']
        for key in meta:
            if meta[key] is not None:
                items[key] = meta[key]
            else: 
                items[key] = ['']
        # Scrapes information on lowest level and adds them to scraper item
        for key in inner_page_fields:
            if inner_page_fields[key] is not None:
                items[key] = [''.join(response.css(inner_page_fields[key]).extract())]                        
        
        # Inserts user typed data fields to the scraper item
        for key in type_in_fields:
            if type_in_fields[key] is not None:
                items[key] = type_in_fields[key]

        # Yields the scraper item to pipeline to be saved to a database
        yield items
