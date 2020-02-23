__author__ = 'wanderknight'
__time__ = '2020/2/20 12:23'

from scrapy.cmdline import execute

# execute(["scrapy", "crawl", "douban", "-o", "tags.csv"])
execute(["scrapy", "crawl", "douban"])
