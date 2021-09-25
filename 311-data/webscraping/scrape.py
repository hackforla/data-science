
from selenium import webdriver
import validators 
import time
import requests
from bs4 import BeautifulSoup, element
import json
import pandas as pd      


def scrape_builtwith(base_url, url_list):
    options = webdriver.ChromeOptions()
    options.add_argument("--remote-debugging-port=9222") 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--window-size=1080x720")
    driver = webdriver.Chrome(options=options)
    driver.get(base_url)
    survey_tech_list = []

    for url in url_list:
        element = driver.find_element_by_name("q")
        element.send_keys(url)
        driver.find_element_by_class_name("btn-primary").click()
        driver.implicitly_wait(10)
        current_url = driver.current_url
        #current_url = base_url + '/' + url
        
        res = requests.get(current_url)
        soup = BeautifulSoup(res.content, "html.parser")
        divs = soup.findAll("div", {"class": "row mb-2 mt-2"})

        for div in divs:
            elt = div.findAll("a")[0]
            survey_tech_list.append({'url': url, 'tech': elt.text ,'href': elt.attrs["href"] })


    return survey_tech_list




if __name__ == "__main__":

    print("run")

    NCsurvey_df = pd.read_csv('NCsurvey.csv')
    url_list = list(filter(lambda x: x==x, NCsurvey_df.iloc[2,2:].values))  

    base_url = "https://builtwith.com"     

    survey_tech_list = scrape_builtwith(base_url, url_list)

    with open('data.json', 'w') as f:
        json.dump(survey_tech_list, f)