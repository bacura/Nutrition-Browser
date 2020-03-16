#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe list 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171114, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$PAGE_LIMIT = 50
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### 表示範囲
def range_html( range )
	range_select = []
	0.upto( 5 ) do |i|
		if range == i
			range_select[i] = 'SELECTED'
		else
			range_select[i] = ''
		end
	end

	html = '表示範囲'
	html << '<select class="form-control form-control-sm" id="range">'
	html << "<option value='0' #{range_select[0]}>全て</option>"
	html << "<option value='1' #{range_select[1]}>下書き</option>"
	html << "<option value='2' #{range_select[2]}>保護</option>"
	html << "<option value='3' #{range_select[3]}>公開</option>"
	html << "<option value='4' #{range_select[4]}>無印</option>"
	html << "<option value='5' #{range_select[5]}>公開(他)</option>"
	html << '</select>'

	return html
end


#### 料理スタイル生成
def type_html( type )
	html = '料理スタイル'
	html << '<select class="form-control form-control-sm" id="type">'
	html << "<option value='99'>全て</option>"
	$RECIPE_TYPE.size.times do |c|
		if type == c
			html << "<option value='#{c}' SELECTED>#{$RECIPE_TYPE[c]}</option>"
		else
			html << "<option value='#{c}'>#{$RECIPE_TYPE[c]}</option>"
		end
	end
	html << '</select>'

	return html
end


#### 献立区分
def role_html( role )
	html = '献立区分'
	html << '<select class="form-control form-control-sm" id="role">'
	html << "<option value='99'>全て</option>"
	$RECIPE_ROLE.size.times do |c|
		if role == c
			html << "<option value='#{c}' SELECTED>#{$RECIPE_ROLE[c]}</option>"
		else
			html << "<option value='#{c}'>#{$RECIPE_ROLE[c]}</option>"
		end
	end
	if role == 100
		html << "<option value='100' SELECTED>[ 調味％ ]</option>"
	else
		html << "<option value='100'>[ 調味％ ]</option>"
	end
	html << '</select>'

	return html
end


#### 調理区分
def tech_html( tech )
	html = '調理区分'
	html << '<select class="form-control form-control-sm" id="tech">'
	html << "<option value='99'>全て</option>"
	$RECIPE_TECH.size.times do |c|
		if tech == c
			html << "<option value='#{c}' SELECTED>#{$RECIPE_TECH[c]}</option>"
		else
			html << "<option value='#{c}'>#{$RECIPE_TECH[c]}</option>"
		end
	end
html << '</select>'

	return html
end


#### 目安時間
def time_html( time )
	html = '目安時間(分)'
	html << '<select class="form-control form-control-sm" id="time">'
	html << "<option value='99'>全て</option>"
	$RECIPE_TIME.size.times do |c|
		if time == c
			html << "<option value='#{c}' SELECTED>#{$RECIPE_TIME[c]}</option>"
		else
			html << "<option value='#{c}'>#{$RECIPE_TIME[c]}</option>"
		end
	end
	html << '</select>'

	return html
end


#### 目安費用
def cost_html( cost )
	html = '目安費用(円)'
	html << '<select class="form-control form-control-sm" id="cost">'
	html << "<option value='99'>全て</option>"
	$RECIPE_COST.size.times do |c|
		if cost == c
			html << "<option value='#{c}' SELECTED>#{$RECIPE_COST[c]}</option>"
		else
			html << "<option value='#{c}'>#{$RECIPE_COST[c]}</option>"
		end
	end
	html << '</select>'

	return html
end


#### ページングパーツ
def pageing_html( page, page_start, page_end, page_max )
	html = ''
	html << '<ul class="pagination pagination-sm justify-content-end">'
	if page == 1
		html << '<li class="page-item disabled"><span class="page-link">前頁</span></li>'
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"recipeList2_BWL1( #{page - 1} )\">前頁</span></li>"
	end
	unless page_start == 1
		html << "<li class='page-item'><a class='page-link' onclick=\"recipeList2_BWL1( '1' )\">1…</a></li>"
	end
	page_start.upto( page_end ) do |c|
		active = ''
		active = ' active' if page == c
		html << "<li class='page-item#{active}'><a class='page-link' onclick=\"recipeList2_BWL1( #{c} )\">#{c}</a></li>"
	end
	unless page_end == page_max
		html << "<li class='page-item'><a class='page-link' onclick=\"recipeList2_BWL1( '#{page_max}' )\">…#{page_max}</a></li>"
	end
	if page == page_max
		html << '<li class="page-item disabled"><span class="page-link">次頁</span></li>'
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"recipeList2_BWL1( #{page + 1} )\">次頁</span></li>"
	end
	html << '  </ul>'

	return html
