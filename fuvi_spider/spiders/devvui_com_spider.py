import scrapy
import re
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from fuvi_spider.items import FuviItem

class DevvuiComSpider(CrawlSpider):
	name = "devvui.com"
	allowed_domains = ["devvui.com"]
	start_urls = [
		"http://devvui.com"
	]
	rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('/page/[0-9]$', ),), callback='parse_item', follow=True),
    )

	site="http://devvui.com/"

	def parse_item(self, response):
		for article in response.css(".content-wrap article"):
			src = article.css(".post-content .title a").xpath("./attribute::href").extract()[0].strip()
			title = article.css(".post-content .title a").xpath("./text()").extract()[0].strip()
			link = article.css(".post-content .img-responsive").xpath("./attribute::src").extract()[0].strip()
			item = FuviItem()
			item["title"] = title
			item["sapo"] = ""
			item["cover"] = ""
			item["link"] = link
			item["src"] = src
			item["site"] = self.site
			item["catId"] = 4
			yield item
