# coding=utf-8
import datetime
import json
import logging
import re
import time

import scrapy
from scrapy import Spider
from scrapy.commands import parse
from selenium import webdriver
from w3lib.html import remove_tags

from myproject.items import ZhihuQuestionItem


class ZhihuSpider(Spider):
    name = 'zhihu'
    start_urls = ['http://www.zhihu.com/#signin']
    allowed_domains = ["www.zhihu.com"]
    headers = {
        'Host': 'www.zhihu.com',
        'Referer': 'http://www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
    }

    def start_requests(self):
        # 首次要执行登录知乎，用来保存cookies，
        # 之后的请求可以注释该方法，每次请求都做登录那真的很烦
        # self.login_zhihu()
        # 读取login保存的cookies值
        with open('zhihuCookies.json', 'r+') as f:
            listcookies = json.load(f)
        # 通过构建字典类型的cookies
        cookies_dict = dict()
        for cookie in listcookies:
            cookies_dict[cookie['name']] = cookie['value']
        # Tips 我们在提取cookies时，其实只要其中name和value即可，其他的像domain等可以不用
        # yield发起知乎首页请求，带上cookies哦-->cookies=cookies_dict
        yield scrapy.Request(url=self.start_urls[0], cookies=cookies_dict, headers=self.headers, dont_filter=True)

    # 爬取知乎首页，这里我们要做的是讲所以是知乎问答的请求url筛选出来
    def parse(self, response):
        logging.info('进入解析页面')
        # 爬取知乎首页->内容TopstoryMain中的->所有urls
        content_urls = response.css(".TopstoryMain a::attr(href)").extract()
        url_list = []  # 保存全部url，并用来进一步提取是question的URl
        for url in content_urls:
            # 大部分的url都是不带主域名的，所以通过parse函数拼接一个完整的url
            urls = parse.urljoin(response.url, url)
            url_list.append(urls)

        # 筛选所有urls中是知乎问答的urls（分析问答urls格式发现是：/question/xxxxxxxxx）
        for url in url_list:
            url = re.findall("(.*question/([\s\S]*?))(/|$)", url)  # 正则表达式匹配问答url
            if url:
                # 如果提取到question的url则通过yield请求question解析方法进一步解析question
                request_url = url[0][0]  # 问答url
                request_id = url[0][1]  # 问答id
                # 请求该问答详情页
                yield scrapy.Request(url=request_url, headers=self.headers, callback=self.parse_detail_question,
                                     meta={"zhihu_id": request_id})
            else:  # 否则说明当前知乎页面中没有question，那么在此请求知乎首页，相当于刷新，直到出现question
                yield scrapy.Request(url=response.url, headers=self.headers, callback=self.parse)
            # 这两次的scrapy.Request()并没有带上cookies了，但实际它依然是登录后的状态，scrapy的作用

        # 爬取并解析问答详细页面，同时请求该问答知乎用户的回答

    def parse_detail_question(self, response):
        start_answe_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdci_info&limit={1}&offset={2}&sort_by=default'

        # 以下是知乎问答的每一个字段提取，通过css方法，这里就不详细注释了
        time.sleep(1)  # 进程休眠1s 防止请求太快，知乎给你掐了ip
        zhihu_id = response.meta.get("zhihu_id", "")
        topics = response.css(".TopicLink>div>div::text").extract()
        topics = ",".join(topics)
        url = response.url
        title = response.css('.QuestionHeader-title::text').extract_first('')
        # 只获取标签，不提取标签的文本，以便下一步做去标签处理
        content = response.css('.QuestionHeader-detail span').extract_first("")
        # from w3lib.html import remove_tags 去除标签，留下文本
        content = remove_tags(content).strip()
        answer_num = response.css(".List-headerText>span::text").extract_first("").strip()
        # 匹配所有的数字，然后拼接成一起，因为大于三位数的回答数中有,隔开
        answer_nums = re.findall('([\d])', answer_num)
        answer_num = ''
        for answer in answer_nums:
            answer_num += answer
        comment_num = response.css(".QuestionHeader-Comment").extract_first('')
        if "评论" in comment_num:  # 判断是否有评论，可能一些问答没有评论
            comment_num = response.css(".QuestionHeader-Comment>button::text").extract_first('')
            comment_num = re.findall('([\s\S]*?)条评论', comment_num)[0].strip()
        watch_click = response.css(".NumberBoard-itemValue::text").extract()
        if len(watch_click[0]) > 3:  # 去除大于3位数多出来的逗号'1,234'
            watch_user_num = watch_click[0]
            watch_user_nums = re.findall('([\d])', watch_user_num)
            watch_user_num = ''
            for i in watch_user_nums:
                watch_user_num += i
        else:
            watch_user_num = watch_click[0]
        if len(watch_click[1]) > 3:  # 去除大于3位数多出来的逗号'1,234'
            click_num = watch_click[0]
            click_nums = re.findall('([\d])', click_num)
            click_num = ''
            for i in click_nums:
                click_num += i
        else:
            click_num = watch_click[1]
        # 获取当前的时间，并把datetime转换成字符
        crawl_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 传给Item
        questionItem = ZhihuQuestionItem()
        questionItem['zhihu_id'] = zhihu_id
        questionItem['topics'] = topics
        questionItem['url'] = url
        questionItem['title'] = title
        questionItem['content'] = content
        questionItem['answer_num'] = answer_num
        questionItem['comment_num'] = comment_num
        questionItem['watch_user_num'] = watch_user_num
        questionItem['click_num'] = click_num
        questionItem['crawl_time'] = crawl_time
        yield questionItem
        # 请求知乎相应回答数据，根据分析出的api接口发起请求，得到是json数据
        # start_answe_url.format(zhihu_id,20,0)，请求url中有三个要传参数通过format()给
        yield scrapy.Request(url=start_answe_url.format(zhihu_id, 20, 0), headers=self.headers,
                             callback=self.parse_answer)

    # 利用selenium登录知乎
    def login_zhihu(self):
        # chrome_path = r"D:\software\tools\chromdriver\chromedriver.exe"
        # driver = webdriver.Chrome(chrome_path)

        options = webdriver.ChromeOptions()
        # 58版本的chrome匹配2.30版本的chromedriver
        options.binary_location = r"C:\Users\liudeyong\AppData\Local\Google\Chrome\Application\chrome.exe"
        chrome_driver_binary = r"D:\software\tools\chromdriver\chromedriver230.exe"
        driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
        loginurl = 'https://www.zhihu.com/signin'
        # 加载webdriver驱动，用于获取登录页面标签属性
        driver.get(loginurl)
        # 扫描二维码登录前，让程序休眠10s
        time.sleep(10)
        a = raw_input('请点击并扫描页面二维码，手机确认登录后，回编辑器点击回车：')
        print a
        cookies = driver.get_cookies()
        # logging.info('cookies:$s', cookies)
        driver.close()
        # 保存cookies，之后请求从文件中读取cookies就可以省去每次都要登录一次的，也可以通过return返回，每次执行先运行登录方法
        # 保存成本地json文件
        jsonCookies = json.dumps(cookies)
        with open('zhihuCookies.json', 'w') as f:
            f.write(jsonCookies)
