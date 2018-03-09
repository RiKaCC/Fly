# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class LianjiaItem(scrapy.Item):
    url  = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()

class ErshoufangSpider(scrapy.Spider):
    name = 'Ershoufang'
    allowed_domains = ['bj.lianjia.com/ershoufang']
    start_urls = ['https://bj.lianjia.com/ershoufang//']
    #rules = [Rule(LinkExtractor(allow=['/tor/\d+']), 'parse')]

    def parse(self, response):
        torrent = LianjiaItem()
        torrent['url'] = response.url
        torrent['name'] = response.xpath("//div[@class='title']/a/text()").extract()
        torrent['price'] = response.xpath("//div[@class='totalPrice']/span/text()").extract()
        ret = {}
        for i, val in enumerate(torrent['name']):
            ret[val] = torrent['price'][i]
        print(ret)
        return torrent
