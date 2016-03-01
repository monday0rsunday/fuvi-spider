import scrapy
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from fuvi_spider.items import FuviItem

class HaivnComSpider(Spider):
	name = "haivn.com"
	allowed_domains = ["haivn.com"]
	start_urls = [
		"http://haivn.com/",
		"http://haivn.com/hot/1",
		"http://haivn.com/hot/2",
		"http://haivn.com/hot/3",
		"http://haivn.com/hot/4",
	]

	site="http://haivn.com/"

	def parse(self, response):
		response = Selector(text=response.body)
		for a in response.xpath("//a[contains(@href,'video') or contains(@href,'photo')]"):
			print a
			src = a.xpath("./attribute::href").extract()[0].strip()
			if src.startswith("http://haivn.com/photo")or src.startswith("http://haivn.com/video"):
				yield Request(src, callback=self.parse_info)

	def parse_info(self, response):
		src = response.url
		response = Selector(text=response.body)
		title = response.css("article .badge-item-title").xpath(".//text()").extract()[0].strip()
		cover = response.css("meta[property=og\\3a image]").xpath("./attribute::content").extract()[0].strip()
		# pdate = response.css(".post-info .post-date").extract()[0].strip()
		item = FuviItem()
		item["title"] = title
		item["sapo"] = ""
		item["cover"] = cover
		item["src"] = src
		item["site"] = self.site
		if len(response.css("article .content-detail .video-frame")) > 0:
			item["link"] = response.css("article .content-detail script").xpath("./attribute::src").extract()[0]
			item["catId"] = 1
		elif len(response.css("article .content-detail video")) > 0:
			item["link"] = response.css("article .content-detail video").xpath("./source[@type='video/mp4']/attribute::src").extract()[0]
			item["catId"] = 1
		else:
			item["link"] = response.css("article .content-detail img").xpath("./attribute::src").extract()[0]
			item["catId"] = 2
		yield(item)