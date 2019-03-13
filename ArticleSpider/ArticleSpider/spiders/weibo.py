# -*- coding: utf-8 -*-
import scrapy


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['https://s.weibo.com/top/summary?cate=realtimehot']
    start_urls = ['https://s.weibo.com/top/summary?cate=realtimehot/']

    def parse(self, response):
        hot_num = response.xpath("//div[@class='data']/table/tbody/tr/td[1]/text()").extract()
        hot_num.insert(0,'')
        hot_titles = response.xpath("//div[@class='data']/table/tbody/tr/td[2]/a/text()").extract()
        hot_urls = []
        for hot_title in hot_titles:
            hot_url = 'https://s.weibo.com/weibo?q=%23' + hot_title + '%23&Refer=top'
            hot_urls.append(hot_url)
        # hot_status = response.xpath("//div[@class='data']/table/tbody/tr/td[3]/i/text()").extract()
        hot_index = response.xpath("//div[@class='data']/table/tbody/tr/td[2]/span/text()").extract()
        hot_index.insert(0,'')
    def parse_detail(self,response):
        topic_name = response.xpath("//*[@id='pl_topic_header']/div[1]/div/div[1]/h1/a/text()").extract()
        topic_read_num =  response.xpath("//*[@id='pl_topic_header']/div[1]/div/div[2]/span[1]/text()").extract()
        topic_discuss_num = response.xpath("//*[@id='pl_topic_header']/div[1]/div/div[2]/span[2]/text()").extract()
        topic_users = response.xpath("//div[@class='card-wrap']/div/div/div[2]/div[1]/div[2]/a[1]/text()").extract()

    def parse_single_detail(self,response):
        topic_users = response.xpath("//div[@class='card-wrap']/div/div/div[2]/div[1]/div[2]/a[1]/text()").extract()
        # for topic_user in topic_users:


        pass
