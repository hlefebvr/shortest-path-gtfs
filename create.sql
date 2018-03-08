-- CREATE TABLES TO STORE GTFS DATA

DROP TABLE IF EXISTS agencies;

CREATE TABLE agencies (
    agency_id VARCHAR(10) PRIMARY KEY,
    agency_name TEXT,
    agency_url TEXT,
    agency_timezone VARCHAR(25),
    agency_lang VARCHAR(2)
);

\COPY agencies FROM 'gtfs/agency.txt' DELIMITER ',' CSV HEADER;

DROP TABLE IF EXISTS routes;

CREATE TABLE routes (
    route_id VARCHAR(25) PRIMARY KEY,
    agency_id VARCHAR(10) references agencies(agency_id),
    route_short_time VARCHAR(2),
    route_long_time VARCHAR(30),
    route_desc VARCHAR(2),
    route_type int,
    route_url TEXT,
    route_color VARCHAR(10),
    route_text_color VARCHAR(10)
);
