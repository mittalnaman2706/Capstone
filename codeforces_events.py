import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector

contest_name = []
contest_url = []
start_time = []
end_time = []

cnx = mysql.connector.connect(user='root', password='', host='localhost', database='capstone')

mycursor = cnx.cursor()

clear_table = "DELETE FROM codeforces";
mycursor.execute(clear_table)
cnx.commit()

months = dict(Jan="01", Feb="02", Mar="03", Apr="04", May="05", Jun="06", Jul="07", Aug="08", Sep="09", Oct="10", Nov="11", Dec="12")

url = "https://www.codeforces.com/contests"

data=requests.get(url).text
soup = BeautifulSoup(data,'lxml')

cnt = 0

for table in soup.findAll('table'):
 
 for row in table.findAll('tr'):
  
  cnt = 0
  for column in row.findAll('td'):
   
   if cnt == 0:
    contest_name.append(column.text)
    contest_url.append("https://www.codeforces.com/contests")
   elif cnt == 1:
    f=0
   elif cnt == 2:
    start_time.append(column.text)
   elif cnt == 3:
    end_time.append(column.text)
   else:
    break 
   cnt = cnt +1

fil=open('text_file.txt','w')

for i in range(len(end_time)):
  fil.write(contest_name[i])
  fil.write(start_time[i])
  fil.write(end_time[i])


# for i in range(len(contest_code)):
  
#   if(i==0):
#     continue
      
#   start_time[i] = start_time[i][7:11]+'-'+months[start_time[i][3:6]]+'-'+start_time[i][0:2]+' '+start_time[i][-8:]
#   end_time[i] = end_time[i][7:11]+'-'+months[end_time[i][3:6]]+'-'+end_time[i][0:2]+' '+end_time[i][-8:]
#   print(2)

#   sql = "INSERT INTO codeforces VALUES(%s, %s, %s, %s, %s)"
#   val = (contest_code[i], contest_name[i], start_time[i], 
#   	end_time[i], contest_url[i])
#   mycursor.execute(sql, val)
#   cnx.commit()

cnx.close()
