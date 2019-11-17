#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi adding panel 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190511, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require 'date'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
@tdiv_set = [ 'breakfast', 'lunch', 'dinner', 'supple', 'memo' ]


#==============================================================================
#DEFINITION
#==============================================================================

#### Getting start year & standard time
def get_starty( uname )
	start_year = $DATETIME.year
	breakfast_st = 0
	lunch_st = 0
	dinner_st = 0
	r = mariadb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
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

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomi-add', language )
start_year, st_set = get_starty( uname )
if @debug
	puts "uname:#{uname}<br>\n"
	puts "status:#{status}<br>\n"
	puts "aliaseu:#{aliaseu}<br>\n"
	puts "language:#{language}<br>\n"
	puts "<hr>\n"
	puts "start_year:#{start_year}<br>\n"
	puts "st_set:#{st_set}<br>\n"
	puts "<hr>\n"
end


#### Getting POST
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
code = cgi['code']
ev = cgi['ev'].to_i
eu = cgi['eu'].to_s
tdiv = cgi['tdiv'].to_i
hh = cgi['hh']
order = cgi['order'].to_i
copy = cgi['copy'].to_i
origin = cgi['origin']
dd = 1 if dd == 0
ev = 100 if ev == 0
if hh == ''
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


#### Move food
new_solid = ''
if command == 'move' && copy != 1
	a = origin.split( ':' )
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{a[0]}-#{a[1]}-#{a[2]}' AND tdiv='#{a[3]}';", false )
	if r.first[@tdiv_set[a[3].to_i]]
		t = r.first[@tdiv_set[a[3].to_i]]
		aa = t.split( "\t" )
		0.upto( aa.size ) do |c|
			new_solid << "#{aa[c]}\t" unless c == a[4].to_i
		end
		new_solid.chop! unless new_solid == ''
	end
	mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{new_solid}' WHERE user='#{uname}' AND date='#{a[0]}-#{a[1]}-#{a[2]}' AND tdiv='#{a[3]}';", false )
end


#### Save food
if command == 'save' || command == 'move'
	hh = st_set[tdiv] if hh == 99
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
	if r.first
		koyomi = r.first['koyomi']
		delimiter = ''
		delimiter = "\t" if koyomi != ''
		koyomi << "#{delimiter}#{code}:#{ev}:#{eu}:#{hh}"
		mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
		origin = "#{yyyy}:#{mm}:#{dd}:#{tdiv}:#{koyomi.split( "\t" ).size - 1}" if command == 'move'
	else
		koyomi = "#{code}:#{ev}:#{eu}:#{hh}"
		mariadb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{uname}', fix='', koyomi='#{koyomi}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", false )
		origin = "#{yyyy}:#{mm}:#{dd}:#{tdiv}:0" if command == 'move'
	end
end

copy_html = ''
save_button = "<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"saveKoyomi_BWF( '#{code}', '#{origin}' )\">#{lp[12]}</button>"


if command == 'modify' || command == 'move'
	copy_html << "<div class='form-group form-check'>"
    copy_html << "<input type='checkbox' class='form-check-input' id='copy'>"
    copy_html << "<label class='form-check-label'>#{lp[24]}</label>"
	copy_html << "</div>"

	save_button = "<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"modifysaveKoyomi( '#{code}', '#{origin}' )\">#{lp[23]}</button>"
end


####
food_name = code
if /\-m\-/ =~ code
	r = mariadb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{code}';", false )
	food_name = r.first['name']
elsif /\-/ =~ code
	r = mariadb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';", false )
	food_name = r.first['name']
else
	q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}';"
	q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{uname}';" if /^U\d{5}/ =~ code
	r = mariadb( q, false )
	food_name = r.first['name']
end


