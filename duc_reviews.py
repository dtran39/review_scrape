#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written as part of https://www.scrapehero.com/how-to-scrape-amazon-product-reviews-using-python/
import json,re

from time import sleep
from helpers import regex, getParser, getAmazonUrl, getProductInfo, getRatingsDict, getReviews
def ParsePageFirstTime(product_id):
	# Added Retrying
	for i in range(5):
		try:
			amazon_url = getAmazonUrl(product_id, 1)
			parser = getParser(amazon_url)
			product_name, product_price = getProductInfo(parser)
			ratings_dict = getRatingsDict(parser)
			reviews_list = getReviews(parser)
			for i in range(2, 5):
				new_parser = getParser(getAmazonUrl(product_id, i))
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
	#Add your own ASINs here
	AsinList = ['B004B8AZH0']
	extracted_data = []
	for i in range(1):
		extracted_data.append(ParsePageFirstTime('B004B8AZH0'))
	# print extracted_data
	f=open('data.json','w')
	json.dump(extracted_data,f,indent=4)

if __name__ == '__main__':
	ReadAsin()
