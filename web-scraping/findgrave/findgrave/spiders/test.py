"""
scrapy example
scraping data from findgrave website
"""

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from findgrave.items import FindgraveItem
from scrapy.http import Request
import re

# Parsing html tags
def html_tags(line):
	p = re.compile(r'<.*?>')
	return p.sub('', line)

def parsing_description(line):
	# Extracting a description
	start = line.index("<br>")+4
	end = line.index("<br><a")
	line = line[start:end]

	return html_tags(line)

# Defining Spider
# Scraping information from a domain
class MySpider(BaseSpider):
	name = "findgrave" # Spider's unique identifier
	allowed_domains = ["findagrave.com."]

	# Searching non-profit jobs in Washington DC.
	# start_urls = ["http://findagrave.com./php/famous.php?page=state&FSstateid=832"]
	start_urls = ["http://findagrave.com./tocs/geographic.html"]

	# look into the front page and crawl into every country and state
	def parse(self, response):

		hxs = HtmlXPathSelector(response)
		# titles = hxs.select("//span[@class='pl']")
		
		titles = hxs.select("//tr")
		
		for titles in titles:
			title = titles.select("//td")
			for t in title:
				links = t.select("a/@href").extract()
				countries = t.select("a/text()").extract()

				for i in range(len(links)):
					country = countries[i]
					yield Request("http://findagrave.com.{}".format(links[i]), callback=self.parse_page)

	# parsing the data and save them into an item dictionary
	def parse_page(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.select("//ul/li")

		items = []
		
		for titles in titles:
			item = FindgraveItem()

			# Extract title and clean out html codes
			item["title"] = titles.select("string(a/b)").extract()
			item["link"] = titles.select("a/@href").extract()[0]
			item["description"] = parsing_description(titles.extract())
			item["country"] = html_tags(titles.select("//font").extract()[1])
			items.append(item)
		return items