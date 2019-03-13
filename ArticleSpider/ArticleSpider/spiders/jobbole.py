# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobboleArticleItem
from ArticleSpider.utils.common import get_md5

# extract()方法调用后返回的数据变为一个数组了
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']#列表：存放所有要爬取的url[可拼凑出所有的url可完成对该页面内所有url的爬取]
    def parse(self, response):
        """
        1. 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse函数
        :param response:
        :return:
        """
        # 获取文章列表页中的文章url并交给scrapy下载后并进行解析
        # 文章urls
        # // *[ @ id="archive"] / div[1] / div[1] / a / img
        post_nodes = response.xpath("//*[@id='archive']/div/div[1]/a")
        for post_node in post_nodes:
            image_url = post_node.xpath("./img/@src").extract_first("")#extract第一个默认为空
            post_url = post_node.xpath("@href").extract_first("")
            yield Request(url=parse.urljoin(response.url,post_url),meta = {"front_image_url":image_url},callback=self.parse_detail) #下载详情页后，对详情页回传callback循环调用parse_detail方法进行页面解析
        # 提取下一页并交给scrapy进行下载
        next_url = response.xpath("//*[@id='archive']/div[21]/a[4]/@href").extract()
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)
        # 文章标题
        response.xpath("//*[@id='archive']/div/div[2]/p[1]/a[1]/text()").extract()
    def parse_detail(self,response):
        # 提取文章的具体字段
        # 获取标题
        article_item = JobboleArticleItem()
        re_selector = response.xpath('//*[@class="entry-header"]/h1/text()')
        front_image_url = response.meta.get("front_image_url","")#文章封面图
        title = response.xpath("//*[@class='entry-header']/h1/text()").extract_first()
        create_date=response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·"," ").strip()
        praise_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract_first()
        fav_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract_first()
        match_re = re.match(".*?(\d+).*",fav_num)
        if match_re:
            fav_num = int(match_re.group(1))
        else:
            fav_num = 0
        comment_num = response.xpath("//a[@href='#article-comment']/span/text()").extract_first()
        match_re=re.match(".*?(\d+).*", comment_num)
        if match_re:
            comment_num=int(match_re.group(1))
        else:
            comment_num = 0
        content = response.xpath("string(//div[@class='entry'])").extract()[0].split()
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.endswith("评论")]
        tags = ",".join(tag_list)


        article_item["title"] = title
        article_item["url"]=response.url
        article_item["url_object_id"] = get_md5(response.url)
        try:
            create_date = datetime.datetime.strptime(create_date,'%y/%m/%d').date()
        except Exception as e:
            create_date = datetime.datetime.now().date()
        article_item["create_date"]=create_date
        article_item["front_image_url"]=[front_image_url]
        article_item["praise_num"]=praise_num
        article_item["comment_num"]=comment_num
        article_item["fav_num"]=fav_num
        article_item["tags"]=tags
        article_item["content"]=content

        yield article_item

