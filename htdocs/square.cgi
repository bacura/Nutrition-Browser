#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser food square 0.00a

#==============================================================================
# CHANGE LOG
#==============================================================================
#20171006, 0.00a, start


#==============================================================================
# LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
# STATIC
#==============================================================================
$DEBUG = false


#==============================================================================
# DEFINITION
#==============================================================================
#### 名前の履歴の取得
def get_history_name( uname, fg )
	name_his = []
	if uname
		r = mariadb( "SELECT his FROM #{$MYSQL_TB_HIS} WHERE user='#{uname}';", false )
		if r.first
			his = r.first['his'].split( "\t" )
########## 応急処置
			his.each do |e|
				unless e == ''
				if ( /P|U/ =~ e && e[1..2].to_i == fg.to_i ) || e[0..1].to_i == fg.to_i
					rr = mariadb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{e}';", false )
					name_his << rr.first['name']
				end
				end
########## 応急処置
			end
		end
	end

	return name_his
end


# ダイレクトグループの作成
def make_direct_group( direct_group, name_his, fg, class1, class2, class3, direct, pseudo_bit )
	dg_html = ''
	direct_group.uniq!
	direct_group.each do |e|
		if name_his.include?( e )
			if pseudo_bit == 1
				@his_class = 'btn btn-outline-success btn-sm nav_button visited'
			else
				@his_class = 'btn btn-outline-primary btn-sm nav_button visited'
			end
		else
			if pseudo_bit == 1
				@his_class = 'btn btn-outline-dark btn-sm nav_button'
			else
				@his_class = 'btn btn-outline-secondary btn-sm nav_button'
			end
		end
		dg_html << "<button type='button' class='#{@his_class}' onclick=\"summonBWL5( '#{fg}:#{class1}:#{class2}:#{class3}:#{e}', #{direct} )\">#{e}</button>\n"
	end

	return dg_html
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
status = 0 if status == nil
lp = lp_init( 'square', language )
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
end

#### GETデータの取得
get_data = get_data()
channel = get_data['channel']
category = get_data['category'].to_i
food_key = CGI.unescape( get_data['food_key'] ) if get_data['food_key'] != '' && get_data['food_key'] != nil
frct_mode = get_data['frct_mode']
food_weight = CGI.unescape( get_data['food_weight'] ) if get_data['food_weight'] != '' && get_data['food_weight'] != nil
food_no = get_data['food_no']
base = get_data['base']
base_fn = get_data['base_fn']
if $DEBUG
	puts "channel: #{channel}<br>"
	puts "category: #{category}<br>"
	puts "food_key: #{food_key}<br>"
	puts "frct_mode: #{frct_mode}<br>"
	puts "food_weight: #{food_weight}<br>"
	puts "food_no: #{food_no}<br>"
	puts "base: #{base}<br>"
	puts "base_fn: #{base_fn}<br>"
	puts "<hr>"
end

#### 食品グループ番号の桁補完
if category > 9
	@fg = category.to_s
else
	@fg = "0#{category}"
end
puts "@fg: #{@fg}<br>" if $DEBUG


#### 食品重量の決定
food_weight = BigDecimal( food_weight_check( food_weight ).first )


#### 端数処理の設定
frct_mode, frct_select = frct_check( frct_mode )


#### 名前の履歴の取得
name_his = get_history_name( uname, @fg )
#puts "name_his: #{name_his}<br>" if $DEBUG


#### 食品キーチェーン
food_key = '' if food_key == nil
fg_key, class1, class2, class3, food_name = food_key.split( ':' )
class_name = ''
class_no = 0
unless class1 == nil || class1 == ''
	class_name = class1
	class_no = 1
end
unless class2 == nil || class2 == ''
	class_name = class2
	class_no = 2
end
unless class3 == nil || class3 == ''
	class_name = class3
	class_no = 3
end
if $DEBUG
	puts "fg_key: #{fg_key}<br>"
	puts "class1: #{class1}<br>"
	puts "class2: #{class2}<br>"
	puts "class3: #{class3}<br>"
	puts "class_no: #{class_no}<br>"
	puts "class_name: #{class_name}<br>"
	puts "<hr>"
end


#### 閲覧選択
html = ''
class_html =''
direct_html = ''
pseudo_button = ''
class1_group = []
class2_group = []
class3_group = []
direct_group = []
class1_group_p = []
class2_group_p = []
class3_group_p = []
direct_group_p = []

