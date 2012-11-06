Poll Scraper
============

Goals
-----
Automate the data importation portion of the Election Prediction project.

Installation
------------
0. Use github to clone the repo.
(in the clone's directory)
1. Use virtualenv to create a virtual environment.
2. Use pip to install the requirements.txt file: pip install -r requirements.txt

Scraping
--------
The Spiders build a CSV of the latest presidential polls since it was last run,
so it is important to run the spider any time that the numbers are ran in order
to keep it up to date.

To run it for the Presidential 2012 Polls:
    1. cd into the base directory: `git/RCP-Poll-Scraper/`
    2. Run `scrapy crawl pres2012`
    3. Check the output in `data/pres2012_latest.csv`

To run it for the Senate 2012 Polls:
    1. cd into the base directory: `git/RCP-Poll-Scraper/`
    2. Run `scrapy crawl senate2012`
    3. Check the output in `data/senate2012_latest.csv`

If you experience any errors, please email Taylor.  Don't delete any of the
files in `data/` or `logs/` so he can diagnose the issue.
