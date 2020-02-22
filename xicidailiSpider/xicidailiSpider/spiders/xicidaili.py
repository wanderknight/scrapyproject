# -*- coding: utf-8 -*-
import scrapy


class XicidailiSpider(scrapy.Spider):
    name = 'xicidaili'
    allowed_domains = ['xicidaili.com']
    start_urls = ['https://www.xicidaili.com/nn/']

    def parse(self, response):
        selectors = response.xpath('//tr')
        for select in selectors:
            ip = select.xpath('./td[2]/text()').extract_first()
            port = select.xpath('./td[3]/text()').extract_first()
            items = {
                'ip': ip,
                'port': port
            }
            yield items

        next_page = response.xpath('//a[@class="next_page"]/@href').extract_first()
        if next_page:
            next_url = response.urljoin(next_page)
            yield scrapy.Request(next_url, callback=self.parse)
