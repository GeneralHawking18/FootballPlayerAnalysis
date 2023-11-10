"""
    This module aims to find out the link of the web for the scrapper.
"""
from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync

import asyncio
import json
import pandas as pd
import bs4 as bs4

import scrapy
from scrapy.selector import Selector
import io_utils


class WhoscoredCrawler(object):
    def __init__(self):
        self.root_url = 'https://1xbet.whoscored.com'
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless = False)
        self.page = self.browser.new_page()

        stealth_sync(self.page)

    def crawlCategoriesValues(self):
        """ Get all category list in select box in order to crawl""" 


        gui_stats_url_example = "https://1xbet.whoscored.com/Regions/252/Tournaments/2/Seasons/9075/Stages/20934/PlayerStatistics/England-Premier-League-2022-2023"
        # Generate statistics url by replace show with player statistics
        # gui_stats_url = season_url_example.replace("Show", "PlayerStatistics")


        self.page.goto(gui_stats_url_example)

        self.page.click('a[href="#stage-top-player-stats-detailed"]')


        self.crawlPositions()
        
        # CSS link to query option choice in option box in whoscored.
        # Query to select text
        category_items = self.page.query_selector_all('select#category > optgroup[label] > option[value]')
        


        category_dict = {category_item.get_attribute('value'): [] for category_item in category_items}

        category_choiceBox = self.page.locator('#category')
        # Choose element category_choiceBox



        for category in category_dict.keys():
            # Choose the category choice box for selecting a value for finding subcategories
            category_choiceBox.select_option(category)
            
            # Find all subcategory choice items
            subcategory_items = self.page.query_selector_all("#subcategory > option[value]")
            
            # Extract all of value in subcategory_items
            for subcategory_item in subcategory_items:
                category_dict[category].append(subcategory_item.get_attribute('value'))

        
        io_utils.to_json(category_dict, 'categories')
        return category_dict   
    

    def extractPositions(self):
        positions_item = self.page.query_selector("#positionOptions")
        positions = positions_item.get_attribute('data-value').replace("\'", "" ).split(',') 
        # Add prefix and suffix %27SUB%27
        print(positions)
        return positions
        
    
    
    def crawlPositions(self):
        positionCodes = self.extractPositions()[: -1] # exclude "%27Sub%27"


        io_utils.to_json(data = positionCodes, file_name = "positions")
        
    

    def crawlTournamementUrls(self):
        "Retrive all the tournament urls in the root url"
        self.page.goto(self.root_url)
        tournament_element_list = self.page.query_selector_all("#popular-tournaments-list > li.hover-target > a")
        tournamement_urls = [self.root_url + element.get_attribute('href') for element in tournament_element_list]
        io_utils.to_json(data = tournamement_urls, file_name = "tournament_urls")
        # return tournamement_urls

    def extractSeasonUrls(self, tournament_url, start: "int" = 2, end: "int" = 4):
        self.page.goto(tournament_url)
        season_items = self.page.query_selector_all("#seasons > option[value]")[start: end]
        season_urls = [self.root_url + season_item.get_attribute('value') for season_item in season_items]
        # io_utils.to_json(data = season_urls, file_name = 'Top5SeasonUrls')
        return season_urls


    def crawlSeasonUrls(self, start = 1, end = 4):
        tournament_urls = io_utils.read_json('tournament_urls')
        AllSeasonUrls = []


        for tournament_url in tournament_urls:
            SeasonUrls = self.extractSeasonUrls(tournament_url, start = start, end = end)
            AllSeasonUrls += SeasonUrls

        io_utils.to_json(data = AllSeasonUrls, file_name = "season_urls")

    def genStatsUrl(self, 
                    category: 'str' = "tackles",
                    subcategory: 'str' = "success", 
                    stageId: 'str' = "20934", 
                    max_n_pages: int = 1000, 
                    positionCode = 'FW'):
        url = "https://1xbet.whoscored.com/StatisticsFeed/1/GetPlayerStatistics?category={}\
&subcategory={}&statsAccumulationType=2&isCurrent=true&playerId=&teamIds=&matchId=&stageId={}&tournamentOptions=2&sortBy=Rating&sortAscending=&age=&ageComparisonType=0&appearances=&appearancesComparisonType=0&field=&nationality=\
&positionOptions=%27{}%27&timeOfTheGameEnd=5&timeOfTheGameStart=0&isMinApp=&page=1&includeZeroValues=&numberOfPlayersToPick={}"\
            .format(category, subcategory, stageId, positionCode, max_n_pages, )
        return url
    
    def extract_stageId(self, season_url):
        self.page.goto(season_url)
        print(season_url)
        link_stat_element = self.page.query_selector('#link-statistics')
        if link_stat_element:
            href = link_stat_element.get_attribute('href')
            # href = "/Regions/252/Tournaments/2/Seasons/9075/Stages/20934/TeamStatistics/England-Premier-League-2022-2023"
            stageId = href.split(sep = '/')[8]
            return stageId

    def crawlAll_stageIds(self):
        top_season_urls = io_utils.read_json(file_name = 'season_urls')
        stageIds = []
        for season_url in top_season_urls:
            stageId = self.extract_stageId(season_url)
            if stageId:
                stageIds.append(stageId)
        io_utils.to_json(data = stageIds, file_name = 'stageIds')


    def crawlStatsUrls(self):
        category_dict = io_utils.read_json(file_name = 'categories')
        stageIds = io_utils.read_json(file_name = 'stageIds')
        positionCodes = io_utils.read_json(file_name = "positions")


        for category in category_dict.keys():
            for subcategory in category_dict[category]:
                stats_urls = {} 
                for stageId in stageIds:
                        for positionCode in positionCodes:
                            stats_urls[positionCode] = stats_urls.setdefault(positionCode, [])

                            stats_url = self.genStatsUrl(
                                category = category,
                                subcategory = subcategory, 
                                stageId = stageId,
                                positionCode = positionCode
                            )


                            stats_urls[positionCode].append(stats_url)

                            
                            
                io_utils.to_json(data = stats_urls, file_name = "urls_data/{}_{}".format(category, subcategory))
        
    def crawl(self):
        # self.crawlCategoriesValues()

        # self.crawlTournamementUrls()
        
        # self.crawlSeasonUrls()
        self.crawlAll_stageIds()

        self.crawlStatsUrls()


        
        


