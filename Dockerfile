FROM python:3

COPY . ./

WORKDIR ./btc_spider

RUN pip install scrapy

RUN pip install psycopg2

RUN pip install scrapy-splash

CMD [ "scrapy", "crawl", "localbitcoins" ]

