from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import settings
from freelancer import FlcomSpider
from fl import FlruSpider


crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)
process.crawl(FlcomSpider)
process.crawl(FlruSpider)
process.start()



