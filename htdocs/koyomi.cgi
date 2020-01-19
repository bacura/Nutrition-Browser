#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190220, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
@tdiv_set = [ 'breakfast', 'lunch', 'dinner', 'supple', 'memo' ]


#==============================================================================
#DEFINITION
#==============================================================================
def meals( meal, uname )

	mb_html = '<ul>'
	a = meal.split( "\t" )
	a.each do |e|
		aa = e.split( ':' )
		if aa[0] == '?--'
			mb_html << "<li style='list-style-type: circle'>何か食べた（微盛）</li>"
		elsif aa[0] == '?-'
			mb_html << "<li style='list-style-type: circle'>何か食べた（小盛）</li>"
		elsif aa[0] == '?='
			mb_html << "<li style='list-style-type: circle'>何か食べた（並盛）</li>"
		elsif aa[0] == '?+'
			mb_html << "<li style='list-style-type: circle'>何か食べた（大盛）</li>"
		elsif aa[0] == '?++'
			mb_html << "<li style='list-style-type: circle'>何か食べた（特盛）</li>"
		elsif /\-m\-/ =~ aa[0]
			r = mdb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{aa[0]}';", false, @debug )
			mb_html << "<li>#{r.first['name']}</li>"
		elsif /\-f\-/ =~ aa[0]
			r = mdb( "SELECT name FROM #{$MYSQL_TB_FCS} WHERE code='#{aa[0]}';", false, @debug )
			mb_html << "<li style='list-style-type: circle'>#{r.first['name']}</li>"
		elsif /\-/ =~ aa[0]
			r = mdb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{aa[0]}';", false, @debug )
			mb_html << "<li>#{r.first['name']}</li>"
		else
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}';"
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}' AND user='#{uname}';" if /^U/ =~ aa[0]
			r = mdb( q, false, @debug )
			mb_html << "<li style='list-style-type: square'>#{r.first['name']}</li>"
		end
	end
	mb_html << '</ul>'

	return mb_html
end


####
def get_starty( uname )
	start_year = $TIME_NOW.year
	r = mdb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, @debug )
	if r.first['koyomiy']
		a = r.first['koyomiy'].split( ':' )
		start_year = a[0].to_i if a[0].to_i != 0
	end

	return start_year
end


#### Multi calc
def multi_calc( uname, yyyy, mm, dd, fc_items )
	results = ''
	some_set = ''
	fct_total = Hash.new
	fct_total.default = BigDecimal( 0 )
	fzcode = ''
	freeze_flag = false

	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv!='4';", false, @debug )
	if r.first
		fzcode = r.first['fzcode']
		r.each do |e|
			menu_set = []
			code_set = []
			rate_set = []
			unit_set = []

			break if freeze_flag
			if e['freeze'] == 1
				rr = mdb( "SELECT * FROM #{$MYSQL_TB_FCZ} WHERE user='#{uname}' AND code='#{fzcode}';", false, @debug )
				if rr.first
					5.upto( 65) do |c|
						fct_total[$FCT_ITEM[c]] = BigDecimal( rr.first[$FCT_ITEM[c]] )
					end
					freeze_flag = true
				end
			else
				a = e['koyomi'].split( "\t" )
				a.each do |ee|
					( koyomi_code, koyomi_rate, koyomi_unit, z ) = ee.split( ':' )
					code_set << koyomi_code
					rate_set << koyomi_rate
					unit_set << koyomi_unit
				end

				code_set.size.times do |c|
					code = code_set[c]
					rate = BigDecimal( rate_set[c] )
					unit = unit_set[c]

#### temporary ####
					if unit == 'g'
						unit = 0
					elsif unit == '%'
						unit == 99
					else
						unit = unit.to_i
					end
