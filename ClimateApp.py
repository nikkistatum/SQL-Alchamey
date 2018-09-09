# Import dependencies
import sqlalchemy

import numpy as np

from sqlalchemy.ext.automap import automap_base

from sqlalchemy.orm import Session

from sqlalchemy import create_engine, func

from flask import Flask, jsonify
engine = create_engine("sqlite:///Resources/hawaii.sqlite") 

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

## flask
app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page.")
    return "Welcome to the Surfs Up Weather API!"

@app.route("/welcome")
#List all available routes
def welcome ():
    return (
        f"Welcome to the Surf Up API<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
#Query for the dates and temperature observations from the last year.
    results = session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= "08-23-2017").all()

    yearprcp = list(np.ravel(results))
#results.___dict___
#Create a dictionary using 'date' as the key and 'prcp' as the value.
    """yearprcp = []
    for result in results:
        row = {}
        row[Measurement.date] = row[Measurement.prcp]
        yearprcp.append(row)"""

    return jsonify(year_prcp)

@app.route("/api/v1.0/stations")
def station():
#return a json list of stations from the dataset.
    results = session.query(Stations.station).all()

    allstations = list(np.ravel(results))

    return jsonify(allstations)

@app.route("/api/v1.0/tobs")
def temperature():
#Return a json list of Temperature Observations (tobs) for the previous year
    year_tobs = []
    results = session.query(Measurement.tobs).filter(Measurement.date >= "08-23-2017").all()

    yeartobs = list(np.ravel(results))

    return jsonify(yeartobs)

@app.route("/api/v1.0/<start>")
def starttrip_temp(start_date):
    starttrip = []

    resultsmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date == startdate).all()
    resultsmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date == startdate).all()
    resultsavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == startdate).all()

    starttrip = list(np.ravel(resultsmin, resultsmax, resultsavg))

    return jsonify(starttrip)

def biggerstartdate(startdate):

    biggerstartdatetemps = []

    resultsmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= startdate).all()
    resultsmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= startdate).all()
    resultsavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= startdate).all()
    
    starttripdatetemps = list(np.ravel(resultsmin,resultsmax, resultsavg))

    return jsonify(starttripdatetemps)


@app.route("/api/v1.0/<start>/<end>")

def startendtrip(startdate, enddate):

    startendtriptemps = []

    resultsmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date == startdate, Measurement.date == enddate).all()
    resultsmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date == startdate, Measurement.date == enddate).all()
    resultsavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == startdate, Measurement.date == enddate).all()

    startendtriptemps = list(np.ravel(resultsmin, resultsmax, resultsavg))

    return jsonify(startendtriptemps)

def startendtrip(startdate, enddate):

    roundtriptemps = []

    resultsmin = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= enddate).all()
    resultsmax = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= enddate).all()
    resultsavg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= enddate).all()
    


    roundtriptemps = list(np.ravel(resultsmin, resultsmax, resultsavg))



    return jsonify(roundtriptemps)

    if __name__ == '__main__':
    app.run(debug=True)

