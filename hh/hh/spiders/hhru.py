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


today = str(date.today())


class HhruSpider(scrapy.Spider):
    list_tags = []
    name = ''
    allowed_domains = ['hh.ru']
    start_urls = []

    # start_urls = ['https://hh.ru/search/vacancy?area=1679&st=searchVacancy&text=' + name] #по нн
    # start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию
    # start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&experience=noExperience&text=' + name] #без опыта
    # start_urls = ['https://nn.hh.ru/search/vacancy?clusters=true&enable_snippets=true&search_field=name&experience=noExperience&from=cluster_experience&showClusters=true&text=' + name]  # без опыта по названию
    # start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]
    # start_urls = ['https://nn.hh.ru/search/vacancy?st=searchVacancy&employer_id=6769'] #EPAM

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(HhruSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

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

    def spider_closed(self):
        print(self.list_tags)
        tags_dict = Counter(self.list_tags)
        tags_df = pd.DataFrame(tags_dict.items(), columns=['tag', 'val'])
        # tags_df.sort_values('val', ascending=False).to_csv('E:\\Temp\\tags\\' + find + '\\' + find + today + '.csv', index=False, encoding='utf-8')
        tags_df.sort_values('val', ascending=False).to_csv('E:\\Temp\\' + self.name + today + '.csv', index=False, encoding='utf-8')


class HhruSpiderDS(HhruSpider):
    list_tags = []
    name = 'Data scientist'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderData(HhruSpider):
    list_tags = []
    name = 'Data'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderEPAM(HhruSpider):
    list_tags = []
    name = 'EPAM'
    start_urls = ['https://nn.hh.ru/search/vacancy?st=searchVacancy&employer_id=6769']  # EPAM

class HhruSpiderDevOps(HhruSpider):
    list_tags = []
    name = 'DevOps'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderFrontend(HhruSpider):
    list_tags = []
    name = 'Frontend'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderGolang(HhruSpider):
    list_tags = []
    name = 'Golang'
    start_urls = {'https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name}  #по названию

class HhruSpiderIntern(HhruSpider):
    list_tags = []
    name = 'Intern'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderJava(HhruSpider):
    list_tags = []
    name = 'Java'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderJavascript(HhruSpider):
    list_tags = []
    name = 'Javascript'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderphp(HhruSpider):
    list_tags = []
    name = 'php'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name]  # по названию

class HhruSpiderPython(HhruSpider):
    list_tags = []
    name = 'Python'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name]  # по названию

class HhruSpiderSpark(HhruSpider):
    list_tags = []
    name = 'Spark'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]

class HhruSpiderSQL(HhruSpider):
    list_tags = []
    name = 'SQL'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]

class HhruSpiderTypescript(HhruSpider):
    list_tags = []
    name = 'Typescript'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]

class HhruSpiderCpp(HhruSpider):
    list_tags = []
    name = 'C%2B%2B'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name]  # по названию

class HhruSpiderCs(HhruSpider):
    list_tags = []
    name = 'C%23'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name]  # по названию

class HhruSpiderMicroservice(HhruSpider):
    list_tags = []
    name = 'микросервис'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]

crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)

process.crawl(HhruSpiderDS)
process.crawl(HhruSpiderGolang)
process.crawl(HhruSpiderData)
process.crawl(HhruSpiderDevOps)
process.crawl(HhruSpiderFrontend)
process.crawl(HhruSpiderIntern)
process.crawl(HhruSpiderJava)
process.crawl(HhruSpiderJavascript)
process.crawl(HhruSpiderphp)
process.crawl(HhruSpiderPython)
process.crawl(HhruSpiderCpp)
process.crawl(HhruSpiderCs)
process.crawl(HhruSpiderEPAM)
process.crawl(HhruSpiderSpark)
process.crawl(HhruSpiderSQL)
process.crawl(HhruSpiderTypescript)
process.crawl(HhruSpiderMicroservice)

process.start()