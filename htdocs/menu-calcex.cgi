#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser magic menu calc expand 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171227, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'menu-calcex'


#==============================================================================
#DEFINITION
#==============================================================================
#### 端数処理の選択
def frct_select( frct_mode, lp )
	frct_select = ''
	case frct_mode
	when 3
		frct_select = lp[10]
	when 2
		frct_select = lp[11]
	else
		frct_select = lp[12]
	end

	return frct_select
end


#### 合計精密チェック
def accu_check( frct_accu, lp )
  accu_check = lp[15]
  accu_check = lp[7] if frct_accu == 1

  return accu_check
end


#### 予想重量チェック
def ew_check( ew_mode, lp )
  ew_check = lp[6]
  ew_check = lp[8] if ew_mode == 1

  return ew_check
end


#### Language init
def lp_init( script, language_set )
  f = open( "#{$HTDOCS_PATH}/language_/#{script}.#{language_set}", "r" )
  lp = [nil]
  f.each do |line|
    lp << line.chomp.force_encoding( 'UTF-8' )
  end
  f.close

  return lp
end

#==============================================================================
# Main
#==============================================================================

html_init( nil )
html_head( nil, 0, '拡張表示' )

#### GETデータの取得
get = get_data()
uname = get['uname']
language = 'jp'
code = get['code']
ew_mode = get['ew_mode']
frct_mode = get['frct_mode']
frct_accu = get['frct_accu']
palette = get['palette']
lp = lp_init( 'menu-calcex', language )
if @debug
	puts "uname: #{uname}<br>"
	puts "<hr>"
	puts "code: #{code}<br>"
	puts "ew_mode: #{ew_mode}<br>"
	puts "frct_mode: #{frct_mode}<br>"
	puts "frct_accu: #{frct_accu}<br>"
	puts "palette: #{palette}<br>"
	puts "<hr>"
end

ew_mode = 0 if ew_mode == nil
ew_mode = ew_mode.to_i
frct_mode = 0 if frct_mode == nil
frct_mode = frct_mode.to_i
frct_accu = 0 if frct_accu == nil
frct_accu = frct_accu.to_i
palette = 0 if palette == nil
palette = palette.to_i


#### セレクト＆チェック設定
frct_select = frct_select( frct_mode, lp )
accu_check = accu_check( frct_accu, lp )
ew_check = ew_check( ew_mode, lp )


