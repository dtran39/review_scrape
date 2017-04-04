regex ={
	'ASIN'  :'/([A-Z0-9]{10})',
	'ISBN' : '/([0-9]{10})',
	'author_id': '/([A-Z0-9]{13})',
	'XPATH_AGGREGATE': '//span[@id="acrCustomerReviewText"]',
	'XPATH_REVIEW_SECTION_1': '//div[contains(@id,"reviews-summary")]',
	'XPATH_REVIEW_SECTION_2': '//div[@data-hook="review"]',
	'XPATH_AGGREGATE_RATING': '//table[@id="histogramTable"]//tr',
	'XPATH_PRODUCT_NAME': '//div[@class="a-row product-title"]//h1//a[@data-hook="product-link"]//text()',
	'XPATH_PRODUCT_PRICE': '//span[@class="a-color-price arp-price"]/text()',
	'XPATH_NUMBER_OF_PAGES': '//li[@data-reftag="cm_cr_arp_d_paging_btm"]//a//text()',
	'XPATH_RATING': './/i[@data-hook="review-star-rating"]//text()',
	'XPATH_REVIEW_HEADER': './/a[@data-hook="review-title"]//text()',
	'XPATH_REVIEW_POSTED_DATE': './/a[contains(@href,"/profile/")]/parent::span/following-sibling::span/text()',
	'XPATH_REVIEW_TEXT_1': './/div[@data-hook="review-body"]//text()',
	'XPATH_REVIEW_TEXT_2': './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview',
	'XPATH_REVIEW_COMMENTS': './/span[@data-hook="review-comment"]//text()',
	'XPATH_AUTHOR': './/a[contains(@href,"/profile/")]/parent::span//text()',
	'XPATH_AUTHOR_URL': './/a[@data-hook="review-author"]/@href',
	'XPATH_REVIEW_TEXT_3': './/div[contains(@id,"dpReviews")]/div/text()',
	'XPATH_REVIEW_TEXT_4': './/span[@data-hook="review-body"]//text()',
}
