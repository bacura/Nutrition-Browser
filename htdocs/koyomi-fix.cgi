#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi fix editer 0.00b

#==============================================================================
# CHANGE LOG
#==============================================================================
#20200611, 0.00b


#==============================================================================
# LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
# STATIC
#==============================================================================
script = 'koyomi-fix'
@debug = false


#==============================================================================
# DEFINITION
#==============================================================================

# Getting start year & standard meal time
def get_starty( uname )
	start_year = $TIME_NOW.year
	breakfast_st = 0
	lunch_st = 0
	dinner_st = 0
	r = mdb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, @debug )
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
fix_opt = Hash.new


#### POSTデータの取得
command = cgi['command']
yyyy = cgi['yyyy']
mm = cgi['mm']
dd = cgi['dd']
tdiv = cgi['tdiv'].to_i
hh = cgi['hh'].to_i
hh = 99 if command == 'init'
order = cgi['order'].to_i
palette = cgi['palette'].to_i
modifyf = cgi['modifyf'].to_i
food_name = cgi['food_name']
food_number = cgi['food_number'].to_i
food_number = 1 if food_number == 0
food_weight = cgi['food_weight']
food_weight = 100 if food_weight == nil || food_weight == ''|| food_weight == '0'
food_weight = BigDecimal( food_weight )
if @debug
	puts "command: #{command}<br>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "food_weight: #{food_weight}<br>\n"
	puts "food_number: #{food_number}<br>\n"
	puts "yyyy: #{yyyy}<br>\n"
	puts "mm: #{mm}<br>\n"
	puts "dd: #{dd}<br>\n"
	puts "tdiv: #{tdiv}<br>\n"
	puts "hh: #{hh}<br>\n"
	puts "order: #{order}<br>\n"
	puts "palette: #{palette}<br>\n"
	puts "modifyf: #{modifyf}<br>\n"
	puts "<hr>\n"
end


#### 成分読み込み
if command == 'init'
	4.upto( 67 ) do |i| fix_opt[$FCT_ITEM[i]] = 0.0 end
end

code = nil
#### Updating fcs & koyomi
if command == 'save'
	5.upto( 65 ) do |i|
		if cgi[$FCT_ITEM[i]] == '' || cgi[$FCT_ITEM[i]] == nil || cgi[$FCT_ITEM[i]] == '-'
			fix_opt[$FCT_ITEM[i]] = '-'
		else
			fix_opt[$FCT_ITEM[i]] = ( BigDecimal( cgi[$FCT_ITEM[i]] ) / 100 * food_weight * food_number ).round( $FCT_FRCT[$FCT_ITEM[i]] )
		end
	end

	# 擬似食品成分表テーブルに追加
	fix_set = ''
	5.upto( 65 ) do |i| fix_set << "#{$FCT_ITEM[i]}='#{fix_opt[$FCT_ITEM[i]]}'," end
	fix_set.chop!

	#### modify
	if  modifyf == 1
		r = mdb( "SELECT koyomi FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		if r.first
			a = r.first['koyomi'].split( "\t" )[order]
			code = a.split( ":" )[0]
			mdb( "UPDATE #{$MYSQL_TB_FCS} SET name='#{food_name}', #{fix_set} WHERE user='#{user.name}' AND code='#{code}';", false, @debug )
		end
		koyomi_update = ''
		r.each do |e|
			a = e['koyomi'].split( "\t" )
			a.size.times do |c|
				if c == order
					aa = a[c].split( ":" )
					koyomi_update << "#{aa[0]}:#{aa[1]}:#{aa[2]}:#{hh}\t"
				else
					koyomi_update << "#{t[c]}\t"
				end
			end
		end
		koyomi_update.chop!
		mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi_update}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug)
	else
 		fix_code = generate_code( user.name, 'f' )
		mdb( "INSERT INTO #{$MYSQL_TB_FCS} SET code='#{fix_code}', name='#{food_name}',user='#{user.name}', #{fix_set};", false, @debug )
		r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		hh = st_set[tdiv] if hh == 99

		if r.first
			koyomi = r.first['koyomi']
			koyomi << "\t#{fix_code}:100:99:#{hh}"
			mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
		else
			koyomi = "#{fix_code}:100:99:#{hh}"
			mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', fzcode='', freeze='0', koyomi='#{koyomi}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", false, @debug )
		end
	end
end
if @debug
	puts "fix_opt: #{fix_opt}<br>\n"
	puts "<hr>\n"
end


#### modify
if command == 'modify' || modifyf == 1
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
	if r.first
		t = r.first['koyomi'].split( "\t" )[order]
		code = t.split( ":" )[0]

		rr = mdb( "SELECT * FROM #{$MYSQL_TB_FCS} WHERE user='#{user.name}' AND code='#{code}';", false, @debug )
		if rr.first
			food_name = rr.first['name']
			5.upto( 65 ) do |i| fix_opt[$FCT_ITEM[i]] = rr.first[$FCT_ITEM[i]].to_f end
		end
	end
	modifyf = 1
