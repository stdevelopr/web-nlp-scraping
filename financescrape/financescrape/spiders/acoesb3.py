import scrapy


class AcoesB3(scrapy.Spider):
    name = "acoesb3"

    custom_settings = {
        'DOWNLOAD_DELAY' : 0.5,
        'ITEM_PIPELINES': {
            'financescrape.pipelines.JsonWriterPipeline': 300,
        }
    }

    def start_requests(self):
        urls = [
            'https://br.advfn.com/bolsa-de-valores/bovespa/A',
            # 'https://br.advfn.com/bolsa-de-valores/bovespa/B'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for active in response.xpath('//tr[contains(@class,"even" ) or contains(@class,"odd" ) ]'):
            name = active.css('td a::text').extract_first()
            symbol = active.css('td::text').extract_first()
            print('----------------------------')
            yield {
                'name': name,
                'symbol': symbol
            }