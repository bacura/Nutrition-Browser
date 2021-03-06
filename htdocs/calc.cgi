#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser magic calc 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171116, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
fct_num = 14
@degug = false
script = 'calc'


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
user = User.new( cgi )
user.debug if @debug
lp = user.language( script )

r = mdb( "SELECT icalc FROM cfg WHERE user='#{user.name}';", false, @debug )
fct_num = r.first['icalc'].to_i unless r.first['icalc'].to_i == 0


#### Getting POST data
command = cgi['command']
code = cgi['code']
ew_mode = cgi['ew_mode']
frct_mode = cgi['frct_mode']
frct_accu = cgi['frct_accu']
palette = cgi['palette']

if ew_mode == nil || ew_mode == ''
	r = mdb( "SELECT calcc FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';",false, @debug )
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


#### Extracting SUM data
r = mdb( "SELECT code, name, sum, dish from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
recipe_name = r.first['name']
code = r.first['code']
dish_num = r.first['dish'].to_i
food_no, food_weight, total_weight = extract_sum( r.first['sum'], dish_num, ew_mode )


#### Checking SELECT & CHECK
frct_select = frct_select( frct_mode )
accu_check = accu_check( frct_accu )
ew_check = ew_check( ew_mode )


#### Setting palette
palette_sets = []
palette_name = []
r = mdb( "SELECT * from #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}';", false, @debug )
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
			q = "SELECT * from #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{user.name}' OR user='#{$GM}' );"
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
			q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}' AND ( user='#{user.name}' OR user='#{$GM}' );" if /P|U/ =~ food_no[c]
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
fct_sum = adjust_digit( fct_item, fct_sum, frct_mode )


#### HTMLパレットの生成
palette_html = ''
palette_sets.size.times do |c|
	if palette == c
		palette_html << "<option value='#{c}' SELECTED>#{palette_name[c]}</option>"
	else
		palette_html << "<option value='#{c}'>#{palette_name[c]}</option>"
	end
end


#### HTML食品成分表の生成
fct_html = ''
table_num = fct_item.size / fct_num + 1
table_num.times do |c|
	fct_html << '<table class="table table-striped table-sm">'

	# 項目名
	fct_html << '    <tr>'
	fct_html << "      <th align='center' width='6%' class='fct_item'>#{lp[13]}</th>"
	fct_html << "      <th align='center' width='20%' class='fct_item'>#{lp[14]}</th>"
	fct_html << "      <th align='center' width='4%' class='fct_item'>#{lp[15]}</th>"
	fct_num.times do |cc|
		fct_no = fct_item[( c * fct_num ) + cc]
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
	fct_num.times do |cc|
		fct_no = fct_item[( c * fct_num ) + cc]
		if $FCT_UNIT[fct_no]
			fct_html << "      <td align='center' class='fct_unit'>( #{$FCT_UNIT[fct_no]} )</td>"
		else
			fct_html << "      <td align='center' class='fct_unit'>&nbsp;</td>"
		end
	end
	fct_html << '    </tr>'


	# 各成分値
	food_no.size.times do |cc|
		unless food_no[cc] == '-' || food_no[cc] == '+'
			fct_html << '    <tr>'
			fct_html << "      <td align='center'>#{food_no[cc]}</td>"
			fct_html << "      <td>#{fct_name[cc]}</td>"
			fct_html << "      <td align='right'>#{food_weight[cc].to_f}</td>"
			fct_num.times do |ccc|
				fct_no = ( c * fct_num ) + ccc
				fct_html << "      <td align='right'>#{fct[cc][fct_no]}</td>"
			end
			fct_html << '    </tr>'
		end
	end

	# 合計値
	fct_html << '    <tr>'
	fct_html << '      <td colspan="2" align="center" class="fct_sum">合計</td>'
	fct_html << "      <td align='right' class='fct_sum'>#{total_weight.to_f}</td>"
	fct_num.times do |cc|
		fct_no = ( c * fct_num ) + cc
		if fct_item[fct_no] == 'REFUSE' || fct_item[fct_no] == 'WCR' || fct_item[fct_no] == 'Notice'
			fct_html << "      <td></td>"
		else
			fct_html << "      <td align='right' class='fct_sum'>#{fct_sum[fct_no]}</td>"
		end
	end
	fct_html << '    </tr>'
	fct_html << '</table>'
	fct_html << '<br>'
end


#### ダウンロード名設定
if recipe_name != nil && recipe_name != ''
	dl_name = "calc-#{recipe_name}"
elsif code != nil && code != ''
	dl_name = "calc-#{code}"
else
	dl_name = "calc-table"
end


#### 食品番号から食品成分を抽出
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: #{recipe_name}</h5></div>
	</div>
	<div class="row">
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="palette">#{lp[2]}</label>
				<select class="form-select form-select-sm" id="palette" onchange="recalcView('#{code}')">
					#{palette_html}
				</select>
			</div>
		</div>
		<div class='col-3' align='left'>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="frct_accu" value="1" #{accu_check} onchange="recalcView('#{code}')">#{lp[3]}
			</div>
			<div class="form-check form-check-inline">
    			<input class="form-check-input" type="checkbox" id="ew_mode" value="1" #{ew_check} onchange="recalcView('#{code}')">#{lp[4]}
			</div>
		</div>
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="frct_mode">#{lp[5]}</label>
				<select class="form-select form-select-sm" id="frct_mode" onchange="recalcView('#{code}')">
					<option value="1"#{frct_select[0]}>#{lp[6]}</option>
					<option value="2"#{frct_select[1]}>#{lp[7]}</option>
					<option value="3"#{frct_select[2]}>#{lp[8]}</option>
				</select>
				<span onclick="recalcView('#{code}')">#{lp[9]}</span>&nbsp;
			</div>
		</div>

		<div class='col-1'></div>
		<div class='col-1'>
			<a href='plain-calc.cgi?uname=#{user.name}&code=#{code}&frct_mode=#{frct_mode}&frct_accu=#{frct_accu}&palette=#{palette}&ew_mode=#{ew_mode}' download='#{dl_name}.txt'>#{lp[11]}</a>
		</div>
		<div class='col-1'>
			<a href='calcex.cgi?uname=#{user.name}&code=#{code}&frct_mode=#{frct_mode}&frct_accu=#{frct_accu}&palette=#{palette}&ew_mode=#{ew_mode}' target='calc-ex'>#{lp[10]}</a>&nbsp;
		</div>
    </div>
</div>
<br>
#{fct_html}
<div align='right' class='code'>#{code}</div>

HTML

puts html

#### Updating Calculation option
mdb( "UPDATE #{$MYSQL_TB_CFG} SET calcc='#{palette}:#{ew_mode}:#{frct_mode}:#{frct_accu}' WHERE user='#{user.name}';", false, @debug )
