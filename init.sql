CREATE TABLE weather (
    id SERIAL,
    user_id INTEGER,
    date_time timestamp,
    json_data JSON,
    PRIMARY KEY (id)
);