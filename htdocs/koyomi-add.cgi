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
$SCRIPT = 'koyomi-add.cgi'
$DEBUG = true

#==============================================================================
#DEFINITION
#==============================================================================

#
def get_starty( uname )
	t = Time.new
	start_year = t.year
	breakfast_st = 0
	lunch_st = 0
	dinner_st = 0
	r = mariadb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
	if r.first
		a = r.first['koyomiy'].split( ':' )
		start_year = a[0].to_i if a[0].to_i != 0
		breakfast_st = a[1].to_i if a[1].to_i != 0
		lunch_st = a[2].to_i if a[2].to_i != 0
		dinner_st = a[3].to_i if a[3].to_i != 0
	end
	return start_year, breakfast_st, lunch_st, dinner_st
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomi-add', language )
start_year, breakfast_st, lunch_st, dinner_st = get_starty( uname )
if $DEBUG
	puts "uname:#{uname}<br>\n"
	puts "status:#{status}<br>\n"
	puts "aliaseu:#{aliaseu}<br>\n"
	puts "language:#{language}<br>\n"
	puts "<hr>\n"
	puts "start_year:#{start_year}<br>\n"
	puts "breakfast_st:#{breakfast_st}<br>\n"
	puts "lunch_st:#{lunch_st}<br>\n"
	puts "dinner_st:#{dinner_st}<br>\n"
	puts "<hr>\n"
end


#### POSTデータの取得
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
code = cgi['code']
ev = cgi['ev'].to_i
eu = cgi['eu'].to_s
tdiv = cgi['tdiv'].to_i
hh = cgi['hh'].to_i
dd = 1 if dd == 0
if $DEBUG
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "hh:#{hh}<br>\n"
	puts "tdiv:#{tdiv}<br>\n"
	puts "ev:#{ev}<br>\n"
	puts "eu:#{eu}<br>\n"
	puts "<hr>\n"
end


#### 日付の取得
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
if $DEBUG
	puts "date:#{date.to_time}<br>\n"
	puts "first_week:#{first_week}<br>\n"
	puts "last_day:#{last_day}<br>\n"
end


#### Save food
if command == 'save'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false)
	if r.first
		breakfast = r.first['breakfast']
		lunch = r.first['lunch']
		dinner = r.first['dinner']
		supple = r.first['supple']
		delimiter = ''
		case tdiv
		when 0
			delimiter = "\t" if breakfast != ''
			hh = breakfast_st if hh == 99
			breakfast << "#{delimiter}#{code}:#{ev}:#{eu}:#{hh}"
		when 1
			delimiter = "\t" if lunch != ''
			hh = lunch_st if hh == 99
			lunch << "#{delimiter}#{code}:#{ev}:#{eu}:#{hh}"
		when 2
			delimiter = "\t" if dinner != ''
			hh = dinner_st if hh == 99
			dinner << "#{delimiter}#{code}:#{ev}:#{eu}:#{hh}"
		when 3
			delimiter = "\t" if supple != ''
			supple << "#{delimiter}#{code}:#{ev}:#{eu}:#{hh}"
		end
		mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET breakfast='#{breakfast}', lunch='#{lunch}', dinner='#{dinner}', supple='#{supple}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false)
	else
		breakfast = ""
		lunch = ""
		dinner = ""
		supple = ""
		case tdiv
		when 0
			hh = breakfast_st if hh == 99
			breakfast = "#{code}:#{ev}:#{eu}:#{hh}"
		when 1
			hh = lunch_st if hh == 99
			lunch = "#{code}:#{ev}:#{eu}:#{hh}"
		when 2
			hh = dinner_st if hh == 99
			dinner = "#{code}:#{ev}:#{eu}:#{hh}"
		when 3
			supple = "#{code}:#{ev}:#{eu}:#{hh}"
		end
		mariadb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{uname}', fix='', breakfast='#{breakfast}', lunch='#{lunch}', dinner='#{dinner}', supple='#{supple}', memo='', date='#{yyyy}-#{mm}-#{dd}';", false)
	end
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
	breakfast_color = 'light'
	lunch_color = 'light'
	dinner_color = 'light'
	supple_color = 'light'
	breakfast_c = '-'
	lunch_c = '-'
	dinner_c = '-'
	supple_c = '-'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{c}';", false)
	if r.first
		if r.first['fix'] != ''
			4.times do date_html << "<td class='btn-secondary'></td>" end
		else
			if r.first['breakfast'] != ''
				breakfast_color = 'info'
				breakfast_c = r.first['breakfast'].split( "\t" ).size
			end
			if r.first['lunch'] != ''
				lunch_color = 'info'
				lunch_c = r.first['lunch'].split( "\t" ).size
			end
			if r.first['dinner'] != ''
				dinner_color = 'info'
				dinner_c = r.first['dinner'].split( "\t" ).size
			end
			if r.first['supple'] != ''
				supple_color = 'info'
				supple_c = r.first['supple'].split( "\t" ).size
			end
			date_html << "<td class='btn-#{breakfast_color}' align='center' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '0' )\">#{breakfast_c}</td>"
			date_html << "<td class='btn-#{lunch_color}' align='center' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '1' )\">#{lunch_c}</td>"
			date_html << "<td class='btn-#{dinner_color}' align='center' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '2' )\">#{dinner_c}</td>"
			date_html << "<td class='btn-#{supple_color}' align='center' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '3' )\">#{supple_c}</td>"
		end
	else
		date_html << "<td class='btn-#{breakfast_color}' align='center' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '0' )\">#{breakfast_c}</td>"
		date_html << "<td class='btn-#{lunch_color}' align='center' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '1' )\">#{lunch_c}</td>"
		date_html << "<td class='btn-#{dinner_color}' align='center' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '2' )\">#{dinner_c}</td>"
		date_html << "<td class='btn-#{supple_color}' align='center' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '3' )\">#{supple_c}</td>"
	end
	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