case channel
#### 第１層閲覧選択ページ
when 'fctb'
	# 正規食品
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{@fg}' AND public='9';", false )
	r.each do |e|
		if e['class1'] != ''
			class1_group << e['class1']
			next
		elsif e['class2'] != ''
			class2_group << e['class2']
			next
		elsif e['class3'] != ''
			class3_group << e['class3']
			next
		else
			direct_group << e['name']
		end
	end
	class1_group.uniq!
	class2_group.uniq!
	class3_group.uniq!

	# Classグループの作成
	tag_button = "<button type='button' class='btn btn-info btn-sm nav_button'"
	class1_group.each do |e| class_html << "#{tag_button} onclick=\"summonBWL2( '#{@fg}:#{e}:::' )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end
	class2_group.each do |e| class_html << "#{tag_button} onclick=\"summonBWL2( '#{@fg}::#{e}::' )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end
	class3_group.each do |e| class_html << "#{tag_button} onclick=\"summonBWL2( '#{@fg}:::#{e}:' )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end

	# ダイレクトグループの作成
	direct_html = make_direct_group( direct_group, name_his, @fg, '', '', '', 1, 0 )

	# 擬似食品
	unless status == 0
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{@fg}' AND (( user='#{uname}' AND public!='2' ) OR public='1' );", false )
		r.each do |e|
			if e['class1'] != ''
				class1_group_p << e['class1']
				next
			elsif e['class2'] != ''
				class2_group_p << e['class2']
				next
			elsif e['class3'] != ''
				class3_group_p << e['class3']
				next
			else
				direct_group_p << e['name']
			end
		end
		class1_group_p = class1_group_p.uniq - class1_group
		class2_group_p = class2_group_p.uniq - class2_group
		class3_group_p = class3_group_p.uniq - class3_group

		# Classグループの作成
		tag_button = "<button type='button' class='btn btn-secondary btn-sm nav_button'"
		class1_group_p.each do |e| class_html << "#{tag_button} onclick=\"summonBWL2( '#{@fg}:#{e}:::' )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end
		class2_group_p.each do |e| class_html << "#{tag_button} onclick=\"summonBWL2( '#{@fg}::#{e}::' )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end
		class3_group_p.each do |e| class_html << "#{tag_button} onclick=\"summonBWL2( '#{@fg}:::#{e}:' )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end

		# ダイレクトグループの作成
		direct_html << make_direct_group( direct_group_p, name_his, @fg, '', '', '', 1, 1 )
	end

	# 擬似食品ボタンの作成
	pseudo_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"pseudoAdd_BWLF( 'init', '#{@fg}::::', '' )\">＋</button>\n" if status > 0

	html = <<-"HTML"
	<h6>#{category}.#{$CATEGORY[category]}</h6>
	#{class_html}
	#{direct_html}
	#{pseudo_button}
HTML

