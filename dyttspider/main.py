__author__ = 'wanderknight'
__time__ = '2020/2/20 12:23'
"""
主要参考：https://blog.csdn.net/weixin_40958757/article/details/79713359
"""

from scrapy.cmdline import execute

# execute(["scrapy", "crawl", "dytt", "-o", "items.csv"]) 设置了个人的csvpipeline后，会报错。
execute(["scrapy", "crawl", "dytt", "-s", "JOBDIR=crawls/somespider-1"])
