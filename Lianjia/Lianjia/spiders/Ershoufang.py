# -*- coding: utf-8 -*-
import scrapy
import pymysql
import time
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

def generate_all(user_in_nub):
      url = 'https://bj.lianjia.com/ershoufang/pg{}/'
      urlArr = []
      for i in range(1, int(user_in_nub)):
          urlArr.append(url.format(i))
      return urlArr

class LianjiaItem(scrapy.Item):
    url         = scrapy.Field()
    total_price = scrapy.Field()
    follow      = scrapy.Field()
    watch       = scrapy.Field()
    houseid     = scrapy.Field()
    region      = scrapy.Field()
    house_type  = scrapy.Field()
    area        = scrapy.Field()
    orientation = scrapy.Field()
    design      = scrapy.Field()
    unit_price  = scrapy.Field()
    name        = scrapy.Field()

class ErshoufangSpider(scrapy.Spider):
    name = 'Ershoufang'
    allowed_domains = ['bj.lianjia.com/ershoufang']
    #start_urls = ['https://bj.lianjia.com/ershoufang//']
    start_urls = generate_all(101)
    #rules = [Rule(LinkExtractor(allow=['/tor/\d+']), 'parse')]


    def parse(self, response):
        db = pymysql.connect(host='localhost',
                             user='root',
                             passwd='public',
                             db='Lianjia',
                             charset="utf8")
        cursor = db.cursor()
        torrent = LianjiaItem()
        torrent['url']         = response.url
        torrent['name']        = response.xpath("//div[@class='title']/a/text()").extract()
        torrent['total_price'] = response.xpath("//div[@class='totalPrice']/span/text()").extract()
        torrent['follow']      = response.xpath("//div[@class='followInfo']/text() [1]").extract()
        torrent['watch']       = response.xpath("//div[@class='followInfo']/text() [2]").extract()
        torrent['houseid']     = response.xpath("//div[@class='unitPrice']/@data-hid").extract()
        torrent['region']      = response.xpath("//div[@class='houseInfo']/a/text()").extract()
        torrent['house_type']  = response.xpath("//div[@class='houseInfo']/text() [1]").extract()
        torrent['area']        = response.xpath("//div[@class='houseInfo']/text() [2]").extract()
        torrent['orientation'] = response.xpath("//div[@class='houseInfo']/text() [3]").extract()
        torrent['design']      = response.xpath("//div[@class='houseInfo']/text() [4]").extract()
        torrent['unit_price']  = response.xpath("//div[@class='unitPrice']/span/text()").extract()
        now = int(time.time())
        ret = {}
        for i, val in enumerate(torrent['name']):
            ret[val] = torrent['name'][i]
            sql = "INSERT INTO ErshoufangBasic(houseid,total_price,follow,watch,region,house_type,area,orientation,design,unit_price,querytime) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update \
                   total_price=%s,unit_price=%s,follow=%s,watch=%s, querytime=%s"#name=`torrent['name'][i]`,price=`torrent['price'][i]`,follow=`torrent['follow'][i]`,watch=`torrent['watch'][i]`,querytime=`now`"
            follow = getNum(torrent['follow'][i])
            watch = getNum(torrent['watch'][i])
            unit_price = getNum(torrent['unit_price'][i])
            print(sql)
            print(torrent['houseid'][i], torrent['total_price'][i], torrent['follow'][i], torrent['watch'][i], now)
            cursor.execute(sql,(torrent['houseid'][i], torrent['total_price'][i], follow, watch, torrent['region'][i], torrent['house_type'][i], torrent['area'][i], torrent['orientation'][i], torrent['design'][i], unit_price, now,    torrent['total_price'][i],unit_price,follow,watch, now))
            #cursor.execute(sql)
           #print(ret)
        return torrent

def getNum(strs):
    print(re.sub("\D", "", strs))
    return re.sub("\D", "", strs)


