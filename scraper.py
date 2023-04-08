import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from website import Website

class Scraper:
    def __init__(self):
        self.driver = webdriver.Chrome('C:\Projects\JobsAlarm\chromedriver.exe')

    def test(self):
        self.driver.get('https://www.google.com')
        self.driver.quit()

    def does_site_contains_word(self, website: Website, word: str):
        self.driver.get(website.url)
        self.enter_careers_page()
        self.driver.quit()

    def enter_careers_page(self):
        try:
            career_link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Careers"))
            )
        except:
            print("couldn't find careers page")
            return

        print("found careers page")
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(career_link))
        except:
            print("couldn't click careers page")

        career_link.click()

        time.sleep(10)
