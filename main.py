from configuration import *
import utils
import re

search_string = "samsung Galaxy s23 Ultra"
cleaned_search_string = search_string.replace(" ", "+")
all_review_data = []

# from the search list provided get the search url that consists of product-review
# page embedded in it
review_url, total_review = utils.get_product_review_page(cleaned_search_string)
html_content = utils.html_parser(review_url)
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
    current_page_url_link = "{}{}".format(review_url,
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

    # If in a continuous there were 15 pages where the data was not there, then we will
    # end the web scrapping to save time
    if total_number > 15:
        print("There are not review from the past {} pages".format(total_number))
        break

# # Added the break to avoid scrapping duplicate data into dataset
# break

utils.write_data_to_csv(all_review_data, search=search_string)

