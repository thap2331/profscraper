# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader

class ProfscraperItem(scrapy.Item):
    name = scrapy.Field()
    department = scrapy.Field()
    scraped_date = scrapy.Field()
    google_scholar = scrapy.Field()
    link = scrapy.Field()
    html_profile = scrapy.Field()

class DepartmentItem(scrapy.Item):
    name = scrapy.Field()
    department = scrapy.Field()
    scraped_date = scrapy.Field()
    link = scrapy.Field()
