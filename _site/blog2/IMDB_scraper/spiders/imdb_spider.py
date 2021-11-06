# to run 
# scrapy crawl imdb_spider -o results.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0109830/']

    def parse(self, response):
              
        cast_crew  = response.css("a.ipc-metadata-list-item__icon-link").attrib["href"]

        if cast_crew is not None:
            cast_crew = response.urljoin(cast_crew)    # make the full URL

            yield scrapy.Request(cast_crew, callback = self.parse_full_credits)


    def parse_full_credits(self, response):

        for actor_link in [a.attrib["href"] for a in response.css("td.primary_photo a")]:

            if actor_link is not None:
                actor_link = response.urljoin(actor_link)  

            yield scrapy.Request(actor_link, callback = self.parse_actor_page)


    def parse_actor_page(self, response):

        actor_name = response.css("h1.header span.itemprop::text").get()
 
        for movie in response.css("div.filmo-category-section div.filmo-row"):
        
            movie_name = [movie.css("b a::text").get()]

            yield {
                   "actor" : actor_name, 
                   "movie_name" : movie_name
            }


