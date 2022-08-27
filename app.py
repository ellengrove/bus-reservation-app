#  Dependencies 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_
from config import protocol, username, password, host, port
from flask import Flask, jsonify, render_template  
from json import dumps

#################################################
# Database Setup
#################################################

database_name = 'reservation_db'

connection_string = f'{protocol}://{username}:{password}@{host}:{port}/{database_name}'

engine = create_engine(connection_string)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
reservations = Base.classes.reservations
riders = Base.classes.riders
runs = Base.classes.runs
seats = Base.classes.seats

print(Base.classes.keys)
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/citySelections")
def dropdown():

    session = Session(engine)

    # Query all departure and arrival cities
    results = session.query(runs.departure_city, runs.departure_state, runs.arrival_city, runs.arrival_state).all()

    session.close()

    # print(results)
    departures = []
    arrivals = []
    for departure_city, departure_state, arrival_city, arrival_state in results:
        departure = f'{departure_city}, {departure_state}'
        arrival = f'{arrival_city}, {arrival_state}'
        departures.append(departure)
        arrivals.append(arrival)

    runs_list = {'departures' : departures,
                'arrivals' : arrivals}    

    return jsonify(runs_list)

@app.route("/findTrips")
def findTrips():
    
    session = Session(engine)

    # Query all departure and arrival cities

    results = session.query(runs.run_id, runs.departure_date, runs.departure_time, runs.departure_city,\
        runs.departure_state, runs.arrival_city, runs.arrival_state, runs.arrival_date, runs.arrival_time,\
        func.count(seats.seat).label('capacity'),\
        func.count(seats.reserved_id).label('num_reserved'))\
        .where(runs.run_id == seats.run_id)\
        .group_by(runs.run_id)\
        .all()
    session.close()

    avail_runs = []
    for run_id, departure_date, departure_time, departure_city, departure_state,\
        arrival_city, arrival_state, arrival_date, arrival_time, capacity, num_reserved in results:

        if num_reserved < capacity:
            avail_runs.append({'run_id' : run_id,
                            'departure_date' : str(departure_date),
                            'departure_time' : str(departure_time),
                            'departure_location' : f'{departure_city}, {departure_state}',
                            'arrival_location' : f'{arrival_city}, {arrival_state}',
                            'arrival_date' : str(arrival_date),
                            'arrival_time' : str(arrival_time)})

    return jsonify(avail_runs)

@app.route("/find/<depart>/<arrive>")
def find(depart,arrive):
    
    session = Session(engine)

    # Query the departure and arrival city selected from dropdown

    results = session.query(runs.run_id, runs.departure_date, runs.departure_time, runs.departure_city,\
        runs.departure_state, runs.arrival_city, runs.arrival_state, runs.arrival_date, runs.arrival_time,\
        func.count(seats.seat).label('capacity'),\
        func.count(seats.reserved_id).label('num_reserved'))\
        .where(and_(runs.run_id == seats.run_id,runs.departure_city == depart,runs.arrival_city == arrive))\
        .group_by(runs.run_id)\
        .all()
    session.close()
        # .where(and_(runs.run_id == seats.run_id,runs.departure_city == depart,runs.arrival_city == arrive))\

    avail_runs = []
    for run_id, departure_date, departure_time, departure_city, departure_state,\
        arrival_city, arrival_state, arrival_date, arrival_time, capacity, num_reserved in results:
        if num_reserved < capacity:
            avail_runs.append({'run_id' : run_id,
                            'departure_date' : str(departure_date),
                            'departure_time' : str(departure_time),
                            'departure_location' : f'{departure_city}, {departure_state}',
                            'arrival_location' : f'{arrival_city}, {arrival_state}',
                            'arrival_date' : str(arrival_date),
                            'arrival_time' : str(arrival_time)})

    return jsonify(avail_runs)


if __name__ == '__main__':
    app.run()