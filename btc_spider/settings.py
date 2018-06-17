# -*- coding: utf-8 -*-

BOT_NAME = 'btc_spider'
SPIDER_MODULES = ['btc_spider.spiders']
NEWSPIDER_MODULE = 'btc_spider.spiders'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 3
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS_PER_IP = 1
ITEM_PIPELINES = {
   'btc_spider.pipelines.BtcSpiderPipeline': 300,
   'btc_spider.pipelines.DatabasePipeline': 301,
}
DB_SETTINGS = {
        'db': 'postgres',
        'user': 'postgres',
        'password': '',
        'host': 'db',
        'port': 5432,
}
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
SPLASH_URL = 'http://splash:8050/'

