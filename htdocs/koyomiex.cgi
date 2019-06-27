#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi ex 0.00

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
$SCRIPT = 'koyomiex.cgi'
$DEBUG = false
start_year = 2019

#==============================================================================
#DEFINITION
#==============================================================================
def meals( meal )
	mb_html = '<ul>'
	a = meal.split( "\t" )
	a.each do |e|
		aa = e.split( ':' )
		if /\-m\-/ =~ aa[0]
			r = mariadb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{aa[0]}';", false )
			mb_html << "<li>#{r.first['name']}</li>"
		elsif /\-f\-/ =~ aa[0]
			r = mariadb( "SELECT name FROM #{$MYSQL_TB_FCS} WHERE code='#{aa[0]}';", false )
			mb_html << "<li>#{r.first['name']}</li>"
		elsif /\-/ =~ aa[0]
			r = mariadb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{aa[0]}';", false )
			mb_html << "<li>#{r.first['name']}</li>"
		elsif /\?/ =~ aa[0]
			mb_html << "<li>?</li>"
		else
			r = mariadb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}';", false )
			mb_html << "<li>#{r.first['name']}</li>"
		end
	end
	mb_html << '</ul>'

	return mb_html
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomiex', language )
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
dd = 1 if dd == 0
item_no = cgi['item_no'].to_i
cell = cgi['cell']
if $DEBUG
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "item_no:#{item_no}<br>\n"
	puts "cell:#{cell}<br>\n"
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


#### loading config
r = mariadb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
item_set = r.first['koyomiex'].split( ':' ) if r.first['koyomiex']
item_set_no = []
0.upto( 9 ) do |c|
	item_set_no << c unless item_set[c] == "" || item_set[c] == nil || item_set[c] == "\t"
end


#### Updating cell
if command == 'update'
	r = mariadb( "SELECT user FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
	if r.first
		mariadb( "UPDATE #{$MYSQL_TB_KOYOMIEX} SET item#{item_no}='#{cell}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
	else
		mariadb( "INSERT INTO #{$MYSQL_TB_KOYOMIEX} SET item#{item_no}='#{cell}', user='#{uname}', date='#{yyyy}-#{mm}-#{dd}';", false )
	end
end




####
th_html = '<thead><tr>'
th_html << "<th align='center'>日付</th>"
item_set_no.each do |e|
	th_html << "<th align='center'>#{item_set[e]}</th>"
end
th_html << '</tr></thead>'





####
date_html = ''
week_count = first_week
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{uname}' AND ( date BETWEEN '#{yyyy}-#{mm}-1' AND '#{yyyy}-#{mm}-#{last_day}' );", false)
koyomir = []
cells = []
r.each do |e| koyomir[e['date'].day] = e end





1.upto( last_day ) do |c|
	date_html << "<tr>"
	if week_count == 0
		date_html << "<td style='color:red;'><span>#{c}</span> (#{weeks[week_count]})</td>"
	else
		date_html << "<td><span>#{c}</span> (#{weeks[week_count]})</td>"
	end

	if koyomir[c] == nil
		item_set_no.each do |e|
			date_html << "<td><input type='text' id='id#{c}_#{e}' value='' onChange=\"updateKoyomiex( '#{c}', '#{e}', 'id#{c}_#{e}' )\"></td>"
		end
	else
		item_set_no.each do |e|
			t = koyomir[c]["item#{e}"]
			date_html << "<td><input type='text' id='id#{c}_#{e}' value='#{t}' onChange=\"updateKoyomiex( '#{c}', '#{e}', 'id#{c}_#{e}' )\"></td>"
		end
	end
	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


####
select_html = ''
select_html << "<div class='input-group input-group-sm'>"
select_html << "<select id='yyyy' class='custom-select' onChange=\"changeKoyomiex_BW1()\">"
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
select_html << "<select id='mm' class='custom-select custom-select-sm' onChange=\"changeKoyomiex_BW1()\">"
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
		<div class='col-2'><h5>#{lp[8]}</h5></div>
		<div class='col-8 form-inline'>
			#{select_html}
		</div>
		<div class='col-2'>
			<button class='btn btn-success' onclick="returnKoyomi_BW1( '#{yyyy}', '#{mm}' )">#{lp[12]}</button>
		</div>
	</div>
	<div class='row'>
		<div class='col'></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	#{th_html}
	#{date_html}
	</table>

HTML

puts html
