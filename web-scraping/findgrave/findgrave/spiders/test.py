"""
scrapy example
scraping data from findgrave
"""

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from findgrave.items import FindgraveItem
from scrapy.http import Request

# Defining Spider
# Scraping information from a domain
import pprint
import re

def parsing_description(line):
	# Extracting a description
	start = line.index("<br>")+4
	end = line.index("<br><a")
	line = line[start:end]

	# parsing html tags
	p = re.compile(r'<.*?>')

	return p.sub('', line)

class MySpider(BaseSpider):
    name = "findgrave" # Spider's unique identifier
    allowed_domains = ["findagrave.com."]

    # Searching non-profit jobs in Washington DC.
    # start_urls = ["http://findagrave.com./php/famous.php?page=state&FSstateid=832"]
    start_urls = ["http://findagrave.com./tocs/geographic.html"]

    def parse(self, response):
		hxs = HtmlXPathSelector(response)
		# titles = hxs.select("//span[@class='pl']")
		
		titles = hxs.select("//tr")
		
		for titles in titles:
			title = titles.select("//td")
			for t in title:
				print "\n::::::::::::::::::::::::::::::::::::::::"
				links = t.select("a/@href").extract()
				countries = t.select("a/text()").extract()
				if links:
					print dict(zip(countries,links))
					for link in links:
						print "\n\n"
						print "http://findagrave.com.{}".format(link)
						yield Request("http://findagrave.com.{}".format(link), callback=self.parse_page)


    def parse_page(self, response):
		hxs = HtmlXPathSelector(response)
		# titles = hxs.select("//span[@class='pl']")
		
		titles = hxs.select("//ul/li")

		items = []
		
		for titles in titles:
			item = FindgraveItem()
			# Extract title and clean out html codes
			item["title"] = titles.select("string(a/b)").extract()
			item["link"] = titles.select("a/@href").extract()[0]
			item["description"] = parsing_description(titles.extract())
			print "\n---------------parse_data------------------"
			print item
			items.append(item)
		return items