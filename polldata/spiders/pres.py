from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.item import Item
from scrapy import log

from polldata.items import PresPollItem

class PresSpider(CrawlSpider):
    name = "pres2012"
    allowed_domains = ["realclearpolitics.com"]
    start_urls = [
        "http://www.realclearpolitics.com/epolls/latest_polls/president/"
    ]
    fields_to_export = ['state', 'service', 'end', 'sample', 'voters', 'dem', 'rep', 'ind']

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
            # follow=None, # default 
            process_links='processLinks',
            process_request='processRequest',
        ),
    )


    def parseStatePolls(self, response):
        items = []
        hxs = HtmlXPathSelector(response)

        state = hxs.select('//*[@id="main-poll-title"]/text()').extract()[0].split(':')[0]
        polls = hxs.select('//*[@id="polling-data-full"]/table/tr[not(@class) or @class="isInRcpAvg"]')

        for poll in polls:
            polldata = poll.select('td/text() | td/a/text()')

            item = PresPollItem()
            item['state'] = state
            item['service'] = polldata[0].extract()

            daterange = polldata[1].extract().split(' - ')
            # BugFix w/ If Statement
            #  - Preventative, based on the BugFix for sampleInfo (see below)
            #  - Prevents errors when either the start or end dates is missing,
            #    thus there is only one component in sampleInfo.
            if len(daterange) > 1:
                item['start'] = daterange[0] + '/2012'
                item['end']  = daterange[1] + '/2012'
            else:
                item['start'] = ''
                item['end'] = daterange[0] # most important, so it gets any content

            sampleInfo      = polldata[2].extract().split(' ')
            # BugFix w/ If Statement
            #  - Prevents errors when either the sample size or the sample type
            #       (RV: registered voters, or LV: likely voters)
            #    is missing, thus there is only one component in sampleInfo.
            if len(sampleInfo) > 1:
                item['sample']  = sampleInfo[0]
                item['voters']  = sampleInfo[1]
            else:
                item['sample'] = sampleInfo[0]
                item['voters'] = ''

            # TODO: check if first is left or right
            item['dem']     = polldata[4].extract()
            item['rep']     = polldata[5].extract()
            # item['ind']     = polldata[0].extract()
            # Calculating ind
            #   * ind = polldata[5] (use if it exists)?
            #   * ind = 100 - dem - rep?
            item['ind']     = 0

            # TODO: check if end date is after current 'last checked' date
            items.append(item)

        return items

    # filters out repeat state poll links
    # ie only get new polls from Ohio once
    def processLinks(self, links):
        return links

    # filters out states that don't have any polling data
    # probably shouldn't worry about this as all latest poll states will have a poll
    # TODO: remove this function and process_request filed from Rules
    def processRequest(self, request):
        return request
