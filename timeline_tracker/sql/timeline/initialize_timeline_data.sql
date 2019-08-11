CREATE TABLE IF NOT EXISTS timeline_data (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    address VARCHAR(255),
    description VARCHAR(1024),
    coordinates VARCHAR,
    category VARCHAR(255),
    distance VARCHAR(255),
    time_begin timestamp,
    time_end timestamp
);