# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class TestpostItem(scrapy.Item):
#     # define the fields for your item here like:
#     info = scrapy.Field()
#     # pass

class AmazonGoodsItem(scrapy.Item):
    # define the fields for your item here like:
    productName = scrapy.Field()
    bylineInfo = scrapy.Field()
    star = scrapy.Field()
    listprice = scrapy.Field()
    price = scrapy.Field()
    info = scrapy.Field()
    img_url = scrapy.Field()
    rate5 = scrapy.Field()
    rate4 = scrapy.Field()
    rate3 = scrapy.Field()
    rate2 = scrapy.Field()
    rate1 = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = "insert into amazon(productName,bylineInfo,star,listprice,price,info,img_url,rate5,rate4,rate3,rate2,rate1) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        params = [self['productName'],self['bylineInfo'],self['star'],self['listprice'],self['price'],self['info'],
                  self['img_url'],self['rate5'],self['rate4'],self['rate3'],self['rate2'],self['rate1'],]
        return insert_sql, params
