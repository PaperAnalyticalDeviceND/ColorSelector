import csv
import MySQLdb


#get database credentials
with open('credentials.txt') as f:
    line = f.readline()
    split = line.split(",")
f.close()

#open database
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user=split[0], # your username
                      passwd=split[1], # your password
                      db="pad") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

i=0
file1 = open("op.csv", "w")

with open("10_reg_rgb_full.csv") as csvfile:
  csvreader = csv.reader(csvfile)
  for crow in csvreader:

    if crow[0]: # and i<10:
      i += 1
      print("row data", crow[0])
      # Use all the SQL you like
      cur.execute('SELECT * FROM `card` WHERE `id`=' + crow[0])

      # print all the first cell of all the rows
      for row in cur.fetchall() :
          print (row)
          leng = len(row)
          for c in range(leng):
            file1.write(str(row[c]).replace(',', '|').replace('\n', ' ')+',')
          file1.write('\n')

file1.close()


