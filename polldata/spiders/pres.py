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
    states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District Of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'PALAU', 'Pennsylvania', 'PUERTO RICO', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
    statesAbv = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY']

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

        lookup = self._getDataPositions( hxs.select('//*[@id="polling-data-full"]/table/tr[1]/th/text()').extract() )

        state = hxs.select('//*[@id="main-poll-title"]/text()').extract()[0].split(':')[0]
        polls = hxs.select('//*[@id="polling-data-full"]/table/tr[not(@class) or @class="isInRcpAvg"]')

        for poll in polls:
            polldata = poll.select('td/text() | td/a/text()')

            item = PresPollItem()
            item['state'] = state
            item['service'] = polldata[ lookup['service'] ].extract()

            daterange = self._parsePollDates(polldata[ lookup['date'] ].extract())
            item['start'] = daterange[0]
            item['end']  = daterange[1]

            sampleInfo = self._parseSampleInfo(polldata[ lookup['sample'] ].extract())
            item['sample']  = sampleInfo[0]
            item['voters']  = sampleInfo[1]

            item['dem']     = polldata[ lookup['dem'] ].extract()
            item['rep']     = polldata[ lookup['rep'] ].extract()
            # item['ind']     = polldata[0].extract()
            # Calculating ind
            #   * ind = polldata[5] (use if it exists)?
            #   * ind = 100 - dem - rep?
            #   *   what about undecideds? 
            item['ind']     = 0

            items.append(item)

        return items

    def _getDataPositions(self, headers):
        lookup = {}

        i = 0
        for header in headers:
            print '"' + str(header) + '"'
            if header == "Poll":
                lookup["service"] = i
            elif header == "Date":
                lookup["date"] = i
            elif header == "Sample":
                lookup["sample"] = i
            elif header == "MoE":
                lookup["error"] = i
            elif header == "Romney (R)":
                lookup["dem"] = i
            elif header == "Obama (D)":
                lookup["rep"] = i

            i += 1

        return lookup

    def _parsePollDates(self, dateText):
        daterange = dateText.split(' - ')

        # BugFix w/ If Statement and Array Resize
        #  - Preventative, based on the BugFix for _parseSampleInfo (see below)
        #  - Prevents errors when either the start or end dates is missing,
        #    so there is only one component in sampleInfo.
        if len(daterange) > 1:
            daterange[0] += '/2012' # start
            daterange[1] += '/2012' # end
        else:
            daterange.resize(2)
            daterange[0] = '' # start
            daterange[1] = daterange[0] + '/2012' # end

        return daterange

    def _parseSampleInfo(self, sampleInfoText):
        sampleInfo = sampleInfoText.split(' ')

        # BugFix w/ If Statement
        #  - Prevents errors when either the sample size or the sample type
        #       (RV: registered voters, or LV: likely voters)
        #    is missing, thus there is only one component in sampleInfo which
        #    is assumed to be the sample size.
        if sampleInfo[0] is None:
            sampleInfo[0] = ''

        if len(sampleInfo) < 2:
            sampleInfo.resize(2)
            sampleInfo[1] = ''

        return sampleInfo

    # filters out repeat state poll links
    # ie only get new polls from Ohio once
    def processLinks(self, links):
        return links

    # filters out states that don't have any polling data
    # probably shouldn't worry about this as all latest poll states will have a poll
    def processRequest(self, request):
        return request
