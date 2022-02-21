select date, avg(temp_value) as temp, avg(noise_value) as noise, avg(hum_value) as humidity
	from us.env_variables
	where (date >= '2022-02-14' and date <= '2022-02-20')
	group by date


select id_sensor, avg(temp_value) as temp,  avg(noise_value) as noise, avg(hum_value) as humidity 
                from us.env_variables 
                where (date >= '2022-02-01' and date <= '2022-02-04')
                group by id_sensor

select * from us.env_variables
where (date >= '2022-02-01' and date <= '2022-02-04')

COPY ods.originaldata(id_sensor, date, temp_value, noise_value, hum_value)
from 'D:\NOVAIMS\2021-2022\Programming_Seminar\GPS_project\lastmeasurements_12022022.csv'
DELIMITER ';'
CSV HEADER;