#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser pseudo food editer 0.00

#==============================================================================
# CHANGE LOG
#==============================================================================
#20180228, 0.00a, start


#==============================================================================
# LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
# STATIC
#==============================================================================
@debug = false


#==============================================================================
# DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'pseudo', language )

html_init( nil )
if @debug
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
end
fct_opt = Hash.new

#### POSTデータの取得
command = cgi['command']
food_key = cgi['food_key']
code = cgi['code']
food_name = cgi['food_name']
food_group = cgi['food_group']
food_weight = cgi['food_weight']
class1 = cgi['class1']
class2 = cgi['class2']
class3 = cgi['class3']
tag1 = cgi['tag1']
tag2 = cgi['tag2']
tag3 = cgi['tag3']
tag4 = cgi['tag4']
tag5 = cgi['tag5']


food_weight_zero = false
food_weight_zero = true if food_weight == '0'
food_weight = 100 if food_weight == nil || food_weight == ''|| food_weight == '0'
food_weight = BigDecimal( food_weight )

code = '' if code == nil
code = '' unless /P|U\d{5}/ =~ code

fg_key, class1_key, class2_key, class3_key, food_name_key = food_key.split( ':' ) if food_key unless nil
food_group = fg_key unless fg_key == nil
food_group_i = food_group.to_i
class1 = class1_key unless class1_key == nil
class2 = class2_key unless class2_key == nil
class3 = class3_key unless class3_key == nil
food_name = food_name_key unless food_name_key == nil

if @debug
	puts "command: #{command}<br>\n"
	puts "code: #{code}<br>\n"
	puts "food_key: #{food_key}<br>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "food_group: #{food_group}<br>\n"
	puts "food_weight: #{food_weight}<br>\n"
	puts "class1: #{class1}<br>\n"
	puts "class2: #{class2}<br>\n"
	puts "class3: #{class3}<br>\n"
	puts "tag1: #{tag1}<br>\n"
	puts "tag2: #{tag2}<br>\n"
	puts "tag3: #{tag3}<br>\n"
	puts "tag4: #{tag4}<br>\n"
	puts "tag5: #{tag5}<br>\n"
	puts "<hr>\n"
end


#### 成分読み込み
if command == 'init' && code != ''
	r = mdb( "select * from #{$MYSQL_TB_FCTP} WHERE FN='#{code}' AND ( user='#{uname}' OR user='#{$GM}' );", false, @debug )
	if r.first
		4.upto( 67 ) do |i| fct_opt[$FCT_ITEM[i]] = r.first[$FCT_ITEM[i]] end
	end
end


#### クラス・タグ読み込み
if command == 'init' && code != ''
	r = mdb( "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND ( user='#{uname}' OR user='#{$GM}' );", false, @debug )
	if r.first
		user = r.first['user']
		class1 = r.first['class1']
		class2 = r.first['class2']
		class3 = r.first['class3']
		tag1 = r.first['tag1']
		tag2 = r.first['tag2']
		tag3 = r.first['tag3']
		tag4 = r.first['tag4']
		tag5 = r.first['tag5']
	end
elsif command == 'save' && code != ''
	r = mdb( "select * from #{$MYSQL_TB_TAG} WHERE FN='#{code}' AND user='#{uname}';", false, @debug )
	user = r.first['user'] if r.first
end


