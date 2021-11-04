#4th asst

import os
import csv
import sys
from flask import Flask, render_template,redirect, url_for, request, flash
import pyodbc
import pandas as pd
import time
from random import randint
import redis 
import pymongo
from pymongo import MongoClient

##DB Connection
server = 'sindoorasqlserver.database.windows.net'
database = 'sindooradatabase'
username = 'sindooraadmin'
password = 'azureSin1996!'   
driver= '{ODBC Driver 17 for SQL Server}'

conn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor()


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/myinfo')
def myInfo():
    return render_template('firstpage.html')


@app.route('/functions', methods=["POST","GET"])
def actions():
  if request.method== "POST":
    return render_template('index.html',input=1)


@app.route('/mag_pie', methods=["POST","GET"])
def sumofearthquakes():
  earthquakes=[]
  quakes={'Mag Range':'Count of Earthquakes'}
  for i in range(1,6):
    query="Select count(*) from [dbo].[newEarthquake] where mag between " +str(i)+ " and " +str((i+1))
    cursor.execute(query)
    val=cursor.fetchall()
    val=int(val[0][0])
    earthquakes.append(val)
    quakes['Mag: '+str(i)+'-'+str(i+1)]=val
  return render_template('piechart.html',data=quakes)

@app.route('/mag_scatter', methods=["POST","GET"])
def scatterquakes():
  query="select Top(100) Mag, depth from [dbo].[newEarthquake] order by time desc"
  cursor.execute(query)
  val=cursor.fetchall()
  quakes=[]
  for i in val:
    quakes.append(list(i))
  #print(quakes)
  return render_template('scatter.html',data1=quakes)


@app.route('/mag_bar', methods=["POST","GET"])
def sumofearthquake1():
  earthquakes=[]
  quakes={'Magnitude':'Count of Earthquakes',}
  # quakes={}
  for i in range(1,6):
    query="Select count(*) from [dbo].[newEarthquake] where mag="+str(i)
    cursor.execute(query)
    val=cursor.fetchall()
    val=int(val[0][0])
    earthquakes.append(val)
    quakes['Mag= '+str(i)]=val
  return render_template('barchart.html',data=quakes)



if __name__ == "__main__":
    app.run(port=5000, debug=True)