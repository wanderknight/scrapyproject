__author__ = 'wanderknight'
__time__ = '2020/2/20 15:39'
import csv


class Pipeline_ToCSV(object):

    def __init__(self):
        # 打开(创建)文件
        self.file = open('items.csv', 'w')
        # csv写法
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        self.writer.writerow(item)
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
