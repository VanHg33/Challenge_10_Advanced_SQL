from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
meas = Base.classes.measurement
sta = Base.classes.station
session = Session(engine)

#Create an app
app = Flask(__name__)

#Define index route
@app.route("/")
def home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
        

@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    data = session.query(meas.date, meas.prcp).\
        filter(meas.date >= year_ago).all()
    session.close()
    precip = {date: prcp for date, prcp in data}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(sta.station).all()
    result_sta = list(np.ravel(stations))
    session.close()
    return jsonify(result_sta)

@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp = session.query(meas.tobs).\
        filter(meas.station == "USC00519281").\
        filter(meas.date >= year_ago).all()
    result_temp = list(np.ravel(temp))
    session.close()
    return jsonify(result_temp)


@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def stats(start=None, end=None):
    sel= [func.min(meas.tobs),
          func.avg(meas.tobs),
          func.max(meas.tobs)]

    if not end:
        start = dt.datetime.strptime(start, "%Y%m%d")
        results = session.query(*sel).\
            filter(meas.date >= start).all()
        session.close()
        temps = list(np.ravel(results))
        return jsonify(temps)

    start = dt.datetime.strptime(start, "%Y%m%d")
    end = dt.datetime.strptime(end, "%Y%m%d")
    results = session.query(*sel).\
        filter(meas.date >= start).\
        filter(meas.date <= end).all()
    session.close()
    temps = list(np.ravel(results))
    return jsonify(temps = temps)


if __name__ == '__main__':
    app.run(debug=True)

