import requests
from bs4 import BeautifulSoup
import mysql.connector

cnx = mysql.connector.connect(user='root', password='',
                              host='localhost',
                              database='capstone')

mycursor = cnx.cursor()

clear_table = "DELETE FROM CODEFORCES_PRACTICE"
mycursor.execute(clear_table)
cnx.commit()

common = "https://codeforces.com/problemset/problem/"
problem_name = []
problem_code = []
problem_url = []
problem_diff = []
index = 1

while(index <= 70):
 print(index)
 url = "https://codeforces.com/problemset/page/" + str(index)
 data=requests.get(url).text
 soup = BeautifulSoup(data,'lxml')

 cnt = 0
 for table in soup.findAll('table'):

     for row in table.findAll('tr'):

         cnt = 0
         for column in row.findAll("td"):

             s = column.text

             if cnt == 0:
                 s = s.rstrip()
                 s = s.strip()
                 problem_code.append(s)

                 n = len(s)
                 i = 0
                 f = ""
                 sc = ""

                 while(i < n and s[i].isalpha() == 0):
                     f += s[i]
                     i = i +1

                 while(i < n):
                     sc += s[i]
                     i = i +1

                 problem_url.append(common+f+"/"+sc)

             if cnt == 1:
              s = s.split('\n')
              s[3] = s[3].rstrip()
              s[3] = s[3].strip()
              problem_name.append((s[3]))

             if cnt == 3:
                 s = s.rstrip()
                 s = s.strip()

                 if len(s) == 0 or s[0] == 'x':
                     problem_diff.append("Easy")
                     continue

                 if int(s) >= 0 and int(s) <= 800:
                     problem_diff.append("Beginner")
                 elif int(s) > 800 and int(s) <= 1400:
                     problem_diff.append("Easy")
                 elif int(s) > 1400 and int(s) <= 1800:
                     problem_diff.append("Medium")
                 else:
                     problem_diff.append("Hard")

             cnt = cnt +1

 index = index + 1

for i in range(len(problem_code)):
    sql = "INSERT INTO CODEFORCES_PRACTICE VALUES(%s, %s, %s, %s)"
    val = (problem_name[i], problem_code[i], problem_diff[i], problem_url[i])

    mycursor.execute(sql, val)
    cnx.commit()

print(problem_code)
print(problem_name)
print(problem_url)
print(problem_diff)

cnx.close()