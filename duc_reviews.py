#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Written as part of https://www.scrapehero.com/how-to-scrape-amazon-product-reviews-using-python/
from lxml import html
import json
import requests
import json,re
from dateutil import parser as dateparser
from time import sleep
from tag_regex import regex

def ParseAPage(product_id, page_num):
	# Added Retrying
	for i in range(5):
		try:
			#This script has only been tested with Amazon.com
			# amazon_url = ('https://www.amazon.com/Gillette-Fusion-Manual-Razor-Refills/product-reviews/B004B8AZH0/ref=cm_cr_getr_d_paging_btm_'
			# 		+ str(page_num)  + '?pageNumber=' + str(page_num) + '&reviewerType=all_reviews')
			amazon_url = ('https://www.amazon.com/product-reviews/' + product_id
							+ '/ref=cm_cr_arp_d_paging_btm_' + str(page_num)  + '?pageNumber=' + str(page_num) + '&reviewerType=all_reviews')
			# Add some recent user agent to prevent amazon from blocking the request
			# Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
			headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
			page = requests.get(amazon_url,headers = headers)
			page_response = page.text
			parser = html.fromstring(page_response)


			raw_product_price = parser.xpath(regex['XPATH_PRODUCT_PRICE'])
			product_price = ''.join(raw_product_price).replace(',','')

			raw_product_name = parser.xpath(regex['XPATH_PRODUCT_NAME'])
			print raw_product_name
			product_name = ''.join(raw_product_name).strip()
			total_ratings  = parser.xpath(regex['XPATH_AGGREGATE_RATING'])
			reviews = parser.xpath(regex['XPATH_REVIEW_SECTION_1'])
			if not reviews:
				reviews = parser.xpath(regex['XPATH_REVIEW_SECTION_2'])
			ratings_dict = {}
			reviews_list = []
			# print reviews
			if not reviews:
				raise ValueError('unable to find reviews in page')

			#grabing the rating  section in product page
			for ratings in total_ratings:
				extracted_rating = ratings.xpath('./td//a//text()')
				if extracted_rating:
					rating_key = extracted_rating[0]
					raw_raing_value = extracted_rating[1]
					rating_value = raw_raing_value
					if rating_key:
						ratings_dict.update({rating_key:rating_value})
			#Parsing individual reviews
			for review in reviews:
				raw_review_author = review.xpath(regex['XPATH_AUTHOR'])
				raw_review_rating = review.xpath(regex['XPATH_RATING'])
				raw_review_header = review.xpath(regex['XPATH_REVIEW_HEADER'])
				raw_review_posted_date = review.xpath(regex['XPATH_REVIEW_POSTED_DATE'])
				raw_review_text1 = review.xpath(regex['XPATH_REVIEW_TEXT_1'])
				raw_review_text2 = review.xpath(regex['XPATH_REVIEW_TEXT_2'])
				raw_review_text3 = review.xpath(regex['XPATH_REVIEW_TEXT_3'])
				raw_review_text4 = review.xpath(regex['XPATH_REVIEW_TEXT_4'])
				# print raw_review_text4

				author = ' '.join(' '.join(raw_review_author).split()).strip('By')

				#cleaning data
				review_rating = ''.join(raw_review_rating).replace('out of 5 stars','')
				review_header = ' '.join(' '.join(raw_review_header).split())
				review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
				review_text = ' '.join(' '.join(raw_review_text1).split())

				#grabbing hidden comments if present
				if raw_review_text2:
					json_loaded_review_data = json.loads(raw_review_text2[0])
					json_loaded_review_data_text = json_loaded_review_data['rest']
					cleaned_json_loaded_review_data_text = re.sub('<.*?>','',json_loaded_review_data_text)
					full_review_text = review_text+cleaned_json_loaded_review_data_text
				else:
					full_review_text = review_text
				if not raw_review_text1:
					full_review_text = ' '.join(' '.join(raw_review_text4).split())

				raw_review_comments = review.xpath(regex['XPATH_REVIEW_COMMENTS'])
				review_comments = ''.join(raw_review_comments)
				review_comments = re.sub('[A-Za-z]','',review_comments).strip()
				review_dict = {
									'review_comment_count':review_comments,
									'review_text':full_review_text,
									'review_posted_date':review_posted_date,
									'review_header':review_header,
									'review_rating':review_rating,
									'review_author':author

								}
				reviews_list.append(review_dict)

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
		extracted_data.append(ParseAPage('B004B8AZH0', i))
	# print extracted_data
	f=open('data.json','w')
	json.dump(extracted_data,f,indent=4)

if __name__ == '__main__':
	ReadAsin()
