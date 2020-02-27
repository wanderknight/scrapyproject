# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import logging
from scrapy_redis.spiders import RedisSpider
import os
import datetime
from doubanSpider.items import crawledItem
from doubanSpider.items import requestItem


class DoubanSpider(RedisSpider):
    name = 'douban'
    allowed_domains = ['www.douban.com',
                       'book.douban.com']  # 解决 Filtered offsite request to 错误
    # start_urls = ['https://book.douban.com/tag/', ]

    # 'https://book.douban.com/tag/%E7%BB%8F%E5%85%B8',
    # 'https://www.douban.com/doulist/481692/'
    tag_filter_list = []

    def __init__(self, category=None, *args, **kwargs):
        super(DoubanSpider, self).__init__(*args, **kwargs)
        self._tag_filter()

    def _tag_filter(self):
        with open('E:\douban_spider_data\豆瓣 tag 大类 去重.csv') as tag_filter_file:
            for line in tag_filter_file.readlines():
                if not 'https://book.douban.com' in line:
                    url = 'https://book.douban.com' + line.strip()
                else:
                    url = line.strip()
                self.tag_filter_list.append(url)

    def _url2filename(self, url):
        """
        WINDOWS系统中，文件名不能包含下列任何字符
        https://blog.csdn.net/cpdoor2163_com/article/details/81094988
        为了便于文件保存，修改url为文件名，当中
        ':'-->'['
        '/'-->']'
        '?'-->'？'
        url:传入的网址
        :filename:
        """
        filename = url.replace(':', '[').replace('/', ']').replace('?', '？')
        return filename

    def parse(self, response):
        logging.debug('test')
        filename = self._url2filename(parse.unquote(response.url))
        now = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        filename = filename + '_' + now + '.html'
        filename = os.path.join('E:\douban_spider_data\html\\', filename)
        with open(filename, 'wb') as file_object:
            file_object.write(response.body)

        item_crawled = crawledItem()
        item_crawled['url'] = parse.unquote(response.url)
        if response.meta.get('refere'):
            item_crawled['refere'] = parse.unquote(response.meta['refere'])
        else:
            item_crawled['refere'] = ''
        item_crawled['status'] = response.status
        item_crawled['title'] = response.xpath('//title/text()')[0].extract().strip()

        yield item_crawled

        tag_urls = response.xpath('//a[contains(@href,"/tag/")]/@href').extract()

        items = []
        for url in tag_urls:
            if not 'https://book.douban.com' in url:
                url = 'https://book.douban.com' + url
            if url in self.tag_filter_list:
                continue
            yield scrapy.Request(url=url, meta={'refere': response.url}, callback=self.parse)

            item_request = requestItem()
            item_request['url'] = parse.unquote(url)
            item_request['refere'] = parse.unquote(response.url)
            items.append(item_request)

        for it in items:
            yield it
