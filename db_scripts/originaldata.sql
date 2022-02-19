SET search_path TO ods;

/*
    The `originaldata` table records the variables
    temperature,humidity and noise.
*/
DROP TABLE IF EXISTS originaldata;
CREATE TABLE originaldata (
    id serial PRIMARY KEY,
    id_sensor varchar(4),
    date date,
    temp_value float(6),
    noise_value float(6),
    hum_value float(6)
);
