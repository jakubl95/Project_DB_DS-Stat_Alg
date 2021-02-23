delimiter //

create procedure updatemonthlysummaryforcountry(in in_date date, in in_country int)
	begin
		insert into cases_monthly(country_id, year_index, month_index, cases, deaths)
			select 
				country_id, 
				year(report_date),
				month(report_date),
				sum(cases), 
				sum(deaths) 
			from reported_cases 
			where year(report_date) = year(in_date)
			and month(report_date) = month(in_date) 
			and country_id = in_country
		ON DUPLICATE KEY update
			cases = (select sum(cases) from reported_cases where year(report_date) = year(in_date)
			and month(report_date) = month(in_date) 
			and country_id = in_country),
			deaths = (select sum(deaths) from reported_cases where year(report_date) = year(in_date)
			and month(report_date) = month(in_date) 
			and country_id = in_country)
			;
	end //
	
delimiter ;