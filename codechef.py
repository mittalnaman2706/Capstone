import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector

contest_code = []
contest_name = []
contest_url = []
start_time = []
end_time = []

cnx = mysql.connector.connect(user='root', password='',
                                 host='localhost',
                                 database='capstone')

mycursor = cnx.cursor()

clear_table = "DELETE FROM CODECHEF";
mycursor.execute(clear_table)
cnx.commit()

months = dict(Jan="01", Feb="02", Mar="03", Apr="04", May="05", Jun="06", Jul="07", Aug="08", Sep="09", Oct="10", Nov="11", Dec="12")

url = "https://www.codechef.com/contests"
f3=open('events.txt','w')

data=requests.get(url).text
soup = BeautifulSoup(data,'lxml')

map = dict() 

cnt = 0
for table in soup.findAll('table'):
 
 for row in table.findAll('tr'):
 
  cnt = 0
  for column in row.findAll('td'):
   
   if cnt == 0:
    contest_code.append(column.text)
    contest_url.append("https://www.codechef.com/"+column.text)
   elif cnt == 1:
    contest_name.append(column.text)
   elif cnt == 2:
    start_time.append(column.text)
   elif cnt == 3:
    end_time.append(column.text)
    
   cnt = cnt +1

for i in range(len(contest_code)):
  
  if i == 0:
   continue
  
  if contest_code[i] in map:
   continue
   
  map[contest_code[i]] = 1
  
  start_time[i] = start_time[i][7:11]+'-'+months[start_time[i][3:6]]+'-'+start_time[i][0:2]+' '+start_time[i][-8:]
  end_time[i] = end_time[i][7:11]+'-'+months[end_time[i][3:6]]+'-'+end_time[i][0:2]+' '+end_time[i][-8:]
  
  sql = "INSERT INTO codechef VALUES(%s, %s, %s, %s, %s)"
  val = (contest_code[i], contest_name[i], start_time[i], 
  	end_time[i], contest_url[i])
  mycursor.execute(sql, val)
  cnx.commit()

cnx.close()