#### temporary ####

					if /\?/ =~ code
						some_set << "+#{$SOMETHING[code]}&nbsp;"
					elsif /\-f\-/ =~ code
						rr = mdb( "SELECT * FROM #{$MYSQL_TB_FCS} WHERE user='#{uname}' AND code='#{code}';", false, @debug )
						if rr.first
							5.upto( 65) do |cc|
								fct_total[$FCT_ITEM[cc]] += BigDecimal( num_opt( rr.first[$FCT_ITEM[cc]], 100, 1, $FCT_FRCT[$FCT_ITEM[cc]] + 3 ))
							end
						end
					else
						recipe_set = []
						fn_set = []
						weight_set = []
						if /\-m\-/ =~ code
							rr = mdb( "SELECT meal FROM #{$MYSQL_TB_MENU} WHERE user='#{uname}' AND code='#{code}';", false, @debug )
							a = rr.first['meal'].split( "\t" )
							a.each do |e| recipe_set << e end
						end

						if recipe_set.size == 0
							recipe_set << code
						end
						recipe_set.size.times do |cc|
							recipe_total_weight = BigDecimal( 0 )

							if /\-r\-/ =~ recipe_set[cc] || /\w+\-\h{4}\-\h{4}/ =~ recipe_set[cc]
#								p 'recipe'
								rr = mdb( "SELECT sum, dish FROM #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' AND code='#{recipe_set[cc]}';", false, @debug )
								a = rr.first['sum'].split( "\t" )
								a.each do |eee|
									( sum_no, sum_weight, z, z, z, z, z, sum_ew ) = eee.split( ':' )

									if sum_no != '+' && sum_no != '-'
										fn_set << sum_no
										sum_ew = sum_weight if sum_ew == nil
										weight_set << ( BigDecimal( sum_ew ) / rr.first['dish'].to_i )
										recipe_total_weight += ( BigDecimal( sum_ew ) / rr.first['dish'].to_i )
									end
								end

								if unit == 99
									weight_set.map! do |x| x * rate / 100 end
								else
									weight_set.map! do |x| x * rate / recipe_total_weight end
								end
							end
						end

						# food
						if fn_set.size == 0
							fn_set << code
							weight_set << rate
						end

						#
						if unit != 0 && unit != 99
							fn_set.size.times do |cc|
								weight_set[cc] = unit_weight( weight_set[cc], unit, fn_set[cc] )
							end
						end

						fn_set.size.times do |cc|
							query = ''
							if /^P/ =~ fn_set[cc]
								query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{fn_set[cc]}';"
							elsif /^U/ =~ fn_set[cc]
								query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{fn_set[cc]}' AND user='#{uname}';"
							else
								query = "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{fn_set[cc]}';"
							end

							rr = mdb( query, false, @debug )
							if rr.first
								5.upto( 65) do |ccc|
									t = convert_zero( rr.first[$FCT_ITEM[ccc]] )
									fct_total[$FCT_ITEM[ccc]] += BigDecimal( num_opt( t, weight_set[cc], 1, $FCT_FRCT[$FCT_ITEM[ccc]] + 3 ))
								end
							end
						end
					end
				end
			end
		end
	end

	unless freeze_flag
		sub_query = ''
		fct_total.each do |k, v|
			t = v.round( $FCT_FRCT[k] )
			fct_total[k] = t
			sub_query << " #{k}='#{t}',"
		end
		sub_query.chop!

		r = mdb( "SELECT code FROM #{$MYSQL_TB_FCZ} WHERE user='#{uname}' AND code='#{fzcode}';", false, @debug )
		if r.first && fzcode != ''
			mdb( "UPDATE #{$MYSQL_TB_FCZ} SET #{sub_query} WHERE user='#{uname}' AND code='#{fzcode}';", false, @debug )
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fzcode='#{fzcode}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}}';", false, @debug )
		else
			new_fzcode = generate_code( uname, 'z' )
			mdb( "INSERT INTO #{$MYSQL_TB_FCZ} SET user='#{uname}', code='#{new_fzcode}', #{sub_query};", false, @debug )
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fzcode='#{new_fzcode}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
		end
	end

	fc_items.each do |e| results << "#{$FCT_NAME[e]}[#{fct_total[e].to_f}]&nbsp;&nbsp;&nbsp;&nbsp;" end
	results << "#{some_set}&nbsp;&nbsp;&nbsp;&nbsp;" unless some_set == ''

	if fct_total['PROT'] == 0
		pfc_p = 0
	else
		pfc_p = ( fct_total['PROT'] * 4 / fct_total['ENERC_KCAL'] * 100 ).round( 1 )
	end
	if fct_total['PROT'] == 0
		pfc_f = 0
	else
		pfc_f = ( fct_total['FAT'] * 4 / fct_total['ENERC_KCAL'] * 100 ).round( 1 )
	end
	pfc_c = 100 - pfc_p - pfc_f
	results << "<span style='color:crimson'>P</span>:<span style='color:green'>F</span>:<span style='color:blue'>C</span> (%) = <span style='color:crimson'>#{pfc_p.to_f}</span> : <span style='color:green'>#{pfc_f.to_f}</span> : <span style='color:blue'>#{pfc_c.to_f}</span>"


	return results
