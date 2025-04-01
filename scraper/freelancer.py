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
import os


today = str(date.today())

class FlcomSpider(scrapy.Spider):
    name = 'flcom'
    allowed_domains = ['freelancer.com']
    start_urls = ['http://freelancer.com/jobs/']
    counter = 0
    list_tags = []

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(FlcomSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self):
        tags_dict = Counter(self.list_tags)
        tags_df = pd.DataFrame(tags_dict.items(), columns=['tag', 'val'])
        tags_df.sort_values('val', ascending=False).to_csv('./freelancer/tags/flcom' + today + '.csv', index=False, encoding='utf-8')

    def parse(self, response: HtmlResponse):
        self.counter += 1
        next_page = str(self.counter)
        tags = response.xpath("//a[@class='JobSearchCard-primary-tagsLink']/text()").extract()
        self.list_tags.extend(tags)
        if len(tags) == 0 or self.counter == 100:
            return
        yield response.follow('http://freelancer.com/jobs/' + next_page, callback=self.parse)


# crawler_settings = Settings()
# crawler_settings.setmodule(settings)
# process = CrawlerProcess(settings=crawler_settings)
# process.crawl(FlcomSpider)
# process.start()
