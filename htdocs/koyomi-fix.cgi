#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi fix editer 0.00

#==============================================================================
# CHANGE LOG
#==============================================================================
#20190517, 0.00a, start


#==============================================================================
# LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
# STATIC
#==============================================================================
$DEBUG = false


#==============================================================================
# DEFINITION
#==============================================================================

# Getting start year & standard meal time
def get_starty( uname )
	t = Time.new
	start_year = t.year
	breakfast_st = 0
	lunch_st = 0
	dinner_st = 0
	r = mariadb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
	if r.first
		a = r.first['koyomiy'].split( ':' )
		start_year = a[0].to_i if a[0].to_i != 0
		breakfast_st = a[1].to_i if a[1].to_i != 0
		lunch_st = a[2].to_i if a[2].to_i != 0
		dinner_st = a[3].to_i if a[3].to_i != 0
	end
	return start_year, breakfast_st, lunch_st, dinner_st
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'koyomi-fix', language )
start_year, breakfast_st, lunch_st, dinner_st = get_starty( uname )
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
	puts "breakfast_st:#{breakfast_st}<br>\n"
	puts "lunch_st:#{lunch_st}<br>\n"
	puts "dinner_st:#{dinner_st}<br>\n"
	puts "<hr>"
end
fct_opt = Hash.new
fix_opt = Hash.new

#### POSTデータの取得
command = cgi['command']
yyyy = cgi['yyyy']
mm = cgi['mm']
dd = cgi['dd']
tdiv = cgi['tdiv'].to_i
hh = cgi['hh'].to_i
some = cgi['some']
palette = cgi['palette'].to_i
food_name = cgi['food_name']
food_weight = cgi['food_weight']
food_weight = 100 if food_weight == nil || food_weight == ''|| food_weight == '0'
food_weight = BigDecimal( food_weight )
if $DEBUG
	puts "command: #{command}<br>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "food_weight: #{food_weight}<br>\n"
	puts "yyyy: #{yyyy}<br>\n"
	puts "mm: #{mm}<br>\n"
	puts "dd: #{dd}<br>\n"
	puts "tdiv: #{tdiv}<br>\n"
	puts "hh: #{hh}<br>\n"
	puts "some: #{some}<br>\n"
	puts "palette: #{palette}<br>\n"
	puts "<hr>\n"
end


#### 成分読み込み
if command == 'init'
	4.upto( 67 ) do |i| fix_opt[$FCT_ITEM[i]] = 0.0 end
end


#### Saving Something
if command == 'some'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false)
	if r.first
		breakfast = r.first['breakfast']
		lunch = r.first['lunch']
		dinner = r.first['dinner']
		supple = r.first['supple']
		delimiter = ''

		case tdiv
		when 0
			hh = breakfast_st if hh == 99
			breakfast = "#{some}:100:%:#{hh}"
		when 1
			hh = lunch_st if hh == 99
			lunch = "#{some}:100:%:#{hh}"
		when 2
			hh = dinner_st if hh == 99
			dinner = "#{some}:100:%:#{hh}"
		when 3
			supple = "#{some}:100:%:#{hh}"
		end
		mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET breakfast='#{breakfast}', lunch='#{lunch}', dinner='#{dinner}', supple='#{supple}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false)
	else
		breakfast = ''
		lunch = ''
		dinner = ''
		supple = ''
		case tdiv
		when 0
			hh = breakfast_st if hh == 99
			breakfast = "#{some}:100:%:#{hh}"
		when 1
			hh = lunch_st if hh == 99
			lunch = "#{some}:100:%:#{hh}"
		when 2
			hh = dinner_st if hh == 99
			dinner = "#{some}:100:%:#{hh}"
		when 3
			supple = "#{some}:100:%:#{hh}"
		end
		mariadb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{uname}', fix='', breakfast='#{breakfast}', lunch='#{lunch}', dinner='#{dinner}', supple='#{supple}', memo='', date='#{yyyy}-#{mm}-#{dd}';", false)
	end
end


