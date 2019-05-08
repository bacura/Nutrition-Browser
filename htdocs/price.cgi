#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser price editor 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20180605, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'price.cgi'


#==============================================================================
#DEFINITION
#==============================================================================
$DEBUG = false


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'price', language )
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
food_volume_p = cgi['food_volume'].to_i
food_price_p = cgi['food_price'].to_i
food_no_p = cgi['food_no']
if $DEBUG
	puts "command:#{command}<br>"
	puts "code:#{code}<br>"
	puts "food_volume:#{food_volume_p}<br>"
	puts "food_price:#{food_price_p}<br>"
	puts "food_no:#{food_no_p}<br>"
	puts "<hr>"
end


#### 基礎データの作成
solid = []
recipe_food_no = []
price_code = []
food_use = []

# レシピデータの読み込み
r = mariadb( "SELECT name, sum, dish, protect from #{$MYSQL_TB_RECIPE} WHERE code='#{code}';", false )
recipe_name = r.first['name']
dish_num = r.first['dish'].to_i
recipe_protect = r.first['protect'].to_i

# 食品番号と１人分の使用量を抽出
solid = r.first['sum'].split( "\t" )
solid.each do |e|
	a = e.split( ':' )
	unless a[0] == '-' || a[0] == '+'
		recipe_food_no << a[0]
		food_use << ( BigDecimal( a[1] ) / dish_num )
	end
end


#### 原価データの読み込み
food_no = []
food_price = []
food_volume = []

r = mariadb( "SELECT * FROM #{$MYSQL_TB_PRICE} WHERE code='#{code}';", false )

# レシピデータに存在する食品番号を抽出
if r.first
	solid = r.first['price'].split( "\t" )
	solid.each do |e|
		a = e.split( ':' )
		if recipe_food_no.include?( a.first )
			food_no << a[0]
			food_volume << a[1].to_i
			food_price << a[2].to_i
		end
	end
# 新規原価表の作成
else
	new_price = ''
	recipe_food_no.each do |e|
		food_no << e
		food_volume << 0
		food_price << 0
		new_price << "#{e}::\t"
	end
	new_price.chop!
	mariadb( "INSERT INTO #{$MYSQL_TB_PRICE} SET code='#{code}', user='#{uname}', price='#{new_price}';", false )
end


#### 個別コマンド
html = ''
case command
# 購入量変更
when 'changeFV'
	food_no.size.times do |c|
		if food_no[c] == food_no_p
			food_volume[c] = food_volume_p
		end
	end
# 支払金額変更
when 'changeFP'
	food_no.size.times do |c|
		if food_no[c] == food_no_p
			food_price[c] = food_price_p
		end
	end
# 初期化
when 'clearCT'
	food_no.size.times do |c|
		food_volume[c] = 0
		food_price[c] = 0
	end
# マスター価格適応
when 'adpt_master'
	food_no.size.times do |c|
		r = mariadb( "SELECT volume, price FROM #{$MYSQL_TB_PRICEM} WHERE FN='#{food_no[c]}' AND user='#{uname}';", false )
		if r.first
			food_volume[c] = r.first['volume']
			food_price[c] = r.first['price']
		end
	end
# マスター価格登録
when 'reg_master'
	food_no.size.times do |c|
		if food_volume[c].to_i != 0 && food_price[c].to_i != 0
			r = mariadb( "SELECT FN FROM #{$MYSQL_TB_PRICEM} WHERE FN='#{food_no[c]}' AND user='#{uname}';", false )

			# マスター価格の登録、または更新
			if r.first
				mariadb( "UPDATE TABLE #{$MYSQL_TB_PRICEM} SET volume='#{food_volume[c]}', price='#{food_price[c]}' WHERE FN='#{food_no[c]}' AND user='#{uname}';", false )
			else
				mariadb( "INSERT INTO #{$MYSQL_TB_PRICEM} SET volume='#{food_volume[c]}', price='#{food_price[c]}', FN='#{food_no[c]}', user='#{uname}';", false )
			end
		else
			# 未設定のマスター価格の削除
			mariadb( "DELETE FROM #{$MYSQL_TB_PRICEM} WHERE FN='#{food_no[c]}' AND user='#{uname}';", false )
		end
	end
end


#### 名前の書き換え
food_name = []
db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
food_no.size.times do |c|
	query = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{food_no[c]}';"
	res = db.query( query )
	food_name[c] = bind_tags( res ) if res.first
end
db.close


