# -*- coding:utf-8 -*- 
# Author: lionel

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Spider

from myproject.items import MovieItem


class MovieSpider(Spider):
    name = 'movie'
    url = 'https://movie.douban.com/top250'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        selector = Selector(response)
        movies = selector.xpath('//div[@class="info"]')
        for movie in movies:
            item = MovieItem()
            title = movie.xpath('div[@class="hd"]/a/span/text()').extract()
            fullTitle = ''
            for each in title:
                fullTitle += each
            movieInfo = movie.xpath('div[@class="bd"]/p/text()').extract()
            star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            quote = movie.xpath('div[@class="bd"]/p/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ''
            item['title'] = fullTitle
            item['movieInfo'] = ';'.join(movieInfo).replace(' ', '').replace('\n', '')
            item['star'] = star[0]
            item['quote'] = quote
            yield item
        nextPage = selector.xpath('//span[@class="next"]/link/@href').extract()
        if nextPage:
            nextPage = nextPage[0]
            yield Request(self.url + str(nextPage), callback=self.parse)
