# -*- coding: utf-8 -*-
import scrapy


class StatSpiderSpider(scrapy.Spider):
    name = 'stat_spider'
    start_urls = ['http://thescore.com/']

    def parse(self, response):
        # page index represents each of the thirty teams per thescores'
        # pagination methodology
        page_index = 1
        url = 'https://www.thescore.com/nba/teams/' + str(page_index) + '/schedule'
        yield scrapy.Request(url, 
                             self.team_page)

    def team_page(self, response):
        last_year = ['Sep', 'Oct', 'Nov', 'Dec']
        
        team = response.css('.TeamBanner__teamName--3sPPZ::text').extract()[0]\
                       .split(" ")[-1]
        
        game_row_selector = '.TableRecord__record--38byC'
        all_game_rows = response.css(game_row_selector)
        
        # Loop every game for the given team
        for game in all_game_rows:
            href = game.xpath('../@href').extract()
            stats_url = 'http://thescore.com' + href[0] + '/stats'
            
            # Fix date formatting (get the correct years)
            date = game.css('.col-xs-4:nth-child(1)::text').extract()[0]
            date_split = date.split(" ")
            if date_split[0] in last_year:
                year = 2018
            else:
                year = 2019
            date_fin = date_split[1] + "-" + date_split[0] + "-" + str(year)
            
            # Setup meta data
            home = game.css('.col-xs-4:nth-child(2)::text')\
                       .extract()[0].split(" ")[0] != '@'
            opponent = game.css('.col-xs-4:nth-child(2)::text')\
                           .extract()[0].split(" ")[1]
            
            # request
            request = scrapy.Request(url=stats_url, 
                                     callback=self.stats_page,
                                     meta={
                                         'team':team,
                                         'date':date_fin,
                                         'home':home,
                                         'opponent':opponent
                                     })
    
            yield request
    
    def stats_page(self, response):
        # Split stats (ie. fgs = 4/5 to fg_made = 4 and fg_attempted = 5)
        def split_on_divide(val):
            splitted = val[0].split("/")
            return splitted[0],splitted[1]

        # Determine if scraping first table or second of stats page
        teams = response.css(".BoxScore__team--1paFP::text").extract()[1::2]
        first_in_table = teams[0].split(" ")[1] == response.meta['team']
        
        # Test if first in table or second on stats page
        if first_in_table:
            scrape_rows = '#app-container span:nth-child(1) .BoxScore__statLine--3Daky'
        else:
            scrape_rows = 'span+ span .BoxScore__boxScore--tDnlB .BoxScore__statLine--3Daky'
        
        # CSS Selectors for stats to scrape
        name_sel = ".BoxScore__rosterCell--1mCYH::text"
        min_sel = ".BoxScore__statCell--1mqbI:nth-child(2)::text"
        pts_sel = ".BoxScore__statCell--1mqbI:nth-child(3)::text"
        reb_sel = ".BoxScore__statCell--1mqbI:nth-child(4)::text"
        ast_sel = ".BoxScore__statCell--1mqbI:nth-child(5)::text"
        st_sel = ".BoxScore__statCell--1mqbI:nth-child(6)::text"
        blk_sel = ".BoxScore__statCell--1mqbI:nth-child(7)::text"
        pf_sel = ".BoxScore__statCell--1mqbI:nth-child(8)::text"
        to_sel = ".BoxScore__statCell--1mqbI:nth-child(9)::text"
        oreb_sel = ".BoxScore__statCell--1mqbI:nth-child(10)::text"
        dreb_sel = ".BoxScore__statCell--1mqbI:nth-child(11)::text"
        fg_sel = ".BoxScore__statCell--1mqbI:nth-child(12)::text"
        ft_sel = ".BoxScore__statCell--1mqbI:nth-child(14)::text"
        three_pt_sel = ".BoxScore__statCell--1mqbI:nth-child(16)::text"
        plus_min_sel = ".BoxScore__statCell--1mqbI:nth-child(18)::text"
        
        # Loops through rows to scrape and gather data
        for player in response.css(scrape_rows):
            # Split the three stats that have / like 3/5
            fg_div = player.css(fg_sel).extract()
            ft_div = player.css(ft_sel).extract()
            three_pt_div = player.css(three_pt_sel).extract()

            # Get the stats
            name = player.css(name_sel).extract()
            minutes = player.css(min_sel).extract()
            points = player.css(pts_sel).extract()
            rebounds = player.css(reb_sel).extract()
            assists = player.css(ast_sel).extract()
            steals = player.css(st_sel).extract()
            blocks = player.css(blk_sel).extract()
            fouls = player.css(pf_sel).extract()
            turnovers = player.css(to_sel).extract()
            o_boards = player.css(oreb_sel).extract()
            d_boards = player.css(dreb_sel).extract()
            fg_made, fg_att = split_on_divide(fg_div)
            ft_made, ft_att = split_on_divide(ft_div)
            three_pts_made, three_pts_att = split_on_divide(three_pt_div)
            plus_minus = player.css(plus_min_sel).extract()
            
            yield {
                'date': response.meta['date'],
                'team': response.meta['team'],
                'opponent': response.meta['opponent'],
                'home': response.meta['home'],
                'name': name,
                'minutes': minutes,
                'points': points,
                'rebounds': rebounds,
                'assists': assists,
                'steals': steals,
                'blocks': blocks,
                'fouls': fouls,
                'turnovers': turnovers,
                'o_rebounds': o_boards,
                'd_rebounds': d_boards,
                'fg_made': fg_made,
                'fg_att': fg_att,
                'ft_made': ft_made,
                'ft_att': ft_att,
                'three_pts_made': three_pts_made,
                'three_pts_att': three_pts_att,
                'plus_minus': plus_minus
            }

