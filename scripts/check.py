import requests, scrapy

url = 'https://www.uidaho.edu/sci/mathstat/our-people/faculty/markn'
# url = 'https://www.uidaho.edu/caa/programs/interior-architecture-and-design/our-people/rula-awwad-rafferty'
response = requests.get(url)

_selector = scrapy.Selector(text=response.content)

# a = _selector.xpath("//div[@class='ui-obj-location-container']").getall()
# for i in a:
#     contact_info = scrapy.Selector(text=i).xpath("//div[@class='contact-info']").getall()
#     if contact_info:
#         web_info = scrapy.Selector(text=i).xpath("//div/p").getall()
#         for j in web_info:
#             a_tag = scrapy.Selector(text=j).xpath("//a").get()
#             if a_tag:
#                 t = scrapy.Selector(text=j).xpath("//p/text()").get()
#                 if 'web' in t.lower():
#                     yu_tag = scrapy.Selector(text=a_tag).xpath("//a/text()").get()
#                     print(yu_tag)

a = _selector.xpath("//div[@class='ui-contain']/h2/a/text()").get()
print("\n haha a: ", a)