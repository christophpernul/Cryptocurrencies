# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 20:50:41 2017

@author: csam5106
"""

import json
import sys
import numpy as np
from datetime import date

if len(sys.argv)==2:###FORMAT: week/year -> compare to today
    year = sys.argv[1].split("/")[1]
    weeknr = sys.argv[1].split("/")[0]
    year1 = date.today().year
    weeknr1 = date.today().isocalendar()[1]    
elif len(sys.argv)==3: ###FORMAT: oldweek/oldyear newweek/newyear
    year = sys.argv[1].split("/")[1]
    weeknr = sys.argv[1].split("/")[0]
    year1 = sys.argv[2].split("/")[1]
    weeknr1 = sys.argv[2].split("/")[0]
else:
    print "Missing argument!!! Format: week/year"


print "Loading data between {1}/{0} and {3}/{2}!".format(year, weeknr, year1, weeknr1)
filename = "data/year_{0}_week_{1}.json".format(year, weeknr)
with open(filename, 'r') as ifile:
    x = json.load(ifile)
filename = "data/year_{0}_week_{1}.json".format(year1, weeknr1)
with open(filename, 'r') as ifile:
    y = json.load(ifile)

n = len(x)
names, namesNew = [], []
ranks = np.zeros((3, 2, n)) ### [ranks, prices, mcaps]
#print 'Bitcoin' in x["name"]
for j in range(n):
    names.append(x[j]["name"])
    namesNew.append(y[j]["name"])
    ranks[0][0][j] = int(x[j]["rank"])
    ranks[0][1][j] = int(y[j]["rank"])
    ranks[1][0][j] = float(x[j]["price_usd"])
    ranks[1][1][j] = float(y[j]["price_usd"])
    ranks[2][0][j] = float(x[j]["market_cap_usd"])
    ranks[2][1][j] = float(y[j]["market_cap_usd"])
    
    
winners = np.sort(ranks[0][1]-ranks[0][0])[:10]*-1
idx_winners = np.argsort(ranks[0][1]-ranks[0][0])[:10]
loosers = np.sort(ranks[0][1]-ranks[0][0])[-10:][::-1]*-1
idx_loosers = np.argsort(ranks[0][1]-ranks[0][0])[-10:][::-1]

print ""
print "Top 10 of gains in ranking of Market Capitalization:"
for j in range(len(winners)):
    print namesNew[idx_winners[j]], "\t+", int(winners[j])

print ""
print "Top 10 of losses in ranking of Market Capitalization:"
for j in range(len(loosers)):
    print namesNew[idx_loosers[j]], "\t+", int(loosers[j])

print ""
print "Newcomers in the Top 100:"
print "Name\t rank\t price in $\t market cap in $"
new = []
for j in range(n):
    if namesNew[j] not in names:
        new.append([namesNew[j], j])
for k in range(len(new)):
    print new[k][0], "\t", ranks[0][1][new[k][1]], "\t", ranks[1][1][new[k][1]], "\t", ranks[2][1][new[k][1]]
    
print ""
print "Dropped out of the Top 100:"
print "Name\t\t rank\t\t price in $\t\t market cap in $"
dropped = []
for j in range(n):
    if names[j] not in namesNew:
        dropped.append([names[j], j])
for k in range(len(dropped)):
    print dropped[k][0], "\t", ranks[0][0][dropped[k][1]], "\t", ranks[1][0][dropped[k][1]], "\t", ranks[2][0][dropped[k][1]]