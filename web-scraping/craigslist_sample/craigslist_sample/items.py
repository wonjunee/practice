# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Defining Items
# Items are containers with loaded scraped data.
# Similar to Python Dicts
class CraigslistSampleItem(scrapy.Item):
	title = scrapy.Field()
	link = scrapy.Field()
