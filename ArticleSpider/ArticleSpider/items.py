# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import re
from scrapy.loader.processors import MapCompose,TakeFirst,Join
from scrapy.loader import ItemLoader

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass




def add_author(value):
    return value + "-Hellenna Weng"


def date_convert(value):
    try:
        create_date=datetime.datetime.strptime(value, '%y/%m/%d').date()
    except Exception as e:
        create_date=datetime.datetime.now().date()
    return create_date


def get_nums(value):
    match_re=re.match(".*?(\d+).*", value)
    if match_re:
        num=int(match_re.group(1))
    else:
        num=0
    return num


def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    #自定义ItemLoader
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    title=scrapy.Field(
        input_processor=MapCompose(lambda x: x+"-jobbole",add_author)
    )
    #item只有Field一种数据类型，所以传什么类型的数据
                          #进来都可以
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert),
        # output_processor = TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field() #限制url为固定长度
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field() #图片在本地的存储路径
    praise_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_num = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        output_processor = Join(","),
        input_processor = MapCompose(remove_comment_tags)
    )
    content = scrapy.Field()


