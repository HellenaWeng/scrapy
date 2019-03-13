# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class JobboleArticleItem(scrapy.Item):
    title=scrapy.Field()  #item只有Field一种数据类型，所以传什么类型的数据
                          #进来都可以
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field() #限制url为固定长度
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field() #图片在本地的存储路径
    praise_num = scrapy.Field()
    comment_num = scrapy.Field() 
    fav_num = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

