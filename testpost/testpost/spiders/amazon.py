# -*- coding: utf-8 -*-
import scrapy
from testpost.items import AmazonGoodsItem

class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.com']
    start_urls = ['https://www.amazon.com/s?k=phone&ref=nb_sb_noss']

    def parse(self, response):
        # print(response.text)
        next_url = response.urljoin(response.xpath('//li[@class="a-last"]/a/@href').extract_first())
        goods_url = response.xpath('//a[@class="a-link-normal a-text-normal"]/@href').extract()
        print(next_url)
        # print(goods_url)
        # goods_url = [goods_url]
        for good_url in goods_url:
            temp = response.urljoin(good_url)
            yield scrapy.Request(temp, callback=self.parse_goods)
        count = 0
        # print(next_url)
        if next_url is not None:
            yield scrapy.Request(next_url,callback=self.parse)

    def parse_goods(self, response):
        productTitle = response.xpath('//span[@id="productTitle"]/text()').extract_first().strip()
        bylineInfo = response.xpath('//div[@class="a-section a-spacing-none"]/a/text()').extract_first()
        recent_shopping_trends = response.xpath('//ol[@class="a-carousel"]/li/div/a/@href').extract()
        star = response.xpath('//span[@class="a-icon-alt"]/text()').extract_first()
        star = star.split(' ')[0]
        listprice = response.xpath('//span[@class="priceBlockStrikePriceString a-text-strike"]/text()').extract_first()
        price = response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first()
        info = response.xpath('//ul[@class="a-unordered-list a-vertical a-spacing-mini"]/li/span/text()').extract()
        info = ''.join(info).strip().replace('\n\n\n', '\n')
        img_url = response.xpath('//div[@class="imgTagWrapper"]/img/@data-old-hires').extract_first()
        rate = response.xpath('//div[@class="a-meter"]/@aria-label').extract()
        rate5 = rate[0]
        rate4 = rate[1]
        rate3 = rate[2]
        rate2 = rate[3]
        rate1 = rate[4]
        print(recent_shopping_trends)
        for rst in recent_shopping_trends:
            print('-----------'+rst)
            if 'https://www.amazon.com/gp/' in rst:
                yield scrapy.Request(rst,callback=self.parse_goods)
            else:
                yield scrapy.Request(response.urljoin(rst),callback=self.parse_goods)

        print(productTitle)
        item = AmazonGoodsItem()
        item['productName'] = productTitle
        item['bylineInfo'] = bylineInfo
        item['star'] = star
        item['listprice'] = listprice
        item['price'] = price
        item['info'] = info
        item['img_url'] = img_url
        item['rate5'] = rate5
        item['rate4'] = rate4
        item['rate3'] = rate3
        item['rate2'] = rate2
        item['rate1'] = rate1
        yield item
        # with open('amazon.html', 'wb') as f:
        #     f.write(response.body)
