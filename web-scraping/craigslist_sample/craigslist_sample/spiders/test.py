"""
scrapy example
scraping craiglist sample items
The following script is from 
	http://mherman.org/blog/2012/11/05/scraping-web-pages-with-scrapy/#.V6obSfkrL4Y
"""

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from craigslist_sample.items import CraigslistSampleItem

# Defining Spider
# Scraping information from a domain
import pprint

class MySpider(BaseSpider):
    name = "craig" # Spider's unique identifier
    allowed_domains = ["craigslist.org"]

    # Searching non-profit jobs in Washington DC.
    start_urls = ["http://washingtondc.craigslist.org/search/npo?query=intern"]

    def parse(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.select("//span[@class='pl']")
		items = []
		print "\n-----------------------------------"
		pprint.pprint(titles)
		for titles in titles:
			item = CraigslistSampleItem()
			# Extract title and clean out html codes
			item["title"] = titles.select("string(a/span[@id='titletextonly'])").extract()
			item["link"] = titles.select("a/@href").extract()
			items.append(item)
		return items