import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#set up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

#create flask object
app = Flask(__name__)

#create flask routes
@app.route("/")
def home():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates vs precipitation
    day_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    day_last = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > day_year_ago).order_by(Measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    all_precip = []
    for date, prcp in results:
        all_precip_dict = {}
        all_precip_dict["Date"] = date
        all_precip_dict["Precipitation"] = prcp
        all_precip.append(all_precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    session.close()    

    all_stations = []
    for station, count in results:
        all_stations_dict = {}
        all_stations_dict["Station ID"] = station
        all_stations_dict["Count of Observations"] = count
        all_stations.append(all_stations_dict)

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
        all_tobs_dict = {}
        all_tobs_dict["Date"] = date
        all_tobs_dict["Temperature Observation"] = tobs
        all_tobs.append(all_tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/start")
def calc_start_temps():
    session = Session(engine)
    start_date = dt.strptime('2016-08-23', '%Y-%m-%d').date()
    start_results = session.query(func.avg(Measurement.tobs),func.max(Measurement.tobs),func.min(Measurement.tobs).\
               filter(Measurement.date >= start_date))
    session.close()

    start_tobs_df = []   
    for tmax,tmin,tavg in start_results:
       start_tobs_dict = {}
       start_tobs_dict["tMin"] = float(tmin)                     
       start_tobs_dict["tMax"] = float(tmax)
       start_tobs_dict["tAvg"] = float(tavg)
       start_tobs_df.append(start_tobs_dict)
    
    return jsonify(start_tobs_df)

if __name__ == '__main__':
    app.run(debug=True)
