# scrapy 爬虫入门
## scrapy 命令
    pip install scrapy 安装爬虫模块
    pip install pywin32 安装这个依赖，不然会一直报“ImportError: No module named win32api” 此错误
    scrapy -h 查看所有的命令
    scrapy startproject myproject 创建项目
    scrapy genspider mydomain mydomain.com 生成spider
    scrapy list 列出所有的spider
    scrapy crawl “spider1” 运行spider1爬虫可以在末尾携带参数。 -a category=electronics
    scrapy check spider1 运行contact检查
    scrapy fetch url 不需要项目，下载一个url，保存到标准输出
    scrapy view url 不需要项目，检查一个url，是否是标注输出
    scrapy runspider spider.py 未创建项目的情况下，启动一个spider爬虫
    scrapy shell http://193.112.73.110/scrapy/html/selectors-sample1.html 爬取该url，然后打开一个shell窗口。
    
## parse解析爬取的页面
定义一个class 然后在scrapy.spiders的类里面定义一个parse方法，在parse方法里面吧解析好的数据写到Item中
<br />
注意：在response里面使用xpath找到元素后，需要用extract()方法抽取里面的详细数据。
```python
class Product(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
    stock = scrapy.Field()
    last_updated = scrapy.Field(serializer=str)

def parse(self, response):
    for sel in response.xpath('//ul/li'):
        item = Product()
        item['title'] = sel.xpath('a/text()').extract()
        item['link'] = sel.xpath('a/@href').extract()
        item['desc'] = sel.xpath('text()').extract()
        yield item
```

### 定制正则爬取url，请查看yiyaowang的spider
生成爬取文件，unicode码转化为中文，需要携带-s参数, ey:-s FEED_EXPORT_ENCODING=utf-8
<br />
scrapy crawl yiyaowang -o demo.json -s FEED_EXPORT_ENCODING=utf-8

### 数据入库
需要重写pipelines，具体裤衩看pipelines包中的movie_pipline.py，通过isinstance是哪个类型，入库需要的类型

### user-agent切换
需要在根包下的settings配置DOWNLOADER_MIDDLEWARES，切换user-agent