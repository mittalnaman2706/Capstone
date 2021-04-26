import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector

url = "https://www.codechef.com/tags/problems/array"
data=requests.get(url).text

print(data)

# soup = BeautifulSoup(data,'lxml')

# cnt = 0
# for table in soup.findAll('table'):
 
#  for row in table.findAll('tr'):
 
#   cnt = 0
#   for column in row.findAll('td'):
   
#    if cnt == 0:
#     problem_name.append(column.text)
#    elif cnt == 1:
#     problem_code.append(column.text)
#     print(column.text)
#     problem_url.append("https://www.codechef.com/problems/"+column.text)
    
#    cnt = cnt +1


