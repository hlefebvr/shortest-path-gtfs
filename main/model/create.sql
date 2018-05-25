-- CREATES ALL TABLES FOR GTFS

DROP TABLE IF EXISTS timetable;
DROP TABLE IF EXISTS stop_times;
DROP TABLE IF EXISTS transfers;
DROP TABLE IF EXISTS stops;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS routes;

CREATE TABLE routes (
    route_id VARCHAR(40) PRIMARY KEY,
    agency_id VARCHAR(10),
    route_short_time VARCHAR(10),
    route_long_time TEXT,
    route_desc VARCHAR(2),
    route_type INT,
    route_url TEXT,
    route_color VARCHAR(10),
    route_text_color VARCHAR(10)
);

CREATE TABLE trips (
    route_id VARCHAR(40),
    service_id int,
    trip_id VARCHAR(40) PRIMARY KEY,
    trip_headsign TEXT,
    trip_short_name VARCHAR(40),
    direction_id INT,
    block_id INT,
    wheelchair_accessible INT,
    bikes_allowed INT,
    trip_desc VARCHAR(10),
    shape_id INT,
    FOREIGN KEY (route_id) REFERENCES routes(route_id)
);

CREATE TABLE stops (
    stop_id VARCHAR(30) PRIMARY KEY,
    stop_name TEXT,
    stop_desc TEXT,
    stop_lat Decimal(9,6),
    stop_lon Decimal(9,6),
    zone_id TEXT,
    stop_url TEXT,
    location_type TEXT,
    parent_station TEXT,
    wheelchair_boarding BOOLEAN
);

CREATE TABLE transfers (
    from_stop_id VARCHAR(30),
    to_stop_id VARCHAR(30),
    transfer_type INT CHECK (transfer_type > 0 AND transfer_type < 4),
    min_transfer_time INT,
    FOREIGN KEY (from_stop_id) REFERENCES stops(stop_id),
    FOREIGN KEY (to_stop_id) REFERENCES stops(stop_id)
);

CREATE TABLE stop_times (
    trip_id VARCHAR(40),
    arrival_time VARCHAR(10),
    departure_time VARCHAR(10),
    stop_id VARCHAR(30),
    stop_sequence INT,
    stop_time_desc VARCHAR(10),
    pickup_type INT,
    drop_off_type INT,
    FOREIGN KEY (stop_id) REFERENCES stops(stop_id),
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
);

CREATE TABLE timetable (
    from_stop_id VARCHAR(30),
    to_stop_id VARCHAR(30),
    departure_time INT,
    travel_time INT,
    route_type INT,
    trip_id VARCHAR(30),
    PRIMARY KEY (from_stop_id, to_stop_id, departure_time, travel_time, route_type, trip_id)
);

CREATE TABLE stops_routes (
    stop_id VARCHAR(30) REFERENCES stops(stop_id),
    route_id VARCHAR(40) REFERENCES routes(route_id),
    PRIMARY KEY (stop_id, route_id)
);
