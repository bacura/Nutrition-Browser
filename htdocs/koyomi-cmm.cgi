#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi menu copy / move 0.01b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'koyomi-cmm'
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

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )
start_year, st_set = get_starty( user.name )


#### Getting POST
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
yyyy_mm_dd = cgi['yyyy_mm_dd']
unless yyyy_mm_dd == ''
	a = yyyy_mm_dd.split( '-' )
	yyyy = a[0].to_i
	mm = a[1].to_i
	dd = a[2].to_i
end
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
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar.debug if @debug


#### Save food
if command == 'save'
	hh = st_set[tdiv] if hh == 99
	( yyyy_, mm_, dd_, tdiv_ ) = origin.split( ':' )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy_}-#{mm_}-#{dd_}' AND tdiv='#{tdiv_}';", false, @debug )
	if r.first
		koyomi_ = r.first['koyomi']
		t = ''
		a = koyomi_.split( "\t" )
		a.each do |e|
			aa = e.split( ':' )
			t << "#{aa[0]}:#{aa[1]}:#{aa[2]}:#{hh}\t"
		end
		koyomi_ = t.chop

		rr = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		if rr.first
			koyomi = rr.first['koyomi']
			if koyomi == ''
				koyomi << koyomi_
			else
				koyomi << "\t#{koyomi_}"
			end

			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', fzcode='', freeze='0', koyomi='#{koyomi_}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", false, @debug )
		end

		if cm_mode == 'move' && ( yyyy != yyyy_.to_i || mm != mm_.to_i || dd != dd_.to_i || tdiv != tdiv_.to_i )
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='' WHERE user='#{user.name}' AND date='#{yyyy_}-#{mm_}-#{dd_}' AND tdiv='#{tdiv_}';", false, @debug )
		end
		( yyyy, mm, dd, tdiv ) = yyyy_.to_i, mm_.to_i, dd_.to_i, tdiv_.to_i
	end
end


####
save_button = ''
if cm_mode == 'copy'
	save_button = "<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"cmmSaveKoyomi( '#{cm_mode}', '#{origin}' )\">#{lp[12]}</button>"
else
	save_button = "<button class='btn btn-sm btn-outline-primary' type='button' onclick=\"cmmSaveKoyomi( '#{cm_mode}', '#{origin}' )\">#{lp[8]}</button>"
end


#### Date HTML
date_html = ''
week_count = calendar.wf
weeks = [lp[1], lp[2], lp[3], lp[4], lp[5], lp[6], lp[7]]
1.upto( calendar.ddl ) do |c|
	date_html << "<tr>"
	if week_count == 0
		date_html << "<td style='color:red;'>#{c} (#{weeks[week_count]})</td>"
	else
		date_html << "<td>#{c} (#{weeks[week_count]})</td>"
	end

	r = mdb( "SELECT freeze FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{c}' AND freeze='1';", false, @debug )
	unless r.first
		0.upto( 3 ) do |cc|
			koyomi_c = '-'
			rr = mdb( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{c}' AND tdiv='#{cc}';", false, @debug )
			onclick = "onclick=\"cmmSaveKoyomi_direct( '#{cm_mode}', '#{yyyy}', '#{mm}', '#{c}', '#{cc}', '#{origin}' )\""
			if rr.first
				if rr.first['koyomi'] == ''
					date_html << "<td class='table-light' align='center' #{onclick}>#{koyomi_c}</td>"
				else
					koyomi_c = rr.first['koyomi'].split( "\t" ).size
					if dd == c and tdiv == cc
						date_html << "<td class='table-warning' align='center' #{onclick}>#{koyomi_c}</td>"
					else
						date_html << "<td class='table-info' align='center' #{onclick}>#{koyomi_c}</td>"
					end
				end
			else
				date_html << "<td class='table-light' align='center' #{onclick}>#{koyomi_c}</td>"
			end
		end
	else
		4.times do date_html << "<td class='table-secondary'></td>" end
	end

	date_html << "</tr>"
	week_count += 1
	week_count = 0 if week_count > 6
end


#### tdiv HTML
tdiv_html = ''
tdiv_set = [ lp[13], lp[14], lp[15], lp[16] ]
tdiv_html << "<select id='tdiv_cmm' class='form-select form-select-sm'>"
0.upto( 3 ) do |c|
	if tdiv == c
		tdiv_html << "<option value='#{c}' SELECTED>#{tdiv_set[c]}</option>"
	else
		tdiv_html << "<option value='#{c}'>#{tdiv_set[c]}</option>"
	end
end
tdiv_html << "</select>"


#### hour HTML
hour_html = ''
hour_html << "<select id='hh_cmm' class='form-select form-select-sm'>"
hour_html << "<option value='99'>時刻</option>"
0.upto( 23 ) do |c|
	if c == hh
		hour_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		hour_html << "<option value='#{c}'>#{c}</option>"
	end
end
hour_html << "</select>"


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-11'><h5>#{yyyy} / #{mm} / #{dd} (#{tdiv_set[tdiv]})</h5></div>
		<div class='col-1'><span onclick="koyomiReturn2KE( '#{yyyy}', '#{mm}', '#{dd}' )">#{lp[11]}</span></div>
	</div>
	<div class='row'>
		<div class='col-2 form-inline'>
			<input type='date' id='yyyy_mm_dd' min='#{calendar.yyyyf}-01-01' max='#{calendar.yyyy + 2}-12-31' value='#{calendar.yyyy}-#{calendar.mms}-#{calendar.dds}' onChange="cmmChangeKoyomi( '#{cm_mode}', '#{origin}' )">
		</div>
		<div class='col-2 form-inline'>
			#{tdiv_html}
		</div>
		<div class='col-2 form-inline'>
			#{hour_html}
		</div>
		<div class='col-1 form-inline'>
		</div>
		<div class='col-1 form-inline'>
			#{save_button}
		</div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
    	<tr>
     		<th align='center'></th>
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
