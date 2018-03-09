DROP VIEW IF EXISTS vSimpleTrips;
DROP VIEW IF EXISTS vSimpleRoutes;

CREATE VIEW vSimpleRoutes AS 
(
    SELECT
    route_id
FROM
    routes
WHERE
    route_type = 1 -- Metro
    OR route_type = 3 -- Bus
    -- OR route_type = 2 -- Train
);

CREATE VIEW vSimpleTrips AS
(
    SELECT
        trip_id
    FROM
        vSimpleRoutes r INNER JOIN trips t ON r.route_id = t.route_id
);

SELECT
    COUNT(*)
FROM
    vSimpleTrips t INNER JOIN stoptimes st ON t.trip_id = st.trip_id;