from flask import Flask, jsonify, render_template
import sqlite3
from google.cloud import storage
import pandas as pd
import numpy as np
from datetime import datetime
import mysql.connector
import sys

# establish sql connection
cnx = mysql.connector.connect(user='root', host='35.239.55.41', database='imdbmovies')
# Create a cursor object and execute the query
cursor = cnx.cursor()

#query for the last date of data upload
cursor.execute("SELECT MAX(date_uploaded) FROM movielist")
DateData = cursor.fetchall()[0][0].strftime("%d %b %Y")
#query for pie chart data
cursor.execute("SELECT director, COUNT(*) AS movie_count  FROM movielist  WHERE date_uploaded = (SELECT MAX(date_uploaded) FROM movielist) GROUP BY director  ORDER BY movie_count DESC LIMIT 10")
barChartData = cursor.fetchall()
#query for pie chart data
cursor.execute("SELECT releaseyear, rating FROM movielist WHERE date_uploaded = (SELECT MAX(date_uploaded) FROM movielist)")
scatterData = cursor.fetchall()

# create web pages
app = Flask(__name__)   

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/directors")
def google_bar_chart1():
    data1 =  [['Director', '#PopularMovies']]
    for row in barChartData:
        data1.append([row[0], row[1]])
    return render_template('bar.html', data1=data1, last_updated = DateData)

@app.route("/year")
def scatter_chart():
    data2 =  [['Release Year', 'Rating']]
    for row in scatterData:
        data2.append([row[0], row[1]])
    return render_template('scatterplot.html', data2=data2, last_updated = DateData)


@app.route("/tree")
def google_tree_chart1():
    treemapData = []
    cursor.execute("SELECT title, director, rating , releaseyear FROM movies ORDER BY rating DESC limit 100")
    treemapData = cursor.fetchall()
    data3 =  [['Movie', 'Director', 'Rating','Year']]
    for row in treemapData:
        print("For loop is running")
        data3.append([row[0], row[1], row[2], row[3]])
        print(data3)
    return jsonify(data3)
    return render_template('treemap.html', data3=data3)

if __name__ == "__main__":
    app.debug = True  # Run flask when the file is called
    app.run(host="0.0.0.0", port=5000)
'''
@app.route("/tree")
def google_tree_chart1():
    treemapData = []
    cursor.execute("SELECT title, director, rating , releaseyear FROM movies ORDER BY rating DESC limit 100")
    treemapData = cursor.fetchall()
    data3 =  [['Movie', 'Director', 'Rating','Year']]
    for row in treemapData:
        data3.append([row[0], row[1], row[2], row[3]])

    return jsonify(data3)
'''














    