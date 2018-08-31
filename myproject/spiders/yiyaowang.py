# -*- coding:utf-8 -*-
# Author: liudeyong
import json

import scrapy
from scrapy.spiders import Spider

from myproject.items import YiYaoWangDrugItem


class YiYaoWangSpider(Spider):
    name = 'yiyaowang'

    def start_requests(self):
        # 可以去官网获取最大页数，这里默认抓取10页。
        # url = 'http://mall.yaoex.com/product/search?page=\d'
        for pageIndex in range(1, 5):
            # FormRequest 是Scrapy发送POST请求的方法
            print pageIndex
            url = 'http://mall.yaoex.com/product/search?page=%s' % pageIndex,
            print url[0]
            yield scrapy.FormRequest(
                url=url[0],
                formdata={
                    "product2ndLM": "神经系统用药",
                    "product2ndLMCode": "AB",
                    "from": "4",
                    "haveGoodsTag": "false",
                    "promotionTag": "false",
                    "buyerHistoryTag": "false"
                },
                callback=self.parse_page
            )

    def parse_page(self, response):
        root = json.loads(response.body)
        for data in root['retData']:
            item = YiYaoWangDrugItem()
            item['id'] = data['id']
            item['short_name'] = data['short_name']
            item['product_name'] = data['product_name']
            yield item
