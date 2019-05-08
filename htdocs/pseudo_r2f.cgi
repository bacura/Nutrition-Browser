#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe to pseudo food 0.00

#==============================================================================
# CHANGE LOG
#==============================================================================
#20180228, 0.00a, start


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
#### 端数処理の選択
def frct_select( frct_mode )
  frct_select = []
  1.upto( 3 ) do |c|
    if frct_mode == c
      frct_select << ' selected'
    else
      frct_select << ''
    end
  end

  return frct_select
end


#### 合計精密チェック
def accu_check( frct_accu )
  accu_check = ''
  accu_check = 'CHECKED' if frct_accu == 1

  return accu_check
end


#### 予想重量チェック
def ew_check( ew_mode )
  ew_check = ''
  ew_check = 'CHECKED' if ew_mode == 1

  return ew_check
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'pseudo_r2f', language )
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
end


#### POSTデータの取得
command = cgi['command']
code = cgi['code']
ew_mode = cgi['ew_mode']
frct_mode = cgi['frct_mode']
frct_accu = cgi['frct_accu']
ew_mode = 0 if ew_mode == nil
ew_mode = ew_mode.to_i
frct_mode = 0 if frct_mode == nil
frct_mode = frct_mode.to_i
frct_accu = 0 if frct_accu == nil
frct_accu = frct_accu.to_i
food_name = cgi['food_name']
food_group = cgi['food_group']
class1 = cgi['class1']
class2 = cgi['class2']
class3 = cgi['class3']
tag1 = cgi['tag1']
tag2 = cgi['tag2']
tag3 = cgi['tag3']
tag4 = cgi['tag4']
tag5 = cgi['tag5']
if $DEBUG
	puts "command: #{command}<br>\n"
	puts "code: #{code}<br>\n"
	puts "ew_mode: #{ew_mode}<br>"
	puts "frct_mode: #{frct_mode}<br>"
	puts "frct_accu: #{frct_accu}<br>"
	puts "<hr>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "food_group: #{food_group}<br>\n"
	puts "class1: #{class1}<br>\n"
	puts "class2: #{class2}<br>\n"
	puts "class3: #{class3}<br>\n"
	puts "tag1: #{tag1}<br>\n"
	puts "tag2: #{tag2}<br>\n"
	puts "tag3: #{tag3}<br>\n"
	puts "tag4: #{tag4}<br>\n"
	puts "tag5: #{tag5}<br>\n"
end


#### SUMからデータを抽出
r = mariadb( "SELECT code, name, sum, dish from #{$MYSQL_TB_SUM} WHERE user='#{uname}';", false )
food_name = r.first['name']
code = r.first['code']
dish_num = r.first['dish'].to_i
food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, ew_mode )


if command == 'form'
	# 食品群オプション html
	food_group_option = ''
	19.times do |c|
		cc = c
		cc = "0#{c}" if c < 10
		food_group_option << "<option value='#{cc}'>#{c}.#{$CATEGORY[c]}</option>"
	end

	html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="food_name">#{lp[1]}</label>
				</div>
				<input type="text" class="form-control form-control-sm" id="food_name" value="#{food_name}">
			</div>
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="food_group">#{lp[2]}</label>
				</div>
				<select class="form-control" id="food_group">
					#{food_group_option}
				</select>
			</div>
		</div>
		<div class="col-3"></div>
		<div class="col-1">
			<button class="btn btn-outline-primary btn-sm" type="button" onclick="Pseudo_R2F_BWLX( '#{code}' )">#{lp[3]}</button>
		</div>
	</div>

	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class1" placeholder="class1" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class2" placeholder="class2" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class3" placeholder="class3" value=""></div>
	</div>
	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag1" placeholder="tag1" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag2" placeholder="tag2" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag3" placeholder="tag3" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag4" placeholder="tag4" value=""></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag5" placeholder="tag5" value=""></div>
		<div class="col-1"></div>
	</div>
</div>

HTML

end


