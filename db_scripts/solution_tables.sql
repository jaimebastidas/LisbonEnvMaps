SET search_path TO us;

/*
    The `originaldata` table records the variables
    temperature, humidity and noise.
*/

DROP TABLE IF EXISTS env_variables;
CREATE TABLE env_variables (
    id serial PRIMARY KEY,
    id_sensor varchar(4),
    date_temp date,
    temp_value float(6),
    date_noise date,
    noise_value float(6),
    date_hum date,
    hum_value float(6),
    freguesia varchar(100),
    address varchar(100)
    --FK
   -- FOREIGN KEY(id_sensor) 
--	REFERENCES stations(id_sensor)
--			ON DELETE CASCADE
    );

/* CREATE TABLE stations (
    id_sensor varchar(4) PRIMARY KEY,
    address_sensor varchar(50),
    coordinate_x float(6) not null,
    coordinate_y float(6) not null,
    coordinate_z float(6) not null, 
    latitude float(6) not null,
    longitude float(6) not null
    );
*/