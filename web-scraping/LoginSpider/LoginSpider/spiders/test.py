"""
scrapy example
attempted to crawl into github but unfortunenately
it is forbidden by https://github.com/robots.txt
"""

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from LoginSpider.items import LoginspiderItem

from scrapy.http import Request, FormRequest
from scrapy.contrib.spiders.init import InitSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import Rule

# Defining Spider
# Scraping information from a domain
import pprint

class MySpider(InitSpider):
    name = "login" # Spider's unique identifier
    allowed_domains = ["github.com"]

    # Accessing login page of Github.
    login_user = "wonjunee"
    login_pass = "asdf1234"
    login_page = "https://github.com/login"
    start_urls = ["https://github.com/new"]
    
    rules = (
        Rule(SgmlLinkExtractor(allow=r'-\w+.html$'),
             callback='parse_item', follow=True),
    )

    def init_request(self):
        """This function is called before crawling starts."""
        return Request(url=self.login_page, callback=self.login)

    def login(self, response):
        """Generate a login request."""
        return FormRequest.from_response(response,
                    formdata={'name': login_user, 'password': login_pass},
                    callback=self.check_login_response)

    def check_login_response(self, response):
        """Check the response returned by a login request to see if we are
        successfully logged in.
        """
        self.log("---------------------------------------------")
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