#### Setting palette
palette_sets = []
palette_name = []
r = mdb( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';", false, @debug )
if r.first
	r.each do |e|
		a = e['palette'].split( '' )
		a.map! do |x| x.to_i end
		palette_sets << a
		palette_name << e['name']
	end
end
palette_set = palette_sets[palette]


# 成分項目の抽出
fct_item = []
$FCT_ITEM.size.times do |c|
	fct_item << $FCT_ITEM[c] if palette_set[c] == 1
end


# HTMLパレットの生成
palette_html = ''
palette_sets.size.times do |c|
	if palette == c
		palette_html << "<option value='#{c}' SELECTED>#{palette_name[c]}</option>"
	else
		palette_html << "<option value='#{c}'>#{palette_name[c]}</option>"
	end
end


#### mealからデータを抽出
r = mdb( "SELECT code, name, meal from #{$MYSQL_TB_MEAL} WHERE user='#{uname}';", false, @debug )
meal_name = r.first['name']
code = r.first['code']
meal = r.first['meal'].split( "\t" )
recipe_code = []
meal.each do |e| recipe_code << e end


#### 大合計の初期化
total_sum = []
fct_item.size.times do |c| total_sum[c] = 0 end
rc = 0
fct_html = []
recipe_name = []
total_total_weight = 0


#### RECIPEからデータを抽出
recipe_code.each do |e|
	query = "SELECT name, sum, dish from #{$MYSQL_TB_RECIPE} WHERE code='#{e}';"
	db_err = 'RECIPE select'
	r = mdb( "SELECT name, sum, dish from #{$MYSQL_TB_RECIPE} WHERE code='#{e}';", false, @debug )
	recipe_name[rc] = r.first['name']
	dish_num = r.first['dish'].to_i
	dish_num = 1 if dish_num == 0
	food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, ew_mode )
	total_total_weight += total_weight


	# 食品番号から食品成分と名前を抽出
	fct = []
	fct_name = []
	db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )

	# 食品成分データの抽出と名前の書き換え
	food_no.each do |ee|
		fct_tmp = []
		if ee == '-'
			fct << '-'
			fct_name << '-'
		elsif ee == '+'
			fct << '+'
			fct_name << '+'
		elsif ee == '00000'
			fct << '0'
			fct_name << '0'
		else
			if /P|U/ =~ ee
				q = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{ee}' AND ( user='#{uname}' OR user='#{$GM}' );"
			else
				q = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{ee}';"
			end
			rr = db.query( q )
			fct_name << rr.first['Tagnames']
			$FCT_ITEM.size.times do |c|
				fct_tmp << rr.first[$FCT_ITEM[c]] if palette_set[c] == 1
			end
			fct << Marshal.load( Marshal.dump( fct_tmp ))
		end
	end

	# 名前の書き換え
	if true
		food_no.size.times do |c|
 			unless food_no[c] == '+' || food_no[c] == '-' || food_no[c] == '0'
				q = "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}';"
				q = "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}' AND ( user='#{uname}' OR user='#{$GM}' );" if /P|U/ =~ food_no[c]
				rr = db.query( q )
				fct_name[c] = bind_tags( rr ) if rr.first
			end
		end
	end
	db.close

	#### データ計算
	fct_sum = []
	fct_item.size.times do |c| fct_sum << 0.0 end
	food_no.size.times do |fn|
		unless food_no[fn] == '-' || food_no[fn] == '+'
			fct_item.size.times do |fi|
				t = convert_zero( fct[fn][fi] )
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


	#### 合計値の桁合わせ
	fct_item.size.times do |fi|
    	limit = $FCT_FRCT[fct_item[fi]]
    	if limit != nil
			case frct_mode
			# 四捨五入
			when 1
				fct_sum[fi] = fct_sum[fi].round( limit )
			# 切り上げ
			when 2
				fct_sum[fi] = fct_sum[fi].ceil( limit )
			# 切り捨て
			when 3
				fct_sum[fi] = fct_sum[fi].floor( limit )
			else
				fct_sum[fi] = fct_sum[fi].round( limit )
			end

        	if limit == 0
            	fct_sum[fi] = fct_sum[fi].to_i
        	else
            	fct_sum[fi] = fct_sum[fi].to_f
        	end
			total_sum[fi] = total_sum[fi] + ( fct_sum[fi] * 1000 ).to_i
		end
	end

	#### HTML食品成分表の生成
	fct_html[rc] = ''
	fct_html[rc] << "	<tr><td colspan='#{fct_item.size + 3}'><h6>#{recipe_name[rc]}</h6></td></tr>"

	# 項目名
	fct_html[rc] << '    <tr>'
	fct_html[rc] << "      <th align='center' width='6%'' class='fct_item' nowrap>#{lp[1]}</th>"
	fct_html[rc] << "      <th align='center' width='20%' class='fct_item' nowrap>#{lp[2]}</th>"
	fct_html[rc] << "      <th align='center' width='4%'' class='fct_item' nowrap>#{lp[3]}</th>"
	fct_item.each do |ee|
		if $FCT_NAME[ee]
			fct_html[rc] << "      <th align='center' width='5%' class='fct_item'>#{$FCT_NAME[ee]}</th>"
		else
			fct_html[rc] << "      <th align='center' width='5%' class='fct_item'>&nbsp;</th>"
		end
	end
	fct_html[rc] << '    </tr>'

	# 単位
	fct_html[rc] << '    <tr>'
	fct_html[rc] << '      <td colspan="2" align="center"></td>'
	fct_html[rc] << "      <td align='center' class='fct_unit' nowrap>( g )</td>"
	fct_item.each do |ee|
		if $FCT_UNIT[ee]
			fct_html[rc] << "      <td align='center' class='fct_unit' nowrap>( #{$FCT_UNIT[ee]} )</td>"
		else
			fct_html[rc] << "      <td align='center' class='fct_unit' nowrap>&nbsp;</td>"
		end
	end
	fct_html[rc] << '    </tr>'

	# 各成分値
	food_no.size.times do |c|
		unless food_no[c] == '-' || food_no[c] == '+'
			fct_html[rc] << '    <tr>'
			fct_html[rc] << "      <td align='center' nowrap>#{food_no[c]}</td>"
			fct_html[rc] << "      <td nowrap>#{fct_name[c]}</td>"
			fct_html[rc] << "      <td align='right' nowrap>#{food_weight[c].to_f}</td>"
			fct_item.size.times do |cc|
				fct_html[rc] << "      <td align='right' nowrap>#{fct[c][cc]}</td>"
			end
			fct_html[rc] << '    </tr>'
		end
	end

	# 合計値
	fct_html[rc] << '    <tr>'
	fct_html[rc] << "      <td colspan='2' align='center' class='fct_sum'>#{lp[4]}</td>"
	fct_html[rc] << "      <td align='right' class='fct_sum'>#{total_weight.to_f}</td>"

	fct_item.size.times do |c|
		if fct_item[c] == 'REFUSE' || fct_item[c] == 'WCR' || fct_item[c] == 'Notice'
			fct_html[rc] << "      <td></td>"
		else
			fct_html[rc] << "      <td align='right' class='fct_sum' nowrap>#{fct_sum[c]}</td>"
		end
	end
	fct_html[rc] << '   </tr>'
	fct_html[rc] << "	<tr><td colspan='#{fct_item.size + 3}'>&nbsp;</td></tr>"

	rc += 1
