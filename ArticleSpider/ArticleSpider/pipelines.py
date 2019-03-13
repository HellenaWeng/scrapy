# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi

import codecs
import json
import MySQLdb
import MySQLdb.cursors

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
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb",**dbparams) #dbapiName 指的就是MySQLdb的模块名，我们直接用MySQLdb,告诉该模块我们用到的是MySQLdb的模块
        return cls(dbpool)
    def process_item(self,item,spider):
        #使用twisted方法runInteraction()方法将mysql插入变成异步执行
        # 在此处需要用到dbpool的一个函数,这个函数第一个参数就是我们自己要定义的一个函数，这个函数中写入我们具体插入的逻辑，item就是我们要插入的数据
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error)
        #process-item执行完可能会有错误，但是因为是异步操作，我们是不能等它执行完直接解决错误的，此处的错误处理是专门的处理函数
        # 此处可添加一个我们自己的异步错误处理函数
    def handle_error(self,failure):
        #自定义函数，处理异步插入的异常
        print(failure)
    def do_insert(self, cursor, item):
        #执行具体插入
        insert_sql="insert into jobbole_article (title,url,url_object_id,fav_num,praise_num,comment_num,content) values( %s, %s, %s, %s, %s, %s, %s)"
        content=",".join(item["content"])
        params=(
        item["title"], item["url"], item["url_object_id"], item["fav_num"], item["praise_num"], item["comment_num"],
        content)
        cursor.execute('SET NAMES utf8mb4')
        cursor.execute(insert_sql, params)
        #不需要做commit，cursor会自动帮我们来做
