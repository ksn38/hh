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
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderData(HhruSpider):
    name = 'Data'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderEPAM(HhruSpider):
    name = 'EPAM'
    start_urls = ['https://nn.hh.ru/search/vacancy?st=searchVacancy&employer_id=6769']  # EPAM

class HhruSpiderDevOps(HhruSpider):
    name = 'DevOps'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderFrontend(HhruSpider):
    name = 'Frontend'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderGolang(HhruSpider):
    name = 'Golang'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderIntern(HhruSpider):
    name = 'Intern'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderJava(HhruSpider):
    name = 'Java'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderJavascript(HhruSpider):
    name = 'Javascript'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name] #по названию

class HhruSpiderphp(HhruSpider):
    name = 'php'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name]  # по названию

class HhruSpiderPython(HhruSpider):
    name = 'Python'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name]  # по названию

class HhruSpiderSpark(HhruSpider):
    name = 'Spark'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]

class HhruSpiderSQL(HhruSpider):
    name = 'SQL'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]

class HhruSpiderTypescript(HhruSpider):
    name = 'Typescript'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&text=' + name]

class HhruSpiderCpp(HhruSpider):
    name = 'C%2B%2B'
    start_urls = ['https://hh.ru/search/vacancy?st=searchVacancy&search_field=name&text=' + name]  # по названию

crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)
# process.crawl(HhruSpiderData)
# process.crawl(HhruSpiderDS)
# process.crawl(HhruSpiderEPAM)
# process.crawl(HhruSpiderDevOps)
# process.crawl(HhruSpiderFrontend)
# process.crawl(HhruSpiderGolang)
# process.crawl(HhruSpiderIntern)
# process.crawl(HhruSpiderJava)
# process.crawl(HhruSpiderJavascript)
# process.crawl(HhruSpiderphp)
# process.crawl(HhruSpiderPython)
# process.crawl(HhruSpiderSpark)
# process.crawl(HhruSpiderSQL)
# process.crawl(HhruSpiderTypescript)
process.crawl(HhruSpiderCpp)
process.start()