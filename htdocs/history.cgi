#! /usr/bin/ruby
#encoding: utf-8
#Nutritoin browser history 0.00b

#==============================================================================
# CHANGE LOG
#==============================================================================
#20180111, 0.00a, start


#==============================================================================
# LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
# STATIC
#==============================================================================
$DEBUG = false
$LIMIT = 100


#==============================================================================
# DEFINITION
#==============================================================================
#### 履歴の取得
def get_histry( uname, sub_fg, order_mode )
	history = []
	r = mariadb( "SELECT his FROM #{$MYSQL_TB_HIS} WHERE user='#{uname}';", false )

	t = r.first['his'].split( "\t" )
	t.sort! if order_mode == 'food_no'
	if sub_fg == 'all'
		$LIMIT.times do |c|
			break if c > t.size - 1
			history << t[c]
		end
	else
		t.each do |e|
			if /P|U/ =~ e
				history << e if e[1..2].to_i == sub_fg.to_i
			else
				history << e if e[0..1].to_i == sub_fg.to_i
			end
		end
	end

	return history
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'history', language )
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
end


#### POSTデータの取得
order_mode = cgi['order_mode']
food_weight = cgi['food_weight']
frct_mode = cgi['frct_mode']
food_no = cgi['food_no']
sub_fg = cgi['sub_fg']
if $DEBUG
	puts "order_mode: #{order_mode}<br>"
	puts "food_weight: #{food_weight}<br>"
	puts "frct_mode: #{frct_mode}<br>"
	puts "food_no: #{food_no}<br>"
	puts "sub_fg: #{sub_fg}<br>"
	puts "<hr>"
end


#### グループ名変換
sub_title = ''
if sub_fg == 'all'
	sub_title = "#{lp[1]}"
elsif sub_fg == '00'
	sub_title = "#{lp[2]}"
else
	sub_title = $CATEGORY[sub_fg.to_i]
end


#### 食品重量の決定
food_weight = BigDecimal( food_weight_check( food_weight ).first )
puts "food_weight: #{food_weight}<br>" if $DEBUG


#### 端数処理の設定
frct_mode, frct_select = frct_check( frct_mode )


#### 履歴の取得
history = get_histry( uname, sub_fg, order_mode )
puts "history: #{history}<br>" if $DEBUG


#### 各食品ラインの生成
food_html = ''
add_button = ''
koyomi_button = ''
sort_button = ''
db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
history.each do |e|
	# 栄養素の一部を取得
	if /^P|U/ =~ e
		q = "SELECT ENERC_KCAL, PROT, FAT, CHO, NACL_EQ FROM #{$MYSQL_TB_FCTP} WHERE FN='#{e}' AND ( user='#{uname}' OR user='#{$GM}' );"
	else
		q = "SELECT ENERC_KCAL, PROT, FAT, CHO, NACL_EQ FROM #{$MYSQL_TB_FCT} WHERE FN='#{e}';"
	end
	r = db.query( q )
	next if r.first == nil
	kcal = num_opt( r.first['ENERC_KCAL'], food_weight, frct_mode, $FCT_FRCT['ENERC_KCAL'] )
	prot = num_opt( r.first['PROT'], food_weight, frct_mode, $FCT_FRCT['PROT'] )
	fat = num_opt( r.first['FAT'], food_weight, frct_mode, $FCT_FRCT['FAT'] )
	cho = num_opt( r.first['CHO'], food_weight, frct_mode, $FCT_FRCT['CHO'] )
	nacl_rq = num_opt( r.first['NACL_EQ'], food_weight, frct_mode, $FCT_FRCT['NACL_EQ'] )

	# TAG要素の抽出
	q = "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{e}';"
	r_tag = db.query( q )
	tags = bind_tags( r_tag ) if r_tag.first

	# クイックビュー栄養素
	sub_components = "<td align='right'>#{kcal}</td><td align='right'>#{prot}</td><td align='right'>#{fat}</td><td align='right'>#{cho}</td><td align='right'>#{nacl_rq}</td>"

	# 追加ボタンの設定
	if uname
		add_button = "<button type='button' class='btn btn btn-dark btn-sm' onclick=\"addingCB( '#{e}', 'weight' )\">#{lp[3]}</button>"
	else
		add_button = "<button type='button' class='btn btn btn-dark btn-sm' onclick='window.alert(\"#{lp[4]}\")'>#{lp[3]}</button>"
	end

	# Koyomi button
	if status >= 2
		koyomi_button = "<button type='button' class='btn btn btn-info btn-sm' onclick=\"addKoyomi_BWF( '#{e}', 1 )\">#{lp[35]}</button>"
	else
		koyomi_button = ''
	end

	# ソートボタン
	if order_mode == 'recent'
		sort_button = "<button class=\"btn btn-sm btn-outline-primary\" onclick=\"historyBWL1( 'food_no', '#{food_weight}', '#{frct_mode}', '#{sub_fg}' )\">#{lp[5]}</button>"
	else
		sort_button = "<button class=\"btn btn-sm btn-outline-primary\" onclick=\"historyBWL1( 'recent', '#{food_weight}', '#{frct_mode}', '#{sub_fg}' )\">#{lp[6]}</button>"
	end

	food_html << "<tr class='fct_value'><td>#{e}</td><td class='link_cursor' onclick=\"detailView_his( '#{e}', '#{frct_mode}' )\">#{tags}</td><td>#{add_button}&nbsp;#{koyomi_button}</td>#{sub_components}</tr>\n"
