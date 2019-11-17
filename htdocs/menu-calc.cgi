#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser magic menu calc 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171218, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
fct_num = 14
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
lp = lp_init( 'menu-calc', language )
if @debug
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "<hr>"
end


#### Getting POST data
command = cgi['command']
code = cgi['code']
ew_mode = cgi['ew_mode']
frct_mode = cgi['frct_mode']
frct_accu = cgi['frct_accu']
palette = cgi['palette']


if ew_mode == nil || ew_mode == ''
	r = mariadb( "SELECT calcc FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
	if r.first && r.first['calcc'] != nil
		a = r.first['calcc'].split( ':' )
		ew_mode = a[0].to_i
		frct_mode = a[1].to_i
		frct_accu = a[2].to_i
	else
		ew_mode = 0
		frct_mode = 0
		frct_accu = 0
	end
end

ew_mode = ew_mode.to_i
frct_mode = frct_mode.to_i
frct_accu = frct_accu.to_i
palette = 0 if palette == nil
palette = palette.to_i
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "ew_mode: #{ew_mode}<br>"
	puts "frct_mode: #{frct_mode}<br>"
	puts "frct_accu: #{frct_accu}<br>"
	puts "palette: #{palette}<br>"
	puts "<hr>"
end


#### Checking SELECT & CHECK
frct_select = frct_select( frct_mode )
accu_check = accu_check( frct_accu )
ew_check = ew_check( ew_mode )


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


# HTMLパレットの生成
palette_html = ''
$PALETTE.size.times do |c|
	if palette == c
		palette_html << "<option value='#{c}' SELECTED>#{$PALETTE_NAME[c]}</option>"
	else
		palette_html << "<option value='#{c}'>#{$PALETTE_NAME[c]}</option>"
	end
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
fct_html = []
recipe_name = []
total_total_weight = 0

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
	table_num = fct_item.size / fct_num + 1
	table_num.times do |c|
		fct_html[rc] << "<h6>#{recipe_name[rc]}</h6>"
		fct_html[rc] << '<table class="table table-striped table-sm">'

		# 項目名
		fct_html[rc] << '    <tr>'
		fct_html[rc] << "      <th align='center' width='6%' class='fct_item'>#{lp[1]}</th>"
		fct_html[rc] << "      <th align='center' width='20%' class='fct_item'>#{lp[2]}</th>"
		fct_html[rc] << "      <th align='center' width='4%' class='fct_item'>#{lp[3]}</th>"
		fct_num.times do |cc|
			fct_no = fct_item[( c * fct_num ) + cc]
			if $FCT_NAME[fct_no]
				fct_html[rc] << "      <th align='center' width='5%' class='fct_item'>#{$FCT_NAME[fct_no]}</th>"
			else
				fct_html[rc] << "      <th align='center' width='5%' class='fct_item'>&nbsp;</th>"
			end
		end
		fct_html[rc] << '    </tr>'

		# 単位
		fct_html[rc] << '    <tr>'
		fct_html[rc] << '      <td colspan="2" align="center"></td>'
		fct_html[rc] << "      <td align='center' class='fct_unit'>( g )</td>"
		fct_num.times do |cc|
			fct_no = fct_item[( c * fct_num ) + cc]
			if $FCT_UNIT[fct_no]
				fct_html[rc] << "      <td align='center' class='fct_unit'>( #{$FCT_UNIT[fct_no]} )</td>"
			else
				fct_html[rc] << "      <td align='center' class='fct_unit'>&nbsp;</td>"
			end
		end
		fct_html[rc] << '    </tr>'

		# 各成分値
		food_no.size.times do |cc|
			unless food_no[cc] == '-' || food_no[cc] == '+'
				fct_html[rc] << '    <tr>'
				fct_html[rc] << "      <td align='center'>#{food_no[cc]}</td>"
				fct_html[rc] << "      <td>#{fct_name[cc]}</td>"
				fct_html[rc] << "      <td align='right'>#{food_weight[cc].to_f}</td>"
				fct_num.times do |ccc|
					fct_no = ( c * fct_num ) + ccc
					fct_html[rc] << "      <td align='right'>#{fct[cc][fct_no]}</td>"
				end
				fct_html[rc] << '    </tr>'
			end
		end

		# 合計値
		fct_html[rc] << '    <tr>'
		fct_html[rc] << "      <td colspan='2' align='center' class='fct_sum'>#{lp[4]}</td>"
		fct_html[rc] << "      <td align='right' class='fct_sum'>#{total_weight.to_f}</td>"
		total_sum.size.times do |cc|
			fct_no = ( c * fct_num ) + cc
			if fct_item[fct_no] == 'REFUSE' || fct_item[fct_no] == 'WCR' || fct_item[fct_no] == 'Notice'
				fct_html[rc] << "      <td></td>"
			else
				fct_html[rc] << "      <td align='right' class='fct_sum'>#{fct_sum[fct_no].to_f}</td>"
			end
		end
		fct_html[rc] << '    </tr>'

		fct_html[rc] << '</table>'
		fct_html[rc] << '<br>'
	end
	rc += 1
end


#### ダウンロード名設定
if meal_name != nil && meal_name != ''
	dl_name = "calc-#{meal_name}"
elsif code != nil && code != ''
	dl_name = "calc-#{code}"
else
	dl_name = "calc-table"
end


#### 食品番号から食品成分を抽出
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[5]}: #{meal_name}</h5></div>
	</div>
	<div class="row">
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="palette">#{lp[6]}</label>
				</div>
				<select class="form-control" id="palette" onchange="menuRecalcView_BWL2('#{code}')">
					#{palette_html}
				</select>
			</div>
		</div>
		<div class='col-3' align='center'>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="frct_accu" value="1" #{accu_check} onchange="menuRecalcView_BWL2('#{code}')">#{lp[7]}
			</div>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="ew_mode" value="1" #{ew_check} onchange="menuRecalcView_BWL2('#{code}')">#{lp[8]}
			</div>
		</div>
		<div class='col-2'>
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="">#{lp[9]}</label>
				</div>
				<select class="form-control" id="frct_mode" onchange="menuRecalcView_BWL2('#{code}')">
					<option value="1"#{frct_select[0]}>#{lp[10]}</option>
					<option value="2"#{frct_select[1]}>#{lp[11]}</option>
					<option value="3"#{frct_select[2]}>#{lp[12]}</option>
				</select>
			</div>
		</div>

		<div class='col-1'>
			<button class="btn btn-outline-primary btn-sm" onclick="menuRecalcView_BWL2('#{code}')">#{lp[13]}</button>&nbsp;
		</div>
		<div class='col-3'>
			<a href='menu-calcex.cgi?uname=#{uname}&code=#{code}&frct_mode=#{frct_mode}&frct_accu=#{frct_accu}&palette=#{palette}&ew_mode=#{ew_mode}' target='menu-calc-ex'><button type='button' class='btn btn-primary btn-sm'>#{lp[14]}</button></a>&nbsp;
			<a href='plain-menu-calc.cgi?uname=#{uname}&code=#{code}&frct_mode=#{frct_mode}&frct_accu=#{frct_accu}&palette=#{palette}&ew_mode=#{ew_mode}' download='#{dl_name}.txt'><button type='button' class='btn btn-primary btn-sm'>#{lp[15]}</button></a>
		</div>
    </div>
