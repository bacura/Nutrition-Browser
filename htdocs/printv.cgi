#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser print web page 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20180312, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'
require 'rqrcode'

#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'print.cgi'
$DEBUG = false
fct_num = 14


#==============================================================================
#DEFINITION
#==============================================================================

#### QRコード生成
def makeQRcode( text, code )
	qrcode = RQRCode::QRCode.new( text )

	# With default options specified explicitly
	png = qrcode.as_png(
		resize_gte_to: false,
		resize_exactly_to: false,
		fill: 'white',
		color: 'black',
		size: 160,
		border_modules: 4,
		module_px_size: 6,
		file: nil # path to write
	)
	IO.write( "#{$PHOTO_PATH}/#{code}-qr.png", png.to_s )
end


#### 食材抽出
def extract_foods( sum, dish_recipe, dish, template, ew_mode )
	calc_weight = [ '単純換算g','予想摂取g' ]
	return_foods = "<table class='table table-sm'>\n"
	case template
	when 1, 2
		return_foods << "<thead><tr><th class='align_c'>食材</th><th class='align_r'>数量</th><th class='align_r'>単位</th></tr></thead>\n"
	when 3, 4
		return_foods << "<thead><tr><th class='align_c'>食材</th><th class='align_c'>備考</th><th class='align_r'>数量</th><th class='align_r'>単位</th></tr></thead>\n"
	when 5, 6
		return_foods << "<thead><tr><th>食品番号</th><th class='align_c'>食材</th><th class='align_c'>備考</th><th class='align_r'>数量</th><th class='align_r'>単位</th><th class='align_r'>#{calc_weight[ew_mode]}</th></tr></thead>\n"
	when 7, 8
		return_foods << "<thead><tr><th>食品番号</th><th class='align_c'>食材</th><th class='align_c'>備考</th><th class='align_r'>数量</th><th class='align_r'>単位</th><th class='align_r'>#{calc_weight[ew_mode]}</th><th class='align_r'>廃棄率%</th><th class='align_r'>発注量kg</th></tr></thead>\n"
	end
	db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
	a = sum.split( "\t" )
	a.each do |e|
		fn, fw, fu, fuv, fc, fi, frr, few = e.split( ':' )
		few = fw if few == nil

		if fn == '-'
			return_foods << "<tr><td></td></tr>\n"
		elsif fn == '+'
			return_foods << "<tr><td class='print_subtitle'>#{fi}</td></tr>\n"
		else
			# 人数分調整
			fuv = BigDecimal( fuv ) / dish_recipe * dish
			fuv_v = fuv.to_f
			fuv_v = fuv.to_i if fuv_v >= 10
			few = BigDecimal( few ) / dish_recipe
			few_v = few.to_f
			few_v = few.to_i if few_v >= 10

			# 単位補完
			fu = '0' if fu == 'g' || fu == ''
			fu = $UNIT[fu.to_i]

			query = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{fn}';"
			res = db.query( query )
			case template
			when 1, 2
  				class_add = ''
  				if /\+/ =~ res.first['class1']
    				class_add = "<span class='tagc'>#{res.first['class1'].sub( '+', '' )}</span> "
  				elsif /\+/ =~ res.first['class2']
    				class_add = "<span class='tagc'>#{res.first['class2'].sub( '+', '' )}</span> "
  				elsif /\+/ =~ res.first['class3']
    				class_add = "<span class='tagc'>#{res.first['class3'].sub( '+', '' )}</span> "
  				end
				return_foods << "<tr><td>#{class_add}#{res.first['name']}</td><td align='right'>#{fuv_v}</td><td align='right'>#{fu}</td></tr>\n" if res.first
			when 3, 4
				tags = bind_tags( res )
				return_foods << "<tr><td>#{tags}</td><td>#{fi}</td><td align='right'>#{fuv_v}</td><td align='right'>#{fu}</td></tr>\n" if res.first
			when 5, 6
				tags = bind_tags( res )
				return_foods << "<tr><td>#{fn}</td><td>#{tags}</td><td>#{fi}</td><td align='right'>#{fuv_v}</td><td align='right'>#{fu}</td><td align='right'>#{few_v}</td></tr>\n" if res.first
			when 7, 8
				tags = bind_tags( res )
				query = "SELECT REFUSE from #{$MYSQL_TB_FCT} WHERE FN='#{fn}';"
				res = db.query( query )
				t = ( BigDecimal( fw ) * BigDecimal( dish ) / ( 100 - res.first['REFUSE'].to_i ) / BigDecimal( 10 )).ceil( 2 ).to_f.to_s
				df = t.split( '.' )
				comp = ( 2 - df[1].size )
				comp.times do |c| df[1] = df[1] << '0' end
				ordering_weight = df[0] + '.' + df[1]
				return_foods << "<tr><td>#{fn}</td><td>#{tags}</td><td>#{fi}</td><td align='right'>#{fuv_v}</td><td align='right'>#{fu}</td><td align='right'>#{few_v}</td><td align='right'>#{res.first['REFUSE']}</td><td align='right'>#{ordering_weight}</td></tr>\n" if res.first
			end
		end
	end
	db.close
	return_foods << "</table>\n"

	return return_foods