#### 第２層閲覧選択ページ
when 'fctb_l2'
	# 正規食品
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND class#{class_no}='#{class_name}' AND public='9';", false )
	r.each do |e|
		if e['class1'] != '' && e['class2'] != ''
			class2_group << e['class2']
			next
		elsif e['class1'] == '' && e['class2'] != '' && e['class3'] != ''
			class3_group << e['class3']
			next
		elsif e['class1'] != '' && e['class2'] == '' && e['class3'] != ''
			class3_group << e['class3']
			next
		else
			direct_group << e['name']
		end
	end
	class2_group.uniq!
	class3_group.uniq!

	# Classグループの作成
	tag_button = "<button type='button' class='btn btn-info btn-sm nav_button'"
	class2_group.each do |e| class_html << "#{tag_button} onclick=\"summonBWL3( '#{fg_key}:#{class1}:#{e}:#{class3}:#{food_name}', 3 )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end
	class3_group.each do |e| class_html << "#{tag_button} onclick=\"summonBWL3( '#{fg_key}:#{class1}:#{class2}:#{e}:#{food_name}', 3 )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end

	# ダイレクトグループの作成
	direct_html = make_direct_group( direct_group, name_his, fg_key, class1, class2, class3, 2, 0 )

	# 擬似食品
	unless status == 0
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG= '#{fg_key}' AND class#{class_no}='#{class_name}' AND (( user='#{uname}' AND public!='2' ) OR public='1');", false )
		r.each do |e|
			if e['class1'] != '' && e['class2'] != ''
				class2_group_p << e['class2']
				next
			elsif e['class1'] == '' && e['class2'] != '' && e['class3'] != ''
				class3_group_p << e['class3']
				next
			elsif e['class1'] != '' && e['class2'] == '' && e['class3'] != ''
				class3_group_p << e['class3']
				next
			else
				direct_group_p << e['name']
			end
		end
		class2_group_p = class2_group_p.uniq - class2_group
		class3_group_p = class3_group_p.uniq - class3_group

		# Classグループの作成
		tag_button = "<button type='button' class='btn btn-secondary btn-sm nav_button'"
		class2_group_p.each do |e| class_html << "#{tag_button} onclick=\"summonBWL3( '#{fg_key}:#{class1}:#{e}:#{class3}:#{food_name}', 3 )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end
		class3_group_p.each do |e| class_html << "#{tag_button} onclick=\"summonBWL3( '#{fg_key}:#{class1}:#{class2}:#{e}:#{food_name}', 3 )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end

		# ダイレクトグループの作成
		direct_html << make_direct_group( direct_group_p, name_his, fg_key, class1, class2, class3, 2, 1 )
	end

	# 擬似食品ボタンの作成
	pseudo_button = "<button type=\"button\" class=\"btn btn-dark btn-sm nav_button\" onclick=\"pseudoAdd_BWLF( 'init', '#{fg_key}:#{class1}:#{class2}:#{class3}:#{food_name}' )\">＋</button>\n" if status > 0

	html = <<-"HTML"
	<h6>#{class_name.sub( '+', '' ).sub( /^.+\-/, '' )}</h6>
	#{class_html}
	#{direct_html}
	#{pseudo_button}
HTML

#### 第３層閲覧選択ページ
when 'fctb_l3'
	# 正規食品
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND class#{class_no}='#{class_name}' AND public='9';", false )
	r.each do |e|
		if e['class3'] != '' && e['class1'] != '' && e['class2'] != ''
			class3_group << e['class3']
			next
		else
			direct_group << e['name']
		end
	end
	class3_group.uniq!

	# Class3グループの作成
	tag_button = "<button type='button' class='btn btn-info btn-sm nav_button'"
	class3_group.each do |e| class_html << "#{tag_button} onclick=\"summonBWL4( '#{fg_key}:#{class1}:#{class2}:#{e}:#{food_name}', 4 )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end

	# ダイレクトグループの作成
	direct_html = make_direct_group( direct_group, name_his, fg_key, class1, class2, class3, 0, 0 )

	# 擬似食品
	unless status == 0
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND class#{class_no}='#{class_name}' AND (( user='#{uname}' AND public!='2' ) OR public='1' );", false )
		r.each do |e|
			if e['class3'] != '' && e['class1'] != '' && e['class2'] != ''
				class3_group_p << e['class3']
				next
			else
				direct_group_p << e['name']
			end
		end
		class3_group_p = class3_group_p.uniq - class3_group

		# Class3グループの作成
		tag_button = "<button type='button' class='btn btn-secondary btn-sm nav_button'"
		class3_group_p.each do |e| class_html << "#{tag_button} onclick=\"summonBWL4( '#{fg_key}:#{class1}:#{class2}:#{e}:#{food_name}', 4 )\">#{e.sub( '+', '' ).sub( /^.+\-/, '' )}</button>\n" end

		# ダイレクトグループの作成
		direct_html << make_direct_group( direct_group_p, name_his, fg_key, class1, class2, class3, 0, 1 )
	end

	# 擬似食品ボタンの作成
 	pseudo_button = "<button type=\"button\" class=\"btn btn-dark btn-sm nav_button\" onclick=\"pseudoAdd_BWLF( 'init', '#{fg_key}:#{class1}:#{class2}:#{class3}:#{food_name}' )\">＋</button>\n" if status > 0

  html = <<-"HTML"
	<h6>#{class_name.sub( '+', '' ).sub( /^.+\-/, '' )}</h6>
	#{class_html}
	#{direct_html}
	#{pseudo_button}
HTML


