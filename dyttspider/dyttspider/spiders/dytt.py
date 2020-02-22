# -*- coding: utf-8 -*-
import scrapy
from dyttspider.items import DyttspiderItem


class DyttSpider(scrapy.Spider):
    name = 'dytt'
    allowed_domains = ['www.ygdy8.net']
    start_urls = ['https://www.ygdy8.net/html/gndy/dyzz/list_23_1.html']
    count = 0

    def parse(self, response):
        items = []

        title = response.xpath('//div[@class="co_content8"]/ul//td//a/text()').extract()
        url = response.xpath('//div[@class="co_content8"]/ul//td//a/@href').extract()

        for i in range(0, len(title)):
            item = DyttspiderItem()
            item['title'] = title[i]
            item['url'] = 'https://www.ygdy8.net/' + url[i]
            items.append(item)

        for item in items:
            yield scrapy.Request(url=item['url'], meta={'meta': item}, callback=self.parse_download_link)

        if self.count < 2:
            next_url = 'https://www.ygdy8.net/html/gndy/dyzz/' + \
                       response.xpath("//a[contains(text(),'下一页')]/@href").extract()[0]
            yield response.follow(next_url, callback=self.parse)

        self.count = self.count + 1

    def parse_download_link(self, response):
        item = response.meta['meta']
        magnet_link = response.xpath('//a[contains(@href,"magnet")]/@href')[0].extract()
        ftp_link = response.xpath('//a[contains(@href,"ftp")]/@href')[0].extract()

        if len(magnet_link) is not None:
            item['magnet_link'] = magnet_link
        else:
            item['magnet_link'] = ''

        if len(ftp_link) is not None:
            item['ftp_link'] = ftp_link
        else:
            item['ftp_link'] = ''
        yield item