#### 保存部分
if command == 'save'
	# 廃棄率
	if cgi['REFUSE'] == '' || cgi['REFUSE'] == nil
		fct_opt['REFUSE'] = 0
	else
		fct_opt['REFUSE'] = cgi['REFUSE'].to_i
	end

	# エネルギー補完
	if  cgi['ENERC_KCAL'].to_f != 0 && cgi['ENERC'].to_f == 0
		fct_opt['ENERC_KCAL'] = cgi['ENERC_KCAL']
		fct_opt['ENERC'] = (( cgi['ENERC_KCAL'].to_i * 4184 ) / 1000 ).to_i
	elsif cgi['ENERC_KCAL'].to_f == 0 && cgi['ENERC'].to_f != 0
		fct_opt['ENERC_KCAL'] = ( cgi['ENERC'] / 4.184 ).to_i
		fct_opt['ENERC'] = cgi['ENERC']
	elsif cgi['ENERC_KCAL'].to_f == 0 && cgi['ENERC'].to_f == 0
		fct_opt['ENERC_KCAL'] = 0
		fct_opt['ENERC'] = 0
	else
		fct_opt['ENERC_KCAL'] = cgi['ENERC_KCAL']
		fct_opt['ENERC'] = cgi['ENERC']
	end

	# 重量影響成分
	fct_opt['ENERC_KCAL'] = ( BigDecimal( fct_opt['ENERC_KCAL'].to_s ) / ( food_weight / 100 )).round( $FCT_FRCT[$FCT_ITEM[5]] )
	fct_opt['ENERC'] = ( BigDecimal( fct_opt['ENERC'].to_s ) / ( food_weight / 100 )).round( $FCT_FRCT[$FCT_ITEM[6]] )
	7.upto( 65 ) do |i|
		if cgi[$FCT_ITEM[i]] == '' || cgi[$FCT_ITEM[i]] == nil || cgi[$FCT_ITEM[i]] == '-'
			fct_opt[$FCT_ITEM[i]] = '-'
		else
			fct_opt[$FCT_ITEM[i]] = ( BigDecimal( cgi[$FCT_ITEM[i]] ) / ( food_weight / 100 )).round( $FCT_FRCT[$FCT_ITEM[i]] )
		end
	end

	# 重量変化率
	if cgi['WCR'] == '' || cgi['WCR'] == nil
		fct_opt['WCR'] = '-'
	else
		fct_opt['WCR'] = cgi['WCR'].to_i
	end

	# 備考
	fct_opt['Notice'] = cgi['Notice']

	# ゼロ重量戻し
	food_weight = 0 if food_weight_zero

	class1_new = ''
	class2_new = ''
	class3_new = ''
	tag1_new = ''
	tag2_new = ''
	tag3_new = ''
	tag4_new = ''
	tag5_new = ''
	class1_new = "＜#{class1}＞" unless class1 == ''
	class2_new = "（#{class2}）" unless class2 == ''
	class3_new = "［#{class3}］" unless class3 == ''
	tag1_new = "　#{tag1}" unless tag1 == ''
	tag2_new = "　#{tag2}" unless tag2 == ''
	tag3_new = "　#{tag3}" unless tag3 == ''
	tag4_new = "　#{tag4}" unless tag4 == ''
	tag5_new = "　#{tag5}" unless tag5 == ''
	tagnames_new = "#{class1_new}#{class2_new}#{class3_new}#{food_name}#{tag1_new}#{tag2_new}#{tag3_new}#{tag4_new}#{tag5_new}"

	# 擬似食品成分表テーブルに追加
	fct_set = ''
	4.upto( 67 ) do |i| fct_set << "#{$FCT_ITEM[i]}='#{fct_opt[$FCT_ITEM[i]]}'," end
	fct_set.chop!

	# タグテーブルに追加
	public_bit = 0
	public_bit = 1 if status == 9

	# 新規食品番号の合成
	over_max_flag = false
	r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{uname}' AND public='2';", false, @debug )
	if r.first
		code = r.first['FN']
	else
		rr = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_FCTP} WHERE FG='#{food_group}' AND user='#{uname}');", false, @debug )
		if rr.first
			last_FN = rr.first['FN'][-3,3].to_i
			if public_bit == 1
				@new_FN = "P#{food_group}%#03d" % ( last_FN + 1 )
			else
				@new_FN = "U#{food_group}%#03d" % ( last_FN + 1 )
			end
		else
			if public_bit == 1
				@new_FN = "P#{food_group}001"
			else
				@new_FN = "U#{food_group}001"
			end
		end
	end

	# 食品番号のチェック
	unless code == ''
		r = mdb( "select FN from #{$MYSQL_TB_TAG} WHERE user='#{uname}' AND FN='#{code}';", false, @debug )
	else
		r = []
	end

	if r.first
		# 擬似食品テーブルの更新
		mdb( "UPDATE #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{code}',Tagnames='#{tagnames_new}',#{fct_set} WHERE FN='#{code}' AND user='#{uname}';", false, @debug )

		# タグテーブルの更新
		mdb( "UPDATE #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{code}',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',public='#{public_bit}' WHERE FN='#{code}' AND user='#{uname}';", false, @debug )

		# 拡張タグテーブルに追加
		mdb( "UPDATE #{$MYSQL_TB_EXT} SET FN='#{code}', user='#{uname}',color1='0', color2='0', color1h='0', color2h='0' WHERE FN='#{code}' AND user='#{uname}';", false, @debug )
	else
		# 擬似食品テーブルに追加
		mdb( "INSERT INTO #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{@new_FN}',user='#{uname}',Tagnames='#{tagnames_new}',#{fct_set};", false, @debug )

		# タグテーブルに追加
		mdb( "INSERT INTO #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{@new_FN}',SID='',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',user='#{uname}',public='#{public_bit}';", false, @debug )

		# 拡張タグテーブルに追加
		mdb( "INSERT INTO #{$MYSQL_TB_EXT} SET FN='#{@new_FN}', user='#{uname}',color1='0', color2='0', color1h='0', color2h='0';", false, @debug )

		code = @new_FN
	end

	food_weight = 100
