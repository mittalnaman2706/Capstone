import requests
from datetime import datetime
from bs4 import BeautifulSoup
import mysql.connector
from selenium import webdriver

cnx = mysql.connector.connect(user='root', password='',
                                 host='localhost',
                                 database='capstone')

mycursor = cnx.cursor()

#clear_table = "DELETE FROM CODECHEF_PRACTICE";
#mycursor.execute(clear_table)
#cnx.commit()

problem_type_array = ["school", "easy", "medium", "hard"]
problem_type_name_array = ["Beginner", "Easy", "Medium", "Hard"]

for j in range(len(problem_type_name_array)):

  problem_name = []
  problem_code = []
  problem_url = []

  url = "https://www.codechef.com/problems/" + problem_type_array[j]
  data=requests.get(url).text
  soup = BeautifulSoup(data,'lxml')

  cnt = 0
  for table in soup.findAll('table'):
   
   for row in table.findAll('tr'):
   
    cnt = 0
    for column in row.findAll('td'):
     
     if cnt == 0:
      problem_name.append(column.text)
     elif cnt == 1:
      problem_code.append(column.text)
      problem_url.append("https://www.codechef.com/problems/"+column.text)
      
     cnt = cnt +1

  for i in range(len(problem_code)):
    
    if i == 0:
     continue

    url = problem_url[i]

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome('C:/Users/HP/Desktop/chromedriver.exe', chrome_options = chrome_options)
    driver.get(url)
    tags = ""
    tables = driver.find_elements_by_xpath("//a[contains(@class,'problem-tag-small  mathjax-support')]")
    for table in tables:
        tags = tags + table.text + '$'
    driver.close()

    sql = "INSERT INTO CODECHEF_PRACTICE VALUES(%s, %s, %s, %s, %s)"
    val = (problem_name[i], problem_code[i], problem_type_name_array[j], problem_url[i], tags)

    mycursor.execute(sql, val)
    cnx.commit()

cnx.close()