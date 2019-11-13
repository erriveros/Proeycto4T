import scrapy
from scrapy.http import FormRequest
from ..items import UandesscraperItem

class SadSpider(scrapy.Spider):
    name = 'saf'
    start_urls = ['https://saf.uandes.cl/ing/default/user/login?_next=/ing/default/index']

    def parse(self, response):
        return FormRequest.from_response(response, formdata={
            'email' : 'rjgonzalez@miuandes.cl',
            'password' : 'qepdotto1'
        }, callback= self.start_scraping)

    def start_scraping(self, response):
        items = UandesscraperItem()

        unread_news = response.css('section#News').css('a.list-group-item')
        for new in unread_news:
            news = new.css('div.label-news-activity-theme').css("strong::text").extract()
            newsHref = new.xpath("@href").extract()
            items['news'] = news
            items['href'] = newsHref
            yield items
