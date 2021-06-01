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

weaksz = (int((size * 50)/100))
goodsz = weaksz + (int((size * 40)/100))
profsz = (int((size * 10)/100))
counter = 0
weak = ""
prof = ""
good = ""

for code in finalTags2:

    if counter < weaksz:
        weak += code + "$";
    elif counter < goodsz:
        good += code + "$"
    else:
        prof += code + "$";

    counter += 1

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

print(username)
print(ratingOverall)
print(countSolved)
print(submissions)
print(submissions/countSolved)

print(easy)
print(beg)
print(medium)
print(hard)

print(partialac)
print(tle)
print(wrong)
print(ac)
print(compileerr)
print(runtimeerr)
print(finalTags2)

print(weak)
print(good)
print(prof)


mycursor.execute("SELECT * FROM codechef_practice")
result = mycursor.fetchall()
sz = len(result)
counter = 0
x = p = 0

mark = {}
w = weak.split('$')
for code in w:
    mark[code] = 1

easyRc = ""
easyRl = ""
while p < sz and counter < 10:

    x = p
    p = p + 1
    tags = result[x][4]

    if result[x][2] != "Beginner":
        continue

    splitted = tags.split('$')

    for t in splitted:
        if len(t) > 0 and t in mark:
            easyRc += result[x][1] + "$"
            easyRl += result[x][3] + "$"
            counter = counter + 1
            break


print(easyRc)
print(easyRl)

counter = 0
x = p = 0
sz = len(result)
mark = {}
g = good.split('$')
for code in g:
    mark[code] = 1

mediumRc = ""
mediumRl = ""
while p < sz and counter < 10:

    x = p
    p = p + 1
    tags = result[x][4]

    if result[x][2] != "Medium":
        continue

    splitted = tags.split('$')

    for t in splitted:
        if len(t) > 0 and t in mark:
            mediumRc += result[x][1] + "$"
            mediumRl += result[x][3] + "$"
            counter = counter + 1
            break

print(mediumRc)
print(mediumRl)

counter = 0
x = p = 0
mark = {}
g = prof.split('$')
for code in g:
    mark[code] = 1

hardRc = ""
hardRl = ""
while p < sz and counter < 10:

    x = p
    p = p + 1
    tags = result[x][4]

    if result[x][2] != "Hard":
        continue

    splitted = tags.split('$')

    for t in splitted:
        if len(t) > 0 and t in mark:
            hardRc += result[x][1] + "$"
            hardRl += result[x][3] + "$"
            counter = counter + 1
            break

    x = x+1

print(hardRc)
print(hardRl)

"""
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

plt.pie([v for v in finalTags2.values()], labels=[k for k in finalTags2],autopct='%1.0f%%')
plt.legend(bbox_to_anchor=(1.05, 1.0, 0.60, 0.1), loc='upper right',)
plt.show()

print(tabulate([['Name', username], ['Username', username], ['Country', country], ['Institution', institution]], headers=['Key', 'Value'], tablefmt='orgtbl'))
print()
print(tabulate([['Rating (Overall)', ratingOverall], ['Long Challenege', ratingLong], ['Cook - Off', ratingCook], ['Lunch Time', ratingLunch]], headers=['Key', 'Value'], tablefmt='orgtbl'))
print()
print(tabulate([['Problems Solved', countSolved], ['Submissions', submissions], ['Average Attempt', submissions/countSolved]], headers=['Key', 'Value'], tablefmt='orgtbl'))
"""

cnx.close()