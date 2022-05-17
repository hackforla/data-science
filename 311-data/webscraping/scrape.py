from selenium import webdriver
import validators 
import time
import requests
from bs4 import BeautifulSoup, element
import json
import pandas as pd      
import numpy as np

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

def to_table(data):
    d = pd.DataFrame(data)
    d['category'] = d.apply(lambda row: row.href[29:].split('/')[0], axis=1) #get category name from href
    d['count'] = 1
   
    table = pd.pivot_table(d, values = "count", index = "tech", columns = "url",aggfunc=np.sum)
    table.fillna(0,inplace = True)
   
    out = pd.merge(d[['tech','href','category']], table, on='tech')
    output = out.drop_duplicates()
    col_names = list(output.columns)

    output.insert(loc=3, column='total_count', value=output[col_names[3:]].sum(axis=1))
    output = output.rename(columns={'href': 'URL of tech', 'tech' : 'Name of tech'})
    
    return output

if __name__ == "__main__":

    print("Beginning web scraping...")

    NCsurvey_df = pd.read_csv('NCsurvey.csv')
    url_list = list(filter(lambda x: x==x, NCsurvey_df.iloc[2,2:].values))  

    base_url = "https://builtwith.com"     

    survey_tech_list = scrape_builtwith(base_url, url_list)

    with open('data.json', 'w') as f:
        json.dump(survey_tech_list, f)

    table = to_table(survey_tech_list)

    table.to_csv("tech_table.csv", index=False)
