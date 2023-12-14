import time

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from ieee.items import ActorItem


class ImdbSpider(scrapy.Spider):
    name = "imdb"

    def __init__(self):
        self.driver = webdriver.Chrome()  # You can use a different browser and driver

    def start_requests(self):
        for i in range(1, 2500):

            url = "https://www.imdb.com/name/nm{}/".format(('0' * (7 - len(str(i)))) + str(i))
            print(url)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        actor_links = [s.strip() for s in response.xpath('//*[@id="main"]/div/div[2]/div[3]/div/div[2]/h3/a/@href').getall()]
        actor_roles = [e for e in [s.strip().lower() for s in response.xpath('//*[@id="main"]/div/div[2]/div[3]/div/div[2]/p[1]/text()').getall()] if e.strip()]

        for link, actor_role in zip(actor_links, actor_roles):
            try:
                link = response.urljoin(link) + '/'

                # Navigate to the page using Selenium
                self.driver.get(link)
                is_male = True


                time.sleep(5)
                button = self.driver.find_element(By.XPATH, '//*[@id="accordion-item-{}-previous-projects"]/div/div/span/button'.format(actor_role))

                x = button.location['x']
                y = button.location['y']

                self.driver.execute_script("window.scrollTo({}, {});".format(x, y-500))

                time.sleep(5)

                button.click()

                time.sleep(5)

                # Extract data or perform other actions on the page
                yield self.parse_actor(actor_role)
            except Exception as e:
                with open("myfile.txt", "a") as f:
                    f.write("Missed: " + str(e))
    def parse_actor(self, actor_role):

        actor = ActorItem()

        actor['actor_name'] = self.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div/h1/span').text.strip()
        actor['number_of_movies'] = self.driver.find_element(By.XPATH, '//*[@id="{}-previous-projects"]/div[1]/label/span[1]/ul/li[2]'.format(actor_role)).text.strip()
        actor['date_of_birth'] = self.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/section/aside/div/span[2]').text.strip()

        awards_info = self.driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[1]/div/ul/li/div/ul/li/span').text.strip().split(' ')
        actor['awards_won'] = int(awards_info[0])
        actor['awards_nominee'] = int(awards_info[3])

        actor['movies'] = [e.text for e in self.driver.find_elements(By.XPATH, '//*[@id="accordion-item-{}-previous-projects"]/div/ul/li/div[2]/div[1]/a'.format(actor_role))]

        return actor


def closed(self, reason):
        self.driver.quit()
