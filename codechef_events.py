import mysql.connector
from selenium import webdriver


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

driver = webdriver.Chrome('C:/Users/HP/Desktop/chromedriver.exe')
driver.get(url)
driver.get("https://www.codechef.com/contests")

tables = driver.find_elements_by_xpath("//table[contains(@class,'dataTable')]//tbody")

for table in tables:
    for row in table.find_elements_by_tag_name("tr"):
        cnt = 0;
        for details in row.find_elements_by_tag_name("td"):
            if cnt == 0:
                contest_code.append(details.text)
                contest_url.append("https://www.codechef.com/"+details.text)
            elif cnt == 1:
                contest_name.append(details.text)
            elif cnt == 2:
                start_time.append(details.text)
                print(details.text)
            else:
                end_time.append(details.text)
            cnt = cnt+1


for i in range(len(contest_code)):

  start_time[i] = start_time[i][7:11]+'-'+months[start_time[i][3:6]]+'-'+start_time[i][0:2]+' '+start_time[i][-8:]
  end_time[i] = end_time[i][7:11]+'-'+months[end_time[i][3:6]]+'-'+end_time[i][0:2]+' '+end_time[i][-8:]
  print(contest_code[i])
  sql = "INSERT INTO codechef VALUES(%s, %s, %s, %s, %s)"
  val = (contest_code[i], contest_name[i], start_time[i], 
    end_time[i], contest_url[i])
  mycursor.execute(sql, val)
  cnx.commit()

cnx.close()