#### 保存部分
if command == 'save'
	fct_opt = Hash.new

	# 成分項目の抽出
	fct_item = []
	$FCT_ITEM.size.times do |c| fct_item << $FCT_ITEM[c] end

	#### 食品番号から食品成分と名前を抽出
	fct = []
	db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
	food_no.each do |e|
		fct_tmp = []
		if e == '-'
			fct << '-'
		elsif e == '+'
			fct << '+'
		elsif e == '00000'
			fct << '0'
		else
			if /P|U/ =~ e
				query = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{uname}' OR user='#{$GM}' );"
			else
				query = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{e}';"
			end
			res = db.query( query )
			$FCT_ITEM.size.times do |c| fct_tmp << res.first[$FCT_ITEM[c]] end
			fct << Marshal.load( Marshal.dump( fct_tmp ))
		end
	end
	db.close

	#### データ計算
	fct_sum = []
	fct_item.size.times do |c| fct_sum << BigDecimal( 0 ) end
	food_no.size.times do |fn|
		unless food_no[fn] == '-' || food_no[fn] == '+'
			5.upto(65) do |fi|
				t = convert_zero( fct[fn][fi] )

				# 通常計算
				fct[fn][fi] = num_opt( t, food_weight[fn], frct_mode, $FCT_FRCT[fct_item[fi]] )
				if frct_accu == 0
					# 通常計算
					fct_sum[fi] += BigDecimal( fct[fn][fi] )
				else
					# 精密計算
					fct_sum[fi] += BigDecimal( num_opt( t, food_weight[fn], frct_mode, $FCT_FRCT[fct_item[fi]] + 3 ))
				end
			end
		end
	end

	# 100 g当たりに換算と合計値の桁合わせ
	5.upto( 65 ) do |i| fct_sum[i] = fct_sum[i] / ( total_weight / 100 ) end
	fct_sum = adjust_digit( fct_item, fct_sum, frct_mode )
	5.upto( 65 ) do |i|	fct_opt[$FCT_ITEM[i]] = fct_sum[i] end

	#計算除外値
	fct_opt['REFUSE'] = 0
	fct_opt['WCR'] = '-'
	fct_opt['Notice'] = code


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

	# 新規食品番号の合成
	over_max_flag = false
	new_FN = ''
	r = mariadb( "select FN from #{$MYSQL_TB_TAG} WHERE FG='#{food_group}' AND user='#{uname}' AND public='2';", false )
	if r.first
		code = r.first['FN']
	else
		rr = mariadb( "select FN from #{$MYSQL_TB_TAG} WHERE FN=(SELECT MAX(FN) FROM #{$MYSQL_TB_FCTP} WHERE FG='#{food_group}' AND user='#{uname}');", false )
		if rr.first
			last_FN = rr.first['FN'][-3,3].to_i
			if public_bit == 1
				new_FN = "P#{food_group}%#03d" % ( last_FN + 1 )
			else
				new_FN = "U#{food_group}%#03d" % ( last_FN + 1 )
			end
		else
			if public_bit == 1
				new_FN = "P#{food_group}001"
			else
				new_FN = "U#{food_group}001"
			end
		end
	end

	# 食品番号のチェック
	unless code == ''
		r = mariadb( "select FN from #{$MYSQL_TB_TAG} WHERE user='#{uname}' AND FN='#{code}';", false )
	else
		r = []
	end

	if r.first
		# 擬似食品テーブルの更新
		mariadb( "UPDATE #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{code}',Tagnames='#{tagnames_new}',#{fct_set} WHERE FN='#{code}' AND user='#{uname}';", false )

		# タグテーブルの更新
		mariadb( "UPDATE #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{code}',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',public='#{public_bit}' WHERE FN='#{code}' AND user='#{uname}';", false )

		# 拡張タグテーブルに追加
		mariadb( "UPDATE #{$MYSQL_TB_EXT} SET FN='#{code}', user='#{uname}',color1='0', color2='0', color1h='0', color2h='0' WHERE FN='#{code}' AND user='#{uname}';", false )
	else
		# 擬似食品テーブルに追加
		mariadb( "INSERT INTO #{$MYSQL_TB_FCTP} SET FG='#{food_group}',FN='#{new_FN}',user='#{uname}',Tagnames='#{tagnames_new}',#{fct_set};", false )

		# タグテーブルに追加
		mariadb( "INSERT INTO #{$MYSQL_TB_TAG} SET FG='#{food_group}',FN='#{new_FN}',SID='',name='#{food_name}',class1='#{class1}',class2='#{class2}',class3='#{class3}',tag1='#{tag1}',tag2='#{tag2}',tag3='#{tag3}',tag4='#{tag4}',tag5='#{tag5}',user='#{uname}',public='#{public_bit}';", false )

		# 拡張タグテーブルに追加
		mariadb( "INSERT INTO #{$MYSQL_TB_EXT} SET FN='#{new_FN}', user='#{uname}',color1='0', color2='0', color1h='0', color2h='0';", false )

		code = new_FN
	end
end

puts html

