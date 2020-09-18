# Config module for koyomiex 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']
	del_no = cgi['del_no'].to_i
	koyomiy = cgi['koyomiy'].to_i
	breakfast_st = cgi['breakfast_st'].to_i
	lunch_st = cgi['lunch_st'].to_i
	dinner_st = cgi['dinner_st'].to_i
	item_set = [cgi['item0'], cgi['item1'], cgi['item2'], cgi['item3'], cgi['item4'], cgi['item5'], cgi['item6'], cgi['item7'], cgi['item8'], cgi['item9']]
	unit_set = [cgi['unit0'], cgi['unit1'], cgi['unit2'], cgi['unit3'], cgi['unit4'], cgi['unit5'], cgi['unit6'], cgi['unit7'], cgi['unit8'], cgi['unit9']]
	kex_select_set = [cgi['kex_select0'].to_i, cgi['kex_select1'].to_i, cgi['kex_select2'].to_i, cgi['kex_select3'].to_i, cgi['kex_select4'].to_i, cgi['kex_select5'].to_i, cgi['kex_select6'].to_i, cgi['kex_select7'].to_i, cgi['kex_select8'].to_i, cgi['kex_select9'].to_i]
	if @debug
		puts "step: #{step}<br>"
		puts "del_no: #{del_no}<br>"
		puts "koyomiy: #{koyomiy}<br>"
		puts "breakfast_st: #{breakfast_st}<br>"
		puts "lunch_st: #{lunch_st}<br>"
		puts "dinner_st: #{dinner_st}<br>"
		puts "item_set: #{item_set}<br>"
		puts "unit_set: #{unit_set}<br>"
		puts "kex_select_set: #{kex_select_set}<br>"
		puts "<hr>"
	end


	case step
	when 'update'
		koyomiex_new = ''
		0.upto( 9 ) do |c| koyomiex_new << "#{kex_select_set[c]}\t#{item_set[c]}\t#{unit_set[c]}:" end
		koyomiex_new.chop!
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET koyomiex='#{koyomiex_new}', koyomiy='#{koyomiy}:#{breakfast_st}:#{lunch_st}:#{dinner_st}' WHERE user='#{user.name}';", false, @debug )
	when 'delete'
		r = mdb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
		kex_select_set = r.first['koyomiex'].split( ':' )
		koyomiex_new = ''
		kex_select_set.size.times do |c|
			if del_no == c
				koyomiex_new << "0\t\t:"
				mdb( "UPDATE #{$MYSQL_TB_KOYOMIEX} SET item#{c}='' WHERE user='#{user.name}';", false, @debug )
			else
				koyomiex_new << "#{kex_select_set[c]}:"
			end
		end
		koyomiex_new.chop!
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET koyomiex='#{koyomiex_new}' WHERE user='#{user.name}';", false, @debug )
	end

	r = mdb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	if r.first['koyomiex'] == '' || r.first['koyomiex'] == nil
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t' WHERE user='#{user.name}';", false, @debug )
		0.upto( 9 ) do |c|
			kex_select_set[c] = 0
			item_set[c] = ''
			unit_set[c] = ''
		end
	else
		a = r.first['koyomiex'].split( ':' )
		0.upto( 9 ) do |c|
			aa = a[c].split( "\t" )
			kex_select_set[c] = aa[0].to_i
			item_set[c] = aa[1]
			unit_set[c] = aa[2]
		end
	end


