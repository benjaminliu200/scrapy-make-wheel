# -*- coding: utf-8 -*-

import urllib2

from lxml import etree


def parse_html():
    wye = urllib2.urlopen('https://movie.douban.com/top250').read().decode("utf-8", 'ignore')
    root = etree.HTML(wye)  # 将获取到的html字符串，转换成树形结构，也就是xpath表达式可以获取的格式
    movies = root.xpath('//div[@class="info"]')
    i = 0
    for movie in movies:
        temp = movie.xpath('div[@class="hd"]/a/span/text()')
        # title = movie.xpath('div[@class="hd"]/a/span/text()').extract()
        # fullTitle = ''
        # for each in title:
        #     fullTitle += each
        # movieInfo = movie.xpath('div[@class="bd"]/p/text()').extract()
        star = movie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')
        # quote = movie.xpath('div[@class="bd"]/p/span/text()').extract()
        # print '%s, %s, %s, %s' % (title, movieInfo, star, quote)
        print star
        if ++i > 10:
            break


if __name__ == '__main__':
    parse_html()
