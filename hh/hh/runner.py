from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from hh import settings
from hh.spiders.hhru import HhruSpider
from hh.spiders.hhruSalary import HhrusalarySpider
from hh.spiders.hhrures import HhruresSpider
from hh.spiders.hhruResText import hhruResText

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    # process.crawl(HhrusalarySpider)
    # process.crawl(HhruresSpider)
    # process.crawl(hhruResText)
    process.start()