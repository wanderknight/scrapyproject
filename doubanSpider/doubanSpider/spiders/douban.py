# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import logging
from scrapy_redis.spiders import RedisSpider

from doubanSpider.items import crawledItem
from doubanSpider.items import requestItem

class DoubanSpider(RedisSpider):
    name = 'douban'
    allowed_domains = ['www.douban.com',
                       'book.douban.com']  # 解决 Filtered offsite request to 错误
    # start_urls = ['https://book.douban.com/tag/', ]

    # 'https://book.douban.com/tag/%E7%BB%8F%E5%85%B8',
    # 'https://www.douban.com/doulist/481692/'
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
        filename = url.replace(':', '[').replace('/', ']').replace('?', '？') + '.html'
        return filename

    def parse(self, response):
        logging.debug('test')
        filename = self._url2filename(parse.unquote(response.url))
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
        i = 0
        items = []
        for url in tag_urls:
            if not 'https://book.douban.com' in url:
                url = 'https://book.douban.com' + url
            yield scrapy.Request(url=url, meta={'refere': response.url}, callback=self.parse)

            item_request = requestItem()
            item_request['url'] = parse.unquote(url)
            item_request['refere'] = parse.unquote(response.url)
            items.append(item_request)

            i = i + 1
            if i > 1:
                break

        for it in items:
            yield it

