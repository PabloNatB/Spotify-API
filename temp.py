# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 00:51:20 2024

@author: pablo
"""

import sqlite3
# establishing  a database connection
con = sqlite3.connect('TEST.db')
# preparing a cursor object
cursor = con.cursor()
# preparing sql statements
sql1 = 'DROP TABLE IF EXISTS EMPLOYEE'

sql2 = '''

       CREATE TABLE EMPLOYEE (
       EMPID INT(6) NOT NULL,
       NAME CHAR(20) NOT NULL,
       AGE INT,
       SEX CHAR(1),
       INCOME FLOAT
       )
      '''

# executing sql statements
cursor.execute(sql1)
cursor.execute(sql2)

# closing the connection
con.close()

import sqlite3
# establishing the connection
con = sqlite3.connect('TEST.db')
# preparing a cursor object
cursor = con.cursor()
# preparing sql statement
rec = (456789, 'Frodo', 45, 'M', 100000.00)
sql = '''
      INSERT INTO EMPLOYEE VALUES ( ?, ?, ?, ?, ?)
      '''
      
# executing sql statement using try ... except blocks

try:

    cursor.execute(sql, rec)

    con.commit()

except Exception as e:

    print("Error Message :", str(e))

    con.rollback()



# closing the database connection

con.close()



import sqlite3



con = sqlite3.connect('TEST.db')



cursor = con.cursor()



# preparing sql statement

records = [

    (123456, 'John', 25, 'M', 50000.00),

    (234651, 'Juli', 35, 'F', 75000.00),

    (345121, 'Fred', 48, 'M', 125000.00),

    (562412, 'Rosy', 28, 'F', 52000.00)

    ]

sql = '''

       INSERT INTO EMPLOYEE VALUES ( ?, ?, ?, ?, ?)

      '''
# executing sql statement using try ... except blocks

try:

    cursor.executemany(sql, records)

    con.commit()

except Exception as e:

    print("Error Message :", str(e))

    con.rollback()



# closing the database connection

con.close()

import sqlite3
# establishing the connection
con = sqlite3.connect('TEST.db')
# preparing a cursor object
cursor = con.cursor()
# preparing sql statement
sql = '''
       SELECT * FROM EMPLOYEE
      '''
# executing the sql statement using `try ... except`
try:
    cursor.execute(sql)
except:
    print('Unable to fetch data.')
    
# fetching the records

records = cursor.fetchall()

#print(records)

# Displaying the records

for record in records:

    print(record)



# closing the connection

con.close()