#### 原価の計算
food_cost = []
total_cost = 0
food_no.size.times do |c|
	unless food_volume[c] == nil || food_volume[c] == 0 || food_price[c] == nil || food_price[c] == 0
		t = BigDecimal( food_use[c] ) / food_volume[c] * food_price[c]
		food_cost << t.ceil
		total_cost += t.ceil
	else
		food_cost << 0
	end
end


#### レシピ価格区分反映
if command == 'ref_recipe'
	cost = 0
	if total_cost > 0 and total_cost < 50
		cost = 1
	elsif total_cost >= 50 and total_cost < 100
		cost = 2
	elsif total_cost >= 100 and total_cost < 150
		cost = 3
	elsif total_cost >= 150 and total_cost < 200
		cost = 4
	elsif total_cost >= 200 and total_cost < 300
		cost = 5
	elsif total_cost >= 300 and total_cost < 400
		cost = 6
	elsif total_cost >= 400 and total_cost < 500
		cost = 7
	elsif total_cost >= 500 and total_cost < 600
		cost = 8
	elsif total_cost >= 600 and total_cost < 800
		cost = 9
	elsif total_cost >= 800 and total_cost < 1000
		cost = 10
	else
		cost = 11
	end

	mariadb( "UPDATE #{$MYSQL_TB_RECIPE} SET cost='#{cost}' WHERE user='#{uname}' and code='#{code}';", false )
end


#### 価格区分反映ボタン
ref_recipe_button = ''
if recipe_protect == 0
	ref_recipe_button = "<button type='button' class='btn btn-outline-primary btn-sm' onclick=\"recipeRef_BWL2( '#{code}' )\">#{lp[1]}</button>"
end


html = <<-"HTML"
<div class='container-fluid'>
<div class='row'>
	<h5>#{lp[2]} #{recipe_name}</h5></div><br>
	<div class='row'>
		<div class='col-3'>
			<button type='button' class='btn btn-outline-primary btn-sm' onclick="pricemAdpt_BWL2( '#{code}' )">#{lp[3]}</button>
		</div>
		<div class='col-3'>
			<button type='button' class='btn btn-outline-primary btn-sm' onclick="pricemReg_BWL2( '#{code}' )">#{lp[4]}</button>
		</div>
		<div class='col-3'>
			#{ref_recipe_button}
		</div>
		<div class='col-3' align='center'>
			<input type='checkbox' id='clearCT_check'>&nbsp;
			<button type='button' class='btn btn-outline-danger btn-sm' onclick="clearCT_BWL2( '#{code}' )">#{lp[5]}</button>
		</div>
	</div>
</div>
<hr>
<div class='container'>
	<div class='row'>
		<div class='col-3 cb_header'>#{lp[6]}</div>
		<div class='col-2 cb_header'>#{lp[7]}</div>
		<div class='col-2 cb_header'>#{lp[8]}</div>
		<div class='col-2 cb_header'>#{lp[9]}</div>
		<div class='col-2 cb_header'>#{lp[10]}</div>
	</div>
</div>
<br>

HTML

html << "<div class='container'>"
food_no.size.times do |c|
	html << "<div class='row'>"
	html << "	<div class='col-3'>#{food_name[c]}</div>"
	html << "	<div class='col-2'><input type='number' class='form-control form-control-sm' id='food_volume#{c}' value='#{food_volume[c]}' onchange=\"changeFV_BWL2( '#{code}', 'food_volume#{c}', '#{food_no[c]}' )\"></div>"
	html << "	<div class='col-2'><input type='number' class='form-control form-control-sm' id='food_price#{c}' value='#{food_price[c]}' onchange=\"changeFP_BWL2( '#{code}', 'food_price#{c}', '#{food_no[c]}' )\"></div>"
	html << "	<div class='col-2'>#{food_use[c].to_f}</div>"
	html << "	<div class='col-2'>#{food_cost[c]}</div>"
	html << "</div>"
end
	html << "<hr>"
	html << "<div class='row'>"
	html << "	<div class='col-9'>#{lp[11]}</div>"
	html << "	<div class='col-2'>#{total_cost}</div>"
	html << "</div>"
html << "</div>"

html << "<div align='right' class='code'>#{code}</div>"

puts html


#### 原価計算表更新
new_price = ''
food_no.size.times do |c| new_price << "#{food_no[c]}:#{food_volume[c]}:#{food_price[c]}\t" end
new_price.chop!

mariadb( "UPDATE #{$MYSQL_TB_PRICE} SET price='#{new_price}' WHERE code='#{code}' AND user='#{uname}';", false )
