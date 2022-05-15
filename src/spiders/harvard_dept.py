import scrapy, json
from src.items import DepartmentItem
from datetime import datetime
from scripts.get_sitemaps import GetURLFromSitemap
from scrapy.linkextractors import LinkExtractor
from furl import furl

class UIUniSpider(scrapy.Spider):
    name = 'harvard_uni'
    custom_settings = {
        "ITEM_PIPELINES": {"src.pipelines.DepartmentPipeline":300}
    }

    def __init__(self):   
        self.sitemap_extractor = GetURLFromSitemap()
        self.link_extractor = LinkExtractor()

    def start_requests(self):
        initial_meta={}
        url, json_line = self.get_dep_url(name="Harvard_University")
        initial_meta['id'] = json_line['id']
        initial_meta['name'] = json_line['name']
        get_all_url = self.sitemap_extractor.get_sitemaps(url)
        initial_meta = {}
        initial_meta['name'] = 'Harvard_University'
        for link in get_all_url:
            yield scrapy.Request(link, callback=self.get_dept_directory, meta=initial_meta)

    def get_dep_url(self, name=None):
        with open('database/dept_finder.jl', 'r') as all_dept_link_file:
            all_links = list(all_dept_link_file)
        for json_str in all_links:  
            if json.loads(json_str)['name']==name:      
                url = json.loads(json_str)['find_dep_url']
                return url, json.loads(json_str)

        return None, None

    def get_dept_directory(self, response):
        a_tag_with_link = response.css("a.c-programs-accordion-content__links__link").getall()
        for a_tag in a_tag_with_link:
            link = scrapy.Selector(text=a_tag).css('a').attrib.get('href')
            if self.should_follow(link):
                parsed_url = furl(link)
                parsed_url.path = None
                parsed_url.args = None
                link = parsed_url.url

                item = DepartmentItem()
                item['name'] = response.meta['name']
                item['department'] = ''
                item['scraped_date'] = datetime.today().strftime('%Y-%m-%d')
                item['link'] = link
                yield item

    def should_follow(self, link):
        not_follow_links = ['admission', 'handbook']
        for i in not_follow_links:
            if i in link:
                return False
        return True
