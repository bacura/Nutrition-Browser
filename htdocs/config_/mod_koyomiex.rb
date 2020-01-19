# Config module for Nutorition browser koyomiex 0.00
#encoding: utf-8

def config_module( cgi )
	uname, uid, status, aliasu, language = login_check( cgi )
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
		mariadb( "UPDATE #{$MYSQL_TB_CFG} SET koyomiex='#{koyomiex_new}', koyomiy='#{koyomiy}:#{breakfast_st}:#{lunch_st}:#{dinner_st}' WHERE user='#{uname}';", false )
	when 'delete'
		r = mariadb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
		kex_select_set = r.first['koyomiex'].split( ':' )
		koyomiex_new = ''
		kex_select_set.size.times do |c|
			if del_no == c
				koyomiex_new << "0\t\t:"
				mariadb( "UPDATE #{$MYSQL_TB_KOYOMIEX} SET item#{c}='' WHERE user='#{uname}';", false )
			else
				koyomiex_new << "#{kex_select_set[c]}:"
			end
		end
		koyomiex_new.chop!
		mariadb( "UPDATE #{$MYSQL_TB_CFG} SET koyomiex='#{koyomiex_new}' WHERE user='#{uname}';", false )
	end

	r = mariadb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
	if r.first['koyomiex'] == '' || r.first['koyomiex'] == nil
		mariadb( "UPDATE #{$MYSQL_TB_CFG} SET koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t' WHERE user='#{uname}';", false )
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
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
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
	html << "<div class='input-group-prepend'><span class='input-group-text'>こよみ開始年</span></div>"
  	html << "<select class='custom-select' id='koyomiy'>"
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
	html << "<div class='input-group-prepend'><span class='input-group-text'>朝食標準時刻</span></div>"
 	html << "<select class='custom-select' id='breakfast_st'>"
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
	html << "<div class='input-group-prepend'><span class='input-group-text'>昼食標準時刻</span></div>"
 	html << "<select class='custom-select' id='lunch_st'>"
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
	html << "<div class='input-group-prepend'><span class='input-group-text'>夕食標準時刻</span></div>"
 	html << "<select class='custom-select' id='dinner_st'>"
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

	html << "<h5>こよみ拡張・項目設定:</h5><br>"

	0.upto( 9 ) do |c|
		html << "<div class='row'>"
		html << "	<div class='col-3'>"
		html << "		<div class='input-group input-group-sm'>"
  		html << "			<div class='input-group-prepend'>"
    	html << "				<label class='input-group-text'>項目#{c}</label>"
  		html << "			</div>"
  		html << "			<select class='custom-select' id='kex_select#{c}' onChange=\"kexChangeselect( '#{c}' )\">"
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
		html << "			<div class='input-group-prepend'>"
		html << "				<span class='input-group-text'>名称</span>"
		html << "			</div>"
		if kex_select_set[c] == 1
			html << "<input type='text' maxlength='32' id='item#{c}' class='form-control form-control-sm' value='#{item_set[c]}'>"
    	else
			html << "<input type='text' maxlength='32' id='item#{c}' class='form-control form-control-sm' value='' disabled>"
    	end
		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-2'>"
		html << "		<div class='input-group input-group-sm'>"
		html << "			<div class='input-group-prepend'>"
		html << "				<span class='input-group-text'>単位</span>"
		html << "			</div>"
		if kex_select_set[c] == 1
			html << "			<input type='text' maxlength='32' id='unit#{c}' class='form-control form-control-sm' value='#{item_set[c]}'>"
    	else
			html << "			<input type='text' maxlength='32' id='unit#{c}' class='form-control form-control-sm' value='' disabled>"
    	end
		html << "		</div>"
		html << "	</div>"
		html << "	<div class='col-1'></div>"
		html << "	<div class='col-2'><input type='checkbox' id='kex_del#{c}'>&nbsp;<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"koyomiex_cfg( 'delete', 'kex_del#{c}', '#{c}' )\">初期化</button></div>"
		html << "</div><br>"
	end

  	html << "<div class='row'>"
	html << "<div class='col-2'></div>"
	html << "<div class='col-4'><button type='button' class='btn btn-outline-primary btn-sm nav_button' onclick=\"koyomiex_cfg( 'update' )\">保存</button></div>"
	html << "</div>"
	html << "</div>"

	return html
end
