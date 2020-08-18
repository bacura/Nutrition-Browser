#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser magic calc expand 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171119, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'calcex'


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
		frct_select = lp[9]
	else
		frct_select = lp[8]
	end

	return frct_select
end


#### 合計精密チェック
def accu_check( frct_accu, lp )
  accu_check = lp[11]
  accu_check = lp[12] if frct_accu == 1

  return accu_check
end


#### 予想重量チェック
def ew_check( ew_mode, lp )
  ew_check = lp[13]
  ew_check = lp[14] if ew_mode == 1

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
frct_mode = get['frct_mode']
frct_accu = get['frct_accu']
palette = get['palette']
ew_mode = get['ew_mode']
lp = lp_init( script, language )


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


#### SUMからデータを抽出
r = mdb( "SELECT code, name, sum, dish from #{$MYSQL_TB_SUM} WHERE user='#{uname}';", false, @debug )
recipe_name = r.first['name']
code = r.first['code']
dish_num = r.first['dish'].to_i
food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, ew_mode )


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


#### 成分項目の抽出
fct_item = []
$FCT_ITEM.size.times do |c|
	fct_item << $FCT_ITEM[c] if palette_set[c] == 1
end


#### 食品番号から食品成分と名前を抽出
fct = []
fct_name = []
db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )

#### 食品成分データの抽出
food_no.each do |e|
	fct_tmp = []
	if e == '-'
		fct << '-'
		fct_name << '-'
	elsif e == '+'
		fct << '+'
		fct_name << '+'
	elsif e == '00000'
		fct << '0'
		fct_name << '0'
	else
		if /P|U/ =~ e
			q = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{uname}' OR user='#{$GM}' );"
		else
			q = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{e}';"
		end
		r = db.query( q )
		fct_name << r.first['Tagnames']
		$FCT_ITEM.size.times do |c|
			fct_tmp << r.first[$FCT_ITEM[c]] if palette_set[c] == 1
		end
		fct << Marshal.load( Marshal.dump( fct_tmp ))
	end
end


#### 名前の書き換え
if true
	food_no.size.times do |c|
 		unless food_no[c] == '+' || food_no[c] == '-' || food_no[c] == '0'
			q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}';"
			q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}' AND ( user='#{uname}' OR user='#{$GM}' );" if /P|U/ =~ food_no[c]
			r = db.query( q )
			fct_name[c] = bind_tags( r ) if r.first
		end
	end
end
db.close


#### データ計算
fct_sum = []
fct_item.size.times do |c| fct_sum << BigDecimal( 0 ) end

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
fct_sum = adjust_digit( fct_item, fct_sum, frct_mode )


#### HTML食品成分表の生成
fct_html = ''
fct_html << '<table class="table table-striped table-sm">'

# 項目名
fct_html << '    <tr>'
fct_html << "      <th align='center' width='6%' class='fct_item'>#{lp[5]}</th>"
fct_html << "      <th align='center' width='20%' class='fct_item'>#{lp[6]}</th>"
fct_html << "      <th align='center' width='4%' class='fct_item'>#{lp[7]}</th>"

fct_item.size.times do |cc|
	fct_no = fct_item[cc]
	if $FCT_NAME[fct_no]
		fct_html << "      <th align='center' width='5%' class='fct_item'>#{$FCT_NAME[fct_no]}</th>"
	else
		fct_html << "      <th align='center' width='5%' class='fct_item'>&nbsp;</th>"
	end
end
fct_html << '    </tr>'

# 単位
fct_html << '    <tr>'
fct_html << '      <td colspan="2" align="center"></td>'
fct_html << "      <td align='center' class='fct_unit'>( g )</td>"
fct_item.size.times do |cc|
	fct_no = fct_item[cc]
	if $FCT_UNIT[fct_no]
		fct_html << "      <td align='center' class='fct_unit' nowrap>( #{$FCT_UNIT[fct_no]} )</td>"
	else
		fct_html << "      <td align='center' class='fct_unit'>&nbsp;</td>"
	end
end
fct_html << '    </tr>'

# 各成分値
food_no.size.times do |cc|
	unless food_no[cc] == '-' || food_no[cc] == '+'
		fct_html << '    <tr>'
		fct_html << "      <td align='center' nowrap>#{food_no[cc]}</td>"
		fct_html << "      <td nowrap>#{fct_name[cc]}</td>"
		fct_html << "      <td align='right' nowrap>#{food_weight[cc].to_f}</td>"
		fct_item.size.times do |ccc|
			fct_no = ccc
			fct_html << "      <td align='right' nowrap>#{fct[cc][fct_no]}</td>"
		end
		fct_html << '    </tr>'
	end
end

# 合計値
fct_html << '    <tr>'
fct_html << "      <td colspan='2' align='center' class='fct_sum'>#{lp[4]}</td>"
fct_html << "      <td align='right' class='fct_sum'>#{total_weight.to_f}</td>"
fct_item.size.times do |cc|
	fct_no = cc
	if fct_item[fct_no] == 'REFUSE' || fct_item[fct_no] == 'WCR' || fct_item[fct_no] == 'Notice'
		fct_html << "      <td></td>"
	else
		fct_html << "      <td align='right' class='fct_sum' nowrap>#{fct_sum[fct_no]}</td>"
	end
end
fct_html << '    </tr>'
fct_html << '</table>'
fct_html << '<br>'


#### 食品番号から食品成分を抽出
html = <<-"HTML"
<div>#{lp[1]}: #{recipe_name}</div>
<div>#{lp[2]}: #{ew_check} #{lp[3]}： #{frct_select} / #{accu_check}</div>
<br>
#{fct_html}

<div align='right' class='code'>#{code}</div>"

HTML

puts html

html_foot()
