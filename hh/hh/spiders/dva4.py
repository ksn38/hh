import scrapy


class Dva4Spider(scrapy.Spider):
    name = 'dva4'
    allowed_domains = ['2ch.hk']
    start_urls = ['http://2ch.hk/']

    def parse(self, response):
        pass
