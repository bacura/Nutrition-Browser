#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser menu basic analysis 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190218, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'plain-menu-analysis'


#==============================================================================
#DEFINITION
#==============================================================================

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

lp = lp_init( 'plain-menu-analysis', $DEFAULT_LP )

#### GETデータの取得
get = get_data()
uname = get['uname']
code = get['code']
frct_mode = get['frct_mode']
frct_accu = get['frct_accu']
ew_mode = get['ew_mode']

ew_mode = 0 if ew_mode == nil
ew_mode = ew_mode.to_i
frct_mode = 0 if frct_mode == nil
frct_mode = frct_mode.to_i
frct_accu = 0 if frct_accu == nil
frct_accu = frct_accu.to_i


#### セレクト＆チェック設定
frct_select = frct_select( frct_mode, lp )
accu_check = accu_check( frct_accu, lp )
ew_check = ew_check( ew_mode, lp )


# 成分項目の抽出
fct_item = ['ENERC_KCAL', 'PROT', 'FAT', 'NACL_EQ']


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
recipe_name = []
total_total_weight = 0
food_no_list = []
food_weight_list = []
animal_protein = BigDecimal( 0 )
grain_energy = BigDecimal( 0 )
recipe_code.each do |e|
	# RECIPEからデータを抽出
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
		elsif ee == '+'
			fct << '+'
		elsif ee == '00000'
			fct << '0'
		else
			if /P|U/ =~ ee
				q = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{ee}' AND ( user='#{uname}' OR user='#{$GM}' );"
			else
				q = "SELECT * from #{$MYSQL_TB_FCT} WHERE FN='#{ee}';"
			end
			r = db.query( q )
			fct_name << r.first['Tagnames']
			food_no_list << ee
			fct_item.each do |eee| fct_tmp << r.first[eee] end
			fct << Marshal.load( Marshal.dump( fct_tmp ))
		end
	end

	#### 食品重量計算
	fct_sum = []
	protein = BigDecimal( 0 )
	energy = BigDecimal( 0 )
	fct_item.size.times do |c| fct_sum << BigDecimal( 0 ) end
	food_no.size.times do |fn|
		unless food_no[fn] == '-' || food_no[fn] == '+'
			fct_item.size.times do |fi|
				t = convert_zero( fct[fn][fi] )
				# 通常計算
				fct[fn][fi] = num_opt( t, food_weight[fn], frct_mode, $FCT_FRCT[fct_item[fi]] )
				if frct_accu == 0
					# 通常計算
					fct_sum[fi] += BigDecimal( fct[fn][fi] )

					#動物性たんぱく質カウント用
					protein = BigDecimal( fct[fn][fi] ) if fi == 1

					# 穀類エネルギーカウント用
					energy = BigDecimal( fct[fn][fi] ) if fi == 0
				else
					# 精密計算
					fct_sum[fi] += BigDecimal( num_opt( t, food_weight[fn], frct_mode, $FCT_FRCT[fct_item[fi]] + 3 ))

					#動物性たんぱく質カウント用
					protein = BigDecimal( num_opt( t, food_weight[fn], frct_mode, $FCT_FRCT[fct_item[fi]] + 3 )) if fi == 1

					# 穀類エネルギーカウント用
					energy = BigDecimal( num_opt( t, food_weight[fn], frct_mode, $FCT_FRCT[fct_item[fi]] + 3 )) if fi == 0
				end
			end
			# 食品構成用重量カウント
			food_weight_list << food_weight[fn]

			# 動物性たんぱく質カウント
			tt = food_no[fn]
			tt.slice!( 0 ) if /P|U/ =~ tt
			food_group = tt.slice( 0, 2 )
			animal_protein += protein if food_group.to_i >= 10 && food_group.to_i <= 13

			# 穀類エネルギーカウント
			tt = food_no[fn]
			tt.slice!( 0 ) if /P|U/ =~ tt
			food_group = tt.slice( 0, 2 )
			grain_energy += energy if food_group == '01'
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
end


