from scrapy.spiders import CrawlSpider

from myproject.items import BaiduItem


class MininovaSpider(CrawlSpider):
    name = 'baidu'
    allowed_domains = ['baidu.com']
    start_urls = ['http://www.baidu.com']

    def parse_torrent(self, response):
        torrent = BaiduItem()
        torrent['url'] = response.url
        torrent['name'] = response.xpath("/html/head/title").extract()
        return torrent
