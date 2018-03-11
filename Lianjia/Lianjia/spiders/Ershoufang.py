# -*- coding: utf-8 -*-
import scrapy
import pymysql
import time
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class LianjiaItem(scrapy.Item):
    url  = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    follow = scrapy.Field()
    watch  = scrapy.Field()
    houseid = scrapy.Field()

class ErshoufangSpider(scrapy.Spider):
    name = 'Ershoufang'
    allowed_domains = ['bj.lianjia.com/ershoufang']
    start_urls = ['https://bj.lianjia.com/ershoufang//']
    #rules = [Rule(LinkExtractor(allow=['/tor/\d+']), 'parse')]


    def parse(self, response):
        db = pymysql.connect(host='localhost',
                             user='root',
                             passwd='public',
                             db='Lianjia',
                             charset="utf8")
        cursor = db.cursor()
        torrent = LianjiaItem()
        torrent['url']    = response.url
        torrent['name']   = response.xpath("//div[@class='title']/a/text()").extract()
        torrent['price']  = response.xpath("//div[@class='totalPrice']/span/text()").extract()
        torrent['follow'] = response.xpath("//div[@class='followInfo']/text() [1]").extract()
        torrent['watch']  = response.xpath("//div[@class='followInfo']/text() [2]").extract()
        torrent['houseid'] = response.xpath("//div[@class='unitPrice']/@data-hid").extract()
        print(torrent['houseid'])
        now = int(time.time())
        ret = {}
        for i, val in enumerate(torrent['name']):
            ret[val] = torrent['price'][i]
            
            sql = "INSERT INTO ErshoufangBasic(houseid,name,price,follow,watch,querytime) VALUES(%s,%s,%s,%s,%s,%s) on duplicate key update name=%s,price=%s,follow=%s,watch=%s, querytime=%s"#name=`torrent['name'][i]`,price=`torrent['price'][i]`,follow=`torrent['follow'][i]`,watch=`torrent['watch'][i]`,querytime=`now`"
            follow = getNum(torrent['follow'][i])
            watch = getNum(torrent['watch'][i])
            print(sql)
            print(torrent['houseid'][i], val, torrent['price'][i], torrent['follow'][i], torrent['watch'][i], now)
            cursor.execute(sql,(torrent['houseid'][i], val, torrent['price'][i], follow, torrent['watch'][i], now, val,torrent['price'][i],follow,watch, now))
            #cursor.execute(sql)
           #print(ret)
        return torrent

def getNum(strs):
    print(re.sub("\D", "", strs))
    return re.sub("\D", "", strs)


