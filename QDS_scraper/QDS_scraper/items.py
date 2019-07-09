# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QdsScraperItem(scrapy.Item):
    player = scrapy.Field()
    minutes = scrapy.Field()
    points = scrapy.Field()
    rebounds = scrapy.Field()
    assists = scrapy.Field()
    steals = scrapy.Field()
    blocks = scrapy.Field()
    turnovers = scrapy.Field()
