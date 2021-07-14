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


# ['Data', 'Data scientist', 'DevOps', 'Frontend', 'Golang', 'Intern', 'Java', 'Javascript', 'php', 'Python', 'Spark', 'SQL', 'Typescript']
today = str(date.today())


class HhruSpider(scrapy.Spider):
    list_tags = []
    name = ''
    allowed_domains = ['hh.ru']

    # if find == 'Spark' or find == 'Typescript' or find == 'SQL':
    #     start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]
    # else:
    #     start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name]  # по названию

    # start_urls = ['https://hh.ru/search/vacancy?area=1679&st=searchVacancy&text=' + name] #по нн
    # start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию
    # start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&experience=noExperience&text=' + name] #без опыта
    start_urls = ['https://nn.hh.ru/search/vacancy?clusters=true&enable_snippets=true&search_field=name&experience=noExperience&from=cluster_experience&showClusters=true&text=' + name]  # без опыта по названию
    # start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]
    # start_urls = ['https://nn.hh.ru/search/vacancy?st=searchVacancy&employer_id=6769'] #EPAM

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(HhruSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider


    def spider_closed(self):
        print(self.list_tags)
        c = Counter(self.list_tags)
        a = pd.DataFrame(c.items(), columns=['tag', 'val'])
        # a.sort_values('val', ascending=False).to_csv('E:\\Temp\\tags\\' + find + '\\' + find + today + '.csv', index=False, encoding='utf-8')
        a.sort_values('val', ascending=False).to_csv('E:\\Temp\\' + self.name + today + '.csv', index=False, encoding='utf-8')

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vaclist = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()

        for link in vaclist:
            yield response.follow(link, callback=self.vacparse)

    def vacparse(self, response: HtmlResponse):
        tags = response.xpath("//span[@class='bloko-tag__section bloko-tag__section_text']/text()").extract()
        # yield HhItem (tags=tags)
        self.list_tags.extend(tags)


class HhruSpiderDS(HhruSpider):
    name = 'Data scientist'
    start_urls = ['https://nn.hh.ru/search/vacancy?clusters=true&enable_snippets=true&search_field=name&experience=noExperience&from=cluster_experience&showClusters=true&text=' + name]  # без опыта по названию


class HhruSpiderData(HhruSpider):
    name = 'Data'
    start_urls = ['https://nn.hh.ru/search/vacancy?clusters=true&enable_snippets=true&search_field=name&experience=noExperience&from=cluster_experience&showClusters=true&text=' + name]  # без опыта по названию


class HhruSpiderEPAM(HhruSpider):
    name = 'EPAM'
    start_urls = ['https://nn.hh.ru/search/vacancy?st=searchVacancy&employer_id=6769']  # EPAM


crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)
process.crawl(HhruSpiderData)
# time.sleep(30)
process.crawl(HhruSpiderDS)
# time.sleep(30)
# process.crawl(HhruSpiderEPAM)
process.start()