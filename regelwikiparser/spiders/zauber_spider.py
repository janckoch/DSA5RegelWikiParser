#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from regelwikiparser.items import SpellItem, SpellClassItem

class Magic(CrawlSpider):
  name = "magic"
  start_urls = ["http://www.ulisses-regelwiki.de/index.php/zauber.html"]
  allowed_domains = ["ulisses-regelwiki.de"]
  rules = (
        Rule(LinkExtractor(allow=('za_rituale\.html', 'za_zaubersprueche\.html', 'Zauber_Zaubertricks\.html' ))),
        Rule(LinkExtractor(allow=('Rit_.*\.html')), callback='parse_spell'),
        Rule(LinkExtractor(allow=('ZT_.*\.html')), callback='parse_spell'),
        Rule(LinkExtractor(allow=('ZS_.*\.html')), callback='parse_spell')
    )

  def parse_spell(self, response):

    item = SpellItem()
    item['properties'] = {}
    properties = [
      "Probe",
      "Wirkung",
      "Ritualdauer",
      "AsP-Kosten",
      "Reichweite",
      "Wirkungsdauer",
      "Zielkategorie",
      "Merkmal",
      "Verbreitung",
      "Steigerungsfaktor"
    ]

    name_query = "//*/div/h1/text()"
    selector = response.xpath(name_query)
    name = selector.extract_first()
    item['name'] = name
    item['link'] = response.url

    short = response.url.rsplit('/', 1)[-1]
    if short.startswith('Rit_'):
      item['spellclass'] = 'Ritual'
    elif short.startswith('ZT_'):
      item['spellclass'] = 'Zaubertrick'
    elif short.startswith('ZS_'):
      item['spellclass'] = 'Zauberspruch'
    else:
      print("\nERROR\n")
      print(short)

    for p in properties:
      p_query = "//*/p/strong[text() = '" + p + ":']/following-sibling::text()[1]"
      selector = response.xpath(p_query)
      item['properties'][p] = str(selector.extract()).lstrip()
    return item