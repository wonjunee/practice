"""
scrapy example
attempted to crawl into github but unfortunenately
it is forbidden by https://github.com/robots.txt
"""

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from login_gmu.items import LoginGmuItem

from scrapy.http import Request, FormRequest
from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

# Defining Spider
# Scraping information from a domain
import pprint

class MySpider(InitSpider):
    name = "logingmu" # Spider's unique identifier
    allowed_domains = ["github.com"]

    # Accessing login page of Github.

    login_page = "https://patriotweb.gmu.edu/pls/prod/twbkwbis.P_WWWLogin"
    start_urls = ["https://patriotweb.gmu.edu/pls/prod/bwskfcls.p_sel_crse_search"]
    
    rules = (
        Rule(SgmlLinkExtractor(allow=r'-\w+.html$'),
             callback='parse_item', follow=True),
    )

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
		login_user = "######"
		login_pass = "######"

		"""Generate a login request."""
		return FormRequest.from_response(response,
					formdata={'name': login_user, 'password': login_pass},
					callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        print("---------------------------------------------")
        print response.body
        if "Hi Herman" in response.body:
            self.log("Successfully logged in. Let's start crawling!")
            # Now the crawling can begin..
            self.initialized()
        else:
            self.log("Bad times :(")
            # Something went wrong, we couldn't log in, so nothing happens.

    def parse_item(self, response):

        # Scrape data from page
        pass