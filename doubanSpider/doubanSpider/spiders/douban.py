# -*- coding: utf-8 -*-
import scrapy
import time
from urllib import parse
from doubanSpider.items import DoubanspiderItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['www.douban.com',
                       'book.douban.com']  # 解决 Filtered offsite request to 错误
    start_urls = ['https://book.douban.com/tag/', ]

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
        filename = self._url2filename(parse.unquote(response.url))
        with open(filename, 'wb') as file_object:
            file_object.write(response.body)

        item = DoubanspiderItem()
        item['url'] = parse.unquote(response.url)
        if response.meta.get('refere'):
            item['refere'] = parse.unquote(response.meta['refere'])
        else:
            item['refere'] = ''
        item['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        item['status'] = response.status
        item['title'] = response.xpath('//title/text()')[0].extract().strip()

        yield item

        tag_urls = response.xpath('//a[contains(@href,"/tag/")]/@href').extract()
        i = 0
        for url in tag_urls:
            if not 'https://book.douban.com' in url:
                url = 'https://book.douban.com' + url
            yield scrapy.Request(url=url, meta={'refere': response.url}, callback=self.parse)
            i = i+1
            if i > 2:
                break