#### 大合計値の桁処理
total_sum.map! do |a| a.to_f / 1000 end
total_sum.size.times do |fi|
	total_sum[fi] = total_sum[fi].round( $FCT_FRCT[fct_item[fi]] ) if $FCT_FRCT[fct_item[fi]] != nil
end


#### 食品構成のカウント
g1 = 0
g2 = 0
g3 = 0
g4 = 0
g5 = 0
g6 = 0
g7 = 0
g8 = 0
g9 = 0
g10 = 0
g11 = 0
g12 = 0
g13 = 0
g14 = 0
g15 = 0
g16 = 0
g17 = 0
g18 = 0
g_total = 0
wcv = 0
gycv = 0
milk_liquid = 0
milk_product = 0
salt = 0
miso = 0
shoyu = 0
seasoning = 0

food_no_list.size.times do |c|
	pseudo_id = ''
	pseudo_id = food_no_list[c].slice!( 0 ) if /P|U/ =~ food_no_list[c]
	food_group = food_no_list[c].slice( 0, 2 )

	case food_group
	when '01'
		g1 += food_weight_list[c]
	when '02'
		g2 += food_weight_list[c]
	when '03'
		g3 += food_weight_list[c]
	when '04'
		g4 += food_weight_list[c]
	when '05'
		g5 += food_weight_list[c]
	when '06'
		g6 += food_weight_list[c]

		# 緑黄色野菜の判定
		r = mdb( "SELECT gycv FROM #{$MYSQL_TB_EXT} WHERE FN='#{pseudo_id}#{food_no_list[c]}';", false, @debug )
		if r.first['gycv'] == 1
			gycv += food_weight_list[c]
		else
			wcv += food_weight_list[c]
		end
	when '07'
		g7 += food_weight_list[c]
	when '08'
		g8 += food_weight_list[c]
	when '09'
		g9 += food_weight_list[c]
	when '10'
		g10 += food_weight_list[c]
	when '11'
		g11 += food_weight_list[c]
	when '12'
		g12 += food_weight_list[c]
	when '13'
		g13 += food_weight_list[c]

		# 牛乳と乳製品の判定
		if food_no_list[c].to_i >= 13001 && food_no_list[c].to_i <= 13006
			milk_liquid += food_weight_list[c]
		else
			milk_product += food_weight_list[c]
		end
	when '14'
		g14 += food_weight_list[c]
	when '15'
		g15 += food_weight_list[c]
	when '16'
		g16 += food_weight_list[c]
	when '17'
		# 液体だしの乾燥重量化
		if food_no_list[c].to_i >= 17019 && food_no_list[c].to_i <= 17025
			food_weight_list[c] = food_weight_list[c] / 100 * 1.0
		elsif food_no_list[c].to_i == 17026
			food_weight_list[c] = food_weight_list[c] / 100 * 2.5
		end
		g17 += food_weight_list[c]

		# 塩の判定
		if ( food_no_list[c].to_i >= 17012 && food_no_list[c].to_i <= 17014 ) || food_no_list[c].to_i == 17089
			salt += food_weight_list[c]
		# 味噌の判定
		elsif ( food_no_list[c].to_i >= 17044 && food_no_list[c].to_i <= 17050 ) || food_no_list[c].to_i == 17119 || food_no_list[c].to_i == 17120
			miso += food_weight_list[c]
		# 醤油の判定
		elsif food_no_list[c].to_i >= 17055 && food_no_list[c].to_i <= 17062
			shoyu += food_weight_list[c]
		else
			seasoning += food_weight_list[c]
		end
	when '18'
		g18 += food_weight_list[c]
	end
end
g_total = g1 + g2 + g3 + g4 + g5 + g6 + g7 + g8 + g9 + g10 + g11 + g12 + g13 + g14 + g15 + g16 + g17 + g18


#### PFC比
pfc_p = ( total_sum[1] * 4 / total_sum[0] * 100 )
pfc_f = ( total_sum[2] * 9 / total_sum[0] * 100 )
case frct_mode
# 四捨五入
when 1
	pfc_p = pfc_p.round( 1 )
	pfc_f = pfc_f.round( 1 )
