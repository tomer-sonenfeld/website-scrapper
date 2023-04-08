import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from website import Website
from selenium import webdriver

if __name__ == '__main__':
    example_url = 'https://rad.com/'
    example_website = Website(example_url)
    print(example_website.does_word_exist('software'))

    # create webdriver object
    # driver = webdriver.Chorme()
    #
    # # enter keyword to search
    # keyword = "geeksforgeeks"
    #
    # # get geeksforgeeks.org
    # driver.get("https://www.geeksforgeeks.org/")
    #
    # # get elements
    # elements = driver.find_elements_by_tag_name("h2")
    #
    # # print complete elements list
    # print(element)