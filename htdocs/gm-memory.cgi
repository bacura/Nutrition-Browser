#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM memory editor 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190226, 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'gm-memory.cgi'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

def init()
	new_html = ''
	memory_html = ''
	category_list = []
	pointer_num = []
	r = mariadb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};", false )
	r.each do |e|
		rr = mariadb( "SELECT DISTINCT pointer FROM #{$MYSQL_TB_MEMORY} WHERE category='#{e['category']}';", false )
		category_list << e['category']
		pointer_num << rr.size
	end
	memory_html << "<table class='table-striped table-bordered'>"
	memory_html << "<thead>"
	memory_html << "<th>カテゴリー</th>"
	memory_html << "<th>項目数</th>"
	memory_html << "<th></th>"
	memory_html << "</thead>"
	category_list.size.times do |c|
		memory_html << "<tr>"
		memory_html << "<td onclick=\"editMemory_BWLF( '#{category_list[c]}' )\">#{category_list[c]}</td>"
		memory_html << "<td>#{pointer_num[c]}</td>"
		memory_html << "<td><input type='checkbox' id='delete_check#{c}'>&nbsp;"
		memory_html << "<button type='button' class='btn btn-danger btn-sm nav_button' onclick=\"deleteMemory_BWLF( '#{category_list[c]}', 'delete_check#{c}' )\">削除</button></td>"
		memory_html << "</tr>"
	end
	memory_html << "</table>"

	new_html << "<div class='row'>"
	new_html << "<div class='col-8'></div>"
	new_html << "<div class='col-2'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"newCategory_BWLF()\">新規カテゴリー</button></div>"
	new_html << "<div class='col-2'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"newMemory_BWLF()\">一括登録</button></div>"
	new_html << "</div>"
	new_html << "</div>"

	return new_html, memory_html
end

def edit( category )
	new_html = ''
	memory_html = ''

	r = mariadb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false )
	memory_html << "<table class='table-striped table-bordered'>"
	memory_html << "<thead>"
	memory_html << "<th>キー</th>"
	memory_html << "<th>記憶</th>"
	memory_html << "<th>ランク</th>"
	memory_html << "<th></th>"
	memory_html << "</thead>"
	c = 0
	r.each do |e|
		memory_html << "<tr>"
		memory_html << "<td onclick=\"newPMemory_BWLF( '#{category}', '#{e['pointer']}', 'front' )\">#{e['pointer']}</td>"
		if e['memory'].size > 80
			memory_html << "<td onclick=\"newPMemory_BWLF( '#{category}', '#{e['pointer']}', 'front' )\">#{e['memory'][0, 80]}...</td>"
		else
			memory_html << "<td onclick=\"newPMemory_BWLF( '#{category}', '#{e['pointer']}', 'front' )\">#{e['memory']}</td>"
		end
		memory_html << "<td>#{e['rank']}</td>"
		memory_html << "<td><input type='checkbox' id='delete_check#{c}'>&nbsp;"
		memory_html << "<button type='button' class='btn btn-danger btn-sm nav_button' onclick=\"deletePMemory_BWLF( '#{category}', '#{e['pointer']}', 'delete_check#{c}' )\">削除</button></td>"
		memory_html << "</tr>"
		c += 1
	end
	memory_html << "</table>"

	new_html << "<div class='row'>"
	new_html << "<div class='col-10'></div>"
	new_html << "<div class='col-2'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"newPMemory_BWLF( '#{category}', '' )\">新規登録</button></div>"
	new_html << "</div>"
	new_html << "</div>"

	return new_html, memory_html
end
#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'gm-account', language )
if @debug
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
end


#### GM check
if status < 9
	puts "GM error."
	exit
end


#### Getting POST data
command = cgi['command']
mode = cgi['mode']
category = cgi['category']
pointer = cgi['pointer']
rank = cgi['rank'].to_i
post_process = cgi['post_process']
memory = cgi['memory']
memory_solid = cgi['memory']
memory_solid.gsub!( ',', "\t" ) if memory_solid != nil && memory_solid != ''
if @debug
	puts "command:#{command}<br>\n"
	puts "mode:#{mode}<br>\n"
	puts "category:#{category}<br>\n"
	puts "pointer:#{pointer}<br>\n"
	puts "rank:#{rank}<br>\n"
	puts "post_process:#{post_process}<br>\n"
#	puts "memory:#{memory}<br>\n"
#	puts "memory_solid:#{memory_solid}<br>\n"
	puts "<hr>\n"
end


memory_html = ''
new_html = ''
title = ''
case command
when 'init'
	new_html, memory_html = init()

when 'edit'
	new_html, memory_html = edit( category )

