import scrapy


class HhrusalarySpider(scrapy.Spider):
    name = 'hhruSalary'
    allowed_domains = ['hh.ru']
    start_urls = ['http://hh.ru/']

    def parse(self, response):
        pass
