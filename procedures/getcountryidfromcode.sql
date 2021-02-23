delimiter //

create procedure getcountryidfromcode(in in_code char(2), out out_id int)
	begin
		set out_id = (select id from country where code = in_code);
	end //
	
delimiter ;
