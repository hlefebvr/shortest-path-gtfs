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