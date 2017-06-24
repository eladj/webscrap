#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd

city_name = "עתלית"
url_yad2_atlit = "http://www.yad2.co.il/Nadlan/sales.php?City=%F2%FA%EC%E9%FA&Neighborhood=" \
      "&HomeTypeID=&fromRooms=&untilRooms=&fromPrice=&untilPrice=&PriceType=1" \
      "&FromFloor=&ToFloor=&Info="

# Get html
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
response = requests.get(url_yad2_atlit, headers=headers)
soup = BeautifulSoup(response.content, "lxml")

# Get all relevant table rows tag
tr_tags = soup.find_all("tr")

# filter out only relevant tags
relevant_tags = []
for tag_ind, tag in enumerate(tr_tags):
    if 'id' in tag.attrs:
        if "tr_Ad_2_1" in tag['id']:
            relevant_tags.append(tag)

df = pd.DataFrame(columns=('href', 'price', 'address', 'type', 'region', 'rooms', 'floor',
                           'has_image', 'date'))
for tag_ind, tag in enumerate(relevant_tags):
    content = tag.find_all('td')
    id = content[0].find('div')['id'].split("ad_favorite_1_")[-1]
    df.loc[id, 'type'] = content[4].get_text().split('\t')[1].replace(" ", "")
    df.loc[id, 'region'] = content[6].get_text().split('\t')[1].replace(" ", "")
    df.loc[id, 'address'] = content[8].get_text().split('\t')[1].replace(" ", "")
    if '\xa0' not in content[10].get_text().split('\t')[2]:
        df.loc[id, 'price'] = int(content[10].get_text().split('\t')[2].split(" ₪")[0].replace(",", ""))
    if '\t' in content[12].get_text():
        df.loc[id, 'rooms'] = content[12].get_text().split('\t')[1].replace(" ", "")
    df.loc[id, 'floor'] = content[14].get_text().split('\t')[1].replace(" ", "")
    # df.loc[id, 'has_image']
    df.loc[id, 'date'] = content[18].get_text().replace('\n', "")

# Write content to html file
response.encoding = 'utf-8'
with open("out.html", "w") as f:
    f.write(response.text)

"""
generic ad: <tr id="tr_Ad_2_1
add with yellow: class="yellow showPopupUnder"
standard add class: class=" showPopupUnder"
"""