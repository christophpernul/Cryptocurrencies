# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 19:47:04 2017

@author: csam5106
"""

import json
import requests
from datetime import date

year = date.today().year
weeknr = date.today().isocalendar()[1]


print "Checking Market Capitalization of Top 100 Cryptocurrencies\n"
r = requests.get("https://api.coinmarketcap.com/v1/ticker/")
y = json.loads(r.text)
with open("data/year_{0}_week_{1}.json".format(year, weeknr), 'w') as ofile:
    ofile.write(json.dumps(y))


    

    
    



