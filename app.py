# 1. Importing all libraries
from flask import Flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    return '''Here are some routes available:</br> 
    - /api/v1.0/precipitation</br>
    - /api/v1.0/stations</br>
    - /api/v1.0/tobs</br>
    - /api/v1.0/<start></br>
    - /api/v1.0/<start>/<end>
    '''


# 4. Define what to do when a user hits the /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def preciptation():
    #Querying the precipitation by date and closing the session.
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()
    session.close()
    #Creating an empty list and a for loop to append the results.
    precipitation_data = []
    for date, prcp in results:
        precipitation_data.append({date : prcp})
    #returning the object
    return jsonify(precipitation_data)

# 5. Define what to do when a user hits the /api/v1.0/stations route
@app.route("/api/v1.0/stations")
def station():
    #Querying the stations by ID and name and closing the session.
    results = session.query(Station.id, Station.name).order_by(Station.id).all()
    session.close()
    #Creating an empty list and a for loop to append the results.
    station_data = []
    for id, name in results:
        station_data.append({id : name})
    #returning the object
    return jsonify(station_data)

# 6. Define what to do when a user hits the /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    #Querying the temperature of the most active station in the last year (2016 to 2017) and closing the session.
    results = session.query(Measurement.date, Measurement.tobs)\
                       .filter(Measurement.station == 'USC00519281')\
                        .filter(Measurement.date >= '2016-08-18')\
                        .order_by(Measurement.date.desc()).all()
    session.close()
    #Creating an empty list and a for loop to append the results.
    tobs_data = []
    for date, tobs in results:
        tobs_data.append({date : tobs})
    #returning the object
    return jsonify(tobs_data)

# 7. Define what to do when a user hits the /api/v1.0/<start> route
@app.route("/api/v1.0/<start>")

def routestart(start):
    #Treating possible mystakes when typing the start date
    right_date = start.replace(" ","")
    final_date = right_date.replace(".","-")
    #Fetching a start date and calculate the max, min and average temperature and closing the session
    Tmax = session.query(func.max(Measurement.tobs))\
    .filter(Measurement.date >= final_date).scalar()
    Tmin = session.query(func.min(Measurement.tobs))\
    .filter(Measurement.date >= final_date).scalar()
    Tavg = session.query(func.avg(Measurement.tobs))\
    .filter(Measurement.date >= final_date).scalar()
    
    session.close()
    #Creating an empty list and appending the results.
    Temperatures = []
    Temperatures.append({'Max Temperature' : Tmax})
    Temperatures.append({'Min Temperature' : Tmin})
    Temperatures.append({'Average Temperature' : Tavg})
    #returning the object
    return jsonify(Temperatures)

# 8. Define what to do when a user hits the /about route
@app.route("/api/v1.0/<start>/<end>")
def routeend(start , end):
    #Treating possible mystakes when typing the start date
    right_date = start.replace(" ","")
    final_date = right_date.replace(".","-")
    end_date = end.replace(" ","")
    finalend_date = end_date.replace(".","-")
    #Fetching a start and end date to calculate max, min and average temperature and closing the session
    Tmax = session.query(func.max(Measurement.tobs))\
    .filter(Measurement.date >= final_date, Measurement.date <= finalend_date).scalar()
    Tmin = session.query(func.min(Measurement.tobs))\
    .filter(Measurement.date >= final_date, Measurement.date <= finalend_date).scalar()
    Tavg = session.query(func.avg(Measurement.tobs))\
    .filter(Measurement.date >= final_date, Measurement.date <= finalend_date).scalar()
    
    session.close()
    #Creating an empty list and appending the results.
    Temperatures = []
    Temperatures.append({'Max Temperature' : Tmax})
    Temperatures.append({'Min Temperature' : Tmin})
    Temperatures.append({'Average Temperature' : Tavg})
    #returning the object
    return jsonify(Temperatures)


if __name__ == "__main__":
    app.run(debug=True)