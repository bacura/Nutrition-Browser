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
$SCRIPT = 'koyomia.cgi'
$DEBUG = false
start_year = 2019

#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomi-add', language )
if $DEBUG
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
			breakfast << "#{delimiter}#{code}:#{ev}:#{eu}:#{hh}"
		when 1
			delimiter = "\t" if lunch != ''
			lunch << "#{delimiter}#{code}:#{ev}:#{eu}:#{hh}"
		when 2
			delimiter = "\t" if dinner != ''
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
			breakfast = "#{code}:#{ev}:#{eu}:#{hh}"
		when 1
			lunch = "#{code}:#{ev}:#{eu}:#{hh}"
		when 2
			dinner = "#{code}:#{ev}:#{eu}:#{hh}"
		when 3
			supple = "#{code}:#{ev}:#{eu}:#{hh}"
		end
		mariadb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{uname}', fix='', breakfast='#{breakfast}', lunch='#{lunch}', dinner='#{dinner}', supple='#{supple}', memo='', date='#{yyyy}-#{mm}-#{dd}';", false)
	end
end


####
date_html = ''
week_count = first_week
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
1.upto( last_day ) do |c|
	date_html << "<div class='row'>"
	if week_count == 0
		date_html << "<div class='col-1' style='color:red;'><span>#{c}</span> (#{weeks[week_count]})</div>"
	else
		date_html << "<div class='col-1'><span>#{c}<span> (#{weeks[week_count]})</div>"
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
			date_html << "<div class='col-1'><span class='badge badge-secondary'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
			date_html << "<div class='col-1'><span class='badge badge-secondary'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
			date_html << "<div class='col-1'><span class='badge badge-secondary'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
			date_html << "<div class='col-1'><span class='badge badge-secondary'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
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
			date_html << "<div class='col-1'><span class='btn-#{breakfast_color} badge badge-#{breakfast_color}' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '0' )\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#{breakfast_c}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
			date_html << "<div class='col-1'><span class='btn-#{lunch_color} badge badge-#{lunch_color}' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '1' )\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#{lunch_c}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
			date_html << "<div class='col-1'><span class='btn-#{dinner_color} badge badge-#{dinner_color}' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '2' )\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#{dinner_c}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
			date_html << "<div class='col-1'><span class='btn-#{supple_color} badge badge-#{supple_color}' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '3' )\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#{supple_c}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
		end
	else
		date_html << "<div class='col-1'><span class='btn-#{breakfast_color} badge badge-#{breakfast_color}' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '0' )\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#{breakfast_c}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
		date_html << "<div class='col-1'><span class='btn-#{lunch_color} badge badge-#{lunch_color}' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '1' )\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#{lunch_c}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
		date_html << "<div class='col-1'><span class='btn-#{dinner_color} badge badge-#{dinner_color}' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '2' )\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#{dinner_c}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
		date_html << "<div class='col-1'><span class='btn-#{supple_color} badge badge-#{supple_color}' onclick=\"saveKoyomi2_BWF( '#{code}','#{yyyy}','#{mm}', '#{c}', '3' )\">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#{supple_c}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span></div>"
	end
	date_html << "</div>"
	week_count += 1
	week_count = 0 if week_count > 6
end


####
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


####
rate_html = ''
rate_html << "<div class='input-group input-group-sm'>"
rate_html << "	<div class='input-group-prepend'>"
rate_html << "		<span class='input-group-text' id='basic-addon1'>#{lp[22]}</span>"
rate_html << "	</div>"
rate_html << "	<input type='number' id='ev' value='100' class='form-control'>"
rate_html << "  <div class='input-group-append'>"
rate_html << "		<select id='eu' class='custom-select custom-select-sm'>"
rate_html << "			<option value='%'>%</option>"
rate_html << "			<option value='g'>g</option>"
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
	<div class='row'>
	<div class='col-1'>#{lp[17]}</div>
	<div class='col-1'>#{lp[18]}</div>
	<div class='col-1'>#{lp[19]}</div>
	<div class='col-1'>#{lp[20]}</div>
	<div class='col-1'>#{lp[21]}</div>
	</div>
	<hr>
	#{date_html}
HTML

puts html