# 切り上げ
when 2
	pfc_p = pfc_p.ceil( 1 )
	pfc_f = pfc_f.ceil( 1 )
# 切り捨て
when 3
	pfc_p = pfc_p.floor( 1 )
	pfc_f = pfc_f.floor( 1 )
else
	pfc_p = pfc_p.round( 1 )
	pfc_f = pfc_f.round( 1 )
end
pfc_c = ( 100 - pfc_p - pfc_f ).round( 1 )


#### 動物性たんぱく質比
animal_protein_rate = ( animal_protein / total_sum[1] * 100 ).round( 1 )


#### 穀物総エネルギー比
grain_energy_rate = ( grain_energy / total_sum[0] * 100 ).round( 1 )


#### ダウンロード名設定
if meal_name != nil && meal_name != ''
	dl_name = "calc-#{meal_name}"
elsif code != nil && code != ''
	dl_name = "calc-#{code}"
else
	dl_name = "calc-table"
end


#### テキスト成形
analysis_text = ''
analysis_text << "#{lp[8]}\t#{lp[9]}\t#{g1.to_f}\n"
analysis_text << "\t#{lp[10]}\t#{g2.to_f}\n"
analysis_text << "\t#{lp[11]}\t#{g3.to_f}\n"
analysis_text << "\t#{lp[12]}\t#{g4.to_f}\n"
analysis_text << "\t#{lp[13]}\t#{g5.to_f}\n"
analysis_text << "\t#{lp[14]}\t#{g6.to_f}\t#{lp[15]}\t#{gycv.to_f}\n"
analysis_text << "\t\t\t#{lp[16]}\t#{wcv.to_f}\n"
analysis_text << "\t#{lp[17]}\t#{g7.to_f}\n"
analysis_text << "\t#{lp[18]}\t#{g8.to_f}\n"
analysis_text << "\t#{lp[19]}\t#{g9.to_f}\n"
analysis_text << "\t#{lp[20]}\t#{g10.to_f}\n"
analysis_text << "\t#{lp[21]}\t#{g11.to_f}\n"
analysis_text << "\t#{lp[22]}\t#{g12.to_f}\n"
analysis_text << "\t#{lp[23]}\t#{g13.to_f}\t#{lp[24]}\t#{milk_liquid.to_f}\n"
analysis_text << "\t\t\t#{lp[25]}\t#{milk_product.to_f}\n"
analysis_text << "\t#{lp[26]}\t#{g14.to_f}\n"
analysis_text << "\t#{lp[27]}\t#{g15.to_f}\n"
analysis_text << "\t#{lp[28]}\t#{g16.to_f}\n"
analysis_text << "\t#{lp[29]}\t#{g17.to_f}\t#{lp[30]}\t#{miso.to_f}\n"
analysis_text << "\t\t\t#{lp[31]}\t#{shoyu.to_f}\n"
analysis_text << "\t\t\t#{lp[32]}\t#{salt.to_f}\n"
analysis_text << "\t\t\t#{lp[33]}\t#{seasoning.to_f}\n"
analysis_text << "\t#{lp[34]}\t#{g18.to_f}\n"
analysis_text << "\t#{lp[35]}\t#{g_total.to_f}\n"
analysis_text << "#{lp[36]}\t#{lp[37]}\t#{pfc_p.to_f}\n"
analysis_text << "\t\t\t#{lp[38]}\t#{pfc_f.to_f}\n"
analysis_text << "\t\t\t#{lp[39]}\t#{pfc_c.to_f}\n"
analysis_text << "#{lp[40]}\t#{lp[41]}\t#{grain_energy_rate.to_f}\n"
analysis_text << "\t\t\t#{lp[42]}\t#{animal_protein_rate.to_f}\n"

#### 食品番号から食品成分を表示
puts "#{lp[43]} #{meal_name}\t#{lp[44]} #{code}\t#{lp[45]} #{ew_check}\t#{lp[46]} #{frct_select} / #{accu_check}\n".encode( 'Shift_JIS' )
puts analysis_text.encode( 'Shift_JIS' )
