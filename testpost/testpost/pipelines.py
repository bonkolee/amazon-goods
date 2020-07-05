# -*- coding: utf-8 -*-
import csv
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# class TestpostPipeline(object):
#     def __init__(self):
#         f = open('test.csv', 'w', newline='')
#         self.f_csv = csv.writer(f)
#
#     def process_item(self, item, spider):
#         title = item['productName']
#         print(title)
#         self.f_csv.writerow([title])
#         return item

class MySpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)

        return cls(dbpool)
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        # print('--------')
        print(insert_sql, params)
        # print('--------')
        cursor.execute(insert_sql, params)
