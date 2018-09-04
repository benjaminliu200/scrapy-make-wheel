# -*- coding: utf-8 -*-
import logging

import pymysql
from PyMysqlPool.db_util.mysql_util import insertOrUpdate

from myproject.items import MovieItem, ZhihuQuestionItem, ZhihuAnswerItem
from myproject.mysql_config import db_config


class ProcessMysqlPipeline(object):

    def process_item(self, item, spider):
        try:
            if isinstance(item, MovieItem):
                _sql = """insert into Movie (name,movieInfo,star,quote) VALUES (%s,%s,%s,%s)"""
                _args = (item['title'], item['movieInfo'], item['star'], item['quote'])
                affect = insertOrUpdate(db_config['local'], _sql, _args)
                logging.info("insert method insert result is %s ,input _data is %s ", affect, _args)
                return
            if isinstance(item, ZhihuQuestionItem) or isinstance(item, ZhihuAnswerItem):
                # 获取sql语句和参数，这个就是调用相应item的get_sql(),这样就能实现不同item各自的插入
                sql, params = item.get_sql()
                # 执行数据库语句
                insertOrUpdate(db_config['local'], sql, params)
                return
        except pymysql.Error:
            print '插入数据库异常'
        return item
