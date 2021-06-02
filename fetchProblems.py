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
mycursor.execute("SELECT * FROM codechef_practice")
result = mycursor.fetchall()

for tup in result:
    print(tup)

mycursor = cnx.cursor()
mycursor.execute("SELECT * FROM codeforces_problems")
result = mycursor.fetchall()

for tup in result:
    print(tup)