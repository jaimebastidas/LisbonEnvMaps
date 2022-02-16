/*
    The purpose of the trigger is to insert into the pa.rides every time a new record is inserted
    in sa.rides. Plus, the longitude and latitude are converted into PostGIS datatypes.
*/
CREATE FUNCTION ods.insert_data_in_us()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO us.env_variables(id_sensor, date_temp, temp_value, date_noise, noise_value, date_hum, hum_value, freguesia, address)
	VALUES (id_sensor, date_temp, temp_value, date_noise, noise_value, date_hum, date_hum, ) 
 
	VALUES (now(), new.pickup_datetime, new.dropoff_datetime, new.passenger_count, 
            new.rate_code, new.tip_amount, new.payment_type, new.total_amount, 
			ST_Transform(ST_SetSRID(ST_MakePoint(new.pickup_longitude, new.pickup_latitude), 2263), 3857),
			ST_Transform(ST_SetSRID(ST_MakePoint(new.dropoff_longitude, new.dropoff_latitude), 2263), 3857));
	RETURN new;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER insert_data_in_us
AFTER INSERT ON ods.originaldata
FOR EACH ROW
EXECUTE PROCEDURE ods.insert_data_in_us();
