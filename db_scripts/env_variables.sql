/*
    The purpose of the trigger is to insert into the pa.rides every time a new record is inserted
    in sa.rides. Plus, the longitude and latitude are converted into PostGIS datatypes.
*/
CREATE FUNCTION ods.insert_data()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO us.env_variables(id_sensor, date_temp, temp_value, date_noise, noise_value, date_hum, hum_value, freguesia, address)
	VALUES (new.id_sensor, 
			new.date_temp, 
			new.temp_value, 
			new.date_noise, 
			new.noise_value, 
			new.date_hum, 
			new.hum_value, 
			(select ST_intersection(f.geometry, sp.geometry), new.f."NOME" from  ods.fraguesias f, ods.sensors_points sp 
			where ST_Intersects(f.geometry, sp.geometry)),
			(select ST_intersection(f.geometry, sp.geometry),new.sp.address from  ods.fraguesias f, ods.sensors_points sp 
			where ST_Intersects(f.geometry, sp.geometry)));
	RETURN new;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER insert_data
AFTER INSERT ON ods.originaldata
FOR EACH ROW
EXECUTE PROCEDURE ods.insert_data();
