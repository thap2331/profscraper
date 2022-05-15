import scrapy, json
from src.items import ProfscraperItem
from datetime import datetime

class UIUniSpider(scrapy.Spider):
    name = 'uidaho_uni'
    custom_settings = {
        "src.pipelines.DepartmentPipeline":300
    }

    all_dept_links = set()

    def start_requests(self):
        initial_meta={}
        url, json_line = self.get_dep_url(name="University_of_Idaho")
        initial_meta['id'] = json_line['id']
        initial_meta['name'] = json_line['name']
        yield scrapy.Request(url, callback=self.get_dept_directory, meta=initial_meta)

    def get_dept_directory(self, response):
        all_page_content = response.css("div.ui-page-content")
        all_links = all_page_content.css('a::attr(href)').getall()
        for link in all_links:
            full_url = response.urljoin(link)
            yield scrapy.Request(full_url, callback=self.get_all_dept, meta=response.meta)

    def get_all_dept(self, response):
        item = ProfscraperItem()
        partial_dept_link = response.css("a.learn-more::attr(href)").get()
        full_url = response.urljoin(partial_dept_link)
        item['dept_url'] = full_url
        item['name'] = response.meta['name']
        item['scraped_date'] = datetime.today().strftime('%Y-%m-%d')

        yield item

    def get_dep_url(self, name=None):
        with open('database/dept_finder.jl', 'r') as all_dept_link_file:
            all_links = list(all_dept_link_file)
        for json_str in all_links:  
            if json.loads(json_str)['name']==name:      
                url = json.loads(json_str)['find_dep_url']
                return url, json.loads(json_str)

        return None, None