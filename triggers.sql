delimiter //

create trigger updatesummariesonupdate after update on reported_cases
	for each row
	begin
		call updatesummaries(new.report_date, new.country_id);
	end //
	
delimiter ;

delimiter //

create trigger moverowtoarchive before delete on reported_cases
	for each row
	begin
			insert into reported_cases_archive values(null, old.country_id, old.report_date, old.cases, old.deaths, current_timestamp());
	end //
	
delimiter ;

create trigger updatesummariesondelete after insert on reported_cases_archive
	for each row
	begin
			call updatesummaries(new.report_date, new.country_id);
	end //
	
delimiter ;

delimiter //
create procedure updatesummaries(in report_date date, in country_id int)
	begin
		call updatemonthlysummaryforcountry(report_date, country_id);
		call updatequarterlysummaryforcountry(report_date, country_id);
		call updateyearlysummaryforcountry(report_date, country_id);
	end
delimiter ;