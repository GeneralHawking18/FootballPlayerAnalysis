from playwright.sync_api import sync_playwright
import json
from playwright_stealth import stealth_sync
import pandas as pd
import io_utils
import crawler
    


"""class Widget():
    def __init__(self, list):
        self.list = list

    def """
# def read_category()
class whoscoredScrapper():
    def __init__(self):
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless = False)
        self.page = self.browser.new_page()
        stealth_sync(self.page)
        self.read_category_dict()

    def read_category_dict(self):
        self.category_dict = io_utils.read_json(file_name = 'categories')

    def scrape_stats_from_url(self, url):
        self.page.goto(url)
        json_text = self.page.query_selector("body").text_content()
        parsed_dict = json.loads(json_text)
        stats_dict = parsed_dict["playerTableStats"]

        stats_df_of_url = pd.DataFrame.from_dict(stats_dict)

        return stats_df_of_url
    
    def scrape_stats_from_parsed_json_list(self, stats_urls_list):   
        stats_df_of_all_urls = pd.DataFrame()


        for positionCode, urls_list in stats_urls_list.items():
            counter1 = 0
            for url in urls_list:
                counter1 += 1
                print("{}/{}".format(counter1, len(urls_list)))
                stats_df_current_url = self.scrape_stats_from_url(url = url)
                stats_df_current_url['positionCode'] = positionCode
                
                # Append dataframe
                stats_df_of_all_urls = pd.concat(objs = [stats_df_of_all_urls, stats_df_current_url], axis = 0)     
            


        """sub_or_not_df = pd.DataFrame(
                data = stats_df_current_url.playerId * 0 + substitution_or_not, 
                columns = ['substituitonPos']
        )
        stats_df_of_all_urls = pd.concat(objs = [stats_df_of_all_urls, sub_or_not_df], axis = 1)\
        
                             
        stats_df_of_all_urls['positionCode'] = position"""

        return stats_df_of_all_urls

    
    def scrape_all_stats(self):

        for category in list(self.category_dict.keys())[-1: ]:
            for subcategory in self.category_dict[category]:
                stats_urls_list = io_utils.read_json(file_name = 'urls_data/{}_{}'.format(category, subcategory))
                stats_df_of_all_urls = self.scrape_stats_from_parsed_json_list(stats_urls_list)
                
                io_utils.to_csv(df = stats_df_of_all_urls,file_name = 'stats_{}_{}'.format(category, subcategory))
        
    





def extract_stats_to_csv():
    # df = pd.DataFrame()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless = False)
        page = browser.new_page()  
        stealth_sync(page)

        # Export category value from json
        category_dict = io_utils.read_json(file_name = 'categories')
        counter1 = 0
        for category in category_dict.keys():
            counter1 += 1
            print("Category of {} {}/{}:".format(category, counter1, len(category_dict)))

            for subcategory in category_dict[category]:
                print(" - Subcategory - {}".format(subcategory))
                stats_urls = io_utils.read_json("urls_data/{}_{}".format(category, subcategory))
        
                counter2 = 0
                df = pd.DataFrame()
                for stats_url in stats_urls:
                    counter2 += 1
                    print("\tStep {}/{}".format(counter2, len(stats_urls)))
                    page.goto(stats_url)
                    
                    json_text = page.query_selector('body').text_content()
                    json_parsing = json.loads(json_text)
                    stats = json_parsing["playerTableStats"]

                    df_new = pd.DataFrame.from_dict(stats) 
                    df = pd.concat(objs = [df, df_new], axis = 0)
                io_utils.to_csv(df = df, file_name = "stats_{}_{}".format(category, subcategory))
        


    

if __name__ == "__main__":
    # df = crawl_to_dataframe()
    # extract_stats_to_csv()
    # io_utils.to_csv(df = df, file_name = 'test')
    scrapper = whoscoredScrapper()
    scrapper.scrape_all_stats()
    