#### Date HTML
date_html = ''
week_count = first_week
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
1.upto( last_day ) do |c|
	date_html << "<tr>"
	if week_count == 0
		date_html << "<td style='color:red;'>#{c} (#{weeks[week_count]})</td>"
	else
		date_html << "<td>#{c} (#{weeks[week_count]})</td>"
	end

	0.upto( 3 ) do |cc|
		koyomi_c = '-'
		r = mariadb( "SELECT fix, koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{c}' AND tdiv='#{cc}';", false)
		onclick = "onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '#{cc}', '#{origin}' )\""
		onclick = "onclick=\"modifysaveKoyomi2( '#{code}','#{yyyy}','#{mm}', '#{c}', '#{cc}', '#{origin}' )\"" if command == 'modify' || command == 'move'
		if r.first
			if r.first['fix'] != ''
				date_html << "<td class='btn-secondary'></td>"
			elsif r.first['koyomi'] == ''
				date_html << "<td class='btn-light' align='center' #{onclick}>#{koyomi_c}</td>"
			else
				koyomi_c = r.first['koyomi'].split( "\t" ).size
				date_html << "<td class='btn-info' align='center' #{onclick}>#{koyomi_c}</td>"
			end
		else
			date_html << "<td class='btn-light' align='center' #{onclick}>#{koyomi_c}</td>"
		end
	end

	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


#### Select HTML
select_html = ''
onchange = "onChange=\"changeKoyomi_BWF( '#{code}', '#{origin}' )\""
onchange = "onChange=\"modifychangeKoyomi( '#{code}', '#{origin}' )\"" if command == 'modify'


select_html << "<select id='yyyy_add' class='custom-select custom-select-sm' #{onchange}>"
start_year.upto( 2020 ) do |c|
	if c == yyyy
		select_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		select_html << "<option value='#{c}'>#{c}</option>"
	end
end
select_html << "</select>&nbsp;/&nbsp;"

select_html << "<select id='mm_add' class='custom-select custom-select-sm' #{onchange}>"
1.upto( 12 ) do |c|
	if c == mm
		select_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		select_html << "<option value='#{c}'>#{c}</option>"
	end
end
select_html << "</select>&nbsp;/&nbsp;"

select_html << "<select id='dd' class='custom-select custom-select-sm'>"
1.upto( last_day ) do |c|
	if c == dd
		select_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		select_html << "<option value='#{c}'>#{c}</option>"
	end
end
select_html << "</select>&nbsp;&nbsp;&nbsp;&nbsp;"

tdiv_set = [ lp[13], lp[14], lp[15], lp[16] ]
select_html << "<select id='tdiv' class='custom-select custom-select-sm'>"
0.upto( 3 ) do |c|
	if tdiv == c
		select_html << "<option value='#{c}' SELECTED>#{tdiv_set[c]}</option>"
	else
		select_html << "<option value='#{c}'>#{tdiv_set[c]}</option>"
	end
end
select_html << "</select>&nbsp;&nbsp;&nbsp;&nbsp;"

select_html << "<select id='hh' class='custom-select custom-select-sm'>"
select_html << "<option value='99'>時刻</option>"
0.upto( 23 ) do |c|
	if c == hh
		select_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		select_html << "<option value='#{c}'>#{c}</option>"
	end
end
select_html << "</select>"


#### Rate HTML
rate_selected = ''
rate_selected = 'SELECTED' if /^[UP]?\d{5}/ =~ code
rate_html = ''
rate_html << "<div class='input-group input-group-sm'>"
rate_html << "	<div class='input-group-prepend'>"
rate_html << "		<span class='input-group-text' id='basic-addon1'>#{lp[22]}</span>"
rate_html << "	</div>"
rate_html << "	<input type='number' id='ev' value='#{ev}' class='form-control'>"
rate_html << "  <div class='input-group-append'>"
rate_html << "		<select id='eu' class='custom-select custom-select-sm'>"
rate_html << "			<option value='%'>%</option>"
rate_html << "			<option value='g' #{rate_selected}>g</option>"
rate_html << "		</select>"
rate_html << "	</div>"
rate_html << "</div>"


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-11'><h5>#{food_name}</h5></div>
		<div class='col-1'><button class='btn btn-success' type='button' onclick="koyomiReturn()">#{lp[11]}</button></div>
	</div>
	<div class='row'>
		<div class='col-5 form-inline'>
			#{select_html}
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
     		<th align='center'>#{lp[17]}</th>
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
add_his( uname, code ) if /^[UP]?\d{5}/ =~ code
