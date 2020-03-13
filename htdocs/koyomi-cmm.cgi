#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi menu copy / move 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20200117, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
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
	r = mdb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, false )
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
cgi = CGI.new

uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomi-cmm', language )
start_year, st_set = get_starty( uname )

html_init( nil )
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
tdiv = cgi['tdiv'].to_i
hh = cgi['hh'].to_i
cm_mode = cgi['cm_mode']
origin = cgi['origin']
origin = "#{yyyy}:#{mm}:#{dd}:#{tdiv}" if origin == ''
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "tdiv:#{tdiv}<br>\n"
	puts "hh:#{hh}<br>\n"
	puts "cm_mode:#{cm_mode}<br>\n"
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


#### Save food
if command == 'save'
	hh = st_set[tdiv] if hh == 99
	( yyyy_, mm_, dd_, tdiv_ ) = origin.split( ':' )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy_}-#{mm_}-#{dd_}' AND tdiv='#{tdiv_}';", false, @debug )
	if r.first
		koyomi_ = r.first['koyomi']
		t = ''
		a = koyomi_.split( "\t" )
		a.each do |e|
			aa = e.split( ':' )
			t << "#{aa[0]}:#{aa[1]}:#{aa[2]}:#{hh}\t"
		end
		koyomi_ = t.chop

		rr = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		if rr.first
			koyomi = rr.first['koyomi']
			if koyomi == ''
				koyomi << koyomi_
			else
				koyomi << "\t#{koyomi_}"
			end

			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{uname}', fzcode='', freeze='0', koyomi='#{koyomi_}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", false, @debug )
		end

		if cm_mode == 'move' && ( yyyy != yyyy_.to_i || mm != mm_.to_i || dd != dd_.to_i || tdiv != tdiv_.to_i )
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='' WHERE user='#{uname}' AND date='#{yyyy_}-#{mm_}-#{dd_}' AND tdiv='#{tdiv_}';", false, @debug )
		end
		( yyyy, mm, dd, tdiv ) = yyyy_.to_i, mm_.to_i, dd_.to_i, tdiv_.to_i
	end
end


####
save_button = ''
if command == 'copy'
	save_button = "<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"cmmSaveKoyomi2( '#{cm_mode}', '#{origin}' )\">#{lp[12]}</button>"
else
	save_button = "<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"cmmSaveKoyomi2( '#{cm_mode}', '#{origin}' )\">#{lp[8]}</button>"
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

	r = mariadb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{c}' AND freeze='1';", false )
	unless r.first
		0.upto( 3 ) do |cc|
			koyomi_c = '-'
			rr = mdb( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{c}' AND tdiv='#{cc}';", false, @debug )
			onclick = "onclick=\"cmmSaveKoyomi( '#{cm_mode}', '#{yyyy}', '#{mm}', '#{c}', '#{cc}', '#{origin}' )\""
			if rr.first
				if rr.first['koyomi'] == ''
					date_html << "<td class='btn-light' align='center' #{onclick}>#{koyomi_c}</td>"
				else
					koyomi_c = rr.first['koyomi'].split( "\t" ).size
					if dd == c and tdiv == cc
						date_html << "<td class='btn-warning' align='center' #{onclick}>#{koyomi_c}</td>"
					else
						date_html << "<td class='btn-info' align='center' #{onclick}>#{koyomi_c}</td>"
					end
				end
			else
				date_html << "<td class='btn-light' align='center' #{onclick}>#{koyomi_c}</td>"
			end
		end
	else
		4.times do date_html << "<td class='btn-secondary'></td>" end
	end

	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


#### Select HTML
select_html = ''
onchange = "onChange=\"\""


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
select_html << "</select>&nbsp;&nbsp;&nbsp;"

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


#### Return button
return_button = "<button class='btn btn-sm btn-success' type='button' onclick=\"koyomiReturn()\">#{lp[11]}</button>"
if command == 'save' || cm_mode == 'move'
	return_button = "<button class='btn btn-sm btn-success' type='button' onclick=\"koyomiReturn2KE( '#{yyyy}', '#{mm}', '#{dd}' )\">#{lp[11]}</button>"
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-11'><h5>#{yyyy} / #{mm} / #{dd} (#{tdiv_set[tdiv]})</h5></div>
		<div class='col-1'>#{return_button}</div>
	</div>
	<div class='row'>
		<div class='col-5 form-inline'>
			#{select_html}
		</div>
		<div class='col-3 form-inline'>

		</div>
		<div class='col-1 form-inline'>
			#{save_button}
		</div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
    	<tr>
     		<th align='center'>#{lp[17]}</th>
     		<th align='center'>#{lp[13]}</th>
     		<th align='center'>#{lp[14]}</th>
     		<th align='center'>#{lp[15]}</th>
     		<th align='center'>#{lp[16]}</th>
    	</tr>
  	</thead>
	#{date_html}
	</table>
HTML
puts html
