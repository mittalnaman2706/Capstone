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
url = "https://www.codechef.com/users/"+username

data = ""
driver = webdriver.Chrome('C:/Users/HP/Desktop/chromedriver.exe')
driver.get(url)
tables = driver.find_elements_by_xpath("//section[contains(@class,'rating-data-section submissions')]")
for table in tables:
    data = (table.text)

output = data.split('\n')

partial_ac = output[1][0:len(output[1])//2]
compile_err = output[2][0:len(output[2])//2]
runtime_err = output[3][0:len(output[3])//2]
tle = output[4][0:len(output[4])//2]
wrong = output[5][0:len(output[5])//2]
accepted = output[6][0:len(output[6])//2]

submissions = int(partial_ac) + int(compile_err) + int(runtime_err) + int(tle) + int(wrong) + int(accepted)

easy = 0
beg = 0
med = 0
hard = 0

y = np.array([accepted, partial_ac, compile_err, runtime_err, tle, wrong])
mylabels = ["Accepted", "Partially Accepted", "Compilation Error", "Runtime Error", "TLE", "Wrong"]
myexplode = [0, 0, 0, 0, 0, 0]

plt.pie(y, labels = mylabels, explode = myexplode, autopct='%1.0f%%')
plt.legend(bbox_to_anchor = (1.05, 1.0, 0.60, 0.1), loc = 'upper right')
plt.show()

data = requests.get(url).text
soup = BeautifulSoup(data,'lxml')

country = None
institution = None

ratingOverall = None
ratingSeparate = []
problemsSolved = ''

country = soup.find('span',{"class": "user-country-name"}).text

map = {}
tagsList = pd.read_excel('Tags.xlsx')
mylist = tagsList['Topic-Tags'].tolist()

for tag in mylist:
    map[tag] = 1

finalTags = {}
countSolved = 0

for problem in soup.find('section', {"class":"rating-data-section problems-solved"}).findAll('a'):
 countSolved = countSolved + 1
 problemsSolved += problem.text + '$'
 code = problem.text

 mycursor.execute("SELECT type FROM codechef_practice WHERE CODE = %s", [code])
 result = mycursor.fetchall()

 if len(result) == 0:
      continue

 tup = result[0]
 s =  ''.join(tup)
 if s == 'Beginner':
     beg = beg + 1
 if s == 'Easy':
     easy = easy + 1
 if s == 'Medium':
     med = med + 1
 if s == 'Hard':
     hard = hard + 1

 mycursor.execute("SELECT tags FROM codechef_practice WHERE CODE = %s", [code])
 result = mycursor.fetchall()

 tup = result[0]
 s =  ''.join(tup)
 s = s.split('$')
 #print(s)

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

print(others)

print(finalTags2)
plt.pie([v for v in finalTags2.values()], labels=[k for k in finalTags2],autopct='%1.0f%%')
plt.legend(bbox_to_anchor=(1.05, 1.0, 0.60, 0.1), loc='upper right',)
plt.show()

y = np.array([easy, beg, med, hard])
mylabels = ["Easy", "Beginner", "Medium", "Hard"]

plt.bar(mylabels, y,color ='maroon',
        width = 0.4)

plt.title("Difficulty wise breakup")
plt.show()

ratingOverall = soup.find('div',{"class":"rating-number"}).text

for rating in soup.find('table', {"class":"rating-table"}).findAll('tr'):
 row = rating.findAll('td')
 if len(row) > 0:
  ratingSeparate.append(row[1].text)

for userdetails in soup.find('ul', {"class":"side-nav"}).findAll('li'):
 if userdetails.text[:11] == "Institution":
  institution = userdetails.text[12:]


print(tabulate([['Name', username], ['Username', username], ['Country', country], ['Institution', institution]], headers=['Key', 'Value'], tablefmt='orgtbl'))
print()
print(tabulate([['Rating (Overall)', ratingOverall], ['Long Challenege', ratingSeparate[0]], ['Cook - Off', ratingSeparate[1]], ['Lunch Time', ratingSeparate[2]]], headers=['Key', 'Value'], tablefmt='orgtbl'))
print()
print(tabulate([['Problems Solved', countSolved], ['Submissions', submissions], ['Average Attempt', submissions/countSolved], ['Strong Areas', ], ['Weak Areas', ]], headers=['Key', 'Value'], tablefmt='orgtbl'))


sql = "INSERT INTO codechef_profile VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
val = (username, country, institution,ratingOverall,ratingSeparate[0],ratingSeparate[1],ratingSeparate[2],problemsSolved, beg, easy,
med, hard, partial_ac, compile_err, runtime_err, tle, wrong, accepted)
mycursor.execute(sql, val)
cnx.commit()

cnx.close()