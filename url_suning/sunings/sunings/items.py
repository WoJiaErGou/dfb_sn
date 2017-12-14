# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #商品型号
    p_Name = scrapy.Field()
    #店铺名称
    shop_name = scrapy.Field()
    #商品ID
    ProductID = scrapy.Field()
    #价格区间稍后设置
    PriceRange=scrapy.Field()
    #正价
    price = scrapy.Field()
    #折扣价
    PreferentialPrice = scrapy.Field()
    #评论总数
    CommentCount = scrapy.Field()
    #好评度
    GoodRateShow = scrapy.Field()
    #好评
    GoodCount = scrapy.Field()
    #中评
    GeneralCount = scrapy.Field()
    #差评
    PoorCount = scrapy.Field()
    #评论关键字
    keyword = scrapy.Field()
    #类别：核心参数等
    type = scrapy.Field()
    #品牌
    brand = scrapy.Field()
    #功能:加热方式+控制方式，预约方式
    X_type = scrapy.Field()
    #商品型号，品牌型号
    X_name = scrapy.Field()
    #不需要展示的数据
    #url前面部分id
    urlID=scrapy.Field()
    #商品名称
    may_name=scrapy.Field()
    #容量
    capacity =scrapy.Field()
    #来源
    source=scrapy.Field()
    #颜色
    color=scrapy.Field()
    product_url=scrapy.Field()
    ProgramStarttime=scrapy.Field()
