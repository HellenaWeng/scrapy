# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import codecs
import json
import MySQLdb

class ArticleSpiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):

        self.file = codecs.open('article.json','w',encoding='utf-8')
    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()

class JsonExporterPipeline(object):
    # 调用scrapy提供的json exporter导出json文件
    def __init__(self):
        self.file = open('articleExporter.json','wb') #打开文件 articleExporter.json  wb : 以二进制的方式打开
        self.exporter = JsonItemExporter(self.file,encoding = 'utf-8')#传递一个exporter进来,用utf-8打开
        self.exporter.start_exporting()
    #关闭信号量
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

class ArticleImagePipeline(ImagesPipeline):
    # 继承之后看那些函数可以重载
    # e.g. convert_image() 过滤制定尺寸的图片
    # 参数：
    # IMAGE_MIN_HEIGHT
    # IMAGE_MIN_WIDTH
    #
    # 两个重要函数
    # get_media_request()  url交给scrapy下载器进行下载
    # 参数：IMAGES_URLS_FIELD
    # item_completed()  先重写该方法，获取文件实际下载地址
    # 打断点看results的实际结构
    # 先删掉之前爬取的图片文件夹
    # results是一个tuple
    # 使用循环 取出path
    def item_completed(self, results, item, info):
        for ok,value in results:
            image_file_path = value["path"]
        item["front_image_path"] = image_file_path
        return item


class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost','root','5201230618102x','graduationproject',charset = 'utf8',use_unicode = True) #参数：主机，用户名，密码，数据库名称
        #数据库操作具体是用cursor完成的
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql = "insert into jobbole_article (title,url,url_object_id,fav_num,praise_num,comment_num,content) values( %s, %s, %s, %s, %s, %s, %s)"
        content = ",".join(item["content"])
        params = (item["title"],item["url"],item["url_object_id"],item["fav_num"],item["praise_num"],item["comment_num"],content)
        #%s占位符
        self.cursor.execute('SET NAMES utf8mb4')
        self.cursor.execute(insert_sql, params)
        self.conn.commit()

class MysqlTwistedPipeline(object):
    @classmethod
    def from_settings(cls,settings):
        host = settings["MYSQL_HOST"]
        dbname = settings["MYSQL_DBNAME"]
        user = settings['MYSQL_USER']
        password = settings['MYSQL_PASSWORD']
        pass

