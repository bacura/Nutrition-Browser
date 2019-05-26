#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171105, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'recipe.cgi'
$DEBUG = false


#==============================================================================
#DEFINITION
#==============================================================================

def update_recipei( code, recipe_name, sum, protocol )
	require 'natto'
	mecab = Natto::MeCab.new( userdic: "/usr/local/share/mecab/dic/mecab-user-dict-seed.20190307.dic" )
	words = Hash.new
	target = []

	#recipe name
	target << recipe_name

	#foods
	a = sum.split( "\t" )
	sum_code = []
	a.each do |ee| sum_code << ee.split( ':' ).first end
	sum_code.each do |ee|
		r = mariadb( "SELECT FG, name, class1, class2, class3 FROM #{$MYSQL_TB_TAG} WHERE FN='#{ee}' AND FG!='00' AND FG!='03' AND FG!='14' AND FG!='15' AND FG!='16' AND FG!='17' AND FG!='18';", false )
		if r.first
			target << r.first['name']
			target << r.first['class1'] if r.first['class1'] != ''
			target << r.first['class2'] if r.first['class2'] != ''
			target << r.first['class3'] if r.first['class3'] != ''
		end
	end

	#comment 1st line
	a = protocol.split( "\n" )
	unless a[0] == nil
		target << a[0] if /^\#.+/ =~ a[0]
	end

	target_dic = []
	target.each do  |e|
		r = mariadb( "SELECT org_name FROM #{$MYSQL_TB_DIC} WHERE alias='#{e}';", false )
		if r.first
			target_dic << r.first['org_name']
			target_dic << e
		else
			target_dic << e
		end
	end

	target_u = []
	target_dic.each do |e|
		mecab.parse( e ) do |n|
			a = n.feature.split( ',' )
		 	if a[0] == '名詞' && ( a[1] == '一般' || a[1] == '固有名詞' )
		 		target_u << n.surface
		 	end
		end
	end
	target_u.uniq!

	target_u.each do |e|
		if words[e]
			words[e] = "#{words[e]}:#{code}"
		else
			words[e] = code
		end
	end

	words.each do |k, v|
		r = mariadb( "SELECT codes FROM #{$MYSQL_TB_RECIPEI} WHERE words='#{k}'", false )
		if r.first
			a = codes.split( ':' )
			a.push( v )
			a.uniq!
			new_code = a.join( ':' )
			mariadb( "UPDATE #{$MYSQL_TB_RECIPEI} SET codes='#{new_code}' WHERE words='#{k}';", false )
		else
			mariadb( "INSERT INTO #{$MYSQL_TB_RECIPEI} SET words='#{k}', codes='#{v}', count='0';", false )
		end
	end
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'recipe', language )
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
recipe_name = cgi['recipe_name']
public_bit = cgi['public'].to_i
protect = cgi['protect'].to_i
draft = cgi['draft'].to_i
type = cgi['type'].to_i
role = cgi['role'].to_i
tech = cgi['tech'].to_i
time = cgi['time'].to_i
cost = cgi['cost'].to_i
protocol = cgi['protocol']
if $DEBUG
	puts "commnad:#{command}<br>"
	puts "code:#{code}<br>"
	puts "recipe_name:#{recipe_name}<br>"
	puts "public_bit:#{public_bit}<br>"
	puts "protect:#{protect}<br>"
	puts "draft:#{draft}<br>"
	puts "type:#{type}<br>"
	puts "role:#{role}<br>"
	puts "tech:#{tech}<br>"
	puts "time:#{time}<br>"
	puts "cost:#{cost;}<br>"
	puts "protocol:#{protocol}<br>"
end


case command
#### レシピの表示
when 'view'
	if code == ''
		# レシピデータベースの仮登録チェック
  		r = mariadb( "SELECT code FROM #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' AND name='' AND code!='';", false )
  		code = r.first['code'] unless r.first == nil

  		unless r.first
  			# 新規コードの生成
			require 'securerandom'
			code = uname[0, 2]
		  	code = "x" + uname[0, 1] if code == nil
		  	code = "#{code}-#{SecureRandom.hex( 2 )}-#{SecureRandom.hex( 2 )}"

		  	# レシピデータベースに仮登録
		  	mariadb( "INSERT INTO #{$MYSQL_TB_RECIPE} SET code='#{code}', user='#{uname}',public=0, protect=0, draft=0, name='', dish=1, type=0, role=0, tech=0, time=0, cost=0, sum='', protocol='', fig1=0, fig2=0, fig3=0;", false )
  		end

  		# サムデータベースへ反映
		mariadb( "UPDATE #{$MYSQL_TB_SUM} SET code='#{code}' WHERE user='#{uname}';", false )
  	end


	# レシピの読み込み
	r = mariadb( "SELECT * from #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' and code='#{code}';", false )

	public_bit = r.first['public'].to_i
	protect = r.first['protect'].to_i
	draft = r.first['draft'].to_i
	type = r.first['type'].to_i
	role = r.first['role'].to_i
	tech = r.first['tech'].to_i
	time = r.first['time'].to_i
	cost = r.first['cost'].to_i
	protocol = r.first['protocol']

	# リセットネーム処理
	r = mariadb( "SELECT name from #{$MYSQL_TB_SUM} WHERE user='#{uname}';", false )
	recipe_name = r.first['name']

