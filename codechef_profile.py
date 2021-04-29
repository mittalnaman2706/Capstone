import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import sys
from selenium import webdriver
import matplotlib.pyplot as plt
import pandas as pd
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

print(partial_ac)
print(compile_err)
print(runtime_err)
print(tle)
print(wrong)
print(accepted)


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

for problem in soup.find('section', {"class":"rating-data-section problems-solved"}).findAll('a'):
 problemsSolved += problem.text + '$'
 code = problem.text

 mycursor.execute("SELECT tags FROM codechef_practice WHERE CODE = %s", [code])
 result = mycursor.fetchall()
 if len(result) == 0:
     continue

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

print(finalTags)
plt.pie([v for v in finalTags.values()], labels=[k for k in finalTags],autopct=None)
plt.legend(bbox_to_anchor=(1.05, 1.0, 0.60, 0.1), loc='upper right')
plt.show()

ratingOverall = soup.find('div',{"class":"rating-number"}).text

for rating in soup.find('table', {"class":"rating-table"}).findAll('tr'):
 row = rating.findAll('td')
 if len(row) > 0:
  ratingSeparate.append(row[1].text)

for userdetails in soup.find('ul', {"class":"side-nav"}).findAll('li'):
 if userdetails.text[:11] == "Institution":
  institution = userdetails.text[12:]

#sql = "INSERT INTO codechef_profile VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
#val = (username, country, institution,ratingOverall,ratingSeparate[0],ratingSeparate[1],ratingSeparate[2],problemsSolved)
#mycursor.execute(sql, val)
#cnx.commit()

cnx.close()