SET search_path TO ods;

/*
    The `originaldata` table records the variables
    temperature,humidity and noise.
*/
DROP TABLE IF EXISTS originaldata;
CREATE TABLE originaldata (
    id serial PRIMARY KEY,
    id_sensor varchar(4),
    lat float(6),
    long float(6),
    date_temp date,
    temp_value float(6),
    date_noise date,
    noise_value float(6),
    date_hum date,
    hum_value float(6)
);
