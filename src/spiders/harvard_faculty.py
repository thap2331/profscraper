import scrapy, json
from datetime import datetime
from scripts.get_sitemaps import GetURLFromSitemap
from scrapy.linkextractors import LinkExtractor
from furl import furl
from database.dept_settings import dept_settings

class HarvardFacultySpider(scrapy.Spider):
    name = 'harvard_faculty'

    def __init__(self):   
        self.sitemap_extractor = GetURLFromSitemap()
        self.link_extractor = LinkExtractor()

    def start_requests(self):
        initial_meta={}
        url_list, json_line = self.get_dep_url(name="Harvard_University")

        i = 0
        for url in url_list:
            settings = self.get_strategy(url)
            strategy = settings.get('strategy') if settings else None
            initial_meta["settings"] = settings
            if strategy and strategy=="sitemap":
                i = 1
                urls = self.sitemap_extractor.get_sitemaps(url)
                if urls:
                    for link in urls:
                        # print("\n url to make request before:", settings.get('faculty')[0], link)
                        if settings.get('faculty')[0] in link:
                            print("\n url to make request:", link)
                            yield scrapy.Request(link, callback=self.process_sitemap, meta=initial_meta)
            if i == 1:
                break

    def get_dep_url(self, name=None):
        all_links = []
        with open('database/department.jl', 'r') as all_dept_link_file:
            link_list = list(all_dept_link_file)
        for json_str in link_list: 
            if json.loads(json_str)['name']==name:     
                url = json.loads(json_str)['link']
                all_links.append(url)
        return all_links, None

    def get_strategy(self, url):
        settings = dept_settings["Harvard_University"]
        all_urls = list(settings.keys())
        webpage = None
        for link in all_urls:
            if link in url:
                webpage = link
        
        strategy = settings[webpage] if webpage else None
        return strategy

    def process_sitemap(self, response):
        print("process sitemap: ", response)
    
    def get_sitemap_url(self, url):
        parsed_url = furl(url)
        url_root = f"{parsed_url.scheme}://{parsed_url.host}/sitemap.xml"
        return url_root