end

#==============================================================================
# Main
#==============================================================================
cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )

html_init( nil )

#### Guild member check
if status < 3
	puts "Guild member error."
	exit
end


lp = lp_init( 'koyomi', language )
start_year = get_starty( uname )
if @debug
	puts "uname:#{uname}<br>\n"
	puts "status:#{status}<br>\n"
	puts "aliaseu:#{aliaseu}<br>\n"
	puts "language:#{language}<br>\n"
	puts "<hr>\n"
end


#### POSTデータの取得
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
dd = 1 if dd == 0
freeze_check = cgi['freeze_check']
freeze_check_all = cgi['freeze_check_all']
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "freeze_check:#{freeze_check}<br>\n"
	puts "freeze_check_all:#{freeze_check_all}<br>\n"
	puts "<hr>\n"
end


#### General menu
if command == 'menu'
html = <<-"MENU"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="initKoyomi()">#{lp[23]}</button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="initKoyomiex_BW1( '', '' )">#{lp[24]}</button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-light' onclick="">#{lp[25]}</button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-light' onclick="">#{lp[26]}</button></div>
		<div class='col-2'></div>
	</div>
</div>

MENU
	puts html
	exit()
end


#### Getting date
date = Date.today
date = Date.new( yyyy, mm, dd ) unless yyyy == 0
date_first = Date.new( date.year, date.month, 1 )
first_week = date_first.wday
last_day = Date.new( date.year, date.month, -1 ).day
if yyyy == 0
 	yyyy = date.year
	mm = date.month
	dd = date.day
end
if @debug
	puts "date:#{date.to_time}<br>\n"
	puts "first_week:#{first_week}<br>\n"
	puts "last_day:#{last_day}<br>\n"
end


####
freeze_all_checked = ''
case command
when 'freeze'
	if freeze_check == 'true'
		r = mdb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='1' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
		else
	   		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{uname}', freeze='1', date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
		end
	elsif freeze_check == 'false'
		r = mdb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='0' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
		end
	end
when 'freeze_all'
	if freeze_check_all == 'true'
		1.upto( last_day ) do |c|
			r = mdb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{c}';", false, @debug )
			if r.first
				if r.first['freeze'] != 1
					mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='1' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{c}';", false, @debug )
				end
			else
	   			mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{uname}', freeze='1', date='#{yyyy}-#{mm}-#{c}';", false, @debug )
			end
		end
		freeze_all_checked = 'CHECKED'
	elsif freeze_check_all == 'false'
		 mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET freeze='0' WHERE user='#{uname}' AND ( date BETWEEN '#{yyyy}-#{mm}-1' AND '#{yyyy}-#{mm}-#{last_day}' );", false, @debug )
	end
end


####
calc_html_set = ['']
fc_items = []
fc_names = []
r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{uname}' AND name='簡易表示用';", false, @debug )
if r.first
	palette = r.first['palette']
	palette.size.times do |c|
		fc_items << $FCT_ITEM[c] if palette[c] == '1'
	end
else
 	fc_items = ['ENERC_KCAL', 'PROT', 'FAT', 'CHO', 'NACL_EQ']
end
fc_items.each do |e| fc_names << $FCT_NAME[e] end

1.upto( last_day ) do |c|
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{c}';", false, @debug )
	if r.first
		calc_html_set << multi_calc( uname, yyyy, mm, c, fc_items )
	else
		calc_html_set << ''
	end
end


