from lxml import html
import requests
regex ={
	'XPATH_AGGREGATE': '//span[@id="acrCustomerReviewText"]',
	'XPATH_REVIEW_SECTION_1': '//div[contains(@id,"reviews-summary")]',
	'XPATH_REVIEW_SECTION_2': '//div[@data-hook="review"]',
	'XPATH_AGGREGATE_RATING': '//table[@id="histogramTable"]//tr',
	'XPATH_PRODUCT_NAME': '//div[@class="a-row product-title"]//h1//a[@data-hook="product-link"]//text()',
	'XPATH_PRODUCT_PRICE': '//span[@class="a-color-price arp-price"]/text()',
	'XPATH_RATING': './/i[@data-hook="review-star-rating"]//text()',
	'XPATH_REVIEW_HEADER': './/a[@data-hook="review-title"]//text()',
	'XPATH_REVIEW_POSTED_DATE': './/a[contains(@href,"/profile/")]/parent::span/following-sibling::span/text()',
	'XPATH_REVIEW_TEXT_1': './/div[@data-hook="review-body"]//text()',
	'XPATH_REVIEW_TEXT_2': './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview',
	'XPATH_REVIEW_COMMENTS': './/span[@data-hook="review-comment"]//text()',
	'XPATH_AUTHOR': './/a[contains(@href,"/profile/")]/parent::span//text()',
	'XPATH_REVIEW_TEXT_3': './/div[contains(@id,"dpReviews")]/div/text()',
	'XPATH_REVIEW_TEXT_4': './/span[@data-hook="review-body"]//text()',
}
def getParser(url):
	# Add some recent user agent to prevent amazon from blocking the request
	# Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
	page = requests.get(url,headers = headers)
	page_response = page.text
	parser = html.fromstring(page_response)
	return parser
def getAmazonUrl(product_id, page_num):
	return ('https://www.amazon.com/product-reviews/' + product_id
			  + '/ref=cm_cr_arp_d_paging_btm_' + str(page_num)
			  + '?pageNumber=' + str(page_num)
			  + '&reviewerType=all_reviews')
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
