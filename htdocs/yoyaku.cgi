#! /usr/bin/ruby
# coding: UTF-8
#Nutrition browser cooking school yoyaku 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20200520, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = true
script = 'yoyaku'

#==============================================================================
#DEFINITION
#==============================================================================

def html_header()
p 'vv'
	html = <<-"HTML"
<!DOCTYPE html>
<head>
  <title>嵯峨お料理教室予約フォーム</title>
  <meta charset="UTF-8">
  <meta name="keywords" content="嵯峨お料理教室">
  <meta name="description" content="食品成分表の検索,栄養計算,栄養評価, analysis, calculation">
  <meta name="robots" content="index,follow">
  <meta name="author" content="Shinji Yoshiyama">
  <!-- bootstrap -->
  <link rel="stylesheet" href="bootstrap-dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="#{$CSS_PATH}/core.css">

<!-- Jquery -->
  <script type="text/javascript" src="./jquery-3.2.1.min.js"></script>
<!-- bootstrap -->
  <script type="text/javascript" src="bootstrap-dist/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="#{$JS_PATH}/core.js"></script>
</head>

<body class="body">
  <span class="world_frame" id="world_frame">
HTML

	puts html
end



#==============================================================================
# Main
#==============================================================================
#### Getting Cookie
cgi = CGI.new

user = User.new( cgi )

#lp = lp_init( 'yoyaku', language )

html_init( nil )
html_header()



#### Getting POST
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


#### Date & calendar config
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar.wf = 7 if calendar.wf == 0

yyyy_prev = calendar.yyyy + 1
mm_prev = calendar.mm - 1
if mm_prev == 0
	mm_prev = 12
	yyyy_prev -= 1
end
calendar_prev = Calendar.new( user.name, yyyy_prev, mm_prev, dd )
calendar_prev.wf = 7 if calendar_prev.wf == 0

yyyy_next = calendar.yyyy - 1
mm_next = calendar.mm + 1
if mm_next == 13
	mm_next = 1
	yyyy_next += 1
end
calendar_next = Calendar.new( user.name, yyyy_next, mm_next, dd )
calendar_next.wf = 7 if calendar_next.wf == 0

calendar.debug if @debug
calendar_prev.debug if @debug
calendar_next.debug if @debug
sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
sql_ym = "#{calendar.yyyy}-#{calendar.mm}"

a = []
mm_set = []
yyyy_set = []
1.upto( calendar.wf - 2 ) do |c|
	a << calendar_prev.ddl - c
	mm_set << calendar_prev.mm
	yyyy_set << calendar_prev.yyyy
end
days = a.reverse
1.upto( calendar.ddl) do |c|
	days << c
	mm_set << calendar.mm
	yyyy_set << calendar.yyyy
end
1.upto( 7 - calendar_next.wf ) do |c|
	days << c
	mm_set << calendar_next.mm
	yyyy_set << calendar_next.yyyy
end

week_count = 0
cal_html = ''
0.upto( days.size - 1 ) do |c|
	if week_count == 0
		cal_html << "<tr><td align='center'>　<br>AM<br>PM</td>"
	end
	cal_html << '<td>'
	cal_html << "<div>#{days[c]}</div>"
	cal_html << "<div align='center'>◎</div>"
	cal_html << "<div align='center'>○</div>"

	cal_html << '</td>'

	if week_count ==  6
		cal_html << '</tr>'
		week_count = 0
	else
		week_count += 1
	end
end


html = <<-"HTML"
<h3>5月</h3>
<table align='center' border='5' width='95%'>
  <tr>
    <td></td>
    <td width='13.5%' align='center'>月</td>
    <td width='13.5%' align='center'>火</td>
    <td width='13.5%' align='center'>水</td>
    <td width='13.5%' align='center'>木</td>
    <td width='13.5%' align='center'>金</td>
    <td width='13.5%' align='center'>土</td>
    <td width='13.5%' align='center'>日</td>
  <tr>
  #{cal_html}
</table>
HTML

puts html


html_foot
