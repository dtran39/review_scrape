#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written as part of https://www.scrapehero.com/how-to-scrape-amazon-product-reviews-using-python/
import json,re
from helpers import regex, getParser, getAmazonUrl, getProductInfo, getRatingsDict, getReviews
def ScrapeProduct(product_id):
	# Added Retrying
	for i in range(5):
		try:
			amazon_url = getAmazonUrl(product_id, 1)
			parser = getParser(amazon_url)
			product_name, product_price = getProductInfo(parser)
			ratings_dict = getRatingsDict(parser)
			reviews_list = getReviews(parser)
			for page_num in range(2, 293):
				new_parser = getParser(getAmazonUrl(product_id, page_num))
				reviews_list += getReviews(new_parser)
			data = {
						'ratings':ratings_dict,
						'reviews':reviews_list,
						'url':amazon_url,
						'price':product_price,
						'name':product_name
					}
			return data
		except ValueError:
			print "Retrying to get the correct response"

	return {"error":"failed to process the page","asin":asin}

def ReadAsin():
	extracted_data = ScrapeProduct('B002Z8E52Y')
	f = open('data_water_pressure.json','w')
	json.dump(extracted_data,f,indent=4)

if __name__ == '__main__':
	ReadAsin()
