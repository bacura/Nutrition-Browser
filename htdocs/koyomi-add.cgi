#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi adding panel 0.02b

#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomi-add'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### Getting start year & standard time
def get_starty( uname )
	start_year = $TIME_NOW.year
	breakfast_st = 0
	lunch_st = 0
	dinner_st = 0
	r = mdb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, @debug )
	if r.first['koyomiy']
		a = r.first['koyomiy'].split( ':' )
		start_year = a[0].to_i if a[0].to_i != 0
		breakfast_st = a[1].to_i if a[1].to_i != 0
		lunch_st = a[2].to_i if a[2].to_i != 0
		dinner_st = a[3].to_i if a[3].to_i != 0
	end
	st_set = [ breakfast_st, lunch_st, dinner_st ]

	return start_year, st_set
end


#### unit select
def unit_select_html( code, selectu )
	# 単位の生成と選択
	unit_select_html = ''
	unit_set = []
	unit_select = []
	r = mdb( "SELECT unitc FROM #{$MYSQL_TB_EXT} WHERE FN='#{code}';", false, false )
	if r.first['unitc'] != nil && r.first['unitc'] != ''
		t = r.first['unitc'].split( ':' )

#### Temporary
		if t.size == 14
			t << '0.0'
			t << ''
		end
#### Temporary

		t.size.times do |c|
			unless t[c] == '0.0'
				unit_set << c
				if c == selectu.to_i
					unit_select << 'SELECTED'
				else
					unit_select << ''
				end
			end
		end
	else
		unit_set = [ 0, 1, 15 ]
		if selectu == 15
			unit_select = [ '', '', 'SELECTED' ]
		elsif selectu == 1
			unit_select = [ '', 'SELECTED', '' ]
		else
			unit_select = [ 'SELECTED', '', '' ]
		end
	end

	unit_set.size.times do |c|
		unit_select_html << "<option value='#{unit_set[c]}' #{unit_select[c]}>#{$UNIT[unit_set[c]]}</option>"
	end

	return unit_select_html
end


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### Getting POST
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
yyyy_mm_dd = cgi['yyyy_mm_dd']
unless yyyy_mm_dd == ''
	a = yyyy_mm_dd.split( '-' )
	yyyy = a[0].to_i
	mm = a[1].to_i
	dd = a[2].to_i
end
code = cgi['code']
ev = cgi['ev'].to_i
eu = cgi['eu'].to_i
tdiv = cgi['tdiv'].to_i
hh = cgi['hh']
order = cgi['order'].to_i
copy = cgi['copy'].to_i
origin = cgi['origin']
dd = 1 if dd == 0
ev = 100 if ev == 0
if hh == '' || command == 'modify'
	hh = 99
else
	hh = hh.to_i
end
origin = "#{yyyy}:#{mm}:#{dd}:#{tdiv}:#{order}" if command == 'modify' && origin == ''
if @debug
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "hh:#{hh}<br>\n"
	puts "tdiv:#{tdiv}<br>\n"
	puts "ev:#{ev}<br>\n"
	puts "eu:#{eu}<br>\n"
	puts "order:#{order}<br>\n"
	puts "copy:#{copy}<br>\n"
	puts "origin:#{origin}<br>\n"
	puts "<hr>\n"
end


#### Date & calendar config
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar.debug if @debug
sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
sql_ym = "#{calendar.yyyy}-#{calendar.mm}"
org_ymd = "#{calendar.yyyy}:#{calendar.mm}:#{calendar.dd}"

#### Temp
( dummy, st_set ) = get_starty( user.name )
#### Temp


#### Move food (deleting origin )
new_solid = ''
if command == 'move' && copy != 1
	a = origin.split( ':' )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{a[0]}-#{a[1]}-#{a[2]}' AND tdiv='#{a[3]}';", false, @debug  )
	if r.first['koyomi']
		t = r.first['koyomi']
		aa = t.split( "\t" )
		0.upto( aa.size - 1 ) do |c|
			new_solid << "#{aa[c]}\t" unless c == a[4].to_i
		end
		new_solid.chop! unless new_solid == ''
	end
	mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{new_solid}' WHERE user='#{user.name}' AND date='#{a[0]}-#{a[1]}-#{a[2]}' AND tdiv='#{a[3]}';", false, @debug )
