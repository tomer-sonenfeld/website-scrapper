import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from website import Website

if __name__ == '__main__':
    example_url = 'https://www.intel.com/'
    example_website = Website(example_url)
    print(example_website.does_word_exist('Architect'))
