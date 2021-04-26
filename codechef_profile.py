import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import sys
from selenium import webdriver

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

print(data)

partial_ac = ""
accepted = ""
wrong = ""
tle = ""
runtime_err = ""
compile_err = ""

data = requests.get(url).text
soup = BeautifulSoup(data,'lxml')

country = None
institution = None

ratingOverall = None
ratingSeparate = []
problemsSolved = ''

country = soup.find('span',{"class": "user-country-name"}).text

for problem in soup.find('section', {"class":"rating-data-section problems-solved"}).findAll('a'):
 problemsSolved += problem.text + '$'

ratingOverall = soup.find('div',{"class":"rating-number"}).text

for rating in soup.find('table', {"class":"rating-table"}).findAll('tr'):
 row = rating.findAll('td')
 if len(row) > 0:
  ratingSeparate.append(row[1].text)

for userdetails in soup.find('ul', {"class":"side-nav"}).findAll('li'):
 if userdetails.text[:11] == "Institution":
  institution = userdetails.text[12:]

sql = "INSERT INTO codechef_profile VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
val = (username, country, institution,ratingOverall,ratingSeparate[0],ratingSeparate[1],ratingSeparate[2],problemsSolved)
mycursor.execute(sql, val)
cnx.commit()

cnx.close()