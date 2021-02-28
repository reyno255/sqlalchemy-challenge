import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#set up database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates vs precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > year_ago).all()

    session.close()

    # Convert list of tuples into normal list
    all_precip = []
    for date, prcp in results:
        all_precip_dict = {}
        all_precip["Date"] = date
        all_precip_dict["Precipitation"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    
    session.close()
    
    all_stations = []
    for station, count in results:
        stations_dict = {}
        stations_dict["Station ID"] = station
        stations_dict["Count of Observations"] = count
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    results = most_active_temp = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == 'USC00519281').all()
    
    session.close()
    
    all_tobs = []
    for date, tobs in results:
        tobs = {}
        tobs["Date"] = date
        tobs["Temperature Observation"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

if __name__ == '__main__':
    app.run(debug=True)