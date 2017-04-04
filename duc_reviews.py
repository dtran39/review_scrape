#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written as part of https://www.scrapehero.com/how-to-scrape-amazon-product-reviews-using-python/
import json,re
from helpers import (regex, getParser, getNumberOfPages, getProductId, getAmazonReviewUrl,
					getProductInfo, getRatingsDict, getReviews)
def ScrapeProduct(product_id):
	# Added Retrying
	for i in range(5):
		try:
			amazonReviewUrl = getAmazonReviewUrl(product_id, 1)
			print amazonReviewUrl
			parser = getParser(amazonReviewUrl)
			# numberOfPages = int(getNumberOfPages(parser).replace(",", ""))
			# product_name, product_price = getProductInfo(parser)
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

	return {"error":"failed to process the page","asin":product_id}

def ScrapeFromUrl(url):
	productId = getProductId(url)
	extracted_data = ScrapeProduct(productId)
	f = open('new_data.json','w')
	json.dump(extracted_data,f,indent=4)
if __name__ == '__main__':
	ScrapeFromUrl('https://www.amazon.com/adidas-Outdoor-Kanadia-Trail-Running/dp/B01CI8A0VK/ref=s9u_simh_gw_i1?_encoding=UTF8&fpl=fresh&pd_rd_i=B01CI8A0VK&pd_rd_r=EDA0ME1F8E1RWRABBF91&pd_rd_w=b4Mlo&pd_rd_wg=XhRJB&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=&pf_rd_r=MWEX4QMW9CYQFMDCBA15&pf_rd_t=36701&pf_rd_p=2a4fafb6-9fdc-425a-aee8-c82daa7b18ed&pf_rd_i=desktop')