end


#### Save food
if command == 'save' || command == 'move'
	hh = st_set[tdiv] if hh == 99
	hh = $TIME_NOW.hour if hh == nil || hh == ''

	if /\-f\-/ =~ code && copy == 1
		r = mdb( "SELECT * FROM #{$MYSQL_TB_FCS} WHERE code='#{code}' and user='#{user.name}';", false, @debug )
		copy_name = r.first['name']
		set_sql = ''
		5.upto( 65 ) do |c| set_sql << ", #{$FCT_ITEM[c]}='#{r.first[$FCT_ITEM[c]]}'" end
		code = generate_code( user.name, 'f' )
		mdb( "INSERT INTO #{$MYSQL_TB_FCS} SET code='#{code}', name='#{copy_name}', user='#{user.name}' #{set_sql};", false, @debug )
	end

	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ymd}' AND tdiv='#{tdiv}';", false, @debug )
	if r.first
		koyomi = r.first['koyomi']
		delimiter = ''
		delimiter = "\t" if koyomi != ''
		koyomi << "#{delimiter}#{code}:#{ev}:#{eu}:#{hh}"
		mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{user.name}' AND date='#{sql_ymd}' AND tdiv='#{tdiv}';", false, @debug )
		origin = "#{org_ymd}:#{tdiv}:#{koyomi.split( "\t" ).size - 1}" if command == 'move'
	else
		koyomi = "#{code}:#{ev}:#{eu}:#{hh}"
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', fzcode='', freeze='0', koyomi='#{koyomi}', date='#{sql_ymd}', tdiv='#{tdiv}';", false, @debug )
		origin = "#{org_ymd}:#{tdiv}:0" if command == 'move'
	end
end

copy_html = ''
save_button = "<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"saveKoyomiAdd( 'save', '#{code}', '#{origin}' )\">#{lp[12]}</button>"


####
if command == 'modify' || command == 'move' || command == 'move_fix'
	copy_html << "<div class='form-group form-check'>"
    copy_html << "<input type='checkbox' class='form-check-input' id='copy'>"
    copy_html << "<label class='form-check-label'>#{lp[24]}</label>"
	copy_html << "</div>"

	save_button = "<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"saveKoyomiAdd( 'move', '#{code}', '#{origin}' )\">#{lp[23]}</button>"
end


####
food_name = code
if /\-m\-/ =~ code
	r = mdb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{code}' and user='#{user.name}';", false, @debug )
	food_name = r.first['name']
elsif /\-f\-/ =~ code
	r = mdb( "SELECT name FROM #{$MYSQL_TB_FCS} WHERE code='#{code}' and user='#{user.name}';", false, @debug )
	food_name = r.first['name']
elsif /\-/ =~ code
	r = mdb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}' and user='#{user.name}';", false, @debug )
	food_name = r.first['name']
else
	q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}';"
	q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{user.name}';" if /^U\d{5}/ =~ code
	r = mdb( q, false, @debug )
	food_name = r.first['name']
end


