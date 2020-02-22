__author__ = 'wanderknight'
__time__ = '2020/2/20 15:35'

from openpyxl import Workbook


class Item_to_xlsx(object):
    def __init__(self):
        # 先实例化一个class对象
        self.wb = Workbook()
        # 激活工作表
        self.ws = self.wb.active
        # 添加一行数据，就是excel表的第一行，标记这一列的作用
        self.ws.append(['名称', '地址详情', '下载链接', '迅雷下载链接'])

    # 下面就是把数据写入表中啦
    def process_item(self, item, spider):
        line = [item['title'], item['url'], item['magnet_link'], item['ftp_link']]
        self.ws.append(line)
        self.wb.save('dytt.xlsx')
        return item