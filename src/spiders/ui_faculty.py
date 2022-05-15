import sys
sys.path.insert(0, '.')
from scrapy.linkextractors import LinkExtractor
import scrapy, json
from furl import furl
from scripts.get_sitemaps import GetURLFromSitemap
from datetime import datetime
from src.items import ProfscraperItem

class UniversitySpider(scrapy.Spider):
    name = 'ui_faculty'

    custom_settings = {
        "ITEM_PIPELINES":{
        "src.pipelines.FacultyPipeline":300
        }
    }

    def __init__(self):
        self.sitemap_extractor = GetURLFromSitemap()
        self.link_extractor = LinkExtractor()

    def start_requests(self):
        url = "https://www.uidaho.edu/sitemap.xml"
        get_all_url = self.sitemap_extractor.get_sitemaps(url)
        initial_meta = {}
        for link in get_all_url:
            if ('people/' in link or 'faculty' in link) and '/ambassador' not in link and '/emeriti/' not in link:                
                yield scrapy.Request(url=link, callback=self.extract_faculty, meta=initial_meta)

    def extract_faculty(self, response):
        profile = response.xpath("//div[@class='ui-obj-person-profile row']").get()
        profile_exists = True if profile else False
        prof_in_profile = 'professor' in profile.lower() if profile else False
        is_faculty = all([profile_exists, prof_in_profile])
        if not is_faculty:
            return

        department = self.extract_department(response)
        google_scholar = self.extract_google_scholar(response)
        name = self.extract_name(response)

        item = ProfscraperItem()
        item['name'] = name
        item['department'] = department
        item['google_scholar'] = google_scholar
        item['scraped_date'] = datetime.today().strftime('%Y-%m-%d')
        item['link']=response.url
        item['html_profile'] = profile

        yield item

    def extract_google_scholar(self, response):
        all_links = self.link_extractor.extract_links(response)
        for link in all_links:
            if '//scholar.google' in link.url:
                return link.url
        return None
    
    def extract_name(self, response):
        try:
            name = response.xpath("//h2[@class='profile-heading']/text()").get()
            name = ' '.join(name.split())
            if name:
                return name
        except:
            return None
        
    def extract_department(self, response):
        try:
            name = response.xpath("//div[@class='ui-contain']/h2/a/text()").get()
            name = ' '.join(name.split())
            if name:
                return name
        except:
            return None

    # def get_all_dept(self, response):
    #     item = ProfscraperItem()
    #     partial_dept_link = response.css("a.learn-more::attr(href)").get()
    #     full_url = response.urljoin(partial_dept_link)
    #     item['dept_url'] = full_url

    # def extract_faculty(self, response):
    #     department = response.xpath("//div[@class='ui-contain']/h2/a/text()").get()
    # def faculty_text_confirmation(self, response):

    #//a[@class='profile-link']
    # //div[@class='ui-obj-person-profile row']

    # def start_requests(self):
    #     with open('items.jl', 'r') as all_dept_link_file:
    #         all_dept_links = list(all_dept_link_file)
        
    #     for json_str in all_dept_links[3:4]:
    #         # print('json str: ', json.loads(json_str))
    #         url = json.loads(json_str)['dept_url']
    #         yield scrapy.Request(url, callback=self.process_links)

    # def process_links(self, response):
    #     le = LinkExtractor()
    #     all_links = le.extract_links(response)

    #     for link in all_links:
    #         profile = []
    #         full_link = response.urljoin(link.url)
    #         parsed_url = furl(full_link)
    #         parsed_url.fragment=None
    #         full_link = parsed_url.url
    #         profile = response.xpath("//div[@class='ui-obj-person-profile row']").getall()
    #         if 'people' in full_link and len(profile)==0:
    #             yield scrapy.Request(url=full_link, callback=self.process_links)
    #         # if response.css('div.ui-obj-person-profile row') and 'people/' in full_link:
    #         #     print('full_link:', full_link)
    #         # if len(profile)==0:
    #         #     print('\n\n profile: ', profile, full_link)
    #         if len(profile)>0 and 'people/' in full_link:
    #             print('\n full_link:', full_link)
    #             # profile = []

    # def get_dept_directory(self, response):
    #     all_page_content = response.css("div.ui-page-content")
    #     all_links = all_page_content.css('a::attr(href)').getall()
    #     for link in all_links:
    #         full_url = response.urljoin(link)
    #         yield scrapy.Request(full_url, callback=self.get_all_dept)


    # def get_all_dept(self, response):
    #     item = ProfscraperItem()
    #     partial_dept_link = response.css("a.learn-more::attr(href)").get()
    #     full_url = response.urljoin(partial_dept_link)
    #     item['dept_url'] = full_url

    #     yield item

        