#### レシピの保存
when 'save'
	# プロトコールのタグ抜き
	protocol.gsub!( '<', '&lt;')
	protocol.gsub!( '>', '&gt;')
	protocol.gsub!( ';', '；')

	r = mariadb( "SELECT sum, name, dish from #{$MYSQL_TB_SUM} WHERE user='#{uname}';", false )
	sum = r.first['sum']
	sum_name = r.first['name']
	dish_num = r.first['dish'].to_i

	query = "SELECT fig1, fig2, fig3 from #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' and code='#{code}';"
	db_err = 'recipe select'
	r = mariadb( "SELECT fig1, fig2, fig3 from #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' and code='#{code}';", false )
	fig1 = r.first['fig1'].to_i
	fig2 = r.first['fig2'].to_i
	fig3 = r.first['fig3'].to_i

	new_code_flag = false
	source_code = code
	p sum if $DEBUG

	# レシピ名の確認と新しいコード
	unless sum_name == ''
		rr = mariadb( "SELECT code from #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' and code='#{code}' and name='#{recipe_name}';", false )
		# 名前が一致しなければ、新規コードとメニューを生成。ただし、下書きの場合はコードの変更なし
		unless rr.first || draft == 1
			source_code = code
			code = insert_recipe( uname, nil, nil )
			draft = 0
			new_code_flag = true
		end
	end

	# 保護の確認と新しいコード
	rr= mariadb( "SELECT name, protect from #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' and code='#{code}';", false )
	# 保存データもポストデータも保護モードだったら、新しいコードと名前を割り振る
	if rr.first['protect'] == 1 && protect == 1
		if recipe_name == rr.first['name']
			t = recipe_name.match( /\((\d+)\)$/ )
			if t == nil
				sn = 1
			else
				sn = t[1].to_i + 1
			end
			recipe_name.sub!( /\((\d+)\)$/, '' )
			recipe_name = "#{recipe_name}(#{sn})"
			source_code = code
			code = insert_recipe( uname, nil, nil )
			protect = 0
			draft = 1
			new_code_flag = true
		end
	end

	# コードが新しくなって写真があったら写真もコピー
	if new_code_flag
		require 'fileutils'
		if fig1 == 1
			FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-1tns.jpg", "#{$PHOTO_PATH}/#{code}-1tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-1tns.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-1tn.jpg", "#{$PHOTO_PATH}/#{code}-1tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-1tn.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-1.jpg", "#{$PHOTO_PATH}/#{code}-1.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-1.jpg" )
			copy_fig1 = 1
		end

		if fig2 == 1
			FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-2tns.jpg", "#{$PHOTO_PATH}/#{code}-2tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-2tns.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-2tn.jpg", "#{$PHOTO_PATH}/#{code}-2tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-2tn.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-2.jpg", "#{$PHOTO_PATH}/#{code}-2.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-2.jpg" )
			copy_fig2 = 1
		end

		if fig3 == 1
			FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-3tns.jpg", "#{$PHOTO_PATH}/#{code}-3tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-3tns.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-3tn.jpg", "#{$PHOTO_PATH}/#{code}-3tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-3tn.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-3.jpg", "#{$PHOTO_PATH}/#{code}-3.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-3.jpg" )
			copy_fig3 = 1
		end
	end

	# 擬似食品と公開フラグのキャンセル
	a = sum.split( "\t" )
	a.each do |e|
		sum_items = e.split( ':' )
		public_bit = 0 if /^U/ =~ sum_items[0]
	end


	# 下書きと公開フラグのキャンセル
	public_bit = 0 if draft == 1


	# 上書き保存
	mariadb( "UPDATE #{$MYSQL_TB_RECIPE} SET name='#{recipe_name}', dish='#{dish_num}',type='#{type}', role='#{role}', tech='#{tech}', time='#{time}', cost='#{cost}', sum='#{sum}', protocol='#{protocol}', public='#{public_bit}',protect='#{protect}',draft='#{draft}', fig1='#{fig1}', fig2='#{fig2}', fig3='#{fig3}', date='#{Time.now}' WHERE user='#{uname}' and code='#{code}';", false )
	mariadb( "UPDATE #{$MYSQL_TB_SUM} SET name='#{recipe_name}', code='#{code}', protect='#{protect}' WHERE user='#{uname}';", false )