end


#### palette
palette_ps = []
palette_name = []
r = mdb( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}';", false, @debug )
r.each do |e|
	a = e['palette'].split( '' )
	a.map! do |x| x.to_i end
	palette_ps << a
	palette_name << e['name']
end
palette_set = palette_ps[palette]

palette_html = ''
palette_html << "<div class='input-group input-group-sm'>"
palette_html << "<label class='input-group-text'>#{lp[6]}</label>"
palette_html << "<select class='form-select form-select-sm' id='palette' onChange=\"paletteKoyomi( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', #{modifyf} )\">"
palette_ps.size.times do |c|
	if palette == c
		palette_html << "<option value='#{c}' SELECTED>#{palette_name[c]}</option>"
	else
		palette_html << "<option value='#{c}'>#{palette_name[c]}</option>"
	end
end
palette_html << "</select>"
palette_html << "</div>"


#### html_fct_block
html_fct_block1 = '<table class="table-sm table-striped" width="100%">'
5.upto( 7 ) do |i|
	if palette_set[i] == 1
		html_fct_block1 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block1 << "<input type='hidden' value='#{fix_opt[$FCT_ITEM[i]].to_f}' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block1 << '</table>'

html_fct_block2 = '<table class="table-sm table-striped" width="100%">'
8.upto( 20 ) do |i|
	if palette_set[i] == 1
		html_fct_block2 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block2 << "<input type='hidden' value='#{fix_opt[$FCT_ITEM[i]].to_f}' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block2 << '</table>'

html_fct_block3 = '<table class="table-sm table-striped" width="100%">'
21.upto( 34 ) do |i|
	if palette_set[i] == 1
		html_fct_block3 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block3 << "<input type='hidden' value='#{fix_opt[$FCT_ITEM[i]].to_f}' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block3 << '</table>'

html_fct_block4 = '<table class="table-sm table-striped" width="100%">'
35.upto( 46 ) do |i|
	if palette_set[i] == 1
		html_fct_block4 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block4 << "<input type='hidden' value='#{fix_opt[$FCT_ITEM[i]].to_f}' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block4 << '</table>'

html_fct_block5 = '<table class="table-sm table-striped" width="100%">'
47.upto( 55 ) do |i|
	if palette_set[i] == 1
		html_fct_block5 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block5 << "<input type='hidden' value='#{fix_opt[$FCT_ITEM[i]].to_f}' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block5 << '</table>'

html_fct_block6 = '<table class="table-sm table-striped" width="100%">'
56.upto( 66 ) do |i|
	if palette_set[i] == 1
		html_fct_block6 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block5 << "<input type='hidden' value='#{fix_opt[$FCT_ITEM[i]].to_f}' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block6 << '</table>'


####
hh_html = ''
hh_html << "<select class='form-select form-select-sm' id='hh_fix'>"
hh_html << "	<option value='99'>時刻</option>"
0.upto( 23 ) do |c|
	if hh == c
		hh_html << "<option value='#{c}' SELECTED>#{c}</option>"
	else
		hh_html << "<option value='#{c}'>#{c}</option>"
	end
end
hh_html << "</select>"


#### html部分
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<input type="text" class="form-control form-control-sm" id="food_name" placeholder="#{lp[3]}" value="#{food_name}">
		</div>
		<div class="col-2">
		#{hh_html}
		</div>
		<div class="col-4">
		</div>
		<div class="col-2">
			<button class='btn btn-success btn-sm' type='button' onclick="koyomiSaveFix( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', '#{modifyf}', '#{order}' )">#{lp[1]}</button>
		</div>
	</div>
	<br>
	<div class="row">
		<div class="col-3">
			#{palette_html}
		</div>
		<div class="col-1"></div>
		<div class="col-3">
			<div class="input-group input-group-sm">
				<div class="form-check">
    				<input type="checkbox" class="form-check-input" id="g100_check" onChange="koyomiG100check()">
    				<label class="form-check-label">#{lp[2]}</label>
  				</div>
  				&nbsp;&nbsp;&nbsp;
				<label class="input-group-text">#{lp[5]}</label>
				<input type="text" class="form-control form-control-sm" id="food_weight" placeholder="100" value="#{food_weight.to_f}" disabled>&nbsp;g
			</div>
		</div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text">#{lp[12]}</label>
				<input type="number" min='1' class="form-control form-control-sm" id="food_number" placeholder="1">
			</div>
		</div>
	</div>
	<br>

	<div class="row">
		<div class="col-4">
			#{html_fct_block1}
		</div>

		<div class="col-4">
			#{html_fct_block2}
		</div>

		<div class="col-4">
			#{html_fct_block3}
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="col-4">
			#{html_fct_block4}
		</div>

		<div class="col-4">
			#{html_fct_block5}
		</div>

		<div class="col-4">
			#{html_fct_block6}
		</div>
	</div>

	<hr>
</div>

HTML


puts html

