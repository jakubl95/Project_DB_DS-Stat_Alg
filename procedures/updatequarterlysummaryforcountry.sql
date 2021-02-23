delimiter //

create procedure updatequarterlysummaryforcountry(in in_date date, in in_country int)
	begin
		insert into cases_quarterly(country_id, quarter_name, quarter_year, quarter_index, cases, deaths)
			select 
				country_id, 
				concat_ws("_",year(report_date),quarter(report_date)),
				year(report_date),
				quarter(report_date),
				sum(cases), 
				sum(deaths) 
			from reported_cases 
			where year(report_date) = year(in_date)
			and quarter(report_date) = quarter(in_date) 
			and country_id = in_country
		ON DUPLICATE KEY update
			cases = (select sum(cases) from reported_cases where year(report_date) = year(in_date)
			and quarter(report_date) = quarter(in_date) 
			and country_id = in_country),
			deaths = (select sum(deaths) from reported_cases where year(report_date) = year(in_date)
			and quarter(report_date) = quarter(in_date) 
			and country_id = in_country)
			;
	end //
	
delimiter ;