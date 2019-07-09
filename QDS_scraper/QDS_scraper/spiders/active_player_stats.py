# -*- coding: utf-8 -*-
import scrapy
from ..items import QdsScraperItem

class PlayerStatsSpider(scrapy.Spider):
    name = 'player_stats'
    start_urls = ['https://www.thescore.com/nba/events/']
    
    def parse(self, response):
        init_url = 'https://www.thescore.com/nba/events/date/'
        
        # create a date converter function
        def date_converter(year, date):
            if len(str(year)) != 4:
                raise Exception('year must be in the format of YYYY')
            date_split = date.split(" ")
            month = date_split[0]
            if len(date_split[1]) == 1:
                day = '0' + date_split[1]
            else:
                day = date_split[1]
            
            month_dict = {
                        'JAN': '01',
                        'FEB': '02',
                        'MAR': '03',
                        'APR': '04',
                        'MAY': '05',
                        'JUN': '06',
                        'JUL': '07',
                        'AUG': '08',
                        'SEP': '09',
                        'OCT': '10',
                        'NOV': '11',
                        'DEC': '12'
                    }
            return str(year) + "-" + month_dict[month] + "-" + day
    
        test_dates = [init_url + '2019-04-21']
        for date in test_dates:
            yield scrapy.Request(date, self.stats_page)

# =============================================================================
#         for date in response.css('.Header__scheduleWrap--2VDJp\
#                                   .ScrollMenuElement__heading--1Ewmh::text')\
#                                   .extract():
#             conv_date = date_converter(2019, date)
#             new_url = init_url + conv_date
#             yield scrapy.Request(new_url, self.stats_page)
# =============================================================================
    
    
    def stats_page(self, response):
        init_url = 'https://www.thescore.com'

        for href in response.css('.Layout__content--18xmE .row+ .row')\
                            .xpath('div/span/span/a/@href').extract():
            yield response.follow(init_url + href + '/stats', self.scraper)


    def scraper(self, response):
        def stat_scraper(css_query):
            return response.css(css_query + '::text').extract()
        
        items = QdsScraperItem()
        
        items['player'] = stat_scraper('.BoxScore__statLine--3Daky .BoxScore__rosterCell--1mCYH')
        items['minutes'] = stat_scraper('.BoxScore__statLine--3Daky .BoxScore__rosterCell--1mCYH+ .BoxScore__statCell--1mqbI')
        items['points'] = stat_scraper('.BoxScore__statLine--3Daky .BoxScore__statCell--1mqbI:nth-child(3)')
# =============================================================================
#         items['rebounds'] = stat_scraper()
#         items['assists'] = stat_scraper()
#         items['steals'] = stat_scraper()
#         items['blocks'] = stat_scraper()
#         items['turnovers'] = stat_scraper() 
# =============================================================================

        
        yield items