end


#### プロトコール変換
def modify_protocol( protocol )
	return_protocol = "<ul>\n"
	a = protocol.split( "\n" )
	a.each do |e|
		if /^\#/ =~ e
			t = e.delete( '#' )
			return_protocol << "<span class='print_comment'>(#{t})</span><br>\n"
		elsif /^\@/ =~ e
			t = e.delete( '@' )
			return_protocol << "<span class='print_subtitle'>#{t}</span><br>\n"
		elsif /^\!/ =~ e
		elsif e == ''
			return_protocol << "<br>\n"
		else
			return_protocol << "<li>#{e}</li>\n"
		end
	end
	return_protocol << "</ul>\n"

	return return_protocol
end


#### 写真構成
def arrange_photo( code, fig1, fig2, fig3, hr_image )
	photo = []

	if fig1 == 1 && fig2 == 1 && fig3 == 1
		photo = [1, 2, 3]
	elsif fig1 == 1 && fig2 == 1 && fig3 == 0
		photo = [1, 2]
	elsif fig1 == 1 && fig2 == 0 && fig3 == 1
		photo = [1, 3]
	elsif fig1 == 0 && fig2 == 1 && fig3 == 1
		photo = [2, 3]
	elsif fig1 == 1 && fig2 == 0 && fig3 == 0
		photo = [1]
	elsif fig1 == 0 && fig2 == 1 && fig3 == 0
		photo = [2]
	elsif fig1 == 0 && fig2 == 0 && fig3 == 1
		photo = [3]
	else
		photo = []
	end

	return_photo = ''
	thumbnail = 'tn'
	thumbnail = '' if hr_image == 1


	case photo.size
	when 1
		return_photo << "<img src='photo/#{code}-#{photo[0]}#{thumbnail}.jpg' width='100%' height='100%' class='img-fluid rounded'>\n"
	when 2
		return_photo << "<img src='photo/#{code}-#{photo[0]}#{thumbnail}.jpg' width='100%' height='100%' class='img-fluid rounded'>\n"
		return_photo << "<img src='photo/#{code}-#{photo[1]}#{thumbnail}.jpg' width='100%' height='100%' class='img-fluid rounded'>\n"
	when 3
		return_photo << "<img src='photo/#{code}-#{photo[0]}#{thumbnail}.jpg' width='100%' height='100%' class='img-fluid rounded'>\n"
		return_photo << "<img src='photo/#{code}-#{photo[2]}#{thumbnail}.jpg' width='100%' height='100%' class='img-fluid rounded'>\n"
		return_photo << "<img src='photo/#{code}-#{photo[3]}#{thumbnail}.jpg' width='100%' height='100%' class='img-fluid rounded'>\n"
	else
	end

	return return_photo
end


#### 端数処理の選択
def frct_select( frct_mode )
	frct_select = ''
	case frct_mode
	when 3
		frct_select = '切り捨て'
	when 2
		frct_select = '切り上げ'
	else
		frct_select = '四捨五入'
	end

	return frct_select
end


#### 合計精密チェック
def accu_check( frct_accu )
  accu_check = '通常合計'
  accu_check = '精密合計' if frct_accu == 1

  return accu_check
end


#### 予想重量チェック
def ew_check( ew_mode )
  ew_check = '単純g'
  ew_check = '予想g' if ew_mode == 1

  return ew_check
end


#==============================================================================
# Main
#==============================================================================

