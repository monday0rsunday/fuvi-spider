import scrapy
import re
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from fuvi_spider.items import FuviItem

class ChatvlComSpider(CrawlSpider):
	name = "chatvl.com"
	allowed_domains = ["chatvl.com", "chatvl.info"]
	start_urls = [
		"http://chatvl.com",
		"http://chatvl.com/hot"
	]
	rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('/(hot|new)/[0-5]$', ),)),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('/v/[0-9]+', )), callback='parse_info'),
    )

	site="http://chatvl.com/"

	def parse_info(self, response):
		src = response.url
		title = response.css(".photoDetails h1").xpath(".//text()").extract()[0].strip()
		link = response.css("#video-container iframe").xpath("./attribute::src").extract()[0]
		cover = response.css("meta[property=og\\3a image]").xpath("./attribute::content").extract()[0].strip()
		pdate = response.css(".post-info .post-date").extract()[0].strip()
		# print(response.css("meta[property=og\\3a description]").xpath("./attribute::content").extract()[0].strip())
		item = FuviItem()
		item["title"] = title
		item["sapo"] = ""
		item["cover"] = cover
		item["link"] = link
		item["src"] = src
		item["site"] = self.site
		item["catId"] = 1
		request = Request(link, callback=self.parse_item)
		request.meta["item"] = item

		yield(request)

	def parse_item(self, response):
		item = response.meta["item"]
		item["link"] = response.xpath("//iframe/attribute::src").extract()[0]
		yield(item)
