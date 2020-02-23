# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql


class mySqlPipeline(object):
    def __init__(self):
        # connection database
        self.connect = pymysql.connect(host='localhost',port=3306, user='root', passwd='knight',
                                       db='doubanspider')  # 后面三个依次是数据库连接名、数据库密码、数据库名称
        # get cursor
        self.cursor = self.connect.cursor()
        print("连接数据库成功")

    def process_item(self, item, spider):
        # sql语句
        insert_sql = """insert into url_table(url, refere, status, time, title) VALUES (%s,%s,%s,%s,%s)"""
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['url'], item['refere'], item['status'], item['time'],
                                         item['title']))
        # 提交，不进行提交无法保存到数据库
        self.connect.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.connect.close()


class DoubanspiderPipeline(object):
    def process_item(self, item, spider):
        return item
