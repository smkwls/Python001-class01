import scrapy
from scrapy.selector import Selector
from maoyan.items import MaoyanItem
from http.cookies import SimpleCookie


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']
    cookies_uc = 'uuid_n_v=v1; uuid=8B5915E0BDD011EAAEDC37E7AA22D469D6E5AA6F48FE4D7AA682403705D7D764; _lxsdk_cuid=17318f25105b-07c54251132507-76212662-1fa400-17318f251066; _lxsdk=8B5915E0BDD011EAAEDC37E7AA22D469D6E5AA6F48FE4D7AA682403705D7D764; mojo-uuid=1b75a1101b53effb12adce7428903247; _csrf=29543f91fb2d13eb99fe8079640ecf68c97376b6cee8117f412f5b5a791154e7; lt=1jBBm8lTnEJze2SKNp4dxlZdsv0AAAAAAAsAAD-LN9LYElZKWVUz7MweBk7vr6JQ4-_O18QjU0PAiz58IMCOL12lQENdRYZjI8LyhA; lt.sig=GIbr_LgvDcwogszZ4K7jCO_6W-4; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1593851400,1593940559,1593943135; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1593943135; __mta=19110535.1593851403909.1593943054461.1593943136633.4; _lxsdk_s=1731ed9c9d7-8f1-00f-09a%7C598323289%7C1' 
    cookie = SimpleCookie(cookies_fromchrome)
    cookies = {i.key:i.value for i in cookie.values()}
    

    def start_requests(self):

        yield scrapy.Request(url=self.start_urls[0],callback=self.parse,dont_filter=False,cookies=self.cookies)




    def parse(self, response):
        movies = Selector(response=response).xpath('//div[@class="channel-detail movie-item-title"]')
        for movie in movies: 
            item = MaoyanItem()
            title = movie.xpath('./a/text()') # 电影名称 
            item['title'] = title.extract_first().strip()
            yield scrapy.Request(url=item['link'],meta={'item': item},callback=self.parse2)
    

    def parse2(self,response):
        """  
        到对应标题的链接中获取电影信息
        """
        item = response.meta['item']
        infos = Selector(response=response).xpath('//div[@class="movie-brief-container"]')
        print(infos)
        for info in infos:
            category = info.xpath('./ul/li/a/text()').extract()
            year = info.xpath('./ul/li[last()]/text()').extract_first().strip()
            item['category'] = category
            item['date'] = date

        yield item