#### 保存部分
if command == 'save'
	# 廃棄率
	if cgi['REFUSE'] == '' || cgi['REFUSE'] == nil
		fct_opt['REFUSE'] = 0
		fix_opt['REFUSE'] = 0
	else
		fix_opt['REFUSE'] = cgi['REFUSE'].to_i
		fct_opt['REFUSE'] = fix_opt['REFUSE']
	end

	# エネルギー補完
	if cgi['ENERC_KCAL'] != '' && cgi['ENERC'] == ''
		fix_opt['ENERC_KCAL'] = cgi['ENERC_KCAL']
		fix_opt['ENERC'] = (( cgi['ENERC_KCAL'].to_i * 4184 ) / 1000 ).to_i
		fct_opt['ENERC_KCAL'] = fix_opt['ENERC_KCAL']
		fct_opt['ENERC_KCAL'] = fix_opt['ENERC']
	elsif cgi['ENERC_KCAL'] == '' && cgi['ENERC'] != ''
		fix_opt['ENERC_KCAL'] = ( cgi['ENERC'] / 4.184 ).to_i
		fix_opt['ENERC'] = cgi['ENERC']
		fct_opt['ENERC_KCAL'] = fix_opt['ENERC_KCAL']
		fct_opt['ENERC'] = fix_opt['ENERC']
	elsif cgi['ENERC_KCAL'] == '' && cgi['ENERC'] == ''
		fix_opt['ENERC_KCAL'] = 0
		fix_opt['ENERC'] = 0
		fct_opt['ENERC_KCAL'] = 0
		fct_opt['ENERC'] = 0
	else
		fix_opt['ENERC_KCAL'] = cgi['ENERC_KCAL']
		fix_opt['ENERC'] = cgi['ENERC']
		fct_opt['ENERC_KCAL'] = fix_opt['ENERC_KCAL']
		fct_opt['ENERC'] = fix_opt['ENERC']
	end

	# 重量影響成分
	7.upto( 65 ) do |i|
		if cgi[$FCT_ITEM[i]] == '' || cgi[$FCT_ITEM[i]] == nil || cgi[$FCT_ITEM[i]] == '-'
			fix_opt[$FCT_ITEM[i]] = '-'
			fct_opt[$FCT_ITEM[i]] = '-'
		else
			fix_opt[$FCT_ITEM[i]] = cgi[$FCT_ITEM[i]]
			t = BigDecimal( cgi[$FCT_ITEM[i]] ) / ( food_weight / 100 )
			fct_opt[$FCT_ITEM[i]] = t
		end
	end

	# 重量変化率
	if cgi['WCR'] == '' || cgi['WCR'] == nil
		fix_opt['WCR'] = '-'
		fct_opt['WCR'] = '-'
	else
		fix_opt['WCR'] = cgi['WCR'].to_i
		fct_opt['WCR'] = fix_opt['WCR']
	end

	# 擬似食品成分表テーブルに追加
	fct_set = ''
	fix_set = ''
	4.upto( 66 ) do |i| fct_set << "#{$FCT_ITEM[i]}='#{fct_opt[$FCT_ITEM[i]]}'," end
	5.upto( 65 ) do |i| fix_set << "#{$FCT_ITEM[i]}='#{fix_opt[$FCT_ITEM[i]]}'," end
	fix_set.chop!
	fct_set.chop!

 	fix_code = generate_code( uname, 'f' )
	mariadb( "INSERT INTO #{$MYSQL_TB_FCS} SET code='#{fix_code}', name='#{food_name}',user='#{uname}',#{fix_set};", false )

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
			breakfast << "#{delimiter}#{fix_code}:100:%:#{hh}"
		when 1
			delimiter = "\t" if lunch != ''
			lunch << "#{delimiter}#{fix_code}:100:%:#{hh}"
		when 2
			delimiter = "\t" if dinner != ''
			dinner << "#{delimiter}#{fix_code}:100:%:#{hh}"
		when 3
			delimiter = "\t" if supple != ''
			supple << "#{delimiter}#{fix_code}:100:%:#{hh}"
		end
		mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET breakfast='#{breakfast}', lunch='#{lunch}', dinner='#{dinner}', supple='#{supple}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false)
	else
		breakfast = ''
		lunch = ''
		dinner = ''
		supple = ''
		case tdiv
		when 0
			breakfast = "#{fix_code}:100:%:#{hh}"
		when 1
			lunch = "#{fix_code}:100:%:#{hh}"
		when 2
			dinner = "#{fix_code}:100:%:#{hh}"
		when 3
			supple = "#{fix_code}:100:%:#{hh}"
		end
		mariadb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{uname}', fix='', breakfast='#{breakfast}', lunch='#{lunch}', dinner='#{dinner}', supple='#{supple}', memo='', date='#{yyyy}-#{mm}-#{dd}';", false)
	end


	# 新規食品番号の合成
	#r = mariadb( "select FN from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_FCTP} WHERE FG='00' AND user='#{uname}');", false )
	#new_FN = ''
	#if r.first
	#	last_FN = rr.first['FN'][-3,3].to_i
	#	new_FN = "U#{food_group}%#03d" % ( last_FN + 1 )
	#else
	#	new_FN = "U#{food_group}001"
	#end


	if false
		# 擬似食品テーブルに追加
		mariadb( "INSERT INTO #{$MYSQL_TB_FCTP} SET FG='00',FN='#{new_FN}',user='#{uname}',Tagnames='#{tagnames_new}',#{fct_set};", false )

		# タグテーブルに追加
		mariadb( "INSERT INTO #{$MYSQL_TB_TAG} SET FG='00',FN='#{new_FN}',SID='',name='#{food_name}',class1='',class2='',class3='',tag1='',tag2='',tag3='',tag4='',tag5='',user='#{uname}',public='0';", false )

		# 拡張タグテーブルに追加
		mariadb( "INSERT INTO #{$MYSQL_TB_EXT} SET FN='#{new_FN}', user='#{uname}',color1='0', color2='0', color1h='0', color2h='0';", false )
	end
