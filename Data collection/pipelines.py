# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class ScraperPipeline(object):
    test = False
    db = "reptilesales.db"

    if test:
        tb = "test_tb"
        new_table = True   
    else:
        tb = "reptiles_tb"
        new_table = False

    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = sqlite3.connect(ScraperPipeline.db)
        self.curr = self.conn.cursor()

    def create_table(self):
        if ScraperPipeline.new_table:
            self.curr.execute("""DROP TABLE IF EXISTS """ + ScraperPipeline.tb + """""")
            self.curr.execute("""create table """ + ScraperPipeline.tb + """(
                            acquired text,
                            source text,
                            timestamp text,
                            reptile text,
                            price text,
                            quantity text,
                            description text,
                            comments text,
                            location text,
                            other text,
                            image text,
                            seller text,
                            commenter text,
                            intent text,
                            website_type text
                            )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into """ + ScraperPipeline.tb + """ values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",(
            item['acquired'][0],
            item['source'][0],
            item['timestamp'][0],
            item['reptile'][0],
            item['price'][0],
            item['quantity'][0],
            item['description'][0],
            item['comments'][0],
            item['location'][0],
            item['other'][0],
            item['image'][0],
            item['seller'][0],
            item['commenter'][0],
            item['intent'][0],
            item['website_type'][0]                        
        ))

        self.conn.commit()