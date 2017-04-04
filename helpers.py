from lxml import html
import requests
from dateutil import parser as dateparser
import re
from regex import regex
def getParser(url):
	# Add some recent user agent to prevent amazon from blocking the request
	# Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
	page = requests.get(url,headers = headers)
	page_response = page.text
	parser = html.fromstring(page_response)
	return parser
def getProductId(url):
 # return either ASIN or ISBN
    asin_search = re.search(regex['ASIN'], url)
    isbn_search = re.search(regex['ISBN'], url)
    if asin_search:
        return asin_search.group(1)
    elif isbn_search:
        return isbn_search.group(1)
    else:
        # log this URL
        return None
def getAuthorProfileId(review):
	 author_url = review.xpath(regex['XPATH_AUTHOR_URL'])
	 author_id = re.search(regex['author_id'], author_url[0]).group(1)
	#  print author_id
	 return author_id
def getAmazonReviewUrl(product_id, page_num):
	return ('https://www.amazon.com/product-reviews/' + product_id
			  + '/ref=cm_cr_arp_d_paging_btm_' + str(page_num)
			  + '?pageNumber=' + str(page_num)
			  + '&reviewerType=all_reviews')
def getAuthorProfileUrl(author_id):
	return ('https://www.amazon.com/gp/pdp/profile/' + author_id)
def getNumberOfPages(parser):
	return parser.xpath(regex['XPATH_NUMBER_OF_PAGES'])[-1]
def getProductInfo(parser):
	# price
	raw_product_price = parser.xpath(regex['XPATH_PRODUCT_PRICE'])
	product_price = ''.join(raw_product_price).replace(',','')
	#name
	raw_product_name = parser.xpath(regex['XPATH_PRODUCT_NAME'])
	product_name = ''.join(raw_product_name).strip()
	return (product_name, product_price)
def getRatingsDict(parser):
	ratings_dict = {}
	total_ratings  = parser.xpath(regex['XPATH_AGGREGATE_RATING'])
	#grabing the rating  section in product page
	for ratings in total_ratings:
		extracted_rating = ratings.xpath('./td//a//text()')
		if extracted_rating:
			rating_key = extracted_rating[0]
			raw_raing_value = extracted_rating[1]
			rating_value = raw_raing_value
			if rating_key:
				ratings_dict.update({rating_key:rating_value})
	return ratings_dict
def getReviewText(review):
	raw_review_text1 = review.xpath(regex['XPATH_REVIEW_TEXT_1'])
	raw_review_text2 = review.xpath(regex['XPATH_REVIEW_TEXT_2'])
	raw_review_text3 = review.xpath(regex['XPATH_REVIEW_TEXT_3'])
	raw_review_text4 = review.xpath(regex['XPATH_REVIEW_TEXT_4'])
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
	return full_review_text
def getReviews(parser):
	reviews = parser.xpath(regex['XPATH_REVIEW_SECTION_1'])
	if not reviews:
		reviews = parser.xpath(regex['XPATH_REVIEW_SECTION_2'])
	reviews_list = []
	# print reviews
	if not reviews:
		raise ValueError('unable to find reviews in page')
	#Parsing individual reviews
	for review in reviews:
		raw_review_author = review.xpath(regex['XPATH_AUTHOR'])
		author_profile_url = getAuthorProfileUrl(getAuthorProfileId(review))
		print author_profile_url
		raw_review_rating = review.xpath(regex['XPATH_RATING'])
		raw_review_header = review.xpath(regex['XPATH_REVIEW_HEADER'])
		raw_review_posted_date = review.xpath(regex['XPATH_REVIEW_POSTED_DATE'])
		# print raw_review_text4
		author = ' '.join(' '.join(raw_review_author).split()).strip('By')

		#cleaning data
		review_rating = ''.join(raw_review_rating).replace('out of 5 stars','')
		review_header = ' '.join(' '.join(raw_review_header).split())
		review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')

		full_review_text = getReviewText(review)
		# print type(full_review_text)
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
	return reviews_list