end
db.close


#### 絞り込みボタン生成
html_sub = <<-"HTML_SUB"
<button type="button" class="btn btn-outline-warning btn-sm nav_button" id="category1" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '1' )">#{lp[7]}</button>
<button type="button" class="btn btn-outline-primary btn-sm nav_button" id="category2" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '2' )">#{lp[8]}</button>
<button type="button" class="btn btn-outline-info btn-sm nav_button" id="category3" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '3' )">#{lp[9]}</button>
<button type="button" class="btn btn-outline-primary btn-sm nav_button" id="category4" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '4' )">#{lp[10]}</button>
<button type="button" class="btn btn-outline-primary btn-sm nav_button" id="category5" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '5' )">#{lp[11]}</button>
<button type="button" class="btn btn-outline-success btn-sm nav_button" id="category6" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '6' )">#{lp[12]}</button>
<button type="button" class="btn btn-outline-success btn-sm nav_button" id="category7" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '7' )">#{lp[13]}</button>
<button type="button" class="btn btn-outline-success btn-sm nav_button" id="category8" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '8' )">#{lp[14]}</button>
<button type="button" class="btn btn-outline-success btn-sm nav_button" id="category9" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '9' )">#{lp[15]}</button>
<button type="button" class="btn btn-outline-danger btn-sm nav_button" id="category10" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '10' )">#{lp[16]}</button>
<button type="button" class="btn btn-outline-danger btn-sm nav_button" id="category11" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '11' )">#{lp[17]}</button>
<button type="button" class="btn btn-outline-danger btn-sm nav_button" id="category12" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '12' )">#{lp[18]}</button>
<button type="button" class="btn btn-outline-danger btn-sm nav_button" id="category13" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '13' )">#{lp[19]}</button>
<button type="button" class="btn btn-outline-info btn-sm nav_button" id="category14" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '14' )">#{lp[20]}</button>
<button type="button" class="btn btn-outline-secondary btn-sm nav_button" id="category15" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '15' )">#{lp[21]}</button>
<button type="button" class="btn btn-outline-secondary btn-sm nav_button" id="category16" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '16' )">#{lp[22]}</button>
<button type="button" class="btn btn-outline-info btn-sm nav_button" id="category17" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '17' )">#{lp[23]}</button>
<button type="button" class="btn btn-outline-secondary btn-sm nav_button" id="category18" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '18' )">#{lp[24]}</button>
<button type="button" class="btn btn-outline-dark btn-sm nav_button" id="category0" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', '00' )">#{lp[25]}</button>
<button type="button" class="btn btn-dark btn-sm nav_button" id="category1" onclick="historyBWL1( '#{order_mode}', '#{food_weight}', '#{frct_mode}', 'all' )">#{lp[26]}</button>
HTML_SUB


#### HTML生成
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
  		<div class="col-3"><h5>#{lp[27]}: #{sub_title}</h5></div>
  		<div class="col-3"><h5>#{food_weight.to_f} g </h5></div>
		<div class="col-3">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="fraction">#{lp[28]}</label>
				</div>
				<select class="form-control" id="fraction">
					<option value="1"#{frct_select[1]}>#{lp[29]}</option>
					<option value="2"#{frct_select[2]}>#{lp[30]}</option>
					<option value="3"#{frct_select[3]}>#{lp[31]}</option>
				</select>
			</div>
		</div>
		<div class="col-3">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="weight">#{lp[32]}</label>
				</div>
				<input type="number" min='0' class="form-control" id="weight" value="#{food_weight.to_f}">
				<div class="input-group-append">
					<button class="btn btn-outline-primary" onclick="history_changeWeight( '#{order_mode}', '#{food_no}', '#{sub_fg}' )">g</button>
				</div>
			</div>
		</div>
	</div>
</div>
<br>

<div align="center">#{html_sub} #{sort_button}</div>
<br>

<table class="table table-sm table-hover">
	<thead>
    	<tr>
      		<th>#{lp[33]}</th>
      		<th>#{lp[34]}</th>
      		<th></th>
      		<th align='right'>#{$FCT_NAME['ENERC_KCAL']}</th>
      		<th align='right'>#{$FCT_NAME['PROT']}(#{$FCT_UNIT['PROT']})</th>
      		<th align='right'>#{$FCT_NAME['FAT']}(#{$FCT_UNIT['FAT']})</th>
      		<th align='right'>#{$FCT_NAME['CHO']}(#{$FCT_UNIT['CHO']})</th>
      		<th align='right'>#{$FCT_NAME['NACL_EQ']}(#{$FCT_UNIT['NACL_EQ']})</th>
    	</tr>
  	</thead>

	#{food_html}

</table>
HTML

puts html
