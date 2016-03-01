import scrapy
import json
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from fuvi_spider.items import FuviItem

class HaivainoiComSpider(Spider):
	name = "haivainoi.com"
	allowed_domains = ["www.haivainoi.video", "haivainoi.video"]
	start_urls = [
		"http://www.haivainoi.video/18",
		# "http://www.haivainoi.com/hot"
	]

	site="http://www.haivainoi.com/"

	def parse(self, response):
		token = response.xpath("//input[@name='_token']/attribute::value").extract()[0]
		for i in range(1,5):
			frmdata = {"id": "all", "postPage": ""+str(i), "type": "", "category": "hot", "_token": token, "action": "getPost"}
			yield FormRequest("http://www.haivainoi.com/post-handler", callback=self.parse_item, formdata=frmdata)

	def parse_item(self, response):
		for article in json.loads(response.body):
			item = FuviItem()
			item["title"] = article.get("title").strip()
			item["link"] = ""
			item["sapo"] = ""
			item["cover"] = ""
			if article.get("type") == "image" or article.get("type") == "gif":
				item["link"] = "http://files.haivainoi.video" + article.get("content")
				item["catId"] = 2 #image
			else:
				item["link"] = "https://www.youtube.com/embed/" + article.get("content")
				item["catId"] = 1 #video
				item["cover"] = "http://img.youtube.com/vi/"+article.get("_id")+"/0.jpg"
			item["src"] = "http://www.haivainoi.com/p/" + article.get("_id")
			item["site"] = self.site
			yield item
