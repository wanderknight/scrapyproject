# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class crawledItem(scrapy.Item):
    """爬取下来的网页信息，没有重复网址，重复网址会被redis过滤掉"""
    url = scrapy.Field()
    refere = scrapy.Field()
    status = scrapy.Field()
    title = scrapy.Field()


class requestItem(scrapy.Item):
    """在解析网页时，请求的网页信息，可能包含大量重复的网址"""
    url = scrapy.Field()
    refere = scrapy.Field()
