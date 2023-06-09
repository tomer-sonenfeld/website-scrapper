import string
import re
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from googletrans import Translator
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By

positions_found = False
visited_links = set()

driver= webdriver.Chrome()

class Website:
    def __init__(self, url):
        self.url = url
        domain_name = urlparse(url).hostname
        if domain_name.startswith('www.'):
            domain_name = domain_name[4:]
        self.name = domain_name

    def does_word_exist(self, word):
        self.does_word_exist__main_page(word)
        global driver
        driver.quit()
        return positions_found

    def does_word_exist__main_page(self,word):
        print('searching main page: ' + self.url)

        global driver
        driver.get(self.url)
        driver.implicitly_wait(10)


        keywords = ['job', 'jobs', 'career', 'careers', 'opportunity', 'opportunities',
                    'position', 'positions', 'opening', 'openings', 'opening', 'openings',
                    'קריירה', 'משרה', 'משרות', 'תפקיד', 'תפקידים', 'פתיחה', 'פתיחות']

        links = driver.find_elements(By.TAG_NAME, "a")

        for link in links:
            if positions_found:
                return
            try:
                link_url = link.get_attribute('href')
                link_text = link.get_attribute('text')
                if link is not None and link_url is not None:
                    if any(keyword in link_text.lower() for keyword in keywords):
                        sub_page = Website(link_url)
                        if link_text not in visited_links:
                            print('entering link: ' + link_text)
                            visited_links.add(link_text)
                            sub_page.does_word_exist__careers_page(word)
            except StaleElementReferenceException:
                continue

    def does_word_exist__careers_page(self,word):
        print('searching career page: ' + self.url)

        # driver = webdriver.Chrome()
        global driver
        driver.get(self.url)
        driver.implicitly_wait(10)

        if word in driver.page_source:
            print('found word: ' + word)
            print('found word in page: ' + self.url)
            global positions_found
            positions_found = True
            return


        keywords = ['job', 'jobs', 'career', 'careers', 'opportunity', 'opportunities',
                    'position', 'positions', 'opening', 'openings', 'opening', 'openings',
                    'קריירה', 'משרה', 'משרות', 'תפקיד', 'תפקידים', 'פתיחה', 'פתיחות']
        rep_keywords = ['more', 'forward', '>','>>']
        heb_rep_keywords = ['עוד','הבא','הלאה','קדימה']

        links = driver.find_elements(By.TAG_NAME, "a")

        if visited_links:
            search_boxes = driver.find_elements(By.TAG_NAME, "input")
            for search_box in search_boxes:
                if positions_found:
                    return
                # search in the search box for "student" then look at the results for "hello"
                print('searching in search box: ' + search_box.get_attribute('name'))
                search_box.send_keys(word)
                search_box.submit()
                if word in driver.page_source:
                    print('found word: ' + word)
                    print('found word in page: ' + self.url)
                    positions_found = True
                    return


        for link in links:
            if positions_found:
                return
            try:
                link_url = link.get_attribute('href')
                link_text = link.get_attribute('text')
                if link is not None and link_url is not None:
                    if any(keyword in link_text.lower() for keyword in keywords) or \
                            any(keyword in link_text.lower() for keyword in rep_keywords) or \
                            any(keyword in link_text.lower() for keyword in heb_rep_keywords):
                        sub_page = Website(link_url)
                        if link_text not in visited_links:
                            print('entering link: ' + link_text)
                            if link_text not in rep_keywords and link_text not in heb_rep_keywords:
                                visited_links.add(link_text)
                            sub_page.does_word_exist__careers_page(word)
            except StaleElementReferenceException:
                continue

    def __repr__(self):
        return f'Website: {self.name}, URL: {self.url}'

class SubWebsite(Website):
    pass

