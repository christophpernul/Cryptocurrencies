# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 20:50:41 2017

@author: csam5106
"""

import json
import sys
import numpy as np
from datetime import date

if len(sys.argv)==2:###FORMAT: year-month-day -> compare to today
    date1 = str(sys.argv[1])
    date2 = date.today()
elif len(sys.argv)==3: ###FORMAT: old year-month-day -> new year-month-day
    date1 = str(sys.argv[1])
    date2 = str(sys.argv[2])
else:
    print "Missing argument!!! Format: year-month-day"
    exit()

print "Loading data between {0} and {1}!".format(date1, date2)
filename = "data/marketcap_{0}.json".format(date1)
with open(filename, 'r') as ifile:
    x = json.load(ifile)
filename = "data/marketcap_{0}.json".format(date2)
with open(filename, 'r') as ifile:
    y = json.load(ifile)

n = len(x)
oldCoins, newCoins = [], []
names, namesNew = [], []
for j in range(n):
    oldCoins.append([x[j]["name"], float(x[j]["price_usd"]), float(x[j]["market_cap_usd"])])
    newCoins.append([y[j]["name"], float(y[j]["price_usd"]), float(y[j]["market_cap_usd"])])
    names.append(x[j]["name"])
    namesNew.append(y[j]["name"])
#oldSorted = sorted(enumerate(oldCoins), key=lambda x: x[1])
newSorted = sorted(enumerate(newCoins), key=lambda x: x[1])

coins = []
lranks, lprices, lcaps = [], [], []

for j in range(n):
    coin = newSorted[j][1][0]
    if coin in names:
        idxOld = names.index(coin)
        coins.append(coin)
        if j<10:
            print idxOld, coin, names[idxOld]
        lranks.append([idxOld, newSorted[j][0]])
        lprices.append([oldCoins[idxOld][1], newSorted[j][1][1]])
        lcaps.append([oldCoins[idxOld][2], newSorted[j][1][2]])   
    
ranks = np.array(lranks).T
prices = np.array(lprices).T      
mcaps = np.array(lcaps).T

winners = np.sort(ranks[1]-ranks[0])[:10]*(-1)
idx_winners = np.argsort(ranks[1]-ranks[0])[:10]
loosers = np.sort(ranks[0]-ranks[1])[:10]*(-1)
idx_loosers = np.argsort(ranks[0]-ranks[1])[:10]


print ""
print "Top 10 of gains in ranking of Market Capitalization:"
for j in range(len(winners)):
    print coins[idx_winners[j]], "\t+", int(winners[j])

print ""
print "Top 10 of losses in ranking of Market Capitalization:"
for j in range(len(loosers)):
    print coins[idx_loosers[j]], "\t-", int(loosers[j])

print ""
print "Newcomers in the Top 100:"
print "Name\t rank\t price in $\t market cap in $"
new = []
for j in range(n):
    if namesNew[j] not in names:
        new.append([namesNew[j], j])
for k in range(len(new)):
    print new[k][0], "\t", new[k][1], "\t", newCoins[new[k][1]][1], "\t", newCoins[new[k][1]][2]
    
print ""
print "Dropped out of the Top 100:"
print "Name\t\t rank\t\t price in $\t\t market cap in $"
dropped = []
for j in range(n):
    if names[j] not in namesNew:
        dropped.append([names[j], j])
for k in range(len(dropped)):
    print dropped[k][0], "\t", dropped[k][1], "\t", oldCoins[dropped[k][1]][1], "\t", oldCoins[dropped[k][1]][2]
