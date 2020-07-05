# -*- coding: utf-8 -*-
import scrapy
# from day6.testpost.testpost.items import TestpostItem

class QimingSpider(scrapy.Spider):
    name = 'qiming'
    allowed_domains = ['5156edu.com', 'threetong.com']
    start_urls = ['http://xh.5156edu.com/xm/nu.html']

    def parse(self, response):
        # print(response.body)
        # with open('qiming.html', 'wb') as f:
        #     f.write(response.body)
        last_name = '李'
        name_list = response.xpath('//a[@class="fontbox"]/text()').extract()
        two_name_list = []
        for name in name_list:
            for name2 in name_list:
                two_name = name + name2
                two_name_list.append(two_name)
        name_list = two_name_list + name_list
        print(len(name_list))
        name_list = name_list[:300]

        for name in name_list:
            form = {
                'isbz': '1',
                'txtName': last_name,
                'name': name,
                'rdoSex': '0',
                'data_type': '0',
                'cboYear': '1998',
                'cboMonth': '1',
                'cboDay': '9',
                'cboHour': '12 - 午时',
                'cboMinute': '4分',
                'pid': '',
                'cid': '选择城市',
                'zty': '0',
            }
            url = 'https://www.threetong.com/ceming/baziceming/xingmingceshi.php'
            req = scrapy.FormRequest(url=url, formdata=form, callback=self.check_name_validate)
            req.meta['wanted_name'] = last_name + name
            yield req

    def check_name_validate(self, response):
        try:
            lishu_score = response.xpath('//span[@class="df_1 left"]/text()').extract_first()
            bazi_score = response.xpath('//span[@class="df_1 right"]/text()').extract_first()
            # print(bazi_score)
            lishu_score = lishu_score.replace('姓名理数评分:', '')
            bazi_score = bazi_score.replace('姓名配合八字评分:', '')
            # title = response.xpath('//p[@class="content__title"]/text()').extract()[0]
            # title = response.xpath('//p[@class="content__title"]/text()').extract_first()
            # print(title)

            if float(lishu_score) > 70.0 and float(bazi_score) > 70.0:
                item = TestpostItem()
                item['info'] = response.meta['wanted_name'] + lishu_score + ' ' + bazi_score
                print(response.meta['wanted_name'])
                yield item
        except Exception as e:
            print(e)
