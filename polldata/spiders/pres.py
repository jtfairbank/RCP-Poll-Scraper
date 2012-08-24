from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from scrapy import log

class PresSpider(CrawlSpider):
    name = "pres2012"
    allowed_domains = ["realclearpolitics.com"]
    start_urls = [
        "http://www.realclearpolitics.com/epolls/latest_polls/president/"
    ]

    rules = (
        Rule(
            SgmlLinkExtractor(
                allow=(r"epolls/2012/president/[a-z]{2}/[a-z]+_romney_vs_obama-[0-9]{4}\.html"),
                # Regex explanation:
                #     [a-z]{2} - matches a two character state abbreviation
                #     [a-z]*   - matches a state name
                #     [0-9]{4} - matches a 4 number unique webpage identifier

                allow_domains=('realclearpolitics.com',),
            ),
            callback='parseStatePolls',
            process_links='processLinks',
            process_request='processRequest',
        ),
    )


    def parseStatePolls(self, response):
        self.log('Hi, this is an item page! %s' % response.url, level=log.DEBUG)
        pass

    # filters out repeat state poll links
    # ie only get new polls from Ohio once
    def processLinks(self, links):
        print links
        return links

    # filters out states that don't have any polling data
    # probably shouldn't worry about this as all latest poll states will have a poll
    # TODO: remove this function and process_request filed from Rules
    def processRequest(self, request):
        return request
