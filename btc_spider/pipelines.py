# -*- coding: utf-8 -*-

import psycopg2
import logging
from scrapy.exceptions import NotConfigured


class BtcSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class DatabasePipeline(object):

    def __init__(self, db, user, passwd, host='', port=''):
        self._logger = logging.getLogger(__name__)
        try:
            self.conn = psycopg2.connect(dbname=db, user=user,
                                         password=passwd, host=host, port=port)
            self.cur = self.conn.cursor()
        except psycopg2.OperationalError:
            self._logger.exception('Error connecting to database!')
            self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        if not db_settings:
            raise NotConfigured
        db = db_settings['db']
        user = db_settings['user']
        password = db_settings['password']
        host = db_settings['host']
        return cls(db, user, password, host)

    def process_item(self, item, spider):
        self.cur.execute("INSERT INTO selling (position, seller_name, payment_method,"
                         " payment_bank, price, limit_from, limit_to, currency,"
                         "email_confirmed_date, phone_confirmed_date, partners_confirmed) "
                         "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (item['position'], item['seller_name'], item['payment_method'],
                          item['payment_bank'], item['price'], item['limit_from'],
                          item['limit_to'], item['currency'], item['email_confirmed_date'],
                          item['phone_confirmed_date'], item['partners_confirmed'])
                         )
        self.conn.commit()
        return item

