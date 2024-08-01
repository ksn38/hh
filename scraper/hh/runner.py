from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import settings
from spiders.flcom import FlcomSpider
from spiders.flru import FlruSpider
from spiders.hhruApi import ApiVac
from spiders.flru import FlruSpider
import time


crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)
process.crawl(FlcomSpider)
process.crawl(FlruSpider)
process.start()

start_url_header = 'https://api.hh.ru/vacancies?st=searchVacancy&search_field=name&text='
for i in ['Golang', 'Data scientist', 'Javascript', 'Frontend', 'C%23', 'Python', 'php', 'Data', 'DevOps', 'C%2B%2B', 'Java', 'Intern']:
    ApiVac(i, start_url_header + i).start()
    time.sleep(10)

start_url_text = 'https://api.hh.ru/vacancies?st=searchVacancy&text='
for i in ['Spark', 'Typescript', '%D0%BC%D0%B8%D0%BA%D1%80%D0%BE%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81', 'SQL']:
    ApiVac(i, start_url_text + i).start()
    time.sleep(10)
    
start_url_EPAM = 'https://api.hh.ru/vacancies?st=searchVacancy&employer_id=6085050'
ApiVac('EPAM', start_url_EPAM).start()

