# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyscrapperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    company_website = scrapy.Field()
    company_email = scrapy.Field()
    company_contact = scrapy.Field()