#### 第４層閲覧選択ページ
when 'fctb_l4'
	# 正規食品
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND class#{class_no}='#{class_name}' AND public='9';", false )
	r.each do |e| direct_group << e['name'] end

	# ダイレクトグループの作成
	direct_html = make_direct_group( direct_group, name_his, fg_key, class1, class2, class3, 0, 0 )

	# 擬似食品
	unless status == 0
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND class#{class_no}='#{class_name}' AND (( user='#{uname}' AND public!='2' ) OR public='1');", false )
		r.each do |e| direct_group_p << e['name'] end

		# ダイレクトグループの作成
		direct_html << make_direct_group( direct_group_p, name_his, fg_key, class1, class2, class3, 0, 1 )
	end

	# 擬似食品ボタンの作成
 	pseudo_button = "<button type=\"button\" class=\"btn btn-dark btn-sm nav_button\" onclick=\"pseudoAdd_BWLF( 'init', '#{fg_key}:#{class1}:#{class2}:#{class3}:#{food_name}' )\">＋</button>\n" if status > 0

	html = <<-"HTML"
	<h6>#{class_name.sub( '+', '' ).sub( /^.+\-/, '' )}</h6>
	#{direct_html}
	#{pseudo_button}
HTML


#### 第５層（最終）食品候補ページ
when 'fctb_l5'
	query = ''
	food_no_list = []
	food_name_list = []
	tag1_list = []
	tag2_list = []
	tag3_list = []
	tag4_list = []
	tag5_list = []
	r = Hash.new

	#### 補助クラスネームの追加処理
	if /\+/ =~ class_name
		class_add = "<span class='tagc'>#{class_name.sub( '+', '' )}</span> "
	else
		class_add = ''
	end

	# 正規食品
	if class_no.to_i == 0
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND name='#{food_name}' AND public='9';", false )
	else
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND class#{class_no}='#{class_name}' AND name='#{food_name}' AND public='9';", false )
	end
	if r.first
		r.each do |e|
			food_no_list << e['FN']
			food_name_list << e['name']
			tag1_list << e['tag1']
			tag2_list << e['tag2']
			tag3_list << e['tag3']
			tag4_list << e['tag4']
			tag5_list << e['tag5']
		end
	end

	# 擬似食品
	if class_no.to_i == 0
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND name='#{food_name}' AND (( user='#{uname}' AND public!='2' ) OR public='1');", false )
	else
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FG='#{fg_key}' AND class#{class_no}='#{class_name}' AND name='#{food_name}' AND (( user='#{uname}' AND public!='2' ) OR public='1');", false )
	end
	if r.first
		r.each do |e|
			food_no_list << e['FN']
			food_name_list << e['name']
			tag1_list << e['tag1']
			tag2_list << e['tag2']
			tag3_list << e['tag3']
			tag4_list << e['tag4']
			tag5_list << e['tag5']
		end
	end

 	# 簡易表示の項目
 	fc_items = []
	fc_items_html = ''
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{uname}' AND name='簡易表示用';", false  )
	if r.first
		palette = r.first['palette']
		palette.size.times do |c|
			fc_items << $FCT_ITEM[c] if palette[c] == '1'
		end
	else
 		fc_items = ['ENERC_KCAL', 'PROT', 'FAT', 'CHO', 'NACL_EQ']
	end
	fc_items.each do |e| fc_items_html << "<th align='right'>#{$FCT_NAME[e]}</th>" end


	# 食品ラインの生成
	food_html = ''
    db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
	food_no_list.size.times do |c|
		pseudo_flag = false
		# 栄養素の一部を取得
		if /^U/ =~ food_no_list[c]
			query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{food_no_list[c]}' AND user='#{uname}';"
			pseudo_flag = true
		elsif /^P/ =~ food_no_list[c]
			query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{food_no_list[c]}';"
			pseudo_flag = true
		else
			query = "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_no_list[c]}';"
		end
		p query if $DEBUG
		res = db.query( query )
		sub_components = ''
		fc_items.each do |e|
			t = num_opt( res.first[e], food_weight, frct_mode, $FCT_FRCT[e] )
			sub_components << "<td align='center'>#{t}</td>"
		end

		# 追加・変更ボタン
		if uname && base == 'cb'
			add_button = "<button type='button' class='btn btn btn-dark btn-sm' onclick=\"changingCB( '#{food_no_list[c]}', '#{base_fn}' )\">#{lp[1]}</button>"
		elsif uname
			add_button = "<button type='button' class='btn btn btn-dark btn-sm' onclick=\"addingCB( '#{food_no_list[c]}', 'weight' )\">#{lp[2]}</button>"
		else
			add_button = ""
		end

		# Koyomi button
		if status >= 2
			koyomi_button = "<button type='button' class='btn btn btn-info btn-sm' onclick=\"addKoyomi_BWF( '#{food_no_list[c]}', -5 )\">#{lp[3]}</button>"
		else
			koyomi_button = ''
		end

		# GM専用単位変換ボタン
		gm_unitc = ''
		gm_unitc = "<button type='button' class='btn btn btn-outline-danger btn-sm' onclick=\"directUnitc_BWLF( '#{food_no_list[c]}' )\">#{lp[4]}</button>" if status == 9

		# GM専用色ボタン
		gm_color = ''
		gm_color = "<button type='button' class='btn btn btn-outline-danger btn-sm' onclick=\"directColor_BWLF( '#{food_no_list[c]}' )\">#{lp[5]}</button>" if status == 9

		# GM専用アレルギーボタン
		gm_allergen = ''
		gm_allergen = "<button type='button' class='btn btn btn-outline-danger btn-sm' onclick=\"directAllergen_BWLF( '#{food_no_list[c]}' )\">#{lp[6]}</button>" if status == 9

		# GM専用旬ボタン
		gm_shun = ''
		gm_shun = "<button type='button' class='btn btn btn-outline-danger btn-sm' onclick=\"directShun_BWLF( '#{food_no_list[c]}' )\">#{lp[7]}</button>" if status == 9


		tags = "<span class='tag1'>#{tag1_list[c]}</span> <span class='tag2'>#{tag2_list[c]}</span> <span class='tag3'>#{tag3_list[c]}</span> <span class='tag4'>#{tag4_list[c]}</span> <span class='tag5'>#{tag5_list[c]}</span>"
		if pseudo_flag
			food_html << "<tr class='fct_value'><td>#{food_no_list[c]}</td><td class='link_cursor' onclick=\"pseudoAdd_BWLF( 'init', '#{fg_key}:#{class1}:#{class2}:#{class3}:#{food_name}', '#{food_no_list[c]}' )\">#{class_add}#{food_name_list[c]} #{tags}</td><td>#{add_button}&nbsp;#{koyomi_button} #{gm_unitc}#{gm_color}#{gm_allergen}#{gm_shun}</td>#{sub_components}</tr>\n"
		else
			food_html << "<tr class='fct_value'><td>#{food_no_list[c]}</td><td class='link_cursor' onclick=\"detailView( '#{food_no_list[c]}' )\">#{class_add}#{food_name_list[c]} #{tags}</td><td>#{add_button}&nbsp;#{koyomi_button} #{gm_unitc}#{gm_color}#{gm_allergen}#{gm_shun}</td>#{sub_components}</tr>\n"
		end
	end
	db.close

	# 擬似食品ボタンの作成
 	pseudo_button = "<button type=\"button\" class=\"btn btn-dark btn-sm nav_button\" onclick=\"pseudoAdd_BWLF( 'init', '#{fg_key}:#{class1}:#{class2}:#{class3}:#{food_name}', '' )\">＋</button>\n" if status > 0

	html = <<-"HTML"
	<div class='container-fluid'><div class="row">
  		<div class="col-3"><h5>#{food_name}</h5></div>
  		<div class="col-3"><h5>#{food_weight.to_f} g</h5></div>
		<div class="col-3">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="fraction">#{lp[8]}</label>
				</div>
				<select class="form-control" id="fraction" onchange="changeWeight( '#{food_key}', '#{food_no}' )">
					<option value="1"#{frct_select[1]}>#{lp[9]}</option>
					<option value="2"#{frct_select[2]}>#{lp[10]}</option>
					<option value="3"#{frct_select[3]}>#{lp[11]}</option>
				</select>
			</div>
		</div>
		<div class="col-3">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="weight">#{lp[12]}</label>
				</div>
				<input type="number" min='0' class="form-control" id="weight" value="#{food_weight.to_f}" onchange="changeWeight( '#{food_key}', '#{food_no}' )">
				<div class="input-group-append">
					<button class="btn btn-outline-primary" type="button" onclick="changeWeight( '#{food_key}', '#{food_no}' )">g</button>
				</div>
			</div>
		</div>
	</div></div>
	<br>

	<table class="table table-sm table-hover">
		<thead>
			<tr>
	  			<th>#{lp[13]}</th>
	  			<th>#{lp[14]}</th>
				<th></th>
				#{fc_items_html}
    		</tr>
  		</thead>

		#{food_html}
	</table>
	#{pseudo_button}
HTML

end

puts html
