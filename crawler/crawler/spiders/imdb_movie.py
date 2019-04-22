import scrapy
from ..items import IMDBItem


class MovieSpider(scrapy.Spider):
    name = "imdb_movie"
    base_url = 'https://www.imdb.com'

    def __init__(self):
        super(MovieSpider, self).__init__()
        self.tb = None

    def start_requests(self):
        urls = {'top': 'http://www.imdb.com/chart/top',
                # 'bottom': 'http://www.imdb.com/chart/bottom',
                }
        for url in urls:
            self.tb = url
            yield scrapy.Request(url=urls[url], callback=self.parse)

    def parse(self, response):
        nmovies = {'top': 250, 'bottom': 100}
        for i in range(1, nmovies[self.tb]+1):
            url = response.xpath('''//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[{}]/td[2]/a/@href'''.format(i)).get()
            yield scrapy.Request(url=self.base_url+url, callback=self.get_info)

    def get_info(self, response):
        item = IMDBItem()
        item['title'] = response.xpath('''//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/h1/text()''').get()
        item['director'] = response.xpath('''//*[@id="title-overview-widget"]/div[2]/div[1]/div[2]/a/text()''').get()
        item['rating'] = float(response.xpath('''//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()''').get())
        item['genres'] = response.xpath('''//*[@id="titleStoryLine"]/div[4]/a/text()''').getall()
        url = response.xpath('''//*[@id="titleStoryLine"]/span[2]/a[2]/@href''').get()
        yield scrapy.Request(url=self.base_url+url, callback=self.get_synopsis, meta={'item': item})

    def get_synopsis(self, response):
        item = response.meta['item']
        item['synopsis'] = ''.join(response.xpath('''//*[contains(@id, 'synopsis-py')]/text()''').getall())
        return item

