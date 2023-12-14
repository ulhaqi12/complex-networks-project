# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ActorItem(scrapy.Item):
    actor_name = scrapy.Field()
    number_of_movies = scrapy.Field()
    date_of_birth = scrapy.Field()
    awards_won = scrapy.Field()
    awards_nominee = scrapy.Field()
    movies = scrapy.Field()