#### Select HTML
select_html = ''
select_html << "<select id='yyyy' class='custom-select custom-select-sm' onChange=\"changeKoyomi_BWF( '#{code}' )\">"
start_year.upto( 2020 ) do |c|
	if c == yyyy
		select_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		select_html << "<option value='#{c}'>#{c}</option>"
	end
end
select_html << "</select>&nbsp;/&nbsp;"

select_html << "<select id='mm' class='custom-select custom-select-sm' onChange=\"changeKoyomi_BWF( '#{code}' )\">"
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

select_html << "<select id='tdiv' class='custom-select custom-select-sm'>"
select_html << "<option value='0'>#{lp[13]}</option>"
select_html << "<option value='1'>#{lp[14]}</option>"
select_html << "<option value='2'>#{lp[15]}</option>"
select_html << "<option value='3'>#{lp[16]}</option>"
select_html << "</select>&nbsp;&nbsp;&nbsp;&nbsp;"

select_html << "<select id='hh' class='custom-select custom-select-sm'>"
select_html << "<option value='99'>時刻</option>"
0.upto( 23 ) do |c| select_html << "<option value='#{c}'>#{c}</option>" end
select_html << "</select>"


#### Rate HTML
rate_selected = ''
rate_selected = 'SELECTED' if /^[UP]?\d{5}/ =~ code
rate_html = ''
rate_html << "<div class='input-group input-group-sm'>"
rate_html << "	<div class='input-group-prepend'>"
rate_html << "		<span class='input-group-text' id='basic-addon1'>#{lp[22]}</span>"
rate_html << "	</div>"
rate_html << "	<input type='number' id='ev' value='100' class='form-control'>"
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
		<div class='col-11'><h5>#{lp[8]}: #{date.year}#{lp[9]} #{date.month}#{lp[10]}</h5></div>
		<div class='col-1'><button class='btn btn-success' type='button' onclick="koyomiReturn()">#{lp[11]}</button></div>
	</div>
	<div class='row'>
		<div class='col-5 form-inline'>
			#{select_html}
		</div>
		<div class='col-3 form-inline'>
			#{rate_html}
		</div>
		<div class='col-2 form-inline'>
			<button class='btn btn-sm btn-outline-primary' type='button' onclick="saveKoyomi_BWF( '#{code}' )">#{lp[12]}</button>
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
