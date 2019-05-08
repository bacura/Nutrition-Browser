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
$SCRIPT = 'koyomi.cgi'
$DEBUG = true
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
lp = lp_init( 'koyomi', language )
if $DEBUG
	puts "uname:#{uname}<br>\n"
	puts "status:#{status}<br>\n"
	puts "aliaseu:#{aliaseu}<br>\n"
	puts "language:#{language}<br>\n"
	puts "<hr>\n"
end


#### GMチェック
if status < 1
	puts "Guild menber error."
	exit
end


#### POSTデータの取得
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
if $DEBUG
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "<hr>\n"
end


#### 日付の取得
date = Date.today
date = Date.new( yyyy, mm, dd ) unless yyyy == 0
date_first = Date.new( date.year, date.month, 1 )
first_week = date_first.wday
last_day = Date.new( date.year, date.month, -1 ).day
if $DEBUG
	puts "date:#{date.to_time}<br>\n"
	puts "first_week:#{first_week}<br>\n"
	puts "last_day:#{last_day}<br>\n"
end



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
	date_html << "<div class='col-2'></div>"
	date_html << "<div class='col-2'></div>"
	date_html << "<div class='col-2'></div>"
	date_html << "<div class='col-2'></div>"
	date_html << "<div class='col-2'></div>"
	date_html << "<div class='col-1'></div>"
	date_html << "</div>"
	week_count += 1
	week_count = 0 if week_count > 6
end


select_html = ''
select_html << "<select id='year'>"
start_year.upto( 2020 ) do |c| select_html << "<option value='#{c}'>#{c}</option>" end
select_html << "</select>"
select_html << "<select id='month'>"
1.upto( 12 ) do |c| select_html << "<option value='#{c}'>#{c}</option>" end
select_html << "</select>"




html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[8]}: </h5></div>
		<div class='col'>
			#{lp[8]}: #{date.year}#{lp[9]} #{date.month}#{lp[10]}
		</div>
	</div>
	<div class='row'>
		<div class='col'></div>
	</div>
	<div class='row'>
	<div class='col-1'>日</div>
	<div class='col-2'>朝食</div>
	<div class='col-2'>昼食</div>
	<div class='col-2'>夕食</div>
	<div class='col-3'>間食</div>
	<div class='col-2'>操作</div>
	</div>
	<hr>
	#{date_html}
HTML

puts html
