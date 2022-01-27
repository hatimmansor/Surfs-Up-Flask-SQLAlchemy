import datetime as dt
import numpy as np

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement=Base.classes.measurement
Station=Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Return the JSON representation <br/>/api/v1.0/precipitation<br/>"
        f"Return a JSON list of stations <br/>/api/v1.0/stations<br/>"
        f"Return a JSON list of temperature observations <br/>/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"Return a JSON list of the minimum temperature, the average \
        temperature, and the max temperature for a given start or \
        start-end range <br/> /api/v1.0/<start>/<end>"
    )


#  Define what to do when a user hits the /api/v1.0/precipitation<br/> route
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the date and precipition"""
    # Query all date and precipition 
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of dicitionary
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)


#  return the station information table
@app.route("/api/v1.0/stations")
def stations():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all the stations"""
    # Query all the station table data 
    results = session.query(Station).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of dicitionary

    all_stations = []
    for row in results:
        
        station_dict = {}
        station_dict['station'] = row.station
        station_dict['name'] = row.name
        station_dict['latitude'] = row.latitude
        station_dict['longitude'] = row.longitude
        station_dict['elevation'] = row.elevation
        all_stations.append(station_dict)

    return jsonify(all_stations)


#  return the most activ station tobs for the last year
@app.route("/api/v1.0/tobs")
def tobs():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of last year tobs for the selected station"""
    # Query all the station table data 
    results = session.query(Measurement.date,Measurement.tobs).\
                  filter(Measurement.date >= '2016-08-18').\
                  filter(Measurement.station == 'USC00519281').all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of dicitionary

    all_tobs = []
    for row in results:
        
        station_dict = {}
        station_dict['tobs'] = row.tobs
        station_dict['date'] = row.date
        
        all_tobs.append(station_dict)

    return jsonify(all_tobs)




#  return the most activ station tobs from  a start date
@app.route("/api/v1.0/<start>")
def start(start):
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of last year tobs for the selected station"""
    # Query all the station table data 
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                  filter(Measurement.date >= start).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of dicitionary

    all_tobs = []
    for min,max,avg in results:
        
        tobs_dict = {}
        tobs_dict['TMIN'] = min
        tobs_dict['TMAX'] = max
        tobs_dict['TAVG'] = avg

        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

#  return the most activ station tobs from  a start date
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of last year tobs for the selected station"""
    # Query all the station table data 
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                  filter(Measurement.date >= start).\
                  filter(Measurement.date <= end).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of dicitionary

    all_tobs = []
    for min,max,avg in results:
        
        tobs_dict = {}
        tobs_dict['TMIN'] = min
        tobs_dict['TMAX'] = max
        tobs_dict['TAVG'] = avg

        
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)






if __name__ == "__main__":
    app.run(debug=True)