end


#### 大合計値の桁処理
total_sum.map! do |a| a.to_f / 1000 end
total_sum.size.times do |fi|
	total_sum[fi] = total_sum[fi].round( $FCT_FRCT[fct_item[fi]] ) if $FCT_FRCT[fct_item[fi]] != nil
end


#### HTML食品成分全合計
fct_html_sum = ''

# 項目名
fct_html_sum << '    <tr>'
fct_html_sum << '      <th align="center" width="6%" class="fct_item"></th>'
fct_html_sum << '      <th align="center" width="20%" class="fct_item"></th>'
fct_html_sum << "      <th align='center' width='4%' class='fct_item'>#{lp[3]}</th>"
fct_item.each do |e|
	if $FCT_NAME[e]
		fct_html_sum << "      <th align='center' width='5%' class='fct_item'>#{$FCT_NAME[e]}</th>"
	else
		fct_html_sum << "      <th align='center' width='5%' class='fct_item'>&nbsp;</th>"
	end
end
fct_html_sum << '    </tr>'

# 単位
fct_html_sum << '    <tr>'
fct_html_sum << '      <td colspan="2" align="center"></td>'
fct_html_sum << "      <td align='center' class='fct_unit'>( g )</td>"
fct_item.each do |e|
	if $FCT_UNIT[e]
		fct_html_sum << "      <td align='center' class='fct_unit'>( #{$FCT_UNIT[e]} )</td>"
	else
		fct_html_sum << "      <td align='center' class='fct_unit'>&nbsp;</td>"
	end
end
fct_html_sum << '    </tr>'

# 合計値
fct_html_sum << '    <tr>'
fct_html_sum << "      <td colspan='2' align='center' class='fct_sum'>#{lp[17]}</td>"
fct_html_sum << "      <td align='right' class='fct_sum'>#{total_total_weight.to_f}</td>"
fct_item.size.times do |c|
	if fct_item[c] == 'REFUSE' || fct_item[c] == 'WCR' || fct_item[c] == 'Notice'
		fct_html_sum << "      <td></td>"
	else
		fct_html_sum << "      <td align='right' class='fct_sum' nowrap>#{total_sum[c]}</td>"
	end
end
fct_html_sum << '    </tr>'


puts "<div>#{lp[5]}: #{meal_name}</div>"
puts "<div>#{lp[14]}: #{ew_check} #{lp[9]}： #{frct_select} / #{accu_check}</div>"
puts "<br>"

puts '<table class="table table-striped table-sm">'
puts fct_html_sum
puts '<tr><td>&nbsp;</td></tr>'
fct_html.each do |e| puts e end
puts "</table>"

puts "<div align='right'>#{code}</div>"
