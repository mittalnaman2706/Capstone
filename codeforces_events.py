import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector

contest_name = []
contest_url = []
start_time = []
contest_duration = []

cnx = mysql.connector.connect(user='root', password='', host='localhost', database='capstone')

mycursor = cnx.cursor()

clear_table = "DELETE FROM codeforces";
mycursor.execute(clear_table)
cnx.commit()

months = dict(Jan="01", Feb="02", Mar="03", Apr="04", May="05", Jun="06", Jul="07", Aug="08", Sep="09", Oct="10", Nov="11", Dec="12")

url = "https://www.codeforces.com/contests"

data=requests.get(url).text
soup = BeautifulSoup(data,'lxml')

liv=0
for table in soup.findAll('table'):

 for row in table.findAll('tr'):

  cnt = 0
  liv=liv+1
  if(liv>6):
    break
  for column in row.findAll('td'):
   if cnt == 0:
    contest_name.append(column.text)
    contest_url.append(url)
   elif cnt == 1:
    random=0
   elif cnt == 2:
    start_time.append(column.text)
   elif cnt == 3:
    contest_duration.append(column.text)
   else:
    break 
   cnt = cnt +1

contest_name = [x.replace("\r","") for x in contest_name]
contest_name = [x.replace("\n","") for x in contest_name]
contest_duration  = [x.replace("\r","") for x in contest_duration]
contest_duration  = [x.replace("\n","") for x in contest_duration]
start_time  = [x.replace("\r","") for x in start_time]
start_time  = [x.replace("\n","") for x in start_time]


print(contest_name)
print(start_time)
print(contest_duration)

fil=open('text_file.txt','w')

for i in range(len(start_time)):
  fil.write(contest_name[i])
  fil.write(start_time[i])
  fil.write(contest_duration[i])


for i in range(len(contest_name)):
  
  start_time[i] = start_time[i][7:11]+'-'+months[start_time[i][0:3]]+'-'+start_time[i][4:6]+' '+start_time[i][-6:]
  # end_time[i] = end_time[i][7:11]+'-'+months[end_time[i][3:6]]+'-'+end_time[i][0:2]+' '+end_time[i][-8:]
  # print(2)

  sql = "INSERT INTO codeforces VALUES(%s, %s, %s, %s)"
  val = (contest_name[i], contest_url[i], start_time[i], contest_duration[i])
  mycursor.execute(sql, val)
  cnx.commit()

cnx.close()
