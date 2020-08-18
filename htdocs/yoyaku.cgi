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
  <script type="text/javascript" src="#{$JS_PATH}/shun.js"></script>
</head>

<body class="body">
  <span class="world_frame" id="world_frame">
HTML

	puts html
end


class Cals
	attr_accessor :yyyy, :mm, :dd, :available, :am, :pm

  def initialize( yyyy, mm, dd, available )
    @yyyy = yyyy
    @mm = mm
    @dd = dd
    @available = available
    @am = 2
    @pm = 2
  end
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


calendar_prev = Calendar.new( user.name, yyyy, mm, dd )
calendar_prev.move_mm( -1 )
calendar_prev.wf = 7 if calendar_prev.wf == 0


calendar_next = Calendar.new( user.name, yyyy, mm, dd )
calendar_next.move_mm( 1 )
calendar_next.wf = 7 if calendar_next.wf == 0


calendar.debug if @debug
calendar_prev.debug if @debug
calendar_next.debug if @debug
sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
sql_ym = "#{calendar.yyyy}-#{calendar.mm}"


calendar_set = []
a = []
mm_set = []
yyyy_set = []
1.upto( calendar.wf - 1 ) do |c|
	a << 0
	mm_set << calendar_prev.mm
	yyyy_set << calendar_prev.yyyy
	calendar_set << Cals.new( calendar_prev.yyyy, calendar_prev.mm, 0, false )
end
days = a.reverse
1.upto( calendar.ddl) do |c|
	days << c
	mm_set << calendar.mm
	yyyy_set << calendar.yyyy
	calendar_set << Cals.new( calendar.yyyy, calendar.mm, c, true )
end
1.upto( 7 - calendar.wl ) do |c|
	days << 0
	mm_set << calendar_next.mm
	yyyy_set << calendar_next.yyyy
	calendar_set << Cals.new( calendar_next.yyyy, calendar_next.mm, 0, false )
end

calendar_next_set = []
a = []
mm_next_set = []
yyyy_next_set = []
1.upto( calendar_next.wf - 1 ) do |c|
	a << 0
	mm_next_set << calendar.mm
	yyyy_next_set << calendar.yyyy
	calendar_next_set << Cals.new( calendar.yyyy, calendar.mm, 0, false )
end
days_next = a.reverse
1.upto( calendar_next.ddl ) do |c|
	days_next << c
	mm_next_set << calendar_next.mm
	yyyy_next_set << calendar_next.yyyy
	calendar_next_set << Cals.new( calendar_next.yyyy, calendar_next.mm, c, true )
end
1.upto( 7 - calendar_next.wl ) do |c|
	days_next << 0
	mm_next_set << calendar_next.mm
	yyyy_next_set << calendar_next.yyyy
	calendar_next_set << Cals.new( calendar_next.yyyy, calendar_next.mm, 0, false )
end


#### This month
week_count = 0
cal_html = ''
0.upto( days.size - 1 ) do |c|
	if week_count == 0
		cal_html << "<tr><td align='center' class='ampm'>　<br>AM<br>PM</td>"
	end
	if calendar_set[c].available
		if calendar_set[c].dd <= calendar.dd + 1 || calendar_set[c].dd > calendar.dd + 29
			cal_html << "<td class='day_off'>"
			cal_html << "<div>#{days[c]}</div>"
			cal_html << "<div align='center'>-</div>"
			cal_html << "<div align='center'>-</div>"
			cal_html << '</td>'
		else
			cal_html << "<td class='day_on'>"
			cal_html << "<div>#{days[c]}</div>"
			if calendar_set[c].am == 2
				cal_html << "<div align='center' class='btn-outline-dark' onclick=\"scsYoyakuNew( '#{calendar_set[c].yyyy}', '#{calendar_set[c].mm}', '#{calendar_set[c].dd}', 'am' )\"><buttton onclick=\"scsYoyakuNew( '#{calendar_set[c].yyyy}', '#{calendar_set[c].mm}', '#{calendar_set[c].dd}', 'am' )\">○</button></div>"
			elsif calendar_set[c].am == 1
				cal_html << "<div align='center' class='btn-outline-dark' onClick=''>△</div>"
			else
				cal_html << "<div align='center' class='btn-outline-dark'>×</div>"
			end

			if calendar_set[c].pm == 2
				cal_html << "<div align='center' onclick=\"scsYoyakuNew( '#{calendar_set[c].yyyy}', '#{calendar_set[c].mm}', '#{calendar_set[c].dd}', 'pm' )\">○</div>"
			elsif calendar_set[c].pm == 1
				cal_html << "<div align='center' class='btn-outline-dark'>△</div>"
			else
				cal_html << "<div align='center' class='btn-outline-dark'>×</div>"
			end
			cal_html << '</td>'
		end
	else
		cal_html << "<td class='day_out'>"
		cal_html << "<div></div>"
		cal_html << "<div align='center'></div>"
		cal_html << '</td>'
	end

	if week_count ==  6
		cal_html << '</tr>'
		week_count = 0
	else
		week_count += 1
	end
