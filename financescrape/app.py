import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# set the output file here
filename = 'finance.jsonl'
file_format = 'jsonlines'

# a list with the name of the spiders to be run
spiders = ['financenews', 'ultimoinstante']


settings = get_project_settings()
settings.set('FEED_FORMAT', file_format)
settings.set('FEED_URI', filename)

process = CrawlerProcess(settings)

for spyder in spiders:
    process.crawl(spyder)

process.start()