####
	t = Time.new
	koyomiy = t.year
	breakfast_st = 7
	lunch_st = 12
	dinner_st = 19
	r = mdb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	if r.first['koyomiy']
		a = r.first['koyomiy'].split( ':' )
		koyomiy = a[0].to_i
		breakfast_st = a[1].to_i
		lunch_st = a[2].to_i
		dinner_st = a[3].to_i
	end

	# HTML
	html = '<div class="container">'
	html << "<div class='row'>"
	html << "<div class='col-3'>"
	html << "<div class='input-group input-group-sm'>"
	html << "<span class='input-group-text'>#{lp[55]}</span>"
  	html << "<select class='form-select' id='koyomiy'>"
	2000.upto(2050) do |c|
		if c == koyomiy
			html << "<option value='#{c}' selected>#{c}</option>"
		else
			html << "<option value='#{c}'>#{c}</option>"
		end
	end
  	html << "</select>"
	html << "</div></div>"
	html << "</div><hr>"

	html << "<div class='row'>"
	html << "<div class='col-3'>"
	html << "<div class='input-group input-group-sm'>"
	html << "<span class='input-group-text'>#{lp[56]}</span>"
 	html << "<select class='form-select' id='breakfast_st'>"
	0.upto(23) do |c|
		if c == breakfast_st
			html << "<option value='#{c}' selected>#{c}</option>"
		else
			html << "<option value='#{c}'>#{c}</option>"
		end
	end
  	html << "</select>"
	html << "</div></div>"

	html << "<div class='col-3'>"
	html << "<div class='input-group input-group-sm'>"
	html << "<span class='input-group-text'>#{lp[57]}</span>"
 	html << "<select class='form-select' id='lunch_st'>"
	0.upto(23) do |c|
		if c == lunch_st
			html << "<option value='#{c}' selected>#{c}</option>"
		else
			html << "<option value='#{c}'>#{c}</option>"
		end
	end
  	html << "</select>"
	html << "</div></div>"

	html << "<div class='col-3'>"
	html << "<div class='input-group input-group-sm'>"
	html << "<span class='input-group-text'>#{lp[58]}</span>"
 	html << "<select class='form-select' id='dinner_st'>"
	0.upto(23) do |c|
		if c == dinner_st
			html << "<option value='#{c}' selected>#{c}</option>"
		else
			html << "<option value='#{c}'>#{c}</option>"
		end
	end
  	html << "</select>"
	html << "</div></div>"

	html << "</div><hr>"

	html << "<h5>#{lp[59]}</h5><br>"

	0.upto( 9 ) do |c|
		html << "<div class='row'>"
		html << "	<div class='col-3'>"
		html << "		<div class='input-group input-group-sm'>"
    	html << "			<label class='input-group-text'>#{lp[60]}#{c}</label>"
  		html << "			<select class='form-select' id='kex_select#{c}' onChange=\"kexChangeselect( '#{c}' )\">"
		$KEX_ITEM.size.times do |cc|
			if cc == kex_select_set[c]
    			html << "<option value='#{cc}' SELECTED>#{$KEX_ITEM[cc]}</option>"
    		else
    			html << "<option value='#{cc}'>#{$KEX_ITEM[cc]}</option>"
    		end
    	end
  		html << "			</select>"
		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-3'>"
		html << "		<div class='input-group input-group-sm'>"
		html << "			<span class='input-group-text'>#{lp[61]}</span>"
		if kex_select_set[c] == 1
			html << "<input type='text' maxlength='32' id='item#{c}' class='form-control form-control-sm' value='#{item_set[c]}'>"
    	else
			html << "<input type='text' maxlength='32' id='item#{c}' class='form-control form-control-sm' value='' disabled>"
    	end
		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-2'>"
		html << "		<div class='input-group input-group-sm'>"
		html << "				<span class='input-group-text'>#{lp[62]}</span>"
		if kex_select_set[c] == 1
			html << "			<input type='text' maxlength='32' id='unit#{c}' class='form-control form-control-sm' value='#{item_set[c]}'>"
    	else
			html << "			<input type='text' maxlength='32' id='unit#{c}' class='form-control form-control-sm' value='' disabled>"
    	end
		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-1'></div>"
		html << "	<div class='col-2'><input type='checkbox' id='kex_del#{c}'>&nbsp;<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"koyomiex_cfg( 'delete', 'kex_del#{c}', '#{c}' )\">#{lp[63]}</button></div>"
		html << "</div><br>"
	end

  	html << "<div class='row'>"
	html << "<div class='col-2'></div>"
	html << "<div class='col-4'><button type='button' class='btn btn-outline-primary btn-sm nav_button' onclick=\"koyomiex_cfg( 'update' )\">#{lp[64]}</button></div>"
	html << "</div>"
	html << "</div>"

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