####
date_html = ''
week_count = first_week
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
1.upto( last_day ) do |c|
	freeze_flag = false
	koyomi_tmp = []
	freeze_checked = ''

	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{c}';", false, @debug )
	if r.first
		r.each do |e|
			koyomi_tmp[e['tdiv']] = e['koyomi'] if e['tdiv'] != nil
			freeze_flag = true if r.first['freeze'] == 1
		end
	else
		5.times do koyomi_tmp << '' end
	end

	freeze_checked = 'CHECKED' if freeze_flag
	onclick = "onclick=\"editKoyomi_BW2( 'init', '#{c}' )\""

	date_html << "<tr>"
	if week_count == 0
#		date_html << "<td style='color:red;'><span>#{c}</span> (#{weeks[week_count]})</td>"
		date_html << "<td style='color:red;'><a id='day#{c}'>#{c} (#{weeks[week_count]})</a></td>"
	else
#		date_html << "<td><span>#{c}</span> (#{weeks[week_count]})</td>"
		date_html << "<td><a id='day#{c}'>#{c} (#{weeks[week_count]})</a></td>"
	end

	4.times do |cc|
		if koyomi_tmp[cc] == '' || koyomi_tmp[cc] == nil
			date_html << "<td #{onclick}>-</td>"
		else
			meal_block = meals( koyomi_tmp[cc], uname )
			date_html << "<td #{onclick}>#{meal_block}</td>"
		end
	end

	if koyomi_tmp[4] == '' || koyomi_tmp[4] == nil
		date_html << "<td #{onclick}>-</td>"
	else
		date_html << "<td #{onclick}>#{koyomi_tmp[4]}</td>"
	end

	date_html << "<td><input type='checkbox' id='freeze_check#{c}' onChange=\"freezeKoyomi( '#{yyyy}', '#{mm}', '#{c}' )\" #{freeze_checked}></td>"
	date_html << "</tr>"

	if calc_html_set[c] == '' || calc_html_set[c] == nil
		date_html << "<tr id='nutrition#{c}' class='table-borderless' style='display:none'>"
	else
		date_html << "<tr id='nutrition#{c}' class='table-borderless'>"
	end

	date_html << "<td></td>"
	date_html << "<td colspan='5'>#{calc_html_set[c]}</td>"
	date_html << "<td></td>"
	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


####
select_html = ''
select_html << "<div class='input-group input-group-sm'>"
select_html << "<select id='yyyy' class='custom-select' onChange=\"changeKoyomi_BW1()\">"
start_year.upto( date.year + 1 ) do |c|
	if c == yyyy
		select_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		select_html << "<option value='#{c}'>#{c}</option>"
	end
end
select_html << "</select>"
select_html << "<div class='input-group-append'><label class='input-group-text'>#{lp[9]}</label></div>"
select_html << "</div>"

select_html << "<div class='input-group input-group-sm'>"
select_html << "<select id='mm' class='custom-select custom-select-sm' onChange=\"changeKoyomi_BW1()\">"
1.upto( 12 ) do |c|
	if c == mm
		select_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		select_html << "<option value='#{c}'>#{c}</option>"
	end
end
select_html << "</select>"
select_html << "<div class='input-group-append'><label class='input-group-text'>#{lp[10]}</label></div>"
select_html << "</div>"


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5><a href='#day{dd}'>#{lp[8]}:</a></h5></div>
		<div class='col-5 form-inline'>
			#{select_html}
		</div>
		<div class='col-3'>
		</div>
		<div class='col-2'>
			<button class='btn btn-sm btn-success' onclick="initKoyomiex_BW1( '#{yyyy}', '#{mm}' )">#{lp[22]}</button>
		</div>
	</div>
	<div class='row'>
		<div class='col'></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
    	<tr>
     		<th align='center'>#{lp[11]}</th>
     		<th align='center'>#{lp[12]}</th>
     		<th align='center'>#{lp[13]}</th>
     		<th align='center'>#{lp[14]}</th>
     		<th align='center'>#{lp[15]}</th>
     		<th align='center'>#{lp[16]}</th>
     		<th align='center'><input type='checkbox' id='freeze_check_all' onChange="freezeKoyomiAll( '#{yyyy}', '#{mm}' )" #{freeze_all_checked}>&nbsp;#{lp[17]}</th>
    	</tr>
  	</thead>
	#{date_html}
	</table>

HTML

puts html


#### Deleting Empty koyomi
mdb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE koyomi='';", false, @debug )
