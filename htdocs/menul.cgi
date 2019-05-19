#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser fctb menu list 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190122, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'menul.cgi'
$PAGE_LIMIT = 20
$DEBUG = false


#==============================================================================
#DEFINITION
#==============================================================================
### 表示範囲
def range_html( range, lp )
	range_select = []
	0.upto( 2 ) do |i|
		if range == i
			range_select[i] = 'SELECTED'
		else
			range_select[i] = ''
		end
	end

	html = '<select class="form-control form-control-sm" id="range">'
	html << "<option value='0' #{range_select[0]}>#{lp[12]}</option>"
	html << "<option value='1' #{range_select[1]}>#{lp[13]}</option>"
	html << "<option value='2' #{range_select[2]}>#{lp[14]}</option>"
	html << '</select>'

	return html
end


#### ラベルパーツ
def label_html( uname, label, lp )
	query = "SELECT label from #{$MYSQL_TB_MENU} WHERE user='#{uname}';"
	db_err = 'MENU select'
	res = db_process( query, db_err, false )
	label_list = []
	res.each do |e| label_list << e['label'] end
	label_list.uniq!

	html = '<select class="form-control form-control-sm" id="label">'
	label_list.each do |e|
		if e == nil
			html << "<option value='#{lp[15]}'>#{lp[15]}</option>"
		elsif label == e
			html << "<option value='#{e}' SELECTED>#{e}</option>"
		else
			html << "<option value='#{e}'>#{e}</option>"
		end
	end
	html << '</select>'

	return html
end


#### ページングパーツ
def pageing_html( page, page_start, page_end, page_max, lp )
	html = ''
	html << '<ul class="pagination pagination-sm justify-content-end">'
	if page == 1
		html << "<li class='page-item disabled'><span class='page-link'>#{lp[16]}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"recipeList2_BWL1( #{page - 1} )\">#{lp[16]}</span></li>"
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
		html << "<li class='page-item disabled'><span class='page-link'>#{lp[17]}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"recipeList2_BWL1( #{page + 1} )\">#{lp[17]}</span></li>"
	end
	html << '  </ul>'

	return html
end
#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'menul', language )
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "<hr>"
end


#### POSTデータの取得
command = cgi['command']
code = cgi['code']
page = cgi['page']
if $DEBUG
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "page: #{page}<br>"
	puts "<hr>"
end


if command == 'view'
	r = mariadb( "SELECT menul FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
	if r.first[0]
		a = r.first['menul'].split( ':' )
		page = a[0].to_i
		range = a[1].to_i
		label = a[2]
		page = 1 if page < 1
	else
		page = 1
		range = 0
		label = ''
	end
else
	page = cgi['page'].to_i
	range = cgi['range'].to_i
	label = cgi['label']
end
if $DEBUG
	puts "page: #{page}<br>"
	puts "range: #{range}<br>"
	puts "label: #{label}<br>"
	puts "<hr>"
end


#### 献立の削除
if command == 'delete'
	# 写真の削除
	File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}tns.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-tns.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}tn.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-tn.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}.jpg" )

	#レシピデータベースのの更新（削除）
	mariadb( "delete FROM #{$MYSQL_TB_MENU} WHERE user='#{uname}' and code='#{code}';", false )
end


#### 献立のインポート
#### 不完全
if command == 'import'
	# インポート元の読み込み
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE code='#{code}';", false )

	if r.first
		#レシピデータベースのの更新(新規)
		require 'securerandom'

		new_code = uname[0, 2]
		new_code = "x" + uname[0, 1] if new_code == nil
		new_code = "#{new_code}-#{SecureRandom.hex( 2 )}-#{SecureRandom.hex( 2 )}"

		mariadb( "INSERT INTO #{$MYSQL_TB_MENU} SET code='#{new_code}', user='#{uname}', public='0', name='*#{r.first['name']}', type='#{r.first['type']}', role='#{r.first['role']}', tech='#{r.first['tech']}', time='#{r.first['time']}', cost='#{r.first['cost']}', sum='#{r.first['sum']}', protocol='#{r.first['protocol']}', fig1='0', fig2='0', fig3='0', date='#{Time.now}';", false )
	end

