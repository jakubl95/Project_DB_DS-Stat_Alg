delimiter //

create procedure insertorupdatereport(in in_date date, in in_country_id int, in in_cases int, in in_deaths int)
	begin
		insert into reported_cases(country_id, report_date, cases, deaths) 
		values(
			in_country_id,
			in_date,
			in_cases,
			in_deaths
		) ON DUPLICATE KEY UPDATE 
			cases = in_cases,
			deaths = in_deaths;
		call updatemonthlysummaryforcountry(in_date, in_country_id);
		call updatequarterlysummaryforcountry(in_date, in_country_id);
		call updateyearlysummaryforcountry(in_date, in_country_id);
	end //
	
delimiter ;