</div>
<br>
HTML


#### 大合計値の桁処理
total_sum.map! do |a| a.to_f / 1000 end
total_sum.size.times do |fi|
	total_sum[fi] = total_sum[fi].round( $FCT_FRCT[fct_item[fi]] ) if $FCT_FRCT[fct_item[fi]] != nil
end


#### HTML食品成分全合計
fct_html_sum = ''
table_num = fct_item.size / fct_num + 1
table_num.times do |c|
	fct_html_sum << '<table class="table table-striped table-sm">'

	# 項目名
	fct_html_sum << '    <tr>'
	fct_html_sum << '      <th align="center" width="6%" class="fct_item"></th>'
	fct_html_sum << '      <th align="center" width="20%" class="fct_item"></th>'
	fct_html_sum << "      <th align='center' width='4%' class='fct_item'>#{lp[16]}</th>"
	fct_num.times do |cc|
		fct_no = fct_item[( c * fct_num ) + cc]
		if $FCT_NAME[fct_no]
			fct_html_sum << "      <th align='center' width='5%' class='fct_item'>#{$FCT_NAME[fct_no]}</th>"
		else
			fct_html_sum << "      <th align='center' width='5%' class='fct_item'>&nbsp;</th>"
		end
	end
	fct_html_sum << '    </tr>'


	# 単位
	fct_html_sum << '    <tr>'
	fct_html_sum << '      <td colspan="2" align="center"></td>'
	fct_html_sum << "      <td align='center' class='fct_unit'>( g )</td>"
	fct_num.times do |cc|
		fct_no = fct_item[( c * fct_num ) + cc]
		if $FCT_UNIT[fct_no]
			fct_html_sum << "      <td align='center' class='fct_unit'>( #{$FCT_UNIT[fct_no]} )</td>"
		else
			fct_html_sum << "      <td align='center' class='fct_unit'>&nbsp;</td>"
		end
	end
	fct_html_sum << '    </tr>'


	# 合計値
	fct_html_sum << '    <tr>'
	fct_html_sum << "      <td colspan='2' align='center' class='fct_sum'>#{lp[17]}</td>"
	fct_html_sum << "      <td align='right' class='fct_sum'>#{total_total_weight.to_f}</td>"
	total_sum.size.times do |cc|
		fct_no = ( c * fct_num ) + cc
		if fct_item[fct_no] == 'REFUSE' || fct_item[fct_no] == 'WCR' || fct_item[fct_no] == 'Notice'
			fct_html_sum << "      <td></td>"
		else
			fct_html_sum << "      <td align='right' class='fct_sum'>#{total_sum[fct_no].to_f}</td>"
		end
	end
	fct_html_sum << '    </tr>'

	fct_html_sum << '</table>'
end


puts html

puts fct_html_sum

fct_html.each do |e| puts e end

puts "<div align='right' class='code'>#{code}</div>"

#### Updating Calculation option
mariadb( "UPDATE #{$MYSQL_TB_CFG} SET calcc='#{palette}:#{ew_mode}:#{frct_mode}:#{frct_accu}' WHERE user='#{uname}';", false )
