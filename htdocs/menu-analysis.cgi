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
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false


#==============================================================================
#DEFINITION
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
lp = lp_init( 'menu-analysis', language )
if @debug
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
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "ew_mode: #{ew_mode}<br>"
	puts "frct_mode: #{frct_mode}<br>"
	puts "frct_accu: #{frct_accu}<br>"
	puts "<hr>"
end


#### セレクト＆チェック設定
frct_select = frct_select( frct_mode )
accu_check = accu_check( frct_accu )
ew_check = ew_check( ew_mode )


# 成分項目の抽出
fct_item = ['ENERC_KCAL', 'PROT', 'FAT', 'NACL_EQ']


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
recipe_name = []
total_total_weight = 0
food_no_list = []
food_weight_list = []
animal_protein = BigDecimal( 0 )
grain_energy = BigDecimal( 0 )
recipe_code.each do |e|
	# RECIPEからデータを抽出
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
		r = mariadb( "SELECT gycv FROM #{$MYSQL_TB_EXT} WHERE FN='#{pseudo_id}#{food_no_list[c]}';", false )
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
		elsif ( food_no_list[c].to_i >= 17007 && food_no_list[c].to_i <= 17011 ) || ( food_no_list[c].to_i >= 17086 && food_no_list[c].to_i <= 17088 )
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
	dl_name = "analysis-#{meal_name}"
elsif code != nil && code != ''
	dl_name = "analysis-#{code}"
else
	dl_name = "analysis-table"
end


#### 食品番号から食品成分を抽出
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: #{meal_name}</h5></div>
	</div>
	<div class="row">
		<div class='col-4' align='center'>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="frct_accu" value="1" #{accu_check} onchange="menuReAnalysis_BWL2('#{code}')">#{lp[2]}
			</div>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="ew_mode" value="1" #{ew_check} onchange="menuReAnalysis_BWL2('#{code}')">#{lp[3]}
			</div>
		</div>
		<div class='col-2'>
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="">#{lp[4]}</label>
				</div>
				<select class="form-control" id="frct_mode" onchange="menuReAnalysis_BWL2('#{code}')">
					<option value="1"#{frct_select[0]}>#{lp[5]}</option>
					<option value="2"#{frct_select[1]}>#{lp[6]}</option>
					<option value="3"#{frct_select[2]}>#{lp[7]}</option>
				</select>
			</div>
		</div>

		<div class='col-4'></div>
		<div class='col-2'>
			<a href='plain-menu-analysis.cgi?uname=#{uname}&code=#{code}&frct_mode=#{frct_mode}&frct_accu=#{frct_accu}&ew_mode=#{ew_mode}' download='#{dl_name}.txt'><button type='button' class='btn btn-primary btn-sm'>#{lp[8]}</button></a>
		</div>
    </div>
</div>
<br>
<div class='table-responsive-sm'>
	<table class="table table-bordered table-sm">
		<tbody>
		<tr><th width="20%" rowspan='24'>#{lp[9]}</th><th width="25%">#{lp[10]}</th><td width="15%">#{g1.to_f}</td></tr>
		<tr><th>#{lp[11]}</th><td>#{g2.to_f}</td></tr>
		<tr><th>#{lp[12]}</th><td>#{g3.to_f}</td></tr>
		<tr><th>#{lp[13]}</th><td>#{g4.to_f}</td></tr>
		<tr><th>#{lp[14]}</th><td>#{g5.to_f}</td></tr>
		<tr><th rowspan="2">#{lp[15]}</th><td rowspan="2">#{g6.to_f}</td><th width="25%">#{lp[16]}</th><td>#{gycv.to_f}</td></tr>
				<tr><th>#{lp[17]}</th><td>#{wcv.to_f}</td></tr>
		<tr><th>#{lp[18]}</th><td>#{g7.to_f}</td></tr>
		<tr><th>#{lp[19]}</th><td>#{g8.to_f}</td></tr>
		<tr><th>#{lp[20]}</th><td>#{g9.to_f}</td></tr>
		<tr><th>#{lp[21]}</th><td>#{g10.to_f}</td></tr>
		<tr><th>#{lp[22]}</th><td>#{g11.to_f}</td></tr>
		<tr><th>#{lp[23]}</th><td>#{g12.to_f}</td></tr>
		<tr><th rowspan="2">#{lp[24]}</th><td rowspan="2">#{g13.to_f}</td><th>#{lp[25]}</th><td>#{milk_liquid.to_f}</td></tr>
				<tr><th>#{lp[26]}</th><td>#{milk_product.to_f}</td></tr>
		<tr><th>#{lp[27]}</th><td>#{g14.to_f}</td></tr>
		<tr><th>#{lp[28]}</th><td>#{g15.to_f}</td></tr>
		<tr><th>#{lp[29]}</th><td>#{g16.to_f}</td></tr>
		<tr><th rowspan="4">#{lp[30]}</th><td rowspan="4">#{g17.to_f}</td><th>#{lp[31]}</th><td>#{miso.to_f}</td></tr>
			<tr><th>#{lp[32]}</th><td>#{shoyu.to_f}</td></tr>
			<tr><th>#{lp[33]}</th><td>#{salt.to_f}</td></tr>
			<tr><th>#{lp[34]}</th><td>#{seasoning.to_f}</td></tr>
		<tr><th>#{lp[35]}</th><td>#{g18.to_f}</td></tr>
		<tr><th>#{lp[36]}</th><td>#{g_total.to_f}</td></tr>
		<tr><th rowspan='3'>#{lp[37]}</th><th>#{lp[38]}</th><td>#{pfc_p.to_f}</td></tr>
			<th>#{lp[39]}</th><td>#{pfc_f.to_f}</td></tr>
			<th>#{lp[40]}</th><td>#{pfc_c.to_f}</td></tr>
		<tr><th rowspan='2'>#{lp[41]}</th><th>#{lp[42]}</th><td>#{grain_energy_rate.to_f}</td></tr>
			<th>#{lp[43]}</th><td>#{animal_protein_rate.to_f}</td></tr>
		</tbody>
	</table>
</div>
HTML

puts html
puts "<div align='right' class='code'>#{code}</div>"
