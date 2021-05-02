import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import sys
from selenium import webdriver
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt

cnx = mysql.connector.connect(user='root', password='', host='localhost', database='capstone')
mycursor = cnx.cursor()

username = sys.argv[1]

mycursor = cnx.cursor()
mycursor.execute("SELECT * FROM codechef_profile WHERE username = %s", [username])
result = mycursor.fetchall()

for tup in result:
    username = tup[0]
    country = tup[1]
    institution = tup[2]
    ratingOverall = tup[3]
    ratingLong = tup[4]
    ratingCook = tup[5]
    ratingLunch = tup[6]
    problems = tup[7]
    beg = tup[8]
    easy = tup[9]
    medium = tup[10]
    hard = tup[11]
    partialac = tup[12]
    compileerr = tup[13]
    runtimeerr = tup[14]
    tle = tup[15]
    wrong = tup[16]
    ac = tup[17]

submissions = partialac + compileerr + runtimeerr + tle + wrong + ac

y = np.array([ac, partialac, compileerr, runtimeerr, tle, wrong])
mylabels = ["Accepted", "Partially Accepted", "Compilation Error", "Runtime Error", "TLE", "Wrong"]
myexplode = [0, 0, 0, 0, 0, 0]
plt.pie(y, labels = mylabels, explode = myexplode, autopct='%1.0f%%')
plt.legend(bbox_to_anchor = (1.05, 1.0, 0.60, 0.1), loc = 'upper right')
plt.show()

y = np.array([easy, beg, medium, hard])
mylabels = ["Easy", "Beginner", "Medium", "Hard"]
plt.bar(mylabels, y,color ='maroon',width = 0.4)
plt.title("Difficulty wise breakup")
plt.show()

map = {}
tagsList = pd.read_excel('Tags.xlsx')
mylist = tagsList['Topic-Tags'].tolist()

for tag in mylist:
    map[tag] = 1

finalTags = {}
countSolved = 0

solved = problems.split('$')

for problem in solved:
    countSolved = countSolved + 1
    code = problem
    mycursor.execute("SELECT tags FROM codechef_practice WHERE CODE = %s", [code])
    result = mycursor.fetchall()

    if (len(result)) == 0:
        continue

    tup = result[0]
    s =  ''.join(tup)
    s = s.split('$')

    for t in s:

        if t in map:
            if t in finalTags:
                finalTags[t] = finalTags[t] + 1
            else:
                finalTags[t] = 1

sorted_tuples = sorted(finalTags.items(), key=lambda item: item[1])
finalTags2 = {k: v for k, v in sorted_tuples}

others = 0
size = len(finalTags2)
z = (int((size * 30)/100))
print(size, z)
sz = len(finalTags2) - z
res = dict(itertools.islice(finalTags2.items(), sz))
for v in res.values():
    others = others + int(v)

o = 'others'
finalTags2[o] = others

i = 0
while(1):
    if i == sz:
        break

    del finalTags2[next(iter(finalTags2))]
    i = i + 1

plt.pie([v for v in finalTags2.values()], labels=[k for k in finalTags2],autopct='%1.0f%%')
plt.legend(bbox_to_anchor=(1.05, 1.0, 0.60, 0.1), loc='upper right',)
plt.show()

print(tabulate([['Name', username], ['Username', username], ['Country', country], ['Institution', institution]], headers=['Key', 'Value'], tablefmt='orgtbl'))
print()
print(tabulate([['Rating (Overall)', ratingOverall], ['Long Challenege', ratingLong], ['Cook - Off', ratingCook], ['Lunch Time', ratingLunch]], headers=['Key', 'Value'], tablefmt='orgtbl'))
print()
print(tabulate([['Problems Solved', countSolved], ['Submissions', submissions], ['Average Attempt', submissions/countSolved]], headers=['Key', 'Value'], tablefmt='orgtbl'))


cnx.close()