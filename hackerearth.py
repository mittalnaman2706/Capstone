import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
import datetime
import mysql.connector

live_challenge_type = []
live_challenge_name = []
live_challenge_url = []

"""
live_challenge_countdown_day = []
live_challenge_countdown_hrs = []
live_challenge_countdown_min = []
"""

upcoming_challenge_type = []
upcoming_challenge_name = []
upcoming_challenge_url = []
upcoming_challenge_date = []

cnx = mysql.connector.connect(user='root', password='',
                                 host='localhost',
                                 database='capstone')

mycursor = cnx.cursor()

clear_table = "DELETE FROM HACKEREARTH_LIVE";
mycursor.execute(clear_table)
cnx.commit()

clear_table = "DELETE FROM HACKEREARTH_UPCOMING";
mycursor.execute(clear_table)
cnx.commit()


months = dict(Jan="01", Feb="02", Mar="03", Apr="04", May="05", Jun="06", Jul="07", Aug="08", Sep="09", Oct="10", Nov="11", Dec="12")
url = "https://www.hackerearth.com/challenges/"

data = requests.get(url).text
soup = BeautifulSoup(data,'lxml')

for live in soup.findAll('div',{"class": "ongoing challenge-list"}):
 for type in live.findAll('div',{"class": "challenge-type light smaller caps weight-600"}):
  live_challenge_type.append(type.text)

for live in soup.findAll('div',{"class": "ongoing challenge-list"}):
 for name in live.findAll('div',{"class": "challenge-name ellipsis dark"}):
  live_challenge_name.append(name.text)

for live in soup.findAll('div',{"class": "ongoing challenge-list"}):
 for url in live.findAll('a',{"class": "challenge-card-wrapper challenge-card-link"}):
   link = url['href']
   if link.startswith("https://"):
    live_challenge_url.append(link)
   else:
    link = "https://www.hackerearth.com" + link
    live_challenge_url.append(link)

"""
for live in soup.findAll('div',{"class": "ongoing challenge-list"}):
 for day1 in live.findAll('div',{"id": "days-1"}):
   print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(day1.text))))
   #print(day1.text+day0.text);
   #live_challenge_countdown_day.append(day1.text+day0.text)

for live in soup.findAll('div',{"class": "ongoing challenge-list"}):
 for hrs in live.findAll('div',{"id": "date date-countdown"}):
  live_challenge_countdown_hrs.append(hrs.text)
  
for live in soup.findAll('div',{"class": "ongoing challenge-list"}):
 for min in live.findAll('div',{"id": "date date-countdown"}):
  live_challenge_countdown_min.append(min.text)
"""

for i in range(len(live_challenge_type)):

  live_challenge_type[i].strip()
  sql = "INSERT INTO hackerearth_live VALUES(%s, %s, %s)"
  val = (live_challenge_type[i], live_challenge_name[i], live_challenge_url[i])
  mycursor.execute(sql, val)
  cnx.commit()

 
for upcoming in soup.findAll('div',{"class": "upcoming challenge-list"}):
 for type in upcoming.findAll('div',{"class": "challenge-type light smaller caps weight-600"}):
  upcoming_challenge_type.append(type.text)

for upcoming in soup.findAll('div',{"class": "upcoming challenge-list"}):
 for name in upcoming.findAll('div',{"class": "challenge-name ellipsis dark"}):
  upcoming_challenge_name.append(name.text)

for upcoming in soup.findAll('div',{"class": "upcoming challenge-list"}):
 for url in upcoming.findAll('a',{"class": "challenge-card-wrapper challenge-card-link"}):
   link = url['href']
   if link.startswith("https://"):
    upcoming_challenge_url.append(link)
   else:
    link = "https://www.hackerearth.com" + link
    upcoming_challenge_url.append(link)
 
for upcoming in soup.findAll('div',{"class": "upcoming challenge-list"}):
 for date in upcoming.findAll('div',{"class": "date less-margin dark"}):
  
  m = months[date.text[0:3]]
  if date.text[4] == ' ':
   d = '0'+date.text[5:6]
  else:
   d = date.text[4:6]
  y = '2021'
  t_d = date.text[8:10]
  t_m = date.text[10:13]
  mrdm = date.text[14:16]
  
  if mrdm == 'PM':
   t_d = int(t_d) + 12
  
  t = str(t_d) + t_m + ':00'

  date = y+'-'+m+'-'+d+' '+t
  upcoming_challenge_date.append(date)


for i in range(len(live_challenge_type)):
 
  sql = "INSERT INTO hackerearth_upcoming VALUES(%s, %s, %s, %s)"
  val = (upcoming_challenge_type[i], upcoming_challenge_name[i], upcoming_challenge_url[i], upcoming_challenge_date[i])
  mycursor.execute(sql, val)
  cnx.commit()
  
cnx.close()
