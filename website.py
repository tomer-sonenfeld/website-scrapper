import string
import re
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from googletrans import Translator

visited_pages=set()
positions_found = False
visited_links = set()

class Website:
    def __init__(self, url):
        self.url = url
        domain_name = urlparse(url).hostname
        if domain_name.startswith('www.'):
            domain_name = domain_name[4:]
        self.name = domain_name

    def does_word_exist(self, word):
        self.does_word_exist__main_page(word)
        return positions_found

    def does_word_exist__main_page(self,word):
        global positions_found
        global visited_pages
        global visited_links
        print('searchin main page: ' + self.url)
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        response = requests.get(self.url, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')


        links = soup.find_all('a')

        keywords = ['job', 'jobs', 'career', 'careers', 'opportunity', 'opportunities',
                    'position', 'positions', 'opening', 'openings', 'opening', 'openings',
                    'קריירה', 'משרה', 'משרות', 'תפקיד', 'תפקידים', 'פתיחה', 'פתיחות']

        for link in links:
            if positions_found:
                break

            link_url = link.get('href')
            link_text = link.get_text()


            if link is not None and link_url is not None:
                if any(keyword in link_text.lower() for keyword in keywords):
                    link_url = urljoin(self.url, link_url)
                    sub_page = Website(link_url)
                    if link_text not in visited_links:
                        print('entering link: ' + link_text)
                        visited_links.add(link_text)
                        sub_page.does_word_exist__careers_page(word)

    def does_word_exist__careers_page(self,word):
        print('searching career page: ' + self.url)
        global positions_found
        global visited_pages
        global visited_links
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        response = requests.get(self.url, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()

        driver = webdriver.Chrome()
        driver.get(self.url)
        driver.implicitly_wait(10)

        if word in driver.page_source:
            positions_found = True
            return

        if word in text.lower():
            positions_found = True
            return

        keywords=['job','jobs', 'career','careers','opportunity','opportunities',
                'position','positions','opening','openings','opening','openings',
                  'קריירה','משרה','משרות','תפקיד','תפקידים','פתיחה','פתיחות']

        links = soup.find_all('a')
        for link in links:
            if positions_found:
                break
            link_url = link.get('href')
            link_text = link.get_text()

            if link is not None and link_url is not None:
                if any(keyword in link_text.lower() for keyword in keywords):
                    link_url = urljoin(self.url, link_url)
                    sub_page = SubWebsite(link_url)
                    if link_text not in visited_links:
                        print('entering link: ' + link_text)
                        visited_links.add(link_text)
                        sub_page.does_word_exist__careers_page(word)

    def __repr__(self):
        return f'Website: {self.name}, URL: {self.url}'

class SubWebsite(Website):
    pass

