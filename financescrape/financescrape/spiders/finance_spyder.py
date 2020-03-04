import scrapy
import w3lib.html
from tld import get_tld

class FinanceSpider(scrapy.Spider):
    name= "finance"

    start_urls = [
        'https://financenews.com.br/feed/',
        'https://www.ultimoinstante.com.br/feed/'
    ]

    def parse(self, response):
        origin = get_tld(response.url, as_object=True).domain
        filename = f"scrapy-{origin}.html"
        with open(filename, 'wb') as f:
            f.write(response.body)

        if origin == 'financenews':
            response.selector.remove_namespaces()
            for item in response.css('item'):
                title = item.css('title::text').get()
                description = item.css('encoded')
                for scope in description:
                    content = scope.xpath('text()').get()
                    # parsed_content = scrapy.selector.Selector(text=text).xpath('//p').getall()
                    yield {
                        'origin': origin,
                        'title': title,
                        'content': content
                    }
        else:
            for item in response.css('item'):
                title = item.css('title::text').get()
                description = item.css('description')
                for scope in description:
                    content = scope.xpath('text()').get()
                    yield {
                                'origin': origin,
                                'title': title,
                                'content': content
                            }