#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe list 0.20b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'recipel'
page_limit = 50
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
		html << "<li class='page-item'><span class='page-link' onclick=\"recipeList2( #{page - 1} )\">前頁</span></li>"
	end
	unless page_start == 1
		html << "<li class='page-item'><a class='page-link' onclick=\"recipeList2( '1' )\">1…</a></li>"
	end
	page_start.upto( page_end ) do |c|
		active = ''
		active = ' active' if page == c
		html << "<li class='page-item#{active}'><a class='page-link' onclick=\"recipeList2( #{c} )\">#{c}</a></li>"
	end
	unless page_end == page_max
		html << "<li class='page-item'><a class='page-link' onclick=\"recipeList2( '#{page_max}' )\">…#{page_max}</a></li>"
	end
	if page == page_max
		html << '<li class="page-item disabled"><span class="page-link">次頁</span></li>'
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"recipeList2( #{page + 1} )\">次頁</span></li>"
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
		puts "query_word:#{query_word}<br>"
		puts "true_query:#{true_query}<br>"
		puts "<hr>"
	end

	# Referencing recipe code
	recipe_code_list = []
	true_query.each do |e|
		if e =~ /\-r\-/
			recipe_code_list << e
		else
			r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE word='#{e}' AND ( user='#{uname}' OR public='1' );", false, @debug )
			r.each do |ee|
				recipe_code_list << ee['code']
			end
		end
	end
	recipe_code_list.uniq!

	return recipe_code_list
end

#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )

r = mdb( "SELECT icache, ilist FROM cfg WHERE user='#{user.name}';", false, @debug )
if r.first['icache'].to_i == 1
	html_init_cache( nil )
else
	html_init( nil )
end
page_limit = r.first['ilist'].to_i unless r.first['ilist'].to_i == 0


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
	r = mdb( "SELECT recipel FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
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
	recipe_code_list = referencing( words, user.name ) if words != '' && words != nil
	words = lp[1] if recipe_code_list.size == 0

when 'delete'
	# Deleting photos
	3.times do |c|
		File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}tns.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-#{c + 1}tns.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}tn.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-#{c + 1}tn.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-#{c + 1}.jpg" )
	end
	# Deleting recipe from DB
	mdb( "delete FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' and code='#{code}';", false, @debug )

	# Updating SUM
	r = mdb( "SELECT code FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}' and code='#{code}';", false, @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_SUM} SET sum='', code='', name='', protect=0, dish=1 WHERE user='#{user.name}';", false, @debug )
	end

	exit

when 'import', 'subspecies'
	# Loading original recipe
	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE code='#{code}';", false, @debug )
	if r.first
		require 'fileutils'
		# Generating new code
		new_code = generate_code( user.name, 'r' )

		# Copying phots
		import_figs = [ nil, 0, 0, 0 ]
		figs = [nil, 'fig1', 'fig2', 'fig3' ]
		1.upto( 3 ) do |c|
			if r.first[figs[c]] == 1
				FileUtils.cp( "#{$PHOTO_PATH}/#{code}-1tns.jpg", "#{$PHOTO_PATH}/#{new_code}-1tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-1tns.jpg" )
				FileUtils.cp( "#{$PHOTO_PATH}/#{code}-1tn.jpg", "#{$PHOTO_PATH}/#{new_code}-1tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-1tn.jpg" )
				FileUtils.cp( "#{$PHOTO_PATH}/#{code}-1.jpg", "#{$PHOTO_PATH}/#{new_code}-1.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{code}-1.jpg" )
				import_figs[c] = 1
			end
		end

		# Insertinbg recipe into DB
		if command == 'import'
			mdb( "INSERT INTO #{$MYSQL_TB_RECIPE} SET code='#{new_code}', user='#{user.name}', dish='#{r.first['dish']}', public='0', protect='0', draft='1', name='#{r.first['name']}', type='#{r.first['type']}', role='#{r.first['role']}', tech='#{r.first['tech']}', time='#{r.first['time']}', cost='#{r.first['cost']}', sum='#{r.first['sum']}', protocol='#{r.first['protocol']}', fig1='#{import_figs[1]}', fig2='#{import_figs[2]}', fig3='#{import_figs[3]}', date='#{$DATETIME}';", false, @debug )
		elsif command == 'subspecies'
			mdb( "INSERT INTO #{$MYSQL_TB_RECIPE} SET code='#{new_code}', user='#{user.name}', root='#{code}', dish='#{r.first['dish']}', public='0', protect='0', draft='1', name='#{r.first['name']}', type='#{r.first['type']}', role='#{r.first['role']}', tech='#{r.first['tech']}', time='#{r.first['time']}', cost='#{r.first['cost']}', sum='#{r.first['sum']}', protocol='#{r.first['protocol']}', fig1='#{import_figs[1]}', fig2='#{import_figs[2]}', fig3='#{import_figs[3]}', date='#{$DATETIME}';", false, @debug )
		end
	end

	exit

