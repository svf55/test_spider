import re
import logging
from urllib.parse import urljoin
from decimal import Decimal
from scrapy.spiders import CrawlSpider
from scrapy_splash import SplashRequest
from btc_spider.items import AdItem
from datetime import datetime

logger = logging.getLogger(__name__)

class LocalbitcoinsSpider(CrawlSpider):
    name = "localbitcoins"
    allowed_domains = ["localbitcoins.net", "splash"]
    start_urls = [
        'https://localbitcoins.net/buy-bitcoins-online/rub/?page=1',
    ]
    visited_urls = []

    def parse(self, response):

        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
            for ad_row in response.xpath('//tr[@class="clickable"]'):
                item = AdItem()

                position_url = ad_row.xpath('.//td[@class="column-button"]/a/@href').extract_first()
                price_txt = ad_row.xpath('.//td[contains(@class, "column-price")]/text()').extract_first().strip()
                limit_txt = ad_row.xpath('.//td[@class="column-limit"]/text()').extract_first().strip()
                item['position'] = position_url.split('/')[2]
                item['payment_method'] = ad_row.xpath('.//td[not(contains(@class, "column-user"))'
                                                      'and not(contains(@class, "column-button"))]'
                                                      '/a/text()').extract_first().strip()[:-1]
                regex = r'[^a-zA-Zа-яА-Я\d _(),.-]'
                payment_bank_txt = re.sub(regex, ' ',
                                          ad_row.xpath('.//td/text()').extract()[4].strip()).strip()
                item['payment_bank'] = re.sub(r'\s+', ' ', payment_bank_txt)
                item['price'] = Decimal(price_txt.split()[0].replace(',', ''))
                item['currency'] = price_txt.split()[1]
                item['limit_from'] = Decimal(limit_txt.split()[0].replace(',', ''))
                item['limit_to'] = Decimal(limit_txt.split()[2].replace(',', ''))

                seller_url = 'https://localbitcoins.net' + ad_row.xpath('.//td[@class="column-user"]/a/@href').extract_first()
                yield self._create_profile_request(seller_url, item)

            next_pages = response.xpath('//ul[@class="pagination"]/li[not(contains(@class, "active"))]/a/@href').extract()
            next_page = next_pages[-1]
            next_page_url = urljoin(response.url, next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def _create_profile_request(self, profile_url, item):
        script = """
                 function wait_for_element(splash, css, maxwait)
                     if maxwait == nil then
                         maxwait = 10
                     end

                     return splash:wait_for_resume(string.format([[
                         function main(splash) {
                             var selector = '%s';
                             var maxwait = %s;
                             var end = Date.now() + maxwait*1000;

                             function check() {
                                 if(document.querySelector(selector)) 
                                     {
                                         splash.resume('Element found');
                                     } 
                                 else 
                                     if(Date.now() >= end) 
                                         {
                                             var err = 'Timeout waiting for element';
                                             splash.error(err + " " + selector);
                                         } 
                                         else {
                                                  setTimeout(check, 200);
                                              }
                             }

                             check();
                         }
                     ]], css, maxwait))  
                 end

                 function main(splash, args)
                     splash:go(splash.args.url)
                     assert(splash:wait(6))
                     wait_for_element(splash, "abbr")    
                     return splash:html()
                 end

                 """

        return SplashRequest(
            profile_url, self._parse_profile, endpoint='execute',
            meta={'item': item, 'seller_url': profile_url},
            args={'lua_source': script, 'timeout': 90}
        )

    def _parse_profile(self, response):
        item = response.meta['item']
        if not response.body:
            logger.info('Reload the page again: {}'.format(response.meta['seller_url']))
            seller_url = response.meta['seller_url']
            yield self._create_profile_request(seller_url, item)
            return

        item['seller_name'] = response.xpath('//h1/text()').extract_first().strip()
        email_confirmed_date_txt = response.xpath('//div[@id="email_verified_row"]/'
                                                  'div[@class="col-md-6 profile-value"]/'
                                                  'abbr/@title').extract_first()
        if email_confirmed_date_txt:
            item['email_confirmed_date'] = datetime.strptime(email_confirmed_date_txt[:10], '%Y-%m-%d').date()
        else:
            item['email_confirmed_date'] = None
        phone_confirmed_date_txt = response.xpath('//div[@id="phone_verified_row"]/'
                                                  'div[@class="col-md-6 profile-value"]/'
                                                  'abbr/@title').extract_first()
        if phone_confirmed_date_txt:
            item['phone_confirmed_date'] = datetime.strptime(phone_confirmed_date_txt[:10], '%Y-%m-%d').date()
        else:
            item['phone_confirmed_date'] = None
        partners_confirmed_list = response.xpath('//div[@id="confirmed_trades_row"]/'
                                                 'div[@class="col-md-6 profile-value"]/'
                                                 'strong/text()').extract()
        item['partners_confirmed'] = int(partners_confirmed_list[1]) if partners_confirmed_list else None

        yield item