end


#### Next month
week_count = 0
cal_next_html = ''
dd_delta = calendar.ddl - calendar.dd
0.upto( days_next.size - 1 ) do |c|
	if week_count == 0
		cal_next_html << "<tr><td align='center' class='ampm'>　<br>AM<br>PM</td>"
	end
	if calendar_next_set[c].available
		if calendar_next_set[c].dd + dd_delta > 28
			cal_next_html << "<td class='day_off'>"
			cal_next_html << "<div></div>"
			cal_next_html << "<div align='center'>-</div>"
			cal_next_html << "<div align='center'>-</div>"
			cal_next_html << '</td>'
		else
			cal_next_html << "<td class='day_on'>"
			cal_next_html << "<div>#{days_next[c]}</div>"
			if calendar_next_set[c].am == 2
				cal_next_html << "<div align='center' >○</div>"
			elsif calendar_next_set[c].am == 1
				cal_next_html << "<div align='center'>△</div>"
			else
				cal_next_html << "<div align='center'>×</div>"
			end

			if calendar_next_set[c].pm == 2
				cal_next_html << "<div align='center'>○</div>"
			elsif calendar_next_set[c].pm == 1
				cal_next_html << "<div align='center'>△</div>"
			else
				cal_next_html << "<div align='center'>×</div>"
			end
			cal_next_html << '</td>'
		end
	else
		cal_next_html << "<td class='day_out'>"
		cal_next_html << "<div></div>"
		cal_next_html << "<div align='center'></div>"
		cal_next_html << "<div align='center'></div>"
		cal_next_html << '</td>'
	end
	if week_count ==  6
		cal_next_html << '</tr>'
		week_count = 0
	else
		week_count += 1
	end
end

html = <<-"HTML"
<h1 align="center" class='month'>嵯峨お料理教室予約フォーム</h1>
<div id='world_frame'>
<div align="center">
	[<span class='day_on_sample'>■</span>]…予約可期間
	[<span class='day_off_sample'>■</span>]…予約不可期間
</div>
<div align="center">
	○…2名予約可　
	△…1名予約可、料理選択不可　
	×…予約済み
</div>

<h2 align="center" class='month'>#{calendar.yyyy}年　#{calendar.mm}月</h2>
<table align='center' width='95%'>
  <tr>
    <td></td>
    <td width='13.5%' align='center' class='weekday'>月</td>
    <td width='13.5%' align='center' class='weekday'>火</td>
    <td width='13.5%' align='center' class='weekday'>水</td>
    <td width='13.5%' align='center' class='weekday'>木</td>
    <td width='13.5%' align='center' class='weekday'>金</td>
    <td width='13.5%' align='center' class='saturday'>土</td>
    <td width='13.5%' align='center' class='sunday'>日</td>
  <tr>
  #{cal_html}
</table>
<br>
<h2 align="center" class='month'>#{calendar_next.yyyy}年　#{calendar_next.mm}月</h2>
<table align='center' width='95%'>
  <tr>
    <td></td>
    <td width='13.5%' align='center' class='weekday'>月</td>
    <td width='13.5%' align='center' class='weekday'>火</td>
    <td width='13.5%' align='center' class='weekday'>水</td>
    <td width='13.5%' align='center' class='weekday'>木</td>
    <td width='13.5%' align='center' class='weekday'>金</td>
    <td width='13.5%' align='center' class='saturday'>土</td>
    <td width='13.5%' align='center' class='sunday'>日</td>
  <tr>
  #{cal_next_html}
</table>
HTML

puts html

html_foot
