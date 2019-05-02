import scrapy
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from regelwikiparser.items import SpecialAbilityItem
from properties_parser import PropertiesParser
import json
import logging

class FightAbilities(scrapy.Spider):
    name = "abilities"
    allowed_domains = ["ulisses-regelwiki.de"]
    base_url = "http://www.ulisses-regelwiki.de/index.php/"

    # load the spell infos from a file
    specialability_file = "specialabilityclassinfo.json"
    with open(specialability_file) as json_data:
        class_info = json.load(json_data)

    def start_requests(self):
        for ability_class, data in self.class_info.items():
            if data['active'] is 1:
                logging.info("Parsing links of " + ability_class)
                request = Request(self.base_url + data['link'],
                                  callback=self.parseNavItems)
                request.meta['type'] = ability_class
                yield request

    def parseNavItems(self, response):
        """Generator to create new requests of the start requests."""

        # The x path query to get all links inside the navigation of the site
        xpath_mod_nav = "//div[contains(@class,'ulSubMenuRTable-cell')]//a[@class='ulSubMenu']/@href"
        hxs = Selector(response=response, type="html")

        # generate the requests from the selector
        sites = hxs.xpath(xpath_mod_nav)
        for site in sites:
            url = self.base_url + site.extract()
            request = Request(url, callback=self.parseItem)
            request.meta['type'] = response.meta['type']
            yield request

    def parseItem(self, response):

        item = SpecialAbilityItem()

        # save the link
        item['link'] = response.url

        item_class = response.meta['type']
        if item_class:
            item['abilityclass'] = item_class
        else:
            logging.warning("Ability Class not found!")

        # get the important divs (can be 2)
        importantDivs = "//div[@id='main']//div[contains(@class,'ce_text')]"
        i_select = response.xpath(importantDivs)

        # create the properties parser
        pp = PropertiesParser(self.class_info[item_class], item_class)

        # extract the name
        pp.parseName(i_select, item)

        # extract the properties
        pp.parseAbility(i_select, item)

        return item