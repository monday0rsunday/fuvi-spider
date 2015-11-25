import scrapy
import re
from scrapy import Spider
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from fuvi_spider.items import FuviItem

class HaynhucnhoiTvSpider(CrawlSpider):
	name = "haynhucnhoi.tv"
	allowed_domains = ["haynhucnhoi.tv"]
	start_urls = [
		"http://haynhucnhoi.tv/video"
	]
	rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('/video/[0-5]$', ),)),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('/photo/[0-9]+', )), callback='parse_item'),
    )

	site="http://haynhucnhoi.tv/"
	ptn1 = re.compile(r"""(?m)file: "([^,]+)",""")
	ptn2 = re.compile(r"""(?m)TODO(http://embed.mecloud.vn/play/[0-9a-zA-Z]+)""")

	def parse_item(self, response):
		src = response.url
		title = response.css(".postDetail h1").xpath(".//text()").extract()[0].strip()
		link = None
		cover = response.css("meta[property=og\\3a image]").xpath("./attribute::content").extract()[0].strip()
		# print(response.css("meta[property=og\\3a description]").xpath("./attribute::content").extract()[0].strip())
		m1 = self.ptn1.search(response.body)
		m2 = self.ptn2.search(response.body)
		if(m1 is not None):
			link = m1.group(1)
		elif(m2 is not None):
			link = m2.group(1)
		item = FuviItem()
		item["title"] = title
		item["sapo"] = ""
		item["cover"] = cover
		item["link"] = link
		item["src"] = src
		item["site"] = self.site
		item["catId"] = 1
		if(link is not None):
			yield item
