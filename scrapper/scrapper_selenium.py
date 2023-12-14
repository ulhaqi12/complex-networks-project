import time

import json
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()  # You can use a different browser and driver
all_data = []

for i in range(1, 2500):

    link = "https://www.imdb.com/name/nm{}/".format(('0' * (7 - len(str(i)))) + str(i))

    try:
        driver.get(link)

        actor_role = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div/ul/li[1]').text.replace(' ', '_').lower()
        print(actor_role)
        time.sleep(3)
        try:

            button = driver.find_element(By.XPATH, '//*[@id="accordion-item-{}-previous-projects"]/div/div/span/button'.format(actor_role))

            x = button.location['x']
            y = button.location['y']

            driver.execute_script("window.scrollTo({}, {});".format(x, y-500))

            time.sleep(2)
            button.click()
        except Exception as e:
            print("Button not pressed.")
        time.sleep(4)

        # Extract data or perform other actions on the page

        actor = {}

        actor['actor_name'] = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[2]/div/h1/span').text.strip()
        actor['role'] = actor_role
        actor['number_of_movies'] = driver.find_element(By.XPATH, '//*[@id="{}-previous-projects"]/div[1]/label/span[1]/ul/li[2]'.format(actor_role)).text.strip()
        actor['date_of_birth'] = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/section/aside/div/span[2]').text.strip()

        awards_info = driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/div/section/div/div[1]/section[1]/div/ul/li/div/ul/li/span').text.strip().split(' ')
        actor['awards_won'] = int(awards_info[0])
        actor['awards_nominee'] = int(awards_info[3])

        actor['movies'] = [e.text for e in driver.find_elements(By.XPATH, '//*[@id="accordion-item-{}-previous-projects"]/div/ul/li/div[2]/div[1]/a'.format(actor_role))]

        all_data.append(actor)
    except Exception as e:
        print("Missed: " + str(e))


json_file_path = "data.json"

# Dump the list of dictionaries to the JSON file
with open(json_file_path, "w") as json_file:
    json.dump(all_data, json_file)
