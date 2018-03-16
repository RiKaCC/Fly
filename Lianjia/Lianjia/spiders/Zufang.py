# -*- coding: utf-8 -*-
import scrapy
import pymysql
import time
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

def generate_all(user_in_nub):
    url = 'https://bj.lianjia.com/ditiezufang/{}/'
    urlArr = []
    for i in range (len(user_in_nub)):
        urlArr.append(url.format(user_in_nub[i]))
    return urlArr


class LianjiaItem(scrapy.Item):
    url         = scrapy.Field()
    name        = scrapy.Field()
    


class ZufangSpider(scrapy.Spider):
    name = 'Zufang'
    allowed_domains = ['bj.lianjia.com/ditiezufang']
    subway = ['li647','li648','li656','li649','li46107350','li46537785','li659','li43145267','li651','li652','li46461179','li1110790465974155','li43143633','li1116796246117001','li653','li43144847','li43144993','li43145111']
    start_urls = generate_all(subway)

    def parse(self, response):
        db = pymysql.connect(host='localhost',
                             user='root',
                             passwd='public',
                             db='Lianjia',
                             charset="utf8")
        cursor = db.cursor()
        torrent = LianjiaItem()
        torrent['url']         = response.url
        torrent['name']        = response.xpath("//div[@class='info-panel']/h2/a/text()").extract()




        return torrent
