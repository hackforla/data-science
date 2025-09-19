"""Scrapes extra info for desired tech categories

Takes tech_table produced by Rajinders' scrape.py script

Extra info includes: url of tech found on builtwith, text description of tech, url for tech website, subcategories listed on builtwith,
number of live sites that use technology, list of top 5 competitors of tech
"""

import requests
from bs4 import BeautifulSoup, element
import pandas as pd
import numpy as np

def get_extra_info(url_list):
    columns = ['builtwith_tech_url', 'tech_description', 'tech_website', 'subcategories','num_live_sites','competitors']
    extra_info = pd.DataFrame(columns=columns)

    for url in url_list:
        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")

        #first card search for tech description, tech website, subcategories
        div = soup.findAll("div", {"class": "col-9 col-md-10"})

        ls = [url]
        for d in div:
            info = d.findAll("p")
            for i in info:
                ls.append(i.text)

        #second search, for top competitors
        div2 = soup.find("div", {"class": "list-group small"})
        comp = div2.findAll("a", href=True)
        links = []

        try:
            for i in range(5): #get top 5 competitors
                if 'trends' in str(comp[i]): #some sites don't have competitors listed
                        links.append(comp[i]["href"][2:])
                else:
                    continue
        except:
            continue

        try:
            ls.append(soup.find("dd", {"class": "col-6"}).text) #get number of live websites
        except:
            ls.append(np.NaN)#some urls don't have this info yet

        ls.append(links)
        extra_info.loc[len(extra_info)] = ls

    return extra_info

def main():
    tech = pd.read_csv('tech_table.csv')
    more_info = tech[tech['category'].isin(['widgets', 'analytics', 'cms','copyright','framework','link','mobile','payment','ssl','widgets'])] #choose which tech categories to collect more data
    urls = list(more_info['URL of tech'])
    info = get_extra_info(urls)
    info['subcategories'] = info['subcategories'].str.replace(' · ', ', ') #formatting for subcategories column
    info.to_csv('techtable_extrainfo.csv', index=False)