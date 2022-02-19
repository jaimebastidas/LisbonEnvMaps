/*
    The purpose of the trigger is to insert into the env_variables table rides every time a new record is inserted
    in originaldata table. Also, using postgis spatial function of intersection the env_variables get the address of the sensor and the fraguesia's name.
*/
CREATE FUNCTION ods.insert_data()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO us.env_variables(id_sensor, date, temp_value, noise_value, hum_value, freguesia, address)
	VALUES (new.id_sensor,
			new.date,
			new.temp_value,  
			new.noise_value,  
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
