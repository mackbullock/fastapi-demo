#!/usr/bin/env python3
import mysql.connector
from mysql.connector import Error
from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import json
import os

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB= "ejv4pz"
db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "Hello API"}


@app.get("/add/{a}/{b}") # {a} and {b} are url parameters
def add(a: int, b: int):
    return {"sum": a + b}


@app.get("/customer/{idx}")
def customer(idx: int): # indicated idx should be an int
    # read the data into a df
    df = pd.read_csv("customers.csv") # ../  if customers.csv is in a different dir than main.py
    # filter the data based on index
    customer = df.iloc[idx] # iloc = index locator, "get the location by index," one param (the index)
    return customer.to_dict() # returning dictionary with key-value pairs


@app.post("/get_body") # decorating api with "post" name
async def get_body(request: Request): #async and await allow for some "slowness" in the fast api
    response = await request.json()
    first_name = response["fname"]
    last_name = response["lname"]
    favorite_number = response["favnum"]
    return {"first_name": first_name, "last name": last_name, "favorite_number": favorite_number}


@app.get('/genres')
def get_genres():
   db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
   cur=db.cursor()
   query = "SELECT * FROM genres ORDER BY genreid;"
   try:
       cur.execute(query)
       headers=[x[0] for x in cur.description]
       results = cur.fetchall()
       json_data = []
       for result in results:
           json_data.append(dict(zip(headers,result)))
       cur.close()
       db.close()
       return(json_data)
   except Error as e:
       cur.close()
       db.close()
       return {"Error": "MySQL Error: " + str(e)}


@app.get('/songs')
def get_songs():
    db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
    cur=db.cursor()
    query = "SELECT * FROM songs s LEFT JOIN genres g ON s.genre = g.genreid;"
    try: 
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers,result)))
        cur.close()
        db.close()
        return(json_data)
    except Error as e:
        cur.close()
        db.close() 
        return{"Error": "MySQL Error: " + str(e)}

