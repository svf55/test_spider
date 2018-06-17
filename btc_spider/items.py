# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AdItem(scrapy.Item):
    position = scrapy.Field()
    payment_method = scrapy.Field()
    payment_bank = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    limit_to = scrapy.Field()
    limit_from = scrapy.Field()
    seller_name = scrapy.Field()
    email_confirmed_date = scrapy.Field()
    phone_confirmed_date = scrapy.Field()
    partners_confirmed = scrapy.Field()

