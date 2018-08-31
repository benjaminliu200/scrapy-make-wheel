# -*- coding: utf-8 -*-
import pymysql

from myproject.items import MovieItem
from myproject.settings import host, port, charset, db, passwd, user


class MoviePipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self.cursor = self.conn.cursor()
        self.cursor.execute("truncate table Movie")
        self.conn.commit()

    def process_item(self, item, spider):
        try:
            if isinstance(item, MovieItem):
                self.cursor.execute("insert into Movie (name,movieInfo,star,quote) VALUES (%s,%s,%s,%s)", (
                    item['title'], item['movieInfo'], item['star'], item['quote']))
                self.conn.commit()
        except pymysql.Error:
            print("Error%s,%s,%s,%s" % (item['title'], item['movieInfo'], item['star'], item['quote']))
        return item