def preprocess(script):
    new_start_pos = script.find("require.config.params['args'] = ")
    new_start_pos += (new_start_pos == -1) + len("require.config.params['args'] = ")
    return script[new_start_pos: ]
def getStageId(script):
    stageId_startpos = script.find("stageId")
    stageId_startpos += (stageId_startpos != -1) * len("stageId: ")
    stageId_endpos = script.find(",", stageId_startpos)
    return script[stageId_startpos: stageId_endpos]


def extractNavigations(tournament_url):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)

        page = browser.new_page()
        stealth_sync(page)

        page.goto(tournament_url)

        navigations = [option_item.get_attribute('value') for option_item in\
            page.query_selector_all('select#seasons > option[value]').text_content()[:5]]
        
    return 


def extractSeason(curr_url):
    with sync_playwright() as pw:
        browser =  pw.chromium.launch(headless=False)
        # context =  browser.new_context(viewport={"width": 1920, "height": 1080})
        page =  browser.new_page()
        stealth_sync(page) 

        page.goto(curr_url) 

        season_box = page.locator('select#seasons')
        option_values = [option_item.get_attribute('value') for option_item in\
            page.query_selector_all('select#seasons > option[value]').text_content()[:5]]
        print(option_items)
        for option_navigation in option_values:
            # Get the navigation of season page which is stored in option[value] 

            print(season_navigation)
            page.goto(root_url + season_navigation)
            js_relate_stageId = page.query_selector("#layout-wrapper > script").text_content()
            # print(js_relate_stageId)
            test = getStageId(script = js_relate_stageId)
            print(test)
            """js_parsed_dict = json.loads(test)
            print(js_parsed_dict['stageId'])
"""
            # season_box.select_option()

            
            
        """tournament_element_list = page.query_selector_all("#popular-tournaments-list > li.hover-target > a")
        return [root_url + element.get_attribute('href') for element in tournament_element_list]
"""

