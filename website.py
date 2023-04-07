import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class Website:
    def __init__(self, url):
        self.url = url
        domain_name = urlparse(url).hostname
        if domain_name.startswith('www.'):
            domain_name = domain_name[4:]
        self.name = domain_name
        self.positions_found= False
        self.visited_pages=[]

    def does_word_exist(self, word):
        self.does_word_exist__main_page(word)
        return self.positions_found

    def does_word_exist__main_page(self,word):
        self.visited_pages.append(self.url)
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        response = requests.get(self.url, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')

        links = soup.find_all('a')
        keywords = ['job', 'jobs', 'career', 'careers', 'opportunity', 'opportunities',
                    'position', 'positions', 'opening', 'openings', 'opening', 'openings']
        for link in links:
            link_url = link.get('href')
            link_text = link.get_text()
            if link is not None and link_url is not None:
                if any(keyword in link_text.lower() for keyword in keywords) or \
                any(keyword in link_url for keyword in keywords):
                    link_url = urljoin(self.url, link_url)
                    sub_page = Website(link_url)
                    if not link_url in self.visited_pages:
                        sub_page.does_word_exist__careers_page(word)

    def does_word_exist__careers_page(self,word):
        super().visited_pages.append(self.url)
        headers = {'Accept-Language': 'en-US,en;q=0.5'}
        response = requests.get(self.url, headers=headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()

        if word in text.lower():
            self.positions_found = True
            return

        keywords=['job','jobs', 'career','careers','opportunity','opportunities',
                'position','positions','opening','openings','opening','openings']

        links = soup.find_all('a')
        for link in links:
            if self.positions_found:
                break
            link_url = link.get('href')
            link_text = link.get_text()
            if link is not None and link_url is not None:
                if any(keyword in link_text.lower() for keyword in keywords) or \
                any(keyword in link_url for keyword in keywords):
                    link_url = urljoin(self.url, link_url)
                    sub_page = SubWebsite(link_url)
                    if not link_url in self.visited_pages:
                        sub_page.does_word_exist__careers_page(word)

    def __repr__(self):
        return f'Website: {self.name}, URL: {self.url}'


