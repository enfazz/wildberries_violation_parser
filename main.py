import requests


from config import KEYWORDS_LIST_FILEPATH, SELLERS_LIST_FILEPATH
from utils import read_txt_file, get_urls

def main():
    keywords = read_txt_file(KEYWORDS_LIST_FILEPATH)
    original_sellers = read_txt_file(SELLERS_LIST_FILEPATH)
    urls = get_urls(keywords, original_sellers)


if __name__ == '__main__':
    main()