end


#### デバッグ用
if $DEBUG
	puts "fct_opt: #{fct_opt}<br>\n"
	puts "fix_opt: #{fix_opt}<br>\n"
	puts "<hr>\n"
end


#### palette
palette_ps = $PALETTE
palette_name = $PALETTE_NAME
r = mariadb( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';", false )
r.each do |e|
	a = e['palette'].split( '' )
	a.map! do |x| x.to_i end
	palette_ps << a
	palette_name << e['name']
end
palette_set = palette_ps[palette]

palette_html = ''
palette_html << "<div class='input-group input-group-sm'>"
palette_html << "<div class='input-group-prepend'>"
palette_html << "	<label class='input-group-text'>#{lp[6]}</label>"
palette_html << "</div>"
palette_html << "<select class='custom-select custom-select-sm' id='palette' onChange=\"paletteKoyomi_BW3( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}' )\">"
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
4.upto( 7 ) do |i|
	if palette_set[i] == 1
		html_fct_block1 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block1 << "<input type='hidden' value='0' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block1 << '</table>'

html_fct_block2 = '<table class="table-sm table-striped" width="100%">'
8.upto( 20 ) do |i|
	if palette_set[i] == 1
		html_fct_block2 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block2 << "<input type='hidden' value='0' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block2 << '</table>'

html_fct_block3 = '<table class="table-sm table-striped" width="100%">'
21.upto( 34 ) do |i|
	if palette_set[i] == 1
		html_fct_block3 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block3 << "<input type='hidden' value='0' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block3 << '</table>'

html_fct_block4 = '<table class="table-sm table-striped" width="100%">'
35.upto( 46 ) do |i|
	if palette_set[i] == 1
		html_fct_block4 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block4 << "<input type='hidden' value='0' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block4 << '</table>'

html_fct_block5 = '<table class="table-sm table-striped" width="100%">'
47.upto( 55 ) do |i|
	if palette_set[i] == 1
		html_fct_block5 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block5 << "<input type='hidden' value='0' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block5 << '</table>'

html_fct_block6 = '<table class="table-sm table-striped" width="100%">'
56.upto( 66 ) do |i|
	if palette_set[i] == 1
		html_fct_block6 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fix_opt[$FCT_ITEM[i]].to_f}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>"
	else
		html_fct_block5 << "<input type='hidden' value='0' id='#{$FCT_ITEM[i]}'>"
	end
end
html_fct_block6 << '</table>'


####
hh_html = ''
hh_html << "<select class='custom-select custom-select-sm' id='hh'>"
hh_html << "	<option value='99'>時刻</option>"
0.upto( 23 ) do |c| hh_html << "<option value='#{c}'>#{c}</option>" end
hh_html << "</select>"


#### html部分
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<input type="text" class="form-control form-control-sm" id="food_name" placeholder="#{lp[3]}" value="#{food_name}">
		</div>
		<div class="col-1">
		#{hh_html}
		</div>
		<div class="col-3">
		#{palette_html}
		</div>
		<div class="col-2">
			<button class='btn btn-success' type='button' onclick="koyomiSaveFix( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}' )">#{lp[1]}</button>
		</div>
		<div class="col-2">
			<button class='btn btn-success' type='button' onclick="koyomiSaveSome( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', '?-' )">#{lp[7]}</button>
			<button class='btn btn-success' type='button' onclick="koyomiSaveSome( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', '?=' )">#{lp[8]}</button>
			<button class='btn btn-success' type='button' onclick="koyomiSaveSome( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', '?+' )">#{lp[9]}</button>
		</div>
	</div>
	<div class="row">
		<div class="col-2">
			<div class="form-group form-check">
    			<input type="checkbox" class="form-check-input" id="fct_check" onChange="koyomiFCTcheck( '#{yyyy}', '#{mm}', '#{dd}', '#{tdiv}', '#{hh}' )">
    			<label class="form-check-label">#{lp[2]}</label>
  			</div>
		</div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text">#{lp[5]}</label>
				</div>
				<input type="text" class="form-control form-control-sm" id="food_weight" placeholder="100" value="#{food_weight.to_f}" disabled>&nbsp;g
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

