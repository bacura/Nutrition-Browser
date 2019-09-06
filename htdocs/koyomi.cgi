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
			r = mariadb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{aa[0]}';", false )
			mb_html << "<li>#{r.first['name']}</li>"
		elsif /\-f\-/ =~ aa[0]
			r = mariadb( "SELECT name FROM #{$MYSQL_TB_FCS} WHERE code='#{aa[0]}';", false )
			mb_html << "<li style='list-style-type: circle'>#{r.first['name']}</li>"
		elsif /\-/ =~ aa[0]
			r = mariadb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{aa[0]}';", false )
			mb_html << "<li>#{r.first['name']}</li>"
		else
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}';"
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}' AND user='#{uname}';" if /^U\d{5}/ =~ aa[0]
			r = mariadb( q, false )
			mb_html << "<li style='list-style-type: square'>#{r.first['name']}</li>"
		end
	end
	mb_html << '</ul>'

	return mb_html
end


####
def get_starty( uname )
	t = Time.new
	start_year = t.year
	r = mariadb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
	if r.first['koyomiy']
		a = r.first['koyomiy'].split( ':' )
		start_year = a[0].to_i if a[0].to_i != 0
	end

	return start_year
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )
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
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "<hr>\n"
end


#### General menu
if command == 'menu'
html = <<-"MENU"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="initKoyomi()">食事記録</button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="initKoyomiex_BW1( '', '' )">拡張記録</button></div>
		<div class='col-2'></div>
		<div class='col-2'></div>
		<div class='col-2'></div>
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
case command
when 'fix'
	mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fix='1' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
when 'fix_all'
	mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fix='1' WHERE user='#{uname}' AND ( date BETWEEN '#{yyyy}-#{mm}-1' AND '#{yyyy}-#{mm}-#{last_day}' );", false )
when 'cancel'
	mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fix='' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
when 'cancel_all'
	mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET fix='' WHERE user='#{uname}' AND ( date BETWEEN '#{yyyy}-#{mm}-1' AND '#{yyyy}-#{mm}-#{last_day}' );", false )
end


####
date_html = ''
week_count = first_week
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
1.upto( last_day ) do |c|
	date_html << "<tr>"
	if week_count == 0
		date_html << "<td style='color:red;'><span>#{c}</span> (#{weeks[week_count]})</td>"
	else
		date_html << "<td><span>#{c}</span> (#{weeks[week_count]})</td>"
	end

	fix_flag = false
	koyomi_tmp = []
	5.times do |cc|
		r = mariadb( "SELECT fix, koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{c}' AND tdiv='#{cc}';", false)
		if r.first
			koyomi_tmp << r.first['koyomi']
			fix_flag = true if r.first['fix'] != ''
		else
			koyomi_tmp << ''
		end
	end

	onclick = ''
	onclick = "onclick=\"editKoyomi_BW2( 'init', '#{c}' )\"" unless fix_flag
	4.times do |cc|
		if koyomi_tmp[cc] == ''
			date_html << "<td #{onclick}>-</td>"
		else
			meal_block = meals( koyomi_tmp[cc], uname )
			date_html << "<td #{onclick}>#{meal_block}</td>"
		end
	end

	if koyomi_tmp[4] == ''
		date_html << "<td>-</td>"
	else
		date_html << "<td>#{koyomi_tmp[4]}</td>"
	end

	if fix_flag
		date_html << "<td><button class='btn btn-sm btn-outline-warning' onclick=\"fixKoyomi_BW1( 'cancel', '#{c}' )\">#{lp[19]}</button></td>"
	else
		date_html << "<td><button class='btn btn-sm btn-outline-primary' onclick=\"fixKoyomi_BW1( 'fix', '#{c}' )\">#{lp[18]}</button></td>"
	end

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
		<div class='col-2'><h5>#{lp[8]}:</h5></div>
		<div class='col-5 form-inline'>
			#{select_html}
		</div>
		<div class='col-1'>
			<button class='btn btn-sm btn-outline-primary' onclick="fixKoyomi_BW1( 'fix_all', '#{dd}' )">#{lp[20]}</button>
		</div>
		<div class='col-2'>
			<button class='btn btn-sm btn-outline-warning' onclick="fixKoyomi_BW1( 'cancel_all', '#{dd}' )">#{lp[21]}</button>
		</div>
		<div class='col-2'>
			<button class='btn btn-success' onclick="initKoyomiex_BW1( '#{yyyy}', '#{mm}' )">#{lp[22]}</button>
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
     		<th align='center'>#{lp[17]}</th>
    	</tr>
  	</thead>
	#{date_html}
	</table>

HTML

puts html