end


def referencing( words, uname )
	words.gsub!( /\s+/, "\t")
	words.gsub!( /　+/, "\t")
	words.gsub!( /,+/, "\t")
	words.gsub!( /、+/, "\t")
	words.gsub!( /\t{2,}/, "\t")
	query_word = words.split( "\t" )
	query_word.uniq!

	# Recoding query & converting by DIC
	true_query = []
	query_word.each do |e|
		mdb( "INSERT INTO #{$MYSQL_TB_SLOGR} SET user='#{uname}', words='#{e}', date='#{$DATETIME}';", false, @debug )
		r = mdb( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{e}';", false, @debug )
		if r.first
			rr = mdb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE class1='#{r.first['org_name']}' OR class2='#{r.first['org_name']}' OR class3='#{r.first['org_name']}';", false, @debug )
			if rr.first
				rr.each do |ee|
					true_query << ee['name']
				end
			else
				true_query << r.first['org_name']
			end
		else
			true_query << e
		end
	end
	if @debug
		puts "query_word:"
		puts query_word
		puts "true_query:"
		puts true_query
		puts "<hr>"
	end

	# Referencing recipe code
	recipe_code_list = []
	true_query.each do |e|
		r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE word='#{e}' AND ( user='#{uname}' OR public='1' );", false, @debug )
		r.each do |ee|
			recipe_code_list << ee['code']
		end
	end
	recipe_code_list.uniq!

	return recipe_code_list
end

#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'recipel', language )

html_init( nil )
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
words = cgi['words']
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "words: #{words}<br>"
	puts "<hr>"
end


#### 検索条件設定
page = 1
range = 0
type = 99
role = 99
tech = 99
time = 99
cost = 99
recipe_code_list = []
case command
when 'init'
	r = mdb( "SELECT recipel FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, status )
	if r.first
		a = r.first['recipel'].split( ':' )
		page = a[0].to_i
		page = 1 if page == 0
		range = a[1].to_i
		type = a[2].to_i
		role = a[3].to_i
		tech = a[4].to_i
		time = a[5].to_i
		cost = a[6].to_i
	end
when 'reset'
	words = ''
when 'refer'
	recipe_code_list = referencing( words, uname ) if words != '' && words != nil
	words = lp[1] if recipe_code_list.size == 0
else
	page = cgi['page'].to_i
	page = 1 if page == 0
	range = cgi['range'].to_i
	type = cgi['type'].to_i
	role = cgi['role'].to_i
	tech = cgi['tech'].to_i
	time = cgi['time'].to_i
	cost = cgi['cost'].to_i

	r = mdb( "SELECT reciperr FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, status )
	if r.first['reciperr'] != '' && r.first['reciperr'] != nil
		recipe_code_list = referencing( r.first['reciperr'], uname )
		words = r.first['reciperr']
	end
end
if @debug
	puts "page: #{page}<br>"
	puts "range: #{range}<br>"
	puts "type: #{type}<br>"
	puts "role: #{role}<br>"
	puts "tech: #{tech}<br>"
	puts "time: #{time}<br>"
	puts "cost: #{cost}<br>"
	puts "recipe_code_list: #{recipe_code_list}<br>"
	puts "<hr>"
end


#### レシピの削除
if command == 'delete'
	# 写真の削除
	3.times do |c|
		File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}tns.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-#{c + 1}tns.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}tn.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-#{c + 1}tn.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-#{c + 1}.jpg" )
	end
	#レシピデータベースのの更新（削除）
	mdb( "delete FROM #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' and code='#{code}';", false, status )
end


#### レシピのインポート
if command == 'import'
	# インポート元の読み込み
	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';", false, status )

	if r.first
		#レシピデータベースのの更新(新規)
		require 'securerandom'
		require 'fileutils'

		new_code = uname[0, 2]
		new_code = "x" + uname[0, 1] if new_code == nil
		new_code = "#{new_code}-#{SecureRandom.hex( 2 )}-#{SecureRandom.hex( 2 )}"

		import_fig1 = 0
		import_fig2 = 0
		import_fig3 = 0

		# 写真のコピー
		if r.first['fig1'] == 1
			FileUtils.cp( "#{$PHOTO_PATH}/#{code}-1tns.jpg", "#{$PHOTO_PATH}/#{new_code}-1tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-1tns.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{code}-1tn.jpg", "#{$PHOTO_PATH}/#{new_code}-1tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-1tn.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{code}-1.jpg", "#{$PHOTO_PATH}/#{new_code}-1.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-1.jpg" )
			import_fig1 = 1
		end

		if r.first['fig2'] == 1
			FileUtils.cp( "#{$PHOTO_PATH}/#{code}-2tns.jpg", "#{$PHOTO_PATH}/#{new_code}-2tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-2tns.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{code}-2tn.jpg", "#{$PHOTO_PATH}/#{new_code}-2tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-2tn.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{code}-2.jpg", "#{$PHOTO_PATH}/#{new_code}-2.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-2.jpg" )
			import_fig2 = 1
		end

		if r.first['fig3'] == 1
			FileUtils.cp( "#{$PHOTO_PATH}/#{code}-3tns.jpg", "#{$PHOTO_PATH}/#{new_code}-3tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-3tns.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{code}-3tn.jpg", "#{$PHOTO_PATH}/#{new_code}-3tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-3tn.jpg" )
			FileUtils.cp( "#{$PHOTO_PATH}/#{code}-3.jpg", "#{$PHOTO_PATH}/#{new_code}-3.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-3.jpg" )
			import_fig3 = 1
		end

		mdb( "INSERT INTO #{$MYSQL_TB_RECIPE} SET code='#{new_code}', user='#{uname}', dish='#{r.first['dish']}', public='0', protect='0', draft='1', name='#{r.first['name']}', type='#{r.first['type']}', role='#{r.first['role']}', tech='#{r.first['tech']}', time='#{r.first['time']}', cost='#{r.first['cost']}', sum='#{r.first['sum']}', protocol='#{r.first['protocol']}', fig1='#{import_fig1}', fig2='#{import_fig2}', fig3='#{import_fig3}', date='#{$DATETIME}';", false, status )
		mdb( "UPDATE #{$MYSQL_TB_SUM} SET code='#{new_code}', dish='#{r.first['dish']}', protect='0', name='#{r.first['name']}', sum='#{r.first['sum']}' WHERE user='#{uname}';", false, status )
	end

end


#### WHERE setting
sql_where = 'WHERE '

case range
# 自分の全て
when 0
	sql_where << " user='#{uname}' AND name!=''"
# 自分の下書き
when 1
	sql_where << "user='#{uname}' AND name!='' AND draft='1'"
# 自分の保護
when 2
	sql_where << "user='#{uname}' AND protect='1' AND name!=''"
# 自分の公開
when 3
	sql_where << "user='#{uname}' AND public='1' AND name!=''"
# 自分の無印
when 4
	sql_where << "user='#{uname}' AND public='0' AND draft='0' AND name!=''"
# 他の公開
when 5
	sql_where << "public='1' AND user!='#{uname}' AND name!=''"
else
	sql_where << " user='#{uname}' AND name!=''"
end

sql_where << " AND type='#{type}'" unless type == 99
sql_where << " AND role='#{role}'" unless role == 99
sql_where << " AND tech='#{tech}'" unless tech == 99
sql_where << " AND time>0 AND time<=#{time}" unless time == 99
sql_where << " AND cost>0 AND cost<=#{cost}" unless cost == 99


# 検索条件HTML
html_range = range_html( range )
html_type = type_html( type )
html_role = role_html( role )
html_tech = tech_html( tech )
html_time = time_html( time )
html_cost = cost_html( cost )


#### レシピ一覧ページ
recipe_solid = []
if recipe_code_list.size > 0
	recipe_code_list.each do |e|
		r = mdb( "SELECT code, user, protect, public, draft, name, fig1 FROM #{$MYSQL_TB_RECIPE} #{sql_where} AND code='#{e}';", false, status )
		if r.first
			recipe_solid << Hash['code' => e, 'user' => r.first['user'], 'protect' => r.first['protect'], 'name' => r.first['name'], 'fig1' => r.first['fig1']]
		end
	end
else
	r = mdb( "SELECT code, user, protect, public, draft, name, fig1 FROM #{$MYSQL_TB_RECIPE} #{sql_where} ORDER BY name;", false, status )
	recipe_solid = r
end


#### ページングパーツ
recipe_num = recipe_solid.size
page_max = recipe_num / $PAGE_LIMIT + 1
page_start = 1
page_end = page_max
if page_end > 5
	if page > 3
		page_start = page - 3
		page_start = page_max - 6 if page_max - page_start < 7
	end
	if page_end - page < 3
		page_end = page_max
	else
		page_end = page + 3
		page_end = 7 if page_end < 7
	end
else
	page_end = page_max
end
html_paging = pageing_html( page, page_start, page_end, page_max )


#### ページ内範囲抽出
recipe_start = $PAGE_LIMIT * ( page - 1 )
recipe_end = recipe_start + $PAGE_LIMIT - 1
recipe_end = recipe_solid.size if recipe_end >= recipe_solid.size


recipe_html = ''
recipe_count = 0
recipe_solid.each do |e|
	if recipe_count >= recipe_start && recipe_count <= recipe_end
		recipe_html << '<tr style="font-size:medium;">'

		if e['fig1'] == 0
			recipe_html << "<td>-</td>"
		else
			recipe_html << "<td><a href='photo/#{e['code']}-1tn.jpg' target='photo'><img src='photo/#{e['code']}-1tns.jpg'></a></td>"
		end
		if e['user'] == uname
			recipe_html << "<td onclick=\"initCB_BWL1( 'load', '#{e['code']}' )\">#{e['name']}</td>"
		else
			recipe_html << "<td>#{e['name']}</td>"
		end

		recipe_html << "<td>"
		if e['public'] == 1
			recipe_html << lp[2]
		else
			recipe_html << lp[7]
		end
		if e['protect'] == 1
			recipe_html << lp[3]
		else
			recipe_html << lp[7]
		end
		if e['draft'] == 1
			recipe_html << lp[4]
		else
			recipe_html << lp[7]
		end

		recipe_html << "</td>"
		recipe_html << "<td>"
		if status >= 2 && e['user'] == uname
			recipe_html << "	<button class='btn btn-dark btn-sm' type='button' onclick=\"addingMeal( '#{e['code']}' )\">#{lp[8]}</button>&nbsp;"
		end
		if status >= 2 && e['user'] == uname
			recipe_html << "&nbsp;<button type='button' class='btn btn btn-info btn-sm' onclick=\"addKoyomi_BWF( '#{e['code']}', 1 )\">#{lp[21]}</button>"
		end
		recipe_html << "	<button class='btn btn-success btn-sm' type='button' onclick=\"print_templateSelect_BWL2( '#{e['code']}' )\">#{lp[9]}</button>"
		recipe_html << "	<button class='btn btn-outline-light btn-sm' type='button' onclick=\"\">#{lp[19]}</button>"
		if status >= 2 && e['user'] == uname
			recipe_html << "	<button class='btn btn-primary btn-sm' type='button' onclick=\"\">#{lp[20]}</button>&nbsp;"
		end
		recipe_html << "</td>"

		if e['user'] == uname
			if e['protect'] == 0
				recipe_html << "<td><input type='checkbox' id='#{e['code']}'>&nbsp;<button class='btn btn-outline-danger btn-sm' type='button' onclick=\"recipeDelete_BWL1( '#{e['code']}', #{page} )\">#{lp[10]}</button></td>"
			else
				recipe_html << "<td></td>"
			end
		else
			recipe_html << "<td><button class='btn btn-outline-primary btn-sm' type='button' onclick=\"recipeImport_BWL1( '#{e['code']}', '#{page}' )\">#{lp[11]}</button></td>"
		end
		recipe_html << '</tr>'
	end
	recipe_count += 1
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-7'><h5>#{lp[12]} (#{recipe_num}) #{words}</h5></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
	<br>
	<div class='row'>
		<div class='col'>#{html_range}</div>
		<div class='col'>#{html_type}</div>
		<div class='col'>#{html_role}</div>
		<div class='col'>#{html_tech}</div>
		<div class='col'>#{html_time}</div>
		<div class='col'>#{html_cost}</div>
	</div><br>
	<div class='row'>
		<div class='col-5'></div>
		<div class='col-5'><button class="btn btn-outline-primary btn-sm" type="button" onclick="recipeList2_BWL1( 'init' )">#{lp[13]}</button></div>
		<div class='col-2'><button class="btn btn-outline-primary btn-sm" type="button" onclick="recipeList_BWL1( 'reset' )">#{lp[14]}</button></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
		<tr>
			<td>#{lp[15]}</td>
			<td width="50%">#{lp[16]}</td>
			<td>#{lp[17]}</td>
			<td>#{lp[18]}</td>
		</tr>
	</thead>

		#{recipe_html}
	</table>

	<div class='row'>
		<div class='col-7'></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
</div>
HTML

puts html

#### 検索設定の保存
recipel = "#{page}:#{range}:#{type}:#{role}:#{tech}:#{time}:#{cost}"
reciperr = ''
reciperr = "#{words}" if recipe_code_list.size > 0
mdb( "UPDATE #{$MYSQL_TB_CFG} SET recipel='#{recipel}', reciperr='#{reciperr}' WHERE user='#{uname}';", false, status )
