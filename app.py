#  Dependencies 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from config import protocol, username, password, host, port
from flask import Flask, jsonify, render_template  

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
def test():

    session = Session(engine)

    # Query all departure and arrival cities
    results = session.query(runs.departure_city, runs.departure_state, runs.arrival_city, runs.arrival_state).all()

    session.close()

    # print(results)
    runs_list = []
    for departure_city, departure_state, arrival_city, arrival_state in results:
        run = {}
        run['departures'] = f'{departure_city}, {departure_state}'
        run['arrivals'] = f'{arrival_city}, {arrival_state}'
        runs_list.append(run)
        print(runs_list)

    return jsonify(runs_list)

if __name__ == '__main__':
    app.run()