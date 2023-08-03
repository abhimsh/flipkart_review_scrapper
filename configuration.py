
FLIPKART_HOME_URL = "https://www.flipkart.com"

FLIPKART_URL = "https://www.flipkart.com/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY"

FLIPKART_SEARCH_URL = \
"""{url}/search?q={product_name}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&as-pos=1&as-type=HISTORY"""

HEADER = \
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

PRODUCT_SELECTION = {"name": "div",
                     "class_": "_2kHMtA"
                     }
ALL_REVIEW_PAGES = {"name": "div",
                    "class_": "_2c2kV-"}

PRODUCTION_SELECTION_ATTRIBUTE = "href"
REGEX_PATTERN_FOR_TOTAL_REVIEW = r"All\s(\d+)\sreviews"
REGEX_PATTERN_FOR_PAGES = r"Page\s(\d+)\sof\s(\d+)"
REVIEW_PAGE_REVIEW_CLASS = \
    {
        "name": "div",
        "class_": "_1AtVbE col-12-12"
    }

REVIEW_DETAILS_CLASS_NAMES = \
    {
        "_2sc7ZR": "review_time",
        "_2-N8zT": "review_title",
        "t-ZTKy": "review_statement",
        "_2sc7ZR _2V5EHH": "review_user_name",
        "_2mcZGG": "review_usertype_and_place",
    }

PAGE_CHANGE = "&page={page_number}"
CSV_HEADER = ["review_title", "review_statement",
              "review_user_name", "review_usertype", "review_place",
              "review_time"]
ALL_DATA_KEYS = \
    ["review_title", "review_statement", "review_user_name", "review_usertype_and_place",
     "review_time"]
REVIEW_TIME = \
    {
        r"(\d+)\sday(|s)\sago": "days",
        r"(\d+)\smonth(|s)\sago": "months"
    }
REVIEW_TIME_FORMAT = "%Y-%m-%d"
CSV_FILE = "flipkart_{}_review.csv"

