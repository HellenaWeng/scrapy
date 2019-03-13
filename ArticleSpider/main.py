# !\C:\Users\admin\PycharmProjects
# _*_ coding:utf-8 _*_
from scrapy.cmdline import execute
#调用该函数可执行scrapy脚本
import sys
#设置工程目录,然后调用execute命令时才能找到项目工程的目录才能生效
import os
#获取main文件当前所在目录的路径的父目录;__file__指当前的main文件
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","jobbole"])
# execute(["scrapy","crawl","weibo"])