#### Date HTML
date_html = ''
week_count = calendar.wf
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
1.upto( calendar.ddl ) do |c|
	date_html << "<tr>"
	if week_count == 0
		date_html << "<td style='color:red;'>#{c} (#{weeks[week_count]})</td>"
	else
		date_html << "<td>#{c} (#{weeks[week_count]})</td>"
	end

	r = mdb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}' AND freeze='1';", false, @debug )
	unless r.first
		0.upto( 3 ) do |cc|
			koyomi_c = '-'
			rr = mdb( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{sql_ym}-#{c}' AND tdiv='#{cc}';", false, @debug )
			onclick = "onclick=\"saveKoyomiAdd_direct( '#{code}','#{calendar.yyyy}','#{calendar.mm}', '#{c}', '#{cc}', '#{origin}' )\""
			onclick = "onclick=\"modifysaveKoyomi_direct( '#{code}','#{calendar.yyyy}','#{calendar.mm}', '#{c}', '#{cc}', '#{origin}' )\"" if command == 'modify' || command == 'move' || command == 'move_fix'

			if rr.first
				if rr.first['koyomi'] == ''
					date_html << "<td class='table-light' align='center' #{onclick}>#{koyomi_c}</td>"
				else
					koyomi_c = rr.first['koyomi'].split( "\t" ).size
					date_html << "<td class='table-info' align='center' #{onclick}>#{koyomi_c}</td>"
				end
			else
				date_html << "<td class='table-light' align='center' #{onclick}>#{koyomi_c}</td>"
			end
		end
	else
		4.times do date_html << "<td class='table-secondary'></td>" end
	end

	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


#### Select HTML
tdiv_set = [ lp[13], lp[14], lp[15], lp[16] ]

tdiv_html = ''
tdiv_html << "<select id='tdiv' class='form-select form-select-sm'>"
0.upto( 3 ) do |c|
	if tdiv == c
		tdiv_html << "<option value='#{c}' SELECTED>#{tdiv_set[c]}</option>"
	else
		tdiv_html << "<option value='#{c}'>#{tdiv_set[c]}</option>"
	end
end
tdiv_html << "</select>"

#### Rate HTML
hour_html = ''
hour_html << "<select id='hh' class='form-select form-select-sm'>"
hour_html << "<option value='99'>時刻</option>"
0.upto( 23 ) do |c|
	if c == hh
		hour_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		hour_html << "<option value='#{c}'>#{c}</option>"
	end
end
hour_html << "</select>"
#select_html << "<button class='btn btn-sm btn-outline-success' type='button' onclick=\"nowKoyomi()\">#{lp[11]}</button>"


#### Rate HTML
rate_selected = ''
rate_html = ''
if command != 'move_fix' && /\-f\-/ !~ code
	rate_selected = 'SELECTED' if /^[UP]?\d{5}/ =~ code
	rate_html = ''
	rate_html << "<div class='input-group input-group-sm'>"
	rate_html << "	<span class='input-group-text'>#{lp[22]}</span>"
	rate_html << "	<input type='text' id='ev' value='#{ev}' class='form-control'>"
	rate_html << "	<select id='eu' class='form-select form-select-sm'>"
	if /^[UP]?\d{5}/ =~ code
		rate_html << unit_select_html( code, eu )
	else
		rate_html << "		<option value='99'>%</option>"
		rate_html << "		<option value='0' #{rate_selected}>g</option>"
	end
	rate_html << "	</select>"
	rate_html << "</div>"
else
#	rate_html = '<input type="hidden" id="ev" value="100">'
#	rate_html = '<input type="hidden" id="eu" value="0">'
end

#### Return button
return_button = "<span onclick=\"koyomiReturn()\">#{lp[11]}</span>"
if command == 'modify' || command == 'move'
	return_button = "<span onclick=\"koyomiReturn2KE( '#{calendar.yyyy}', '#{calendar.mm}', '#{calendar.dd}' )\">#{lp[11]}</span>"
end


onchange = "onChange=\"changeKoyomiAdd( 'init', '#{code}', '#{origin}' )\""
onchange = "onChange=\"changeKoyomiAdd( 'modify', '#{code}', '#{origin}' )\"" if command == 'modify'


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-11'><h5>#{food_name}</h5></div>
		<div class='col-1'>#{return_button}</div>
	</div>
	<div class='row'>
		<div class='col-2 form-inline'>
			<input type='date' id='yyyy_mm_dd' min='#{calendar.yyyyf}-01-01' max='#{calendar.yyyy + 2}-12-31' value='#{calendar.yyyy}-#{calendar.mms}-#{calendar.dds}' #{onchange}>
		</div>
		<div class='col-2 form-inline'>
			#{tdiv_html}
		</div>
		<div class='col-2 form-inline'>
			#{hour_html}
		</div>
		<div class='col-3 form-inline'>
			#{rate_html}
		</div>
		<div class='col-1 form-inline'>
			#{save_button}
		</div>
		<div class='col-1 form-inline'>
			#{copy_html}
		</div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
    	<tr>
     		<th align='center'></th>
     		<th align='center'>#{lp[18]}</th>
     		<th align='center'>#{lp[19]}</th>
     		<th align='center'>#{lp[20]}</th>
     		<th align='center'>#{lp[21]}</th>
    	</tr>
  	</thead>
	#{date_html}
	</table>
HTML
puts html

#### Adding history
add_his( user.name, code ) if /^[UP]?\d{5}/ =~ code
