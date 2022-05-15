from lxml import etree
import requests


class GetURLFromSitemap:
    def get_sitemaps(self, url):
        all_links = set()
        try:
            r = requests.get(url)
            root = etree.fromstring(r.content)
            for sitemap in root:
                children = sitemap.getchildren()
                print("\n children: ", children, '\n')
                all_links.add(children[0].text)
            return list(all_links)
        except Exception as e:
            print('ERROR getting url from sitemap: ', e)
        return None