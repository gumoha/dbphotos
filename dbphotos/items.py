# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DbphotosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field() #相册地址
    nums = scrapy.Field() #相片张数
    title = scrapy.Field() #相册标题
    intro = scrapy.Field()#相册介绍

    imgsrcs = scrapy.Field() #图片原图地址集合
    imgpath = scrapy.Field() #同一系列图片存储文件夹路径
