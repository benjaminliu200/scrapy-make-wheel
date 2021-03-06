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


class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comment_num = scrapy.Field()
    watch_user_num = scrapy.Field()
    click_num = scrapy.Field()
    crawl_time = scrapy.Field()

    # 这个是插入语句，1 构建insert语句， 2 准备insert要的参数
    def get_sql(self):
        sql = """
               insert into question (zhihu_id,topics,url,title,content,answer_num,comment_num,watch_user_num,click_num,crawl_time)
               values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
           """
        params = (self['zhihu_id'], self['topics'], self['url'], self['title'], self['content'], self['answer_num'],
                  self['comment_num'], self['watch_user_num'], self['click_num'], self['crawl_time'])
        # 并将insert语句和参数返回(即返回到了pipeline中)
        return sql, params


class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    praise_num = scrapy.Field()
    comments_num = scrapy.Field()
    update_time = scrapy.Field()
    create_time = scrapy.Field()
    crawl_time = scrapy.Field()

    # 这个是插入语句，1 构建insert语句， 2 准备insert要的参数
    def get_sql(self):
        sql = """
                   insert into answer (zhihu_id, url, question_id, author_id, content, praise_num, comments_num, update_time, create_time, crawl_time)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s, now())
               """
        params = (self['zhihu_id'], self['url'], self['question_id'], self['author_id'], self['content'], self['praise_num'],
                  self['comments_num'], self['update_time'], self['create_time'])
        # 并将insert语句和参数返回(即返回到了pipeline中)
        return sql, params
