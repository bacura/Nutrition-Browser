#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser plain menu calc 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171228, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'plain-menu-calc.cgi'
$DEBUG = false


#==============================================================================
#DEFINITION
#==============================================================================
#### 端数処理の選択
def frct_select( frct_mode, lp )
	frct_select = ''
	case frct_mode
	when 3
		frct_select = lp[1]
	when 2
		frct_select = lp[2]
	else
		frct_select = lp[3]
	end

	return frct_select
end


#### 合計精密チェック
def accu_check( frct_accu, lp )
  accu_check = lp[4]
  accu_check = lp[5] if frct_accu == 1

  return accu_check
end


#### 予想重量チェック
def ew_check( ew_mode, lp )
  ew_check = lp[6]
  ew_check = lp[7] if ew_mode == 1

  return ew_check
end


#==============================================================================
# Main
#==============================================================================
puts "Content-type: text/text\n\n"

lp = lp_init( 'plain-menu-calc', $DEFAULT_LP )

#### GETデータの取得
get = get_data()
uname = get['uname']
code = get['code']
ew_mode = get['ew_mode']
frct_mode = get['frct_mode']
frct_accu = get['frct_accu']
palette = get['palette']
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "<hr>"
	puts "command: #{command}<br>"
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


#### パレット
r = mariadb( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';", false )
if r.first
	r.each do |e|
		a = e['palette'].split( '' )
		a.map! do |x| x.to_i end
		$PALETTE << a
		$PALETTE_NAME << e['name']
	end
end
palette_set = $PALETTE[palette]


# 成分項目の抽出
fct_item = []
$FCT_ITEM.size.times do |c|
	fct_item << $FCT_ITEM[c] if palette_set[c] == 1
end


#### mealからデータを抽出
r = mariadb( "SELECT code, name, meal from #{$MYSQL_TB_MEAL} WHERE user='#{uname}';", false )
meal_name = r.first['name']
code = r.first['code']
meal = r.first['meal'].split( "\t" )
recipe_code = []
meal.each do |e| recipe_code << e end


#### 大合計の初期化
total_sum = []
fct_item.size.times do |c| total_sum[c] = 0 end
rc = 0
fct_txt = []
recipe_name = []
total_weight = 0
total_total_weight = 0


#### RECIPEからデータを抽出
recipe_code.each do |e|
	r = mariadb( "SELECT name, sum, dish from #{$MYSQL_TB_RECIPE} WHERE code='#{e}';", false )
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
		elsif ee == '+'
			fct << '+'
		elsif ee == '00000'
			fct << '0'
		else
			if /P|U/ =~ ee
				query = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{ee}' AND ( user='#{uname}' OR user='#{$GM}' );"
			else
				query = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{ee}';"
			end
			res = db.query( query )
			fct_name << res.first['Tagnames']
			$FCT_ITEM.size.times do |c|
				fct_tmp << res.first[$FCT_ITEM[c]] if palette_set[c] == 1
			end
			fct << Marshal.load( Marshal.dump( fct_tmp ))
		end
	end

	# 名前の書き換え
	if false
		food_no.size.times do |c|
			q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}';"
			q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}' AND user='#{uname}';" if /^U\d{5}/ =~ food_no[c]
			r = db.query( q )
			fct_name[c] = bind_tags( r ) if r.first
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
	fct_txt[rc] = ''
	fct_txt[rc] << "#{recipe_name[rc]}\n"

	# 項目名
	fct_txt[rc] << lp[8]
	fct_item.each do |ee|
		if $FCT_NAME[ee]
			fct_txt[rc] << "\t#{$FCT_NAME[ee]}"
		else
			fct_txt[rc] << "\t"
		end
	end
	fct_txt[rc] << "\n"

	# 単位
	fct_txt[rc] << "\t\t\t( g )"
	fct_item.each do |ee|
		if $FCT_UNIT[ee]
			fct_txt[rc] << "\t( #{$FCT_UNIT[ee]} )"
		else
			fct_txt[rc] << "\t"
		end
	end
	fct_txt[rc] << "\n"

	# 各成分値
	food_no.size.times do |c|
		unless food_no[c] == '-' || food_no[c] == '+'
			fct_txt[rc] << "\t#{food_no[c]}\t#{fct_name[c]}\t#{food_weight[c].to_f}"
			fct_item.size.times do |cc|
				fct_txt[rc] << "\t#{fct[c][cc]}"
			end
		end
		fct_txt[rc] << "\n"
	end

	# 合計値
	fct_txt[rc] << "\t\t#{lp[9]}\t#{total_weight.to_f}"
	fct_item.size.times do |c|
		if fct_item[c] == 'REFUSE' || fct_item[c] == 'WCR' || fct_item[c] == 'Notice'
			fct_txt[rc] << "\t"
		else
			fct_txt[rc] << "\t#{fct_sum[c]}"
		end
	end
	fct_txt[rc] << "\n\n"

	rc += 1
end


#### 大合計値の桁処理
total_sum.map! do |a| a.to_f / 1000 end
total_sum.size.times do |fi|
	total_sum[fi] = total_sum[fi].round( $FCT_FRCT[fct_item[fi]] ) if $FCT_FRCT[fct_item[fi]] != nil
end


#### HTML食品成分全合計
fct_txt_sum = ''

# 項目名
fct_txt_sum << "\t\t\t#{lp[10]}\t"
fct_item.each do |e|
	if $FCT_NAME[e]
		fct_txt_sum << "#{$FCT_NAME[e]}\t"
	else
		fct_txt_sum << "\t"
	end
end
fct_txt_sum.chop!
fct_txt_sum << "\n"

# 単位
fct_txt_sum << "\t\t\tg\t"
fct_item.each do |e|
	if $FCT_UNIT[e]
		fct_txt_sum << "#{$FCT_UNIT[e]}\t"
	else
		fct_txt_sum << "\t"
	end
end
fct_txt_sum.chop!
fct_txt_sum << "\n"

# 合計値
fct_txt_sum << "\t\t#{lp[11]}\t#{total_weight.to_f}\t"
fct_item.size.times do |c|
	if fct_item[c] == 'REFUSE' || fct_item[c] == 'WCR' || fct_item[c] == 'Notice'
		fct_txt_sum << "\t"
	else
		fct_txt_sum << "#{total_sum[c]}\t"
	end
end
fct_txt_sum.chop!
fct_txt_sum << "\n"


#### 食品番号から食品成分を表示
puts "#{lp[12]} #{meal_name}\t#{lp[13]} #{code}\t#{lp[14]} #{ew_check}\t#{lp[15]} #{frct_select} / #{accu_check}\n".encode( 'Shift_JIS' )
fct_txt.each do |e| puts e.encode( 'Shift_JIS' ) end
puts fct_txt_sum.encode( 'Shift_JIS' )
