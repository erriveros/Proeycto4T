# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UandesscraperItem(scrapy.Item):
    # define the fields for your item here like:
    news = scrapy.Field()
    href = scrapy.Field()
    course = scrapy.Field()
    pass