html_init( nil )
html_head( nil, 0, '印刷表示' )

#### GETデータの取得
get_data = get_data()
code = get_data['c']
template = get_data['t'].to_i
dish = get_data['d'].to_i
palette = get_data['p'].to_i
frct_accu = get_data['fa'].to_i
ew_mode = get_data['ew'].to_i
frct_mode = get_data['fm'].to_i
hr_image = get_data['hr'].to_i

url = "http://fctb.bacura.jp/printv.cgi?c=#{code}&t=#{template}&d=#{dish}&p=#{palette}&fa=#{frct_accu}&ew=#{ew_mode}&fm=#{frct_mode}&hr=#{hr_image}"

#### デバッグ用
if $DEBUG
	puts "code: #{code}<br>"
	puts "template: #{template}<br>"
	puts "dish: #{dish}<br>"
	puts "url: #{url}<br>"
	puts "<hr>"
end


#### コードの読み込み
query = "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';"
db_err = 'select recipe code check'
res = db_process( query, db_err, false )
unless res.first
	puts "指定のレシピコード(#{code})は存在しません。"
	exit( 9 )
end
uname = res.first['user']
recipe_name = res.first['name']
sum = res.first['sum']
dish_recipe = res.first['dish'].to_i
protocol = res.first['protocol']
fig1 = res.first['fig1'].to_i
fig2 = res.first['fig2'].to_i
fig3 = res.first['fig3'].to_i
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "recipe_name: #{recipe_name}<br>"
	puts "sum: #{sum}<br>"
	puts "dish_recipe: #{dish_recipe}<br>"
	puts "protocol: #{protocol}<br>"
	puts "fig1: #{fig1}<br>"
	puts "fig2: #{fig2}<br>"
	puts "fig3: #{fig3}<br>"
	puts "<hr>"
end


#### 食材変換
foods = extract_foods( sum, dish_recipe, dish, template, ew_mode )
puts "foods: #{foods}<br>" if $DEBUG


#### プロトコール変換
protocol = modify_protocol( protocol )


#### 写真変換
photos = arrange_photo( code, fig1, fig2, fig3, hr_image )


#### デバッグ用
if $DEBUG
	puts "recipe_name: #{recipe_name}<br>"
	puts "dish_recipe: #{dish_recipe}<br>"
	puts "protocol: #{protocol}<br>"
	puts "fig1: #{fig1}<br>"
	puts "fig2: #{fig2}<br>"
	puts "fig3: #{fig3}<br>"
	puts "<hr>"
end


#### QR codeの生成
makeQRcode( url, code )


#### 食品番号から食品成分と名前を抽出
fct = []
fct_name = []
fct_sum = []
if template > 4
	# セレクト＆チェック設定
	frct_select = frct_select( frct_mode )
	accu_check = accu_check( frct_accu )
	ew_check = ew_check( ew_mode )

	# パレット
	palette_set = $PALETTE[palette]

	# 成分項目の抽出
	fct_item = []
	$FCT_ITEM.size.times do |c|
		fct_item << $FCT_ITEM[c] if palette_set[c] == 1
	end

	food_no, food_weight, total_weight = extract_sum( sum, dish_recipe, ew_mode )
	db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )

	# 食品成分データの抽出と名前の書き換え
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
			fct_name << res.first['Tagnames']
			$FCT_ITEM.size.times do |c|
				fct_tmp << res.first[$FCT_ITEM[c]] if palette_set[c] == 1
			end

			fct << Marshal.load( Marshal.dump( fct_tmp ))
		end
	end

	# 名前の書き換え
	if true
		food_no.size.times do |c|
			query = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}';"
			res = db.query( query )
			fct_name[c] = bind_tags( res ) if res.first
		end
	end
	db.close

	# データ計算
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

	# 合計値の桁合わせ
	fct_sum = adjust_digit( fct_item, fct_sum, frct_mode )
end

