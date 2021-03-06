import scrapy
from scrapy.http import HtmlResponse
from hh.items import HhItem
from scrapy import signals
from collections import Counter
import pandas as pd
from datetime import date


find = 'data'
today = str(date.today())
t = []

class hhruResText(scrapy.Spider):
    name = 'hhrurestext'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/resume?clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=position&text=' + find]
    # start_urls = ['https://nn.hh.ru/search/resume?clusters=true&exp_period=all_time&logic=normal&no_magic=false&order_by=relevance&pos=full_text&area=1679&text=' + find]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(hhruResText, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self):
        a = open('E:\\Temp\\' + find + 'restext.txt', 'w', encoding="utf-8")
        # print(t)
        a.write('\n::::::::::::\n'.join(map(str, t)))
        print(a)
        a.close()

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vaclist = response.xpath("//a[@class='resume-search-item__name']/@href").extract()

        for link in vaclist:
            yield response.follow(link, callback=self.vacparse)


    def vacparse(self, response: HtmlResponse):
        text = response.xpath("//div[@data-qa='resume-block-skills-content']/text()").extract()
        if len(text[0]) > 2000:
            t.append(response)
            t.extend(text)