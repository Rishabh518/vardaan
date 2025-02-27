'''import pyodbc as odbc
import json
connection_string ='Driver={ODBC Driver 18 for SQL Server};Server=tcp:2203051050471.database.windows.net,1433;Database=vardaan;Uid=Rishabh;Pwd=Rishpu96;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

try:
    conn = odbc.connect(connection_string)
    print("Connection successful!")
except odbc.Error as e:
    print("Error:", e)

cursor = conn.cursor()

query = CREATE TABLE wellwisher (
      userid INT NOT NULL IDENTITY(1,1),
      username VARCHAR(45) NOT NULL,
      name VARCHAR(55) NOT NULL,
      mobileno VARCHAR(13) NOT NULL,
      email VARCHAR(45) NOT NULL,
      address VARCHAR(60) NOT NULL,
      password VARCHAR(45) NOT NULL,
      type VARCHAR(45) DEFAULT 'active',
      PRIMARY KEY (userid),
      UNIQUE (mobileno),
      UNIQUE (email),
      UNIQUE (username)
    )
cursor.execute(query)

sql = INSERT INTO wellwisher (username, name, mobileno, email, address, password) 
             VALUES ('Rishabh_121', 'Rishabh', '8194898905', 'rishabh@gmail.com', 'parul', 'rishabh123')
cursor.execute(sql)

print("inserted")

query2=CREATE TABLE organization(
        id INT NOT NULL IDENTITY(1,1),
        org_id VARCHAR(45) NOT NULL,
        org_name VARCHAR(100) NOT NULL,
        org_email VARCHAR(45) NOT NULL,
        org_mobile VARCHAR(45) NOT NULL,
        org_address VARCHAR(100) NOT NULL,
        org_country VARCHAR(45) NOT NULL,
        org_state VARCHAR(45) NOT NULL,
        description VARCHAR(500) NOT NULL,
        org_pswd VARCHAR(45) NOT NULL,
        PRIMARY KEY (id),
    UNIQUE (org_id),
    UNIQUE (org_mobile),
    UNIQUE (org_email)
) 

cursor.execute(query2)
print("succesfully executed query2")
cursor.commit()


cursor.execute(INSERT INTO organization 
                (org_name, org_id, org_email, org_mobile, org_address, org_country, org_state, description, org_pswd) 
                VALUES ('smile', 6750,'smile@gmail.com', 8754327890 , 'parul', 'america', 'ohio', 'testing', '1234'))
print('Successfully')
cursor.commit()


query3=
  CREATE TABLE wellwisher_posts(
   post_id INT NOT NULL IDENTITY(1,1),
   userid VARCHAR(45) NOT NULL,
   username VARCHAR(45) NOT NULL,
   name VARCHAR(45) NOT NULL,
   postdesc VARCHAR(500) NOT NULL,
   date DATE NOT NULL,
   address VARCHAR(100) NOT NULL,
   status VARCHAR(45) NOT NULL DEFAULT 'active',
  PRIMARY KEY (post_id ),
  UNIQUE (post_id) 
  )

cursor.execute(query3)
cursor.commit()
print('query3 executed')


query4=
CREATE TABLE organization_posts(
  post_id INT NOT NULL IDENTITY(1,1) ,
  org_id VARCHAR(45) NOT NULL,
  org_name VARCHAR(100) NOT NULL,
  postdesc VARCHAR(500) NOT NULL,
  org_address VARCHAR(100) NOT NULL,
  date DATE NOT NULL,
  status VARCHAR(45) NOT NULL DEFAULT 'active',
  PRIMARY KEY (post_id)
  );

cursor.execute(query4)
cursor.commit()
print('query4 executed')


query5=
CREATE TABLE food_post (
  post_id int NOT NULL IDENTITY(1,1),
  userid varchar(45) NOT NULL,
  username varchar(45) NOT NULL,
  name varchar(45) NOT NULL,
  postdesc varchar(500) NOT NULL,
  qtyavl varchar(45) NOT NULL,
  pickuplocation varchar(45) NOT NULL,
  pickuptime varchar(45) NOT NULL,
  address varchar(45) NOT NULL,
  date date NOT NULL,
  status varchar(45) NOT NULL DEFAULT 'active',
  PRIMARY KEY (post_id)
);

cursor.execute(query5)
cursor.commit()
print=("query5 executed")
<<<<<<< HEAD
'''
query='Truncate table wellwisher_posts'
query3='ALTER TABLE food_post ALTER COLUMN imageurl VARCHAR(100) NULL;'
cursor.execute(query3)


cursor.commit()

print('successfull!!')

Hi i have some old clothes that are in good condition they are not of my use because i have loose my weight and thoose clothes are in xl pr xxl size so if you need them or know any people need them please feel free to contact

I There we are organising a blanket distribution drive at phase 10 market. we need some people while distributing so they can help us or can bring any unused blankets if they have any . Thank you for your support!!

=======


query = CREATE TABLE wellwisher (
      userid INT NOT NULL IDENTITY(1,1),
      username VARCHAR(45) NOT NULL,
      name VARCHAR(55) NOT NULL,
      mobileno VARCHAR(13) NOT NULL,
      email VARCHAR(45) NOT NULL,
      state VARCHAR(60) NOT NULL,
      country VARCHAR(60) NOT NULL,
      password VARCHAR(45) NOT NULL,
      status VARCHAR(45) DEFAULT 'active',
      PRIMARY KEY (userid),
      UNIQUE (mobileno),
      UNIQUE (email),
      UNIQUE (username)
    )
cursor.execute(query)
cursor.commit()
print("succesfully executed")
'''
import certifi
from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# Corrected MONGO_URI with proper encoding
MONGO_URI = "mongodb+srv://2203051050471:Rish%40bh%402004@firstcluster.v2fb3.mongodb.net/vardaan?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())  # Connect to MongoDB
    db = client["vardaan"]
    print("✅ Connected successfully!")
except Exception as e:
    print("❌ Connection failed:", e)

# Insert Data
collection = db["wellwisher"]
collection.insert_one({"name": "Rishabh"})
print("✅ Data inserted successfully!")
>>>>>>> 2fbe3c3 (codeunnati)