if template > 4
	fct_html = "<div class='fct_item'>#{frct_select} / #{accu_check} / #{ew_check}</div>\n"
	table_num = fct_item.size / fct_num + 1
	table_num.times do |c|
		fct_html << '<table class="table table-sm">'

		# 項目名
		fct_html << '<tr>'
		if template > 6
			fct_html << '<th align="center" width="6%" class="fct_item">食品番号</th>'
			fct_html << '<th align="center" width="20%" class="fct_item align_c">食品名</th>'
			fct_html << '<th align="center" width="4%" class="fct_item">重量</th>'
		end

		fct_num.times do |cc|
			fct_no = fct_item[( c * fct_num ) + cc]
			if $FCT_NAME[fct_no]
				fct_html << "<th align='center' width='5%' class='fct_item'>#{$FCT_NAME[fct_no]}</th>"
			else
				fct_html << "<th align='center' width='5%' class='fct_item'>&nbsp;</th>"
			end
		end
		fct_html << '</tr>'

		# 単位
		fct_html << '<tr>'
		if template > 6
			fct_html << '<td colspan="2" align="center"></td>'
			fct_html << "<td align='center' class='fct_unit'>( g )</td>"
		end
		fct_num.times do |cc|
			fct_no = fct_item[( c * fct_num ) + cc]
			if $FCT_UNIT[fct_no]
				fct_html << "<td align='center' class='fct_unit'>( #{$FCT_UNIT[fct_no]} )</td>"
			else
				fct_html << "<td align='center' class='fct_unit'>&nbsp;</td>"
			end
		end
		fct_html << '</tr>'

		if template > 6
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
		end

		# 合計値
		fct_html << '    <tr>'
		if template > 6
			fct_html << '      <td colspan="2" align="center" class="fct_sum">合計</td>'
			fct_html << "      <td align='right' class='fct_sum'>#{total_weight.to_f}</td>"
		end
		fct_num.times do |cc|
			fct_no = ( c * fct_num ) + cc
			fct_html << "      <td align='right' class='fct_sum'>#{fct_sum[fct_no]}</td>"
		end
		fct_html << '    </tr>'
		fct_html << '</table>'
	end
end


#### 共通ヘッダ
html_head = <<-"HTML"
<div class='container'>
	<div class='row'>
		<div class='col-6'>
			<h4>#{recipe_name}</h4>
		</div>
		<div class='col-2'>
			<h5>#{dish}人分</h5>
		</div>
		<div class='col-4'>
			<h5>#{code}</h5>
		</div>
	</div>
	<hr>
HTML


#### 共通フッタ
html_foot = <<-"HTML"
	<hr>
	<div class='row'>
		<div class='col-10'>
			<a href='fctb.bacura.jp/'>食品成分表ブラウザ2015</a>・<a href='http://neg.bacura.jp/'>日本栄養ギルド</a>・<a href='http://bacura.jp'>ばきゅら京都Lab</a><br>
			#{url}
		</div>
		<div class='col-2'>
			<img src='photo/#{code}-qr.png'>
		</div>
	</div>
</div>
HTML


case template
#### 基本レシピ・写真有
when 2
html = <<-"HTML"
	<div class='row'>
		<div class='col'>
			#{photos}
		</div>
		<div class='col'>
			<h5>材料</h5>
			#{foods}
		</div>
	</div>
	<hr>
	<div class='row'>
		<div class='col'>
			<h5>作り方</h5>
			#{protocol}
		</div>
	</div>
HTML


#### 詳細レシピ・写真有
when 4
html = <<-"HTML"
	<div class='row'>
		<div class='col-5'>
			#{photos}
		</div>
		<div class='col-7'>
			<h5>材料</h5>
			#{foods}
		</div>
		<div class='col'>
			<h5>作り方</h5>
			#{protocol}
		</div>
	</div>
HTML


#### 栄養レシピ・写真有
when 6
html = <<-"HTML"
	<div class='row'>
		<div class='col-8'>
			<h5>材料</h5>
			#{foods}
		</div>
		<div class='col-4'>
			#{photos}
		</div>
	</div>
	<hr>
	<div class='row'>
		<div class='col'>
			<h5>作り方</h5>
			#{protocol}
		</div>
	</div>
	#{fct_html}
HTML


#### フルレシピ・写真有
when 8
html = <<-"HTML"
	<div class='row'>
		<div class='col'>
			<h5>材料</h5>
			#{foods}
		</div>
	</div>
	<hr>
	<div class='row'>
		<div class='col-8'>
			<h5>作り方</h5>
			#{protocol}
		</div>
		<div class='col-4'>
			#{photos}
		</div>
	</div>
	#{fct_html}
HTML

end

puts html_head
puts html
puts html_foot