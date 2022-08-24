CREATE TABLE riders (
rider_id VARCHAR PRIMARY KEY,
first_name VARCHAR,
last_name VARCHAR);

CREATE TABLE reservations (
reserved_id VARCHAR PRIMARY KEY,
rider_id VARCHAR,
FOREIGN KEY (rider_id) REFERENCES riders(rider_id));

CREATE TABLE runs (
run_id VARCHAR PRIMARY KEY,
departure_date DATE,
departure_time TIME,
departure_city VARCHAR,
departure_state VARCHAR,
arrival_city VARCHAR,
arrival_state VARCHAR,
arrival_date DATE,
arrival_time TIME);

CREATE TABLE seats (
seat_id SERIAL PRIMARY KEY,
seat VARCHAR NOT NULL,
run_id VARCHAR NOT NULL,
reserved_id VARCHAR,
FOREIGN KEY (reserved_id) REFERENCES reservations(reserved_id),
FOREIGN KEY (run_id) REFERENCES runs(run_id));