//
var koyomiex_cfg = function( step, del_id, del_no ){
	closeBroseWindows( 2 );

	if( step == 'update' ){
		var koyomiy = document.getElementById( "koyomiy" ).value;

		var breakfast_st = document.getElementById( "breakfast_st" ).value;
		var lunch_st = document.getElementById( "lunch_st" ).value;
		var dinner_st = document.getElementById( "dinner_st" ).value;

		var kex_select0 = document.getElementById( "kex_select0" ).value;
		var kex_select1 = document.getElementById( "kex_select1" ).value;
		var kex_select2 = document.getElementById( "kex_select2" ).value;
		var kex_select3 = document.getElementById( "kex_select3" ).value;
		var kex_select4 = document.getElementById( "kex_select4" ).value;
		var kex_select5 = document.getElementById( "kex_select5" ).value;
		var kex_select6 = document.getElementById( "kex_select6" ).value;
		var kex_select7 = document.getElementById( "kex_select7" ).value;
		var kex_select8 = document.getElementById( "kex_select8" ).value;
		var kex_select9 = document.getElementById( "kex_select9" ).value;

		var item0 = document.getElementById( "item0" ).value;
		var item1 = document.getElementById( "item1" ).value;
		var item2 = document.getElementById( "item2" ).value;
		var item3 = document.getElementById( "item3" ).value;
		var item4 = document.getElementById( "item4" ).value;
		var item5 = document.getElementById( "item5" ).value;
		var item6 = document.getElementById( "item6" ).value;
		var item7 = document.getElementById( "item7" ).value;
		var item8 = document.getElementById( "item8" ).value;
		var item9 = document.getElementById( "item9" ).value;

		var unit0 = document.getElementById( "unit0" ).value;
		var unit1 = document.getElementById( "unit1" ).value;
		var unit2 = document.getElementById( "unit2" ).value;
		var unit3 = document.getElementById( "unit3" ).value;
		var unit4 = document.getElementById( "unit4" ).value;
		var unit5 = document.getElementById( "unit5" ).value;
		var unit6 = document.getElementById( "unit6" ).value;
		var unit7 = document.getElementById( "unit7" ).value;
		var unit8 = document.getElementById( "unit8" ).value;
		var unit9 = document.getElementById( "unit9" ).value;

		$.post( "config.cgi", {
			mod:'koyomiex', step:step, koyomiy:koyomiy, breakfast_st:breakfast_st, lunch_st:lunch_st, dinner_st:dinner_st,
			kex_select0:kex_select0, kex_select1:kex_select1, kex_select2:kex_select2, kex_select3:kex_select3, kex_select4:kex_select4, kex_select5:kex_select5, kex_select6:kex_select6, kex_select7:kex_select7, kex_select8:kex_select8, kex_select9:kex_select9,
			item0:item0, item1:item1, item2:item2, item3:item3, item4:item4, item5:item5, item6:item6, item7:item7, item8:item8, item9:item9,
			unit0:unit0, unit1:unit1, unit2:unit2, unit3:unit3, unit4:unit4, unit5:unit5, unit6:unit6, unit7:unit7, unit8:unit8, unit9:unit9,
		}, function( data ){ $( "#bw_level2" ).html( data );});
		displayVideo( 'Saved' );
	}else if( step == 'delete' ){
		if( document.getElementById( del_id ).checked ){
			$.post( "config.cgi", { mod:'koyomiex', step:step, del_no:del_no }, function( data ){ $( "#bw_level2" ).html( data );});
			displayVideo( 'Deleted' );
		}else{
			displayVideo( 'Check!(>_<)' );
		}
	}else{
		$.post( "config.cgi", { mod:'koyomiex', step:step,  }, function( data ){ $( "#bw_level2" ).html( data );});
	}
	document.getElementById( "bw_level2" ).style.display = 'block';
};

var kexChangeselect = function( no ){
	var select_id = 'kex_select' + no;
	displayVideo( document.getElementById( select_id ).value );

	if( document.getElementById( select_id ).value == 1 ){

		document.getElementById('item' + no ).disabled = false;
		document.getElementById('unit' + no ).disabled = false;
	}else{
		document.getElementById('item' + no ).disabled = true;
		document.getElementById('unit' + no ).disabled = true;
	}
};

</script>
JS
	puts js
end
