delimiter //

create procedure deletereport(in in_date date, in in_country_id char(2))
	begin
		delete from reported_cases where report_date = in_date and country_id = in_country_id;
	end //
	
delimiter ;