end


#### 削除部分
if command == 'delete'
	mdb( "UPDATE #{$MYSQL_TB_TAG} SET public='2' WHERE user='#{uname}' AND FN='#{code}';", false, @debug )
	code = ''
end


#### debug
if @debug
	puts "fct_opt: #{fct_opt}<br>\n"
	puts "<hr>\n"
end


#### food froup html
food_group_option = ''
19.times do |c|
	cc = c
	cc = "0#{c}" if c < 10
	if food_group_i == c
		food_group_option << "<option value='#{cc}' SELECTED>#{c}.#{$CATEGORY[c]}</option>"
	else
		food_group_option << "<option value='#{cc}'>#{c}.#{$CATEGORY[c]}</option>"
	end
end


#### disable option
disabled_option = ''
disabled_option = 'disabled' if user != uname && user != nil

#### html_fct_block
html_fct_block1 = '<table class="table-sm table-striped" width="100%">'
4.upto( 7 ) do |i| html_fct_block1 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]].to_f}\" #{disabled_option}></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block1 << '</table>'

html_fct_block2 = '<table class="table-sm table-striped" width="100%">'
8.upto( 20 ) do |i| html_fct_block2 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]].to_f}\" #{disabled_option}></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block2 << '</table>'

html_fct_block3 = '<table class="table-sm table-striped" width="100%">'
21.upto( 34 ) do |i| html_fct_block3 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]].to_f}\" #{disabled_option}></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block3 << '</table>'

html_fct_block4 = '<table class="table-sm table-striped" width="100%">'
35.upto( 46 ) do |i| html_fct_block4 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]].to_f}\" #{disabled_option}></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block4 << '</table>'

html_fct_block5 = '<table class="table-sm table-striped" width="100%">'
47.upto( 55 ) do |i| html_fct_block5 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]].to_f}\" #{disabled_option}></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block5 << '</table>'

html_fct_block6 = '<table class="table-sm table-striped" width="100%">'
56.upto( 66 ) do |i| html_fct_block6 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]].to_f}\" #{disabled_option}></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block6 << '</table>'


#### save button
save_button = ''
if user == uname || code == ''
	save_button = "<button class=\"btn btn-outline-primary btn-sm\" type=\"button\" onclick=\"pseudoSave_BWLF( '#{code}' )\">#{lp[1]}</button>"
end


#### delete button
delete_button = ''
if code != '' && user == uname
	delete_button = "<button class='btn btn-outline-danger btn-sm' type='button' onclick=\"pseudoDelete_BWLF( '#{code}' )\">#{lp[2]}</button>"
end


#### html part
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<input type="text" class="form-control form-control-sm" id="food_name" placeholder="#{lp[3]}" value="#{food_name}">
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="food_group">#{lp[4]}</label>
				</div>
				<select class="form-control" id="food_group">
					#{food_group_option}
				</select>
			</div>
		</div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="food_weight">#{lp[5]}</label>
				</div>
				<input type="text" class="form-control form-control-sm" id="food_weight" placeholder="100" value="#{food_weight.to_f}">&nbsp;g
			</div>

		</div>

		<div class="col-1"></div>

		<div class="col-1">
			#{save_button}
		</div>
	</div>

	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class1" placeholder="class1" value="#{class1}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class2" placeholder="class2" value="#{class2}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class3" placeholder="class3" value="#{class3}"></div>
	</div>
	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag1" placeholder="tag1" value="#{tag1}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag2" placeholder="tag2" value="#{tag2}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag3" placeholder="tag3" value="#{tag3}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag4" placeholder="tag4" value="#{tag4}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag5" placeholder="tag5" value="#{tag5}"></div>
		<div class="col-1"></div>
		<div class="col-1">#{delete_button}</div>
	</div>
	<hr>
	<div class="row">
		<div class="col-4">
			#{html_fct_block1}

			<div style='border: solid gray 1px; margin: 0.5em; padding: 0.5em;'>
				備考：<br>
				<textarea rows="6" cols="32" id="Notice" #{disabled_option}>#{fct_opt['Notice']}</textarea>
			</div>
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

	<div class="row">
		<div class="col-8">
			#{lp[6]}
		</div>
		<div class="col-4">
		</div>
	</div>
</div>

HTML


puts html

