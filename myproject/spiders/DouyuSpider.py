# -*- coding:utf-8 -*-
# Author: liudeyong
import json

import scrapy
from scrapy import Request
from scrapy.spiders import Spider

from myproject.items import YiYaoWangDrugItem, DouyuItem


class DouyuSpider(Spider):
    name = 'douyu'

    def start_requests(self):
        # 可以去官网获取最大页数，这里默认抓取10页。
        # url = 'http://mall.yaoex.com/product/search?page=\d'
        for pageIndex in range(1, 2):
            # FormRequest 是Scrapy发送POST请求的方法
            url = 'https://www.douyu.com/gapi/rkc/directory/0_0/%s' % pageIndex,
            print '-----------------------------' + str(url[0])
            yield Request(str(url[0]), callback=self.parse)

    def parse(self, response):
        print response
        root = json.loads(response.body)
        for data in root['data']['rl']:
            item = DouyuItem()
            item['rid'] = data['rid']
            item['nn'] = data['nn']
            yield item
