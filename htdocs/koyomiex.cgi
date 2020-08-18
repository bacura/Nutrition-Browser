#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi ex 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20200611, 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomiex'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

####
def meals( meal )
	mb_html = '<ul>'
	a = meal.split( "\t" )
	a.each do |e|
		aa = e.split( ':' )
		if /\-m\-/ =~ aa[0]
			r = mdb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{aa[0]}';", false, @debug )
			mb_html << "<li>#{r.first['name']}</li>"
		elsif /\-f\-/ =~ aa[0]
			r = mdb( "SELECT name FROM #{$MYSQL_TB_FCS} WHERE code='#{aa[0]}';", false, @debug )
			mb_html << "<li>#{r.first['name']}</li>"
		elsif /\-/ =~ aa[0]
			r = mdb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{aa[0]}';", false, @debug )
			mb_html << "<li>#{r.first['name']}</li>"
		elsif /\?/ =~ aa[0]
			mb_html << "<li>?</li>"
		else
			r = mdb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}';", false, @debug )
			mb_html << "<li>#{r.first['name']}</li>"
		end
	end
	mb_html << '</ul>'

	return mb_html
end


#### Getting start year
def get_starty( uname )
	start_year = $TIME_NOW.year
	r = mdb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, @debug )
	if r.first['koyomiy']
		a = r.first['koyomiy'].split( ':' )
		start_year = a[0].to_i if a[0].to_i != 0
	end

	return start_year
end

#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )

#### Guild member check
if user.status < 3
	puts "Guild member error."
	exit
end


#### Getting POST data
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
dd = 1 if dd == 0
item_no = cgi['item_no'].to_i
cell = cgi['cell']
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "item_no:#{item_no}<br>\n"
	puts "cell:#{cell}<br>\n"
	puts "<hr>\n"
end


#### Getting date
date = Date.today
date = Date.new( yyyy, mm, dd ) unless yyyy == 0
if yyyy == 0
 	yyyy = date.year
	mm = date.month
	dd = date.day
end
if @debug
	puts "date:#{date.to_time}<br>\n"
end


#### Date & calendar config
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar_nm = Calendar.new( user.name, yyyy, mm, dd )
calendar_nm.move_mm( 1 )
calendar_pm = Calendar.new( user.name, yyyy, mm, dd )
calendar_pm.move_mm( -1 )
calendar_td = Calendar.new( user.name, 0, 0, 0 )
calendar.debug if @debug
sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
sql_ym = "#{calendar.yyyy}-#{calendar.mm}"


#### Loading config
kex_select_set = []
item_set = []
unit_set = []
r = mdb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	a = r.first['koyomiex'].split( ':' )
	0.upto( 9 ) do |c|
		aa = a[c].split( "\t" )
		if aa[0] == "0"
		elsif aa[0] == "1"
			kex_select_set << aa[0].to_i
			item_set << aa[1]
			unit_set << aa[2]
		else
			kex_select_set << aa[0].to_i
			item_set << $KEX_ITEM[aa[0].to_i]
			unit_set << $KEX_UNIT[aa[0].to_i]
		end
	end
end


#### Updating cell
if command == 'update'
	r = mdb( "SELECT user FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_KOYOMIEX} SET item#{item_no}='#{cell}' WHERE user='#{user.name}' AND date='#{sql_ymd}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMIEX} SET item#{item_no}='#{cell}', user='#{user.name}', date='#{sql_ymd}';", false, @debug )
	end
end


####
th_html = '<thead><tr>'
th_html << "<th align='center'>日付</th>"
kex_select_set.size.times do |c|
	th_html << "<th align='center'>#{item_set[c]} (#{unit_set[c]})</th>"
end
th_html << '</tr></thead>'


####
date_html = ''
week_count = calendar.wf
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND ( date BETWEEN '#{sql_ym}-1' AND '#{sql_ym}-#{calendar.ddl}' );", false, @debug )
koyomir = []
r.each do |e| koyomir[e['date'].day] = e end

1.upto( calendar.ddl ) do |c|
	date_html << "<tr id='day#{c}'>"
	if week_count == 0
		date_html << "<td style='color:red;'><span>#{c}</span> (#{weeks[week_count]})</td>"
	else
		date_html << "<td><span>#{c}</span> (#{weeks[week_count]})</td>"
	end

	if koyomir[c] == nil
		kex_select_set.each do |e|
			date_html << "<td><input type='text' id='id#{c}_#{e}' value='' onChange=\"updateKoyomiex( '#{c}', '#{e}', 'id#{c}_#{e}' )\"></td>"
		end
	else
		kex_select_set.each do |e|
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
calendar.yyyyf.upto( calendar_td.yyyy + 1 + 1 ) do |c|
	if c == calendar.yyyy
		select_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		select_html << "<option value='#{c}'>#{c}</option>"
	end
end
select_html << "</select>"
select_html << "<div class='input-group-append'><label class='input-group-text'>#{lp[9]}</label></div>"
select_html << "</div>"

select_html << "<div class='input-group input-group-sm'>"
select_html << "<select id='mm' class='custom-select custom-select-sm' onChange=\"initKoyomiex( '', '' )\">"
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
		<div class='col-2'>
			<h5>#{lp[8]}</h5>
		</div>
		<div class='col-3 form-inline'>
			#{select_html}
		</div>
		<div class='col-2'>
			<a href='#day#{date.day}'><button class='btn btn-sm btn-outline-primary'>#{lp[14]}</button></a>&nbsp;
			<button class='btn btn-sm btn-outline-primary' onclick="initKoyomiex( '#{calendar_pm.yyyy}', '#{calendar_pm.mm}' )">#{lp[15]}</button>
			<button class='btn btn-sm btn-outline-primary' onclick="initKoyomiex( '#{calendar_td.yyyy}', '#{calendar_td.mm}' )">#{lp[13]}</button>
			<button class='btn btn-sm btn-outline-primary' onclick="initKoyomiex( '#{calendar_nm.yyyy}', '#{calendar_nm.mm}' )">#{lp[16]}</button>
		</div>
		<div class='col-3'>
		</div>
		<div class='col-2'>
			<button class='btn btn-sm btn-success' onclick="changeKoyomi( '#{calendar.yyyy}', '#{calendar.mm}' )">#{lp[12]}</button>
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