when 'new'
	memory_html << "<div class='row'>"
	memory_html << "	<textarea class='form-control' aria-label='memory' id='memory'></textarea>"
	memory_html << "※タブもしくはカンマ区切りで、キー、記憶、カテゴリ、ランク。複数行可。"
	memory_html << "</div>"
	memory_html << "</div><br>"
	memory_html << "<div class='row'>"
	memory_html << "<div class='col-2'><button type='button' class='btn btn-success btn-sm' onclick=\"saveMemory_BWLF( 'insert' )\">記憶追加</button></div>"
	memory_html << "<div class='col-2'><button type='button' class='btn btn-warning btn-sm' onclick=\"saveMemory_BWLF( 'update' )\">記憶置換</button></div>"
	memory_html << "</div>"

when 'new_category'
	memory_html << "<div class='row'>"
	memory_html << "	<div class='input-group input-group-sm'>"
  	memory_html << "		<div class='input-group-prepend'>"
    memory_html << "			<span class='input-group-text' id='inputGroup-sizing-sm'>新規カテゴリー</span>"
  	memory_html << "		</div>"
 	memory_html << "		<input type='text' class='form-control' id='category'>"
	memory_html << "	</div>"
	memory_html << "</div><br>"
	memory_html << "<div class='row'>"
	memory_html << "<div class='col-2'><button type='button' class='btn btn-success btn-sm' onclick=\"saveCategory_BWLF()\">登録</button></div>"
	memory_html << "</div>"

when 'save_category'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false )
	mariadb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{uname}', pointer='', memory='', category='#{category}', rank='1', date='#{$DATETIME}';", false ) unless r.first

	new_html, memory_html = init()

when 'new_pointer'
	title = pointer
	if pointer != ''
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false )
		pointer = r.first['pointer']
		memory = r.first['memory']
		rank = r.first['rank']
	end

	new_html << "<div class='row'>"
	new_html << "<div class='input-group input-group-sm'>"
	new_html << "<div class='input-group-prepend'>"
	new_html << "<span class='input-group-text' id='inputGroup-sizing-sm'>キー</span>"
	new_html << "</div>"
	new_html << "	<input type='text' class='form-control' id='pointer' value='#{pointer}'>"
	new_html << "</div>"
	new_html << "</div><br>"
	memory_html << "<div class='row'>"
	memory_html << "	<textarea class='form-control' aria-label='memory' id='memory'>#{memory}</textarea>"
	memory_html << "</div><br>"
	memory_html << "<div class='row'>"
	memory_html << "	<div class='col-2'>"
	memory_html << "		<div class='input-group input-group-sm'>"
 	memory_html << "			<div class='input-group-prepend'>"
	memory_html << "				<label class='input-group-text' for='rank'>ランク</label>"
	memory_html << "			</div>"
	memory_html << "			<select class='custom-select custom-select-sm' id='rank'>"
	1.upto( 5 ) do |c|
		if c == rank
			memory_html << "    			<option value='#{c}' SELECTED>#{c}</option>"
		else
			memory_html << "    			<option value='#{c}'>#{c}</option>"
		end
	end
	memory_html << "			</select>"
	memory_html << "		</div>"
	memory_html << "	</div>"
	memory_html << "	<div class='col-2'><button type='button' class='btn btn-success btn-sm' onclick=\"savePMemory_BWLF( '#{category}', '#{pointer}', '#{post_process}' )\">保存</button></div>"
	memory_html << "</div>"

when 'save'
	a = memory_solid.split( "\n" )
	a.each do |e|
		a = e.split( "\t" )
		pointer = a[0]
		pointer = '' if pointer == nil
		memory = a[1]
		category = a[2]
		rank = a[3].to_i
		rank = 1 if rank == 0
		if mode == 'insert'
			mariadb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{uname}', pointer='#{pointer}', memory='#{memory}', category='#{category}', rank='#{rank}', date='#{$DATETIME}';", false ) if pointer != ''
		else
			r = mariadb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false )
			if r.first
				mariadb( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{memory}', category='#{category}', rank='#{rank}', date='#{$DATETIME}' WHERE category='#{category}' AND pointer='#{pointer}';", false ) if pointer != ''
			else
				mariadb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{uname}', pointer='#{pointer}', memory='#{memory}', category='#{category}', rank='#{rank}', date='#{$DATETIME}';", false ) if pointer != ''
			end
		end
	end

	new_html, memory_html = init()

when 'delete'
	mariadb( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false )
	new_html, memory_html = init()

when 'delete_pointer'
	mariadb( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false )
	new_html, memory_html = edit( category )

when 'save_pointer'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false )
	if r.first
		mariadb( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{memory_solid}', category='#{category}', rank='#{rank}', date='#{$DATETIME}' WHERE category='#{category}' AND pointer='#{pointer}';", false )
	else
		mariadb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{uname}', pointer='#{pointer}', memory='#{memory_solid}', category='#{category}', rank='#{rank}', date='#{$DATETIME}';", false )
	end

	new_html, memory_html = edit( category )
else

end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>記憶管理: #{category}</h5></div>
	</div>
	<hr>
	#{new_html}
	#{memory_html}
</div>
HTML

puts html
