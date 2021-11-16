import scrapy
from scrapy.http import HtmlResponse
from scrapy import signals
from collections import Counter
import pandas as pd
from datetime import date
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import settings
import time


today = str(date.today())

class UpworkSpider(scrapy.Spider):
    list_tag = []
    name = 'upwork'
    allowed_domains = ['upwork.com']
    start_urls = ['https://www.upwork.com/search/jobs/']
    counter = 1

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(UpworkSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self):
        tags_dict = Counter(self.list_tag)
        tags_df = pd.DataFrame(tags_dict.items(), columns=['tag', 'val'])
        tags_df.sort_values('val', ascending=False).to_csv('/tmp/upwork' + today + '.csv', index=False, encoding='utf-8')

    def parse(self, response: HtmlResponse):
        self.counter += 1
        next_page = '?page=' + str(self.counter)
        print(next_page)
        tag = response.xpath("//span[@class='o-tag-skill disabled']/text()").extract()
        print(tag)
        self.list_tag.extend(tag)
        #if self.counter < 3:
        time.sleep(5)
        yield response.follow(next_page, callback=self.parse)


crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)
process.crawl(UpworkSpider)
process.start()