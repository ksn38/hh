import scrapy
from scrapy.http import HtmlResponse
from hh.items import HhItem
from scrapy import signals
from collections import Counter
import pandas as pd
from datetime import date
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from hh import settings
import time
import random


# ['Data', 'Data scientist', 'DevOps', 'Frontend', 'Golang', 'Intern', 'Java', 'Javascript', 'php', 'Python', 'Spark', 'SQL', 'Typescript']
today = str(date.today())


class FlruSpider(scrapy.Spider):
    list_tags = []
    name = 'flru'
    allowed_domains = ['fl.ru']
    start_urls = ['https://www.fl.ru/projects/']
    counter = 0

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FlruSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self):
        c = Counter(self.list_tags)
        df = pd.DataFrame(c.items(), columns=['tag', 'val'])
        # a.sort_values('val', ascending=False).to_csv('E:\\Temp\\tags\\' + find + '\\' + find + today + '.csv', index=False, encoding='utf-8')
        df.to_csv('E:\\Temp\\' + self.name + today + '.csv', index=False, encoding='utf-8')

    def parse(self, response: HtmlResponse):
        # next_page = response.xpath("//a[@class='b-pager__link']/@href").extract_first()
        self.counter += 1
        next_page = '?page=' + str(self.counter) + '&kind=5'
        # print(next_page)
        header = response.xpath("//a[@class='b-post__link']/text()").extract()
        print(len(header))
        price = response.xpath('//div[@data-id="qa-lenta-1"]//text()').extract()
        print('price',price)
        #yield response.follow(next_page, callback=self.parse)


crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)
process.crawl(FlruSpider)
process.start()