#	update_recipei( code, recipe_name, sum, protocol )
else
end


# 公開チェック
p public_bit if $DEBUG
check_public = ''
check_public = 'CHECKED' if public_bit == 1


# ロックチェック
p protect if $DEBUG
check_protect = ''
check_protect = 'CHECKED' if protect == 1


# 下書きチェック
p draft if $DEBUG
check_draft = ''
check_draft = 'CHECKED' if draft == 1


# 料理スタイル生成
html_type = lp[1]
html_type << '<select class="form-control form-control-sm" id="type">'
$RECIPE_TYPE.size.times do |c|
	if type == c
		html_type << "<option value='#{c}' SELECTED>#{$RECIPE_TYPE[c]}</option>"
	else
		html_type << "<option value='#{c}'>#{$RECIPE_TYPE[c]}</option>"
	end
end
html_type << '</select>'


# 献立区分
html_role = lp[2]
html_role << '<select class="form-control form-control-sm" id="role">'
$RECIPE_ROLE.size.times do |c|
	if role == c
		html_role << "<option value='#{c}' SELECTED>#{$RECIPE_ROLE[c]}</option>"
	else
		html_role << "<option value='#{c}'>#{$RECIPE_ROLE[c]}</option>"
	end
end
if role == 100
	html_role << "<option value='100' SELECTED>[ 調味％ ]</option>"
else
	html_role << "<option value='100'>[ 調味％ ]</option>"
end
html_role << '</select>'


# 調理区分
html_tech = lp[3]
html_tech << '<select class="form-control form-control-sm" id="tech">'
$RECIPE_TECH.size.times do |c|
	if tech == c
		html_tech << "<option value='#{c}' SELECTED>#{$RECIPE_TECH[c]}</option>"
	else
		html_tech << "<option value='#{c}'>#{$RECIPE_TECH[c]}</option>"
	end
end
html_tech << '</select>'


# 目安時間
html_time = lp[4]
html_time << '<select class="form-control form-control-sm" id="time">'
$RECIPE_TIME.size.times do |c|
	if time == c
		html_time << "<option value='#{c}' SELECTED>#{$RECIPE_TIME[c]}</option>"
	else
		html_time << "<option value='#{c}'>#{$RECIPE_TIME[c]}</option>"
	end
end
html_time << '</select>'


# 目安費用
html_cost = lp[5]
html_cost << '<select class="form-control form-control-sm" id="cost">'
$RECIPE_COST.size.times do |c|
	if cost == c
		html_cost << "<option value='#{c}' SELECTED>#{$RECIPE_COST[c]}</option>"
	else
		html_cost << "<option value='#{c}'>#{$RECIPE_COST[c]}</option>"
	end
end
html_cost << '</select>'


#### レシピフォームの表示
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{lp[6]}</h5></div>
		<div class="col-3">
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="public" #{check_public} onchange="recipeBit_public()"> #{lp[7]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="protect" #{check_protect} onchange="recipeBit_protect()"> #{lp[8]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="draft" #{check_draft} onchange="recipeBit_draft()"> #{lp[9]}
  				</label>
			</div>
		</div>
		<div class="col-1">
    	</div>
  		<div class="col-5">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="recipe_name">#{lp[10]}</label>
				</div>
      			<input type="text" class="form-control" id="recipe_name" value="#{recipe_name}" required>
				<div class="input-group-append">
      				<button class="btn btn-outline-primary" type="button" onclick="recipeSave_BWL2( '#{code}' )">#{lp[11]}</button>
				</div>
    		</div>
    	</div>
    </div>
    <br>
	<div class='row'>
		<div class='col'>#{html_type}</div>
		<div class='col'>#{html_role}</div>
		<div class='col'>#{html_tech}</div>
		<div class='col'>#{html_time}</div>
		<div class='col'>#{html_cost}</div>
	</div>
	<br>
	<div class='row'>
		<div class="col form-group">
			<div class="col">
    			<label for="exampleFormControlTextarea1">#{lp[12]}</label>
				<textarea class="form-control" id="protocol" rows="10">#{protocol}</textarea>
			</div>
  		</div>
	</div>
	<div align='right' class='code'>#{code}</div>
</div>
HTML

puts html
