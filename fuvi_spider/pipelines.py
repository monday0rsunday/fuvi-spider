# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from scrapy import log
from fuvi_spider.items import FuviItem

class FuviPipeline(object):
	def __init__(self):
		self.conn = MySQLdb.connect(
			user="fuvi"
			, passwd=""
			, db="fuvi"
			, host="localhost"
			, charset="utf8"
			, use_unicode=True)
		self.cursor = self.conn.cursor()
		self.count = 0
		pass

	def process_item(self, item, spider):
		self.count += 1
		if isinstance(item, FuviItem):
			self.cursor.executemany("""INSERT IGNORE INTO item(site, src, link, title, sapo, cover, cat_id) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
				, [(item["site"], item["src"], item["link"], item["title"], item["sapo"], item["cover"], item["catId"])])
		if self.count >= 5:
			self.count = 0
			self.conn.commit()
		# return item

	def close_spider(self, spider):
		self.conn.commit()