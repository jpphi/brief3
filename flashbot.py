#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:40:18 2020

@author: jpphi
"""

# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

from pprint import pprint


class FlashbotSpider(scrapy.Spider):
    name = 'flashbot'
    allowed_domains = ['rss.jobsearch.monster.com']

    # Start the crawler at this URLs
    start_urls = ['file:///home/jpphi/Documents/brief/brief3-bddNosql/rssquery.xml']
    #start_urls = ['http://localhost:8888/view/Documents/brief/brief3-bddNosql/rssquery.ashx.xml']
    #start_urls = ['http://rss.jobsearch.monster.com/rssquery.ashx?q={query}']

    thesaurus = ["machine learning", "machine", "learning", "big data", "big", "data"]

    LOG_LEVEL = "INFO"

    def parse(self, response):

        # We stat with this url
        url = self.start_urls[0]

        # Build and send a request for each word of the thesaurus
        for query in self.thesaurus:
            target = url.format(query=query)
            print("fetching the URL: %s" % target)
            if target.startswith("file://"):
                r = Request(target, callback=self.scrapit, dont_filter=True)
            else:
                r = Request(target, callback=self.scrapit)
            r.meta['query'] = query
            yield r

    def scrapit(self, response):
        query = response.meta["query"]

        # Base item with query used to this response
        item = {"query": query}
        print(query, response)

        # Scrap the data
        for doc in response.xpath("//item"):
            item["title"] = doc.xpath("title/text()").extract()
            item["description"] = doc.xpath("description/text()").extract()
            item["link"] = doc.xpath("link/text()").extract()
            item["pubDate"] = doc.xpath("pubDate/text()").extract()
            item["guid"] = doc.xpath("guid/text()").extract()
            #pprint(item, indent=2)
            print("item scraped:", item["title"])
            yield item