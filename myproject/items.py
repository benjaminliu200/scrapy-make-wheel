# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)


class BaiduItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()


class MovieItem(scrapy.Item):
    title = scrapy.Field()
    movieInfo = scrapy.Field()
    star = scrapy.Field()
    quote = scrapy.Field()


class YiYaoWangDrugItem(scrapy.Item):
    id = scrapy.Field()
    short_name = scrapy.Field()
    product_name = scrapy.Field()


class DouyuItem(scrapy.Item):
    rid = scrapy.Field()
    nn = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
