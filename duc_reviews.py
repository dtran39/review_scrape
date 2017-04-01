#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written as part of https://www.scrapehero.com/how-to-scrape-amazon-product-reviews-using-python/
import json,re
from helpers import (regex, getParser, getProductId, getAmazonReviewUrl,
					getProductInfo, getRatingsDict, getReviews)
def ScrapeProduct(product_id):
	# Added Retrying
	for i in range(5):
		try:
			amazonReviewUrl = getAmazonReviewUrl(product_id, 1)
			parser = getParser(amazonReviewUrl)
			product_name, product_price = getProductInfo(parser)
			ratings_dict = getRatingsDict(parser)
			reviews_list = getReviews(parser)
			for page_num in range(2, 3):
				new_parser = getParser(getAmazonReviewUrl(product_id, page_num))
				reviews_list += getReviews(new_parser)
			data = {
						'ratings':ratings_dict,
						'reviews':reviews_list,
						'url':amazonReviewUrl,
						'price':product_price,
						'name':product_name
					}
			return data
		except ValueError:
			print "Retrying to get the correct response"

	return {"error":"failed to process the page","asin":asin}

def ScrapeFromUrl(url):
	productId = getProductId(url)
	print productId
	extracted_data = ScrapeProduct(productId)
	print extracted_data
	# f = open('data_water_pressure.json','w')
	# json.dump(extracted_data,f,indent=4)

if __name__ == '__main__':
	ScrapeFromUrl('https://www.amazon.com/dp/B00OQVZDJM/ref=fs_ods_fs_eink_mt')
