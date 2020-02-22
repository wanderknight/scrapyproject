# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DyttspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 列表页
    title = scrapy.Field()
    # 详情页
    url = scrapy.Field()
    magnet_link = scrapy.Field()
    ftp_link = scrapy.Field()