end


#### WHERE setting
sql_where = "WHERE user='#{uname}'"


#### 表示範囲
html_range = range_html( range, lp )


#### ラベルhtml
html_label = label_html( uname, label, lp )


#### レシピ一覧ページ
r = mariadb( "SELECT * FROM #{$MYSQL_TB_MENU} #{sql_where} ORDER BY name;", false )
menu_num = r.size
page_max = menu_num / $PAGE_LIMIT + 1


#### ページングパーツ
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
html_paging = pageing_html( page, page_start, page_end, page_max, lp )


#### ページ内範囲抽出
menu_start = $PAGE_LIMIT * ( page - 1 )
menu_end = menu_start + $PAGE_LIMIT - 1
menu_end = r.size if menu_end >= r.size
if $DEBUG
	puts "page_start: #{page_start}<br>"
	puts "page_end: #{page_end}<br>"
	puts "page_max: #{page_max}<br>"
	puts "menu_start: #{menu_start}<br>"
	puts "menu_end: #{menu_end}<br>"
	puts "<hr>"
end


menu_html = ''
menu_count = 0
r.each do |e|
	if menu_count >= menu_start && menu_count <= menu_end
		menu_html << '<tr style="font-size:medium;">'
		if e['fig'] == 0 || e['fig'] == nil
			menu_html << "<td>-</td>"
		else
			menu_html << "<td>><a href='photo/#{e['code']}-tn.jpg' target='photo'><img src='photo/#{e['code']}-tns.jpg'></a></td>"
		end
		menu_html << "<td onclick=\"initMeal_BWL1( 'load', '#{e['code']}' )\">#{e['name']}</td>"

		menu_html << "<td>#{e['label']}</td>"
		menu_html << "<td>-</td>"


		menu_html << "<td>"
		if status >= 2
			menu_html << "<button type='button' class='btn btn btn-info btn-sm' onclick=\"addKoyomi_BWF( '#{e['code']}', 1 )\">#{lp[18]}</button>&nbsp;&nbsp;"
		end



		if e['user'] == uname
			menu_html << "<input type='checkbox' id='#{e['code']}'>&nbsp;<button class='btn btn-outline-danger btn-sm' type='button' onclick=\"menuDelete_BWL1( '#{e['code']}', '#{e['name']}' )\">#{lp[1]}</button>"
		else
			menu_html << "<button class='btn btn-outline-primary btn-sm' type='button' onclick=\"recipeImport_BWL1( '#{e['code']}' )\">#{lp[2]}</button>"
		end
		menu_html << "</td>"

	end
	menu_count += 1
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-7'><h5>#{lp[3]} (#{menu_num})</h5></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-2'>
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="range">#{lp[4]}</label>
				</div>
				#{html_range}
			</div>
		</div>
		<div class='col-4'>
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="menu_name">#{lp[5]}</label>
				</div>
				#{html_label}
			</div>
		</div>
		<div class='col-2'>
			<button class="btn btn-outline-warning btn-sm" type="button" onclick="menuList_BWL1( '#{page}' )">#{lp[6]}</button>
		</div>
	</div>
	<br>
	<table class="table table-sm table-hover">
	<thead>
		<tr>
			<td>#{lp[7]}</td>
			<td width="50%">#{lp[8]}</td>
			<td>#{lp[9]}</td>
			<td>#{lp[10]}</td>
			<td>#{lp[11]}</td>
		</tr>
	</thead>
	#{menu_html}
	</table>

	<div class='row'>
		<div class='col-7'></div>
		<div class='col-5'>#{html_paging}</div>
	</div>
HTML

puts html

#### 検索設定の保存
menul = "#{page}:#{range}:#{label}"
mariadb( "UPDATE #{$MYSQL_TB_CFG} SET menul='#{menul}' WHERE user='#{uname}';", false )
