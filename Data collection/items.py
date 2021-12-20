# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    acquired = scrapy.Field()
    timestamp = scrapy.Field()
    source = scrapy.Field()
    reptile = scrapy.Field()
    price = scrapy.Field()
    quantity = scrapy.Field()
    location = scrapy.Field()
    other = scrapy.Field()
    description = scrapy.Field()
    comments = scrapy.Field()
    image = scrapy.Field()
    seller = scrapy.Field()
    commenter = scrapy.Field()
    intent = scrapy.Field()
    website_type = scrapy.Field()              
    pass
