

# Import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc
from sqlalchemy.sql import label

from flask import Flask, jsonify

import matplotlib.pyplot as plt

engine = create_engine("sqlite:///Resources/hawaii.sqlite") 

Base = automap_base()
Base.prepare(engine, reflect=True)


Base.classes.keys()

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

# Getting the table names for each table
inspector = inspect(engine)
inspector.get_table_names()

#Get a list of the coumn names and types i am working with
columns = inspector.get_columns('measurement')
for c in columns:
    print(c['name'], c["type"])

#get a list of column names for station
columns = inspector.get_columns('station')
for c in columns:
    print(c['name'], c["type"])


for row in session.query(Measurement, Measurement.prcp).limit(5).all():
    print(row)

engine.execute('SELECT * FROM Measurement LIMIT 5').fetchall()

#engine.execute('SELECT * FROM Station LIMIT 5').fetchall()

# Grabs the last date entry in the data table
lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
print(lastdate)

# to get the last 12 months of data, last date - 365
lastyear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
print(lastyear)

# query to pull the last year of precipitation data# query  
wetdays= session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > lastyear).\
    order_by(Measurement.date).all()
wetdays

#Create Dataframe with the info and 0 out the NAN

wetnessdf = pd.DataFrame(wetdays)
wetness = wetnessdf.fillna(0)
wetness
#Change dataframe index to date
raindrops = wetness.set_index("date")
raindrops

raindrops.plot()

#Set plot title.
plt.title("Precipitation")

#Save graph.
plt.savefig("Precipitation")

#Show graph.

plt.show()

totrainfall= raindrops["prcp"].sum()
totrainfall

wetstat = raindrops.describe()
wetstat

#get a list of column names for station
columns = inspector.get_columns('Station')
for c in columns:
    print(c['name'], c["type"])

stations_first = session.query(Station).first()
stations_first
stations_first.__dict__

# How many stations are available in this dataset?

totalstations = session.query(Station.station).count()
totalstations

# What are the most active stations?
activestation = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
        
activestation

mostactive = activestation[0][0]
mostactive

datestation = session.query(Measurement.tobs).filter(Measurement.date >= "2016-08-23", Measurement.station == mostactive).all()
       
datestation

datestationdf = pd.DataFrame(datestation)
datestationdf.head()

plt.hist(datestationdf["tobs"], bins=12)

plt.show()

 def calc_temps(start_date, end_date):
    tripdates = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_date,\
         Measurement.date <= end_date).all()
    tripdatesdf = pd.DataFrame(tripdates)
    max_temp = tripdatesdf["tobs"].max()
    min_temp = tripdatesdf["tobs"].min()
    mean_temp = tripdatesdf["tobs"].mean()
    plt.figure(figsize=(2,5))
    plt.bar(1,mean_temp, yerr= max_temp - min_temp, tick_label="")
    plt.show()
calc_temps("2017-08-03", "2017-08-19")