def extract_stageId(curr_url):
    with sync_playwright() as pw:
        browser =  pw.chromium.launch(headless=False)
        # context =  browser.new_context(viewport={"width": 1920, "height": 1080})
        page =  browser.new_page()
        stealth_sync(page) 

        for tournament_url in io_utils.read_json(file_name = 'tournament_urls'):
            page.goto(tournament_url)
                
            
     
        tournament_element_list = page.query_selector_all("#popular-tournaments-list > li.hover-target > a")
        return [root_url + element.get_attribute('href') for element in tournament_element_list]
    
def extractTournamementUrls(root_url):
    with sync_playwright() as pw:
        browser =  pw.chromium.launch(headless=False)
        # context =  browser.new_context(viewport={"width": 1920, "height": 1080})
        page =  browser.new_page()
        stealth_sync(page) 

        page.goto(root_url)
        
        # page.locator("#tournament-groups > li.col12-lg-3.col12-m-4.col12-s-4.col12-xs-6 > a")

        # page.click('a[href="#stage-top-player-stats-detailed"]')
        
        # tournament_box = page.locator("#popular-tournaments-list")
        tournament_element_list = page.query_selector_all("#popular-tournaments-list > li.hover-target > a")
        return [root_url + element.get_attribute('href') for element in tournament_element_list]

def selectBox(AfterFunc: 'function' = None):
    """ Select the choice in box in subcategory in choice Box
    """
    with sync_playwright() as pw:
        browser =  pw.chromium.launch(headless=False)
        # context =  browser.new_context(viewport={"width": 1920, "height": 1080})
        
        page =  browser.new_page()
        stealth_sync(page) 

        page.goto(url)
    
        page.click('a[href="#stage-top-player-stats-detailed"]')
        
        option_items = page.query_selector_all('select#category > optgroup[label] > option[value]')
        for option_item in option_items:
            choice_box = page.locator('select#category') # Locate choice box in whoscored
            curr_val = option_item.get_attribute('value')
            # print(curr_val)
            choice_box.select_option(curr_val)  
            AfterFunc()
    

def extractCategories():
    """ Get all category list in select box in order to crawl
    """ 
    categories = []
    with sync_playwright() as pw:
        browser =  pw.chromium.launch(headless=False)
        # context =  browser.new_context(viewport={"width": 1920, "height": 1080})
        
        page =  browser.new_page()
        # stealth_sync(page) 

        page.goto(url)
    
        page.click('a[href="#stage-top-player-stats-detailed"]')
        
        option_items = page.query_selector_all('select#category > optgroup[label] > option[value]')
        for option_item in option_items:
            categories.append(option_item.get_attribute('value'))

        
        return categories   

if __name__ == "__main__":
    """# io_utils.to_json(crawlToList(), file_name = 'categories')
    categories = io_utils.read_json(file_name = 'categories')
    print(categories)
    
    # tournament_urls = extractTournamementUrls(root_url)
    tournament_urls = io_utils.read_json(file_name = "tournament_urls")
    # io_utils.to_json(tournament_urls, "tournament_urls")
    crawler = WhoscoredCrawler()
    season_url = crawler.extractTop5SeasonUrls(tournament_urls[0])[0]
    print(crawler.extractStageIds(season_url))

    # extractSeason(tournament_urls[0])"""
    crawler = WhoscoredCrawler()

    crawler.crawl()