#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser fctb menu list 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$PAGE_LIMIT = 20
@debug = false
script = 'menul'


#==============================================================================
#DEFINITION
#==============================================================================
### HTML display range
def range_html( range, lp )
	range_select = []
	0.upto( 3 ) do |i|
		if range == i
			range_select[i] = 'SELECTED'
		else
			range_select[i] = ''
		end
	end

	html = '<select class="form-select form-select-sm" id="range">'
	html << "<option value='0' #{range_select[0]}>#{lp[12]}</option>"
	html << "<option value='1' #{range_select[1]}>#{lp[19]}</option>"
	html << "<option value='2' #{range_select[2]}>#{lp[13]}</option>"
	html << "<option value='3' #{range_select[3]}>#{lp[14]}</option>"
	html << '</select>'

	return html
end


#### HTML of label
def label_html( uname, label, lp )
	r = mdb( "SELECT label from #{$MYSQL_TB_MENU} WHERE user='#{uname}' AND name!='';", false, @debug )
	label_list = []
	r.each do |e| label_list << e['label'] end
	label_list.uniq!

	html = '<select class="form-select form-select-sm" id="label">'
	html << "<option value=''>#{lp[12]}</option>"
	label_list.each do |e| html << "<option value='#{e}' #{selected( e, label )}}>#{e}</option>" end
	html << '</select>'

	return html
end


#### HTML of Paging
def pageing_html( page, page_start, page_end, page_max, lp )
	html = ''
	html << '<ul class="pagination pagination-sm justify-content-end">'
	if page == 1
		html << "<li class='page-item disabled'><span class='page-link'>#{lp[16]}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"menuList( #{page - 1} )\">#{lp[16]}</span></li>"
	end
	unless page_start == 1
		html << "<li class='page-item'><a class='page-link' onclick=\"menuList( '1' )\">1…</a></li>"
	end
	page_start.upto( page_end ) do |c|
		active = ''
		active = ' active' if page == c
		html << "<li class='page-item#{active}'><a class='page-link' onclick=\"menuList( #{c} )\">#{c}</a></li>"
	end
	unless page_end == page_max
		html << "<li class='page-item'><a class='page-link' onclick=\"menuList( '#{page_max}' )\">…#{page_max}</a></li>"
	end
	if page == page_max
		html << "<li class='page-item disabled'><span class='page-link'>#{lp[17]}</span></li>"
	else
		html << "<li class='page-item'><span class='page-link' onclick=\"menuList( #{page + 1} )\">#{lp[17]}</span></li>"
	end
	html << '  </ul>'

	return html
end
#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### Getting POST data
command = cgi['command']
code = cgi['code']
page = cgi['page']
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "page: #{page}<br>"
	puts "<hr>"
end


if command == 'view'
	r = mdb( "SELECT menul FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
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
	page = 1 if page < 1
	range = cgi['range'].to_i
	label = cgi['label']
end
if @debug
	puts "page: #{page}<br>"
	puts "range: #{range}<br>"
	puts "label: #{label}<br>"
	puts "<hr>"
end


#### Deleting menu
if command == 'delete'
	# 写真の削除
	File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}tns.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-tns.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}tn.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-tn.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{code}-#{c + 1}.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}.jpg" )
	#レシピデータベースのの更新（削除）
	menu = Menu.new( user.name )
	menu.code = code
	menu.delete_db

	meal = Meal.new( user.name )
	if meal.code == code
		meal.code = ''
		meal.name = ''
		meal.update_db
	end
end


#### 献立のインポート
#### 不完全
if command == 'import'
	# インポート元の読み込み
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE code='#{code}';", false, @debug )

	if r.first
		#レシピデータベースのの更新(新規)
		new_code = generate_code( user.name, 'm' )
#		mdb( "INSERT INTO #{$MYSQL_TB_MENU} SET code='#{new_code}', user='#{user.name}', public='0', name='*#{r.first['name']}', type='#{r.first['type']}', role='#{r.first['role']}', tech='#{r.first['tech']}', time='#{r.first['time']}', cost='#{r.first['cost']}', sum='#{r.first['sum']}', protocol='#{r.first['protocol']}', fig1='0', fig2='0', fig3='0', date='#{$DATETIME}';", false, @debug )
	end

end


#### WHERE setting
sql_where = "WHERE "
case range
when 1
	sql_where << "user='#{user.name}' AND name!='' AND protect=1"
when 2
	sql_where << "user='#{user.name}' AND name!='' AND public=1"
when 3
	sql_where << "user!='#{user.name}' AND name!='' AND public=1"
else
	sql_where << "user='#{user.name}' AND name!=''"
end
sql_where << " AND label='#{label}'" unless label == ''


#### 表示範囲
html_range = range_html( range, lp )


#### HTML label
html_label = label_html( user.name, label, lp )


#### レシピ一覧ページ
r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} #{sql_where} ORDER BY name;", false, @debug )
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
if @debug
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
		if user.status >= 2
			menu_html << "<span onclick=\"addKoyomi_BWF( '#{e['code']}', 1 )\">#{lp[18]}</span>&nbsp;&nbsp;"
		end
		menu_html << "</td>"

		menu_html << "<td>"
		if e['user'] == user.name
			menu_html << "<input type='checkbox' id='#{e['code']}'>&nbsp;<span onclick=\"menuDelete( '#{e['code']}', '#{e['name']}' )\">#{lp[1]}</span>"
		else
			menu_html << "<span onclick=\"menuImport( '#{e['code']}' )\">#{lp[2]}</span>"
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
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="range">#{lp[4]}</label>
				#{html_range}
			</div>
		</div>
		<div class='col-4'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="menu_name">#{lp[5]}</label>
				#{html_label}
			</div>
		</div>
		<div class='col-2'>
			<button class="btn btn-outline-primary btn-sm" type="button" onclick="menuList2( '#{page}' )">#{lp[6]}</button>
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
			<td></td>
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
mdb( "UPDATE #{$MYSQL_TB_CFG} SET menul='#{menul}' WHERE user='#{user.name}';", false, @debug )
