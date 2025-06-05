import scrapy
from scrapy.http import HtmlResponse
from scrapy import signals
from collections import Counter
import pandas as pd
from datetime import date
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
#from hh import settings
import settings
import re
import os


today = str(date.today())

class FlruSpider(scrapy.Spider):
    list_headers = []
    list_key_words = []
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
        f = open('./fl/source/fl' + today + '.txt', 'w', encoding='utf-8')
        out = (''.join(map(str, self.list_headers)))
        #print(out)
        f.write(out)
        f.close()
        tags_dict = Counter(self.list_key_words)
        tags_df = pd.DataFrame(tags_dict.items(), columns=['tag', 'val'])
        tags_df.sort_values('val', ascending=False).to_csv('./fl/keywords/fl' + today + '.csv', index=False, encoding='utf-8')

    def parse(self, response: HtmlResponse):
        self.counter += 1
        next_page = '?page=' + str(self.counter)
        # print(next_page)
        header = response.xpath("//a[@class='text-dark text-decoration-none link-hover-danger cursor-pointer']/text()").extract()
        for i in header:
            i = str(i).lower()
            #print(i)
            if len(re.findall(r'1с\S{0,}|\S{0,}24|\w{0,}[A-z]{1,}[\w#+]{0,}|битрикс', i)) > 0:
                #print(i)
                self.list_headers.append(i + '\n')
                self.list_key_words.extend(re.findall(r'1с\S{0,}|\S{0,}24|\w{0,}[A-z]{1,}[\w#+]{0,}|битрикс', i))
        #if self.counter < 3:
        yield response.follow(next_page, callback=self.parse)


# crawler_settings = Settings()
# crawler_settings.setmodule(settings)
# process = CrawlerProcess(settings=crawler_settings)
# process.crawl(FlruSpider)
# process.start()
