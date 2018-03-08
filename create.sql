-- CREATE TABLES TO STORE GTFS DATA

DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS stops;
DROP TABLE IF EXISTS shapes;
DROP TABLE IF EXISTS routes;
DROP TABLE IF EXISTS agencies;

CREATE TABLE agencies (
    agency_id VARCHAR(10) PRIMARY KEY,
    agency_name TEXT,
    agency_url TEXT,
    agency_timezone VARCHAR(25),
    agency_lang VARCHAR(2)
);

\COPY agencies FROM 'gtfs/agency.txt' DELIMITER ',' CSV HEADER;

CREATE TABLE routes (
    route_id VARCHAR(40) PRIMARY KEY,
    agency_id VARCHAR(10) REFERENCES agencies(agency_id),
    route_short_time VARCHAR(10),
    route_long_time TEXT,
    route_desc VARCHAR(2),
    route_type INT,
    route_url TEXT,
    route_color VARCHAR(10),
    route_text_color VARCHAR(10)
);

\COPY routes FROM 'gtfs/routes.txt' DELIMITER ',' CSV HEADER QUOTE '"';

CREATE TABLE shapes (
    shape_id TEXT PRIMARY KEY,
    shape_pt_lat TEXT,
    shape_pt_lon TEXT,
    shape_pt_sequence TEXT
);

\COPY shapes FROM 'gtfs/shapes.txt' DELIMITER ',' CSV HEADER QUOTE '"';

CREATE TABLE trips (
    route_id VARCHAR(40) REFERENCES routes(route_id),
    service_id int,
    trip_id VARCHAR(40) PRIMARY KEY,
    trip_headsign TEXT,
    trip_short_name VARCHAR(40),
    direction_id INT,
    block_id INT,
    wheelchair_accessible INT,
    bikes_allowed INT,
    trip_desc VARCHAR(10),
    shape_id INT
);

\COPY trips FROM 'gtfs/trips.txt' DELIMITER ',' CSV HEADER;

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

\COPY stops FROM 'gtfs/stops.txt' DELIMITER ',' CSV HEADER QUOTE '"';
