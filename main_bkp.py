from configuration import *
import utils
import re
from pprint import pprint

search_string = "s23 Ultra"
search_string = search_string.replace(" ", "+")
all_review_data = []

url = FLIPKART_SEARCH_URL.format(url=FLIPKART_HOME_URL, product_name=product_name)
html_content = utils.html_parser(url)

content = html_content.find_all(**PRODUCT_SELECTION)

for search_results in content:
    initial_page = FLIPKART_HOME_URL + search_results.a["href"]
    html_content = utils.html_parser(initial_page)
    content = html_content.find_all("a")
    required_link = ""
    total_reviews = ""
    for each_content in content:
        link = each_content.get("href")
        text = each_content.getText()
        reviews = re.findall(REGEX_PATTERN_FOR_TOTAL_REVIEW, text)
        if "/product-reviews/" in link and \
                re.search(REGEX_PATTERN_FOR_TOTAL_REVIEW, text):
            total_reviews, required_link = int(reviews[0]), FLIPKART_HOME_URL + link
            break

    if required_link and total_reviews:
        print("Got the URL link where the review link is present for the product")
        break

# Perform scrapping for the first page separately since the number of pages information
# is yet to be figured out
if not (total_reviews and required_link):
    raise Exception("There is no review page link")
html_content = utils.html_parser(required_link)
content = html_content.find_all(**REVIEW_PAGE_REVIEW_CLASS)
# The text also contains the number of pages and pages text to click on next
number_of_reviews = content[-1].text.split("234")[0].split()[-1]
number_of_pages_text = content[-1].next_element.find_all_next("span")[0].text
number_of_pages = re.findall(REGEX_PATTERN_FOR_PAGES, number_of_pages_text)
if number_of_pages:
    current_page, number_of_pages = number_of_pages[0]

all_review_data.extend(utils.get_all_reviews_from_single_page(content))
total_number = 0

# Go to each pages from page-2 till last pages provided by Flipkart page and srap the reviews
# in each page
for page_num in range(2, int(number_of_pages)):
    current_page_url_link = "{}{}".format(required_link,
                                          PAGE_CHANGE.format(page_number=page_num))
    html_content = utils.html_parser(current_page_url_link)
    content = html_content.find_all(**REVIEW_PAGE_REVIEW_CLASS)
    print("Page: {}".format(page_num))
    reviews = utils.get_all_reviews_from_single_page(content)
    if not reviews:
        total_number += 1
    else:
        total_number = 0
        all_review_data.extend(reviews)

    # If in a row there were 15 pages where the data was not there, then we will
    # end the web scrapping to save time
    if total_number > 15:
        print("There are not review from the past {} pages".format(total_number))
        break


for data in all_review_data:
    pprint(data)

print("total review: {}".format(len(all_review_data)))
print("Actual number of reviews: {}".format(total_reviews))