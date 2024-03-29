import scrapy
from scrapy.http import FormRequest
from ..items import UandesscraperItem


class SadSpider(scrapy.Spider):
    name = 'saf'
    start_urls = ['https://saf.uandes.cl/ing/default/user/login?_next=/ing/default/index']
    items = UandesscraperItem()

    # def __init__(self, email, password, user):
    #      self.email = email
    #      self.password = password
    #      self.user = user

    def parse(self, response):
        self.email  = "rjgonzalez@miuandes.cl"
        self.password = "qepdotto1"

        self.user = 1
        return FormRequest.from_response(response, formdata={
            'email': self.email,
            'password': self.password
        }, callback=self.start_scraping)

    def start_scraping(self, response):
        self.items = UandesscraperItem()
        for n in self.scrape_open_activities(response):
            yield n
        for i in self.scrape_courses(response):
            yield i
        self.base = 'https://saf.uandes.cl'
        self.baseHref = ['/ing/vle/news.html/491', '/ing/vle/news.html/522', '/ing/vle/news.html/483']

        unread_news = response.css('section#News').css('a.list-group-item')
        for new in unread_news:
            news = new.css('div.label-news-activity-theme').css("strong::text").extract()
            href = new.xpath("@href").extract()
            self.items['news'] = news
            self.items['href'] = href
            self.items['user'] = self.user
            #yield self.items
        # for i in self.baseHref:
            yield response.follow(self.base + href, callback=self.scrape_news)
        print('wgaaaaaaaaaaaaaaaaaaaa')
        yield response.follow('https://www.uandes.cl/noticias/', callback=self.scrape_uandes_news)

    def scrape_news(self, response):
        course = response.css('div.span12').css('a::text').extract()
        news = response.css('div.well-small')
        for i in news:
            title = i.css('div.span5').css('h4::text').extract()
            date = i.css('div.span2').css('span.label::text').extract()
            content = i.css('p::text').extract()

            self.items['course'] = course
            self.items['newsDate'] = date
            self.items['newsContent'] = ' '.join(content)
            self.items['newsTitle'] = title
            self.items['table'] = 'unread'
            self.items['user'] = self.user

            yield self.items

    def scrape_open_activities(self, response):
        open_activities = response.css('div#opened_activities')
        courses = open_activities.css('strong::text').extract()
        titles = open_activities.css('i::text').extract()
        dates = open_activities.css('span::text').extract()
        for i in range(len(courses)):
            self.items['course'] = courses[i]
            self.items['openActivityTitle'] = titles[i]
            self.items['openActivityDate'] = dates[i]
            self.items['table'] = 'open_activities'
            self.items['user'] = self.user

            yield self.items

    def scrape_courses(self, response):
        current_semester = response.css('div#current_semester')
        courses = current_semester.css('div.col-lg-12::text').extract()
        for course in courses:
            self.items['course'] = course
            self.items['table'] = 'current_semester'
            self.items['user'] = self.user

            yield self.items

    def scrape_uandes_news(self, response):
        news_box = response.css('.inner')
        titles = response.css('.block-list-item-title::text').extract()
        dates = response.css('.block-list-item-post-date::text').extract()
        for i in range(len(titles)):
            self.items['uandesNewsTitles'] = titles[i]
            self.items['uandesNewsDates'] = dates[i]
            self.items['table'] = 'uandes'

            yield self.items



