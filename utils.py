import os
import csv
from bs4 import BeautifulSoup
import datetime
from dateutil.relativedelta import relativedelta

import configuration
from configuration import *
import requests
import re


def get_url_content(url: str):
    """
    This function will use request to contents of url
    :param url:
        The URL that we want to get the contents from
    :return:
        the content of the URL
    """
    response_url = requests.get(url, headers=HEADER)
    response_url.raise_for_status()
    return response_url.content


def get_all_reviews_from_single_page(page_content) -> list:
    """
    This method will work on each of the flipkart review page and parse the contents
    to get all the review information present in that page
    :param page_content:
        parsed html soup object
    :return:
        list of dictionaries containing the review details present in the particular page
    """

    list_of_reviews = []
    # Getting all the list of div tags in the review page
    # the first and the last entries are not considered
    # Since 1st entry contain the review statistics
    # Last entry contains page information
    for each_review_panel in page_content[1:-1]:
        class_name = each_review_panel.next_element.get("class")
        # check for a particular div tag with class name as "_27M-vq", that
        # contains each review information, if the class name is different, then discard the
        # current div tag and go for the next one
        if " ".join(class_name) != "_27M-vq":
            continue
        # just initialized to help us stop looking for div tags once we have found all the required
        # information about each review
        attr_list = list(REVIEW_DETAILS_CLASS_NAMES.keys())
        data = {}
        # find all the child tags
        for each_entry in each_review_panel.next_element.find_all_next():
            temp_class_data = each_entry.get("class")
            # if we have a tag with no class name, discard
            if not temp_class_data:
                continue
            class_name = "".join(temp_class_data).replace(" ", "")
            # check if the class name of current div tag is part of the required class name
            # which are for a particular review information in consideration
            if class_name in attr_list:
                data[REVIEW_DETAILS_CLASS_NAMES[class_name]] = each_entry.text.replace("READ MORE", "")
                attr_list.remove(class_name)
            # Once all the review information has been updated then stop looking
            if not attr_list:
                list_of_reviews.append(data)
                break

    return list_of_reviews


def html_parser(url, parser="html.parser"):
    """
    This method will parse the URL and provides the beatuiful soup object which is parsed as
    per the parameter provides
    :param url:
        The url to parse the content
    :param parser:
        parsing technique: lxml/html.parser and so on..
    :return:
        Beautiful soup object of parsed content of URL
    """
    response = get_url_content(url)
    return BeautifulSoup(response, parser)


def get_product_review_page(product_name):
    url = FLIPKART_SEARCH_URL.format(url=FLIPKART_HOME_URL, product_name=product_name)
    html_content = html_parser(url)

    content = html_content.find_all(**PRODUCT_SELECTION)

    for search_results in content:
        initial_page = FLIPKART_HOME_URL + search_results.a["href"]
        html_content = html_parser(initial_page)
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
                return required_link, int(total_reviews)
                # yield required_link, int(total_reviews)
                # break
    else:
        print("All test case complete")


def prepare_data_in_a_format(list_of_dict: list):
    """
    This Method will convert the review data in the form of dictionary to list of
    list to be written into csv file
    :param list_of_dict:
        the data scrapped from the flipkart
    :return:
        list of tuples of each review data
    """
    # clean_data = []
    for each_data in list_of_dict:
        temp_list = []
        for field in configuration.ALL_DATA_KEYS:
            if field == "review_time":
                temp_list.append(get_correct_date(each_data[field]))
            elif field == "review_usertype_and_place":
                for fields in each_data[field].split(","):
                    temp_list.append(fields.replace('"', "").strip())
            else:
                temp_list.append(each_data[field])
        # Making a generator because if the data is huge , It will eat up all the RAM space
        yield temp_list


def write_data_to_csv(list_of_data, search) -> None:
    """
    This method will write the review data into csv file
    :param list_of_data:
        dict of review data scrapped from the flipkart
    :param search:
        search string provided to get the reviews
    :return:
        None
    """
    search_string = search.replace(" ", "_")
    file_path = configuration.CSV_FILE.format(search_string)
    with open(file_path, "w", encoding="utf-8", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(configuration.CSV_HEADER)
        csv_writer.writerows(prepare_data_in_a_format(list_of_data))


def get_correct_date(date_value):
    """
    This method will convert the review time like 5 months ago/1 day ago etc..
     to correct date
    :param date_value:
        The value fetched from the flipkart review page
    :return:
        string of date in the YYYY-MM-DD format
    """
    if "Today" in date_value:
        actual_date = datetime.date.today()
    else:
        for pattern in configuration.REVIEW_TIME:
            output = re.findall(pattern, date_value)
            if output:
                dict_data = {configuration.REVIEW_TIME[pattern]: int(output[0][0])}
                actual_date = datetime.date.today() - relativedelta(**dict_data)
                break

        else:
            print("New Format: {}".format(date_value))
        return actual_date.strftime(configuration.REVIEW_TIME_FORMAT)