else
	page = cgi['page'].to_i
	page = 1 if page == 0
	range = cgi['range'].to_i
	type = cgi['type'].to_i
	role = cgi['role'].to_i
	tech = cgi['tech'].to_i
	time = cgi['time'].to_i
	cost = cgi['cost'].to_i

	r = mdb( "SELECT reciperr FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	if r.first['reciperr'] != '' && r.first['reciperr'] != nil
		recipe_code_list = referencing( r.first['reciperr'], user.name )
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


#### WHERE setting
sql_where = 'WHERE '

case range
# 自分の全て
when 0
	sql_where << " user='#{user.name}' AND name!=''"
# 自分の下書き
when 1
	sql_where << "user='#{user.name}' AND name!='' AND draft='1'"
# 自分の保護
when 2
	sql_where << "user='#{user.name}' AND protect='1' AND name!=''"
# 自分の公開
when 3
	sql_where << "user='#{user.name}' AND public='1' AND name!=''"
# 自分の無印
when 4
	sql_where << "user='#{user.name}' AND public='0' AND draft='0' AND name!=''"
# 他の公開
when 5
	sql_where << "public='1' AND user!='#{user.name}' AND name!=''"
else
	sql_where << " user='#{user.name}' AND name!=''"
end

sql_where << " AND type='#{type}'" unless type == 99
sql_where << " AND role='#{role}'" unless role == 99
sql_where << " AND tech='#{tech}'" unless tech == 99
sql_where << " AND time>0 AND time<=#{time}" unless time == 99
sql_where << " AND cost>0 AND cost<=#{cost}" unless cost == 99


#### 検索条件HTML
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
		r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} #{sql_where} AND code='#{e}';", false, @debug )
		recipe_solid << r.first if r.first
	end
else
	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} #{sql_where} ORDER BY name;", false, @debug )
	recipe_solid = r
end


#### ページングパーツ
recipe_num = recipe_solid.size
page_max = recipe_num / page_limit + 1
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
recipe_start = page_limit * ( page - 1 )
recipe_end = recipe_start + page_limit - 1
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
		if e['user'] == user.name
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
		if user.status >= 2 && e['user'] == user.name
			recipe_html << "	<span onclick=\"addingMeal( '#{e['code']}' )\">#{lp[8]}</span>&nbsp;"
		end
		if user.status >= 2 && e['user'] == user.name
			recipe_html << "&nbsp;<span onclick=\"addKoyomi_BWF( '#{e['code']}' )\">#{lp[21]}</span>"
		end
		recipe_html << "	<span onclick=\"print_templateSelect( '#{e['code']}' )\">#{lp[9]}</span>"
		if user.status >= 2 && e['user'] == user.name && ( e['root'] == nil || e['root'] == '' )
			recipe_html << "	<span onclick=\"recipeImport( 'subspecies', '#{e['code']}', '#{page}' )\">#{lp[20]}</span>&nbsp;"
		end
		recipe_html << "</td>"

		if e['user'] == user.name
			if e['protect'] == 0
				recipe_html << "<td><input type='checkbox' id='#{e['code']}'>&nbsp;<span onclick=\"recipeDelete( '#{e['code']}', #{page} )\">#{lp[10]}</span></td>"
			else
				recipe_html << "<td></td>"
			end
		else
			recipe_html << "<td><span onclick=\"recipeImport( 'import', '#{e['code']}', '#{page}' )\">#{lp[11]}</span></td>"
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
		<div class='col-5'><button class="btn btn-outline-primary btn-sm" type="button" onclick="recipeList2( '#{page}' )">#{lp[13]}</button></div>
		<div class='col-2'><button class="btn btn-outline-primary btn-sm" type="button" onclick="recipeList( 'reset' )">#{lp[14]}</button></div>
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
mdb( "UPDATE #{$MYSQL_TB_CFG} SET recipel='#{recipel}', reciperr='#{reciperr}' WHERE user='#{user.name}';", false, @debug )
