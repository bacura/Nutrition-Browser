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
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'gm-memory'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### init
def init()
	category_list = []
	pointer_num = []
	r = mdb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};", false, @debug )
	r.each do |e|
		rr = mdb( "SELECT DISTINCT pointer FROM #{$MYSQL_TB_MEMORY} WHERE category='#{e['category']}';", false, @debug )
		category_list << e['category']
		pointer_num << rr.size
	end

	list_html = ''
	category_list.size.times do |c|
		list_html << "<tr>"
		list_html << "<td onclick=\"listPointer( '#{category_list[c]}' )\">#{category_list[c]}</td>"
		list_html << "<td>#{pointer_num[c]}</td>"
		list_html << "<td><input type='checkbox' id='delete_check#{c}'>&nbsp;"
		list_html << "<button type='button' class='btn btn-danger btn-sm nav_button' onclick=\"deleteCategory( '#{category_list[c]}', 'delete_check#{c}' )\">削除</button></td>"
		list_html << "</tr>"
	end

	memory_html = <<-"MEMORY"
	<table class='table-striped table-bordered'>
	<thead>
	<th>カテゴリー</th>
	<th>項目数</th>
	<th></th>
	</thead>
		#{list_html}
	</table>
MEMORY

	new_html = <<-"NEW"
	<div class='row'>
	<div class='col-8'></div>
	<div class='col-2'><button type='button' class='btn btn-success btn-sm nav_button' onclick="newCategory()">新規カテゴリー</button></div>
	<div class='col-2'><button type='button' class='btn btn-success btn-sm nav_button' onclick="newMemoryBat()">一括登録</button></div>
	</div>
	</div>
NEW

	return new_html, memory_html
end

#### Listing pointers
def list( category )
	new_html = ''
	memory_html = ''

	new_html << "<div class='row'>"
	new_html << "<div class='col-10'></div>"
	new_html << "<div class='col-2'><button type='button' class='btn btn-success btn-sm nav_button' onclick=\"newPMemory_BWLF( '#{category}', '', 'front' )\">新規登録</button></div>"
	new_html << "</div>"
	new_html << "</div>"

	r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false, @debug )
	memory_html << "<table class='table-striped table-bordered'>"
	memory_html << "<thead>"
	memory_html << "<th>キー</th>"
	memory_html << "<th>記憶</th>"
	memory_html << "<th>ランク</th>"
	memory_html << "</thead>"

	c = 0
	r.each do |e|
		memory_html << "<tr onclick=\"newPMemory_BWLF( '#{category}', '#{e['pointer']}', 'front' )\">"
		memory_html << "<td>#{e['pointer']}</td>"
		if e['memory'].size > 80
			memory_html << "<td>#{e['memory'][0, 80]}...</td>"
		else
			memory_html << "<td>#{e['memory']}</td>"
		end
		memory_html << "<td>#{e['rank']}</td>"
		memory_html << "</tr>"
		c += 1
	end
	memory_html << "</table>"

	return new_html, memory_html
end


#### Pointer editor
def new_pointer( category, pointer, memory, rank, category_set, post_process )
	rank_select_html = ''
	rank_select_html << "<select class='form-select form-select-sm' id='rank'>"
	1.upto( 5 ) do |c|
		if c == rank
			rank_select_html << "<option value='#{c}' SELECTED>#{c}</option>"
		else
			rank_select_html << "<option value='#{c}'>#{c}</option>"
		end
	end
	rank_select_html << "</select>"

	category_select_html = ''
	category_select_html << "<select class='form-select form-select-sm' id='mvcategory'>"
	category_set.each do |e|
		if e == category
			category_select_html << "<option value='#{e}' SELECTED>#{e}</option>"
		else
			category_select_html << "<option value='#{e}'>#{e}</option>"
		end
	end
	category_select_html << "</select>"

	new_html = <<-"NEW"
	<div class='row'>
		<div class='col-6'>
			<div class='input-group input-group-sm'>
				<span class='input-group-text' id='inputGroup-sizing-sm'>キー</span>
				<input type='text' class='form-control' id='pointer' value='#{pointer}'>
			</div>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text' for='rank'>ランク</label>
				#{rank_select_html}
			</div>
		</div>
		<div class='col-4'>
			<div class='input-group input-group-sm'>
				<label class='input-group-text' for='mvcategory'>カテゴリー</label>
				#{category_select_html}
				<button type='button' class='btn btn-success btn-sm' onclick="movePMemory( '#{category}', '#{pointer}', '#{post_process}' )">移動</button>
			</div>
		</div>
	</div><br>
NEW

	memory_html = <<-"MEMORY"
	<div class='row'>
		<textarea class='form-control' rows='5' aria-label='memory' id='memory'>#{memory}</textarea>
	</div><br>
	<div class='row'>
		<div class='col-1'><button type='button' class='btn btn-success btn-sm' onclick="savePMemory_BWLF( '#{category}', '#{pointer}', '#{post_process}' )">保存</button></div>
		<div class='col-9'></div>
		<div class='col-2'><input type='checkbox' id='deletepm_check'>&nbsp;
		<button type='button' class='btn btn-danger btn-sm' onclick="deletePMemory( '#{category}', '#{pointer}', '#{post_process}' )">削除</button></div>
	</div>
MEMORY

	return new_html, memory_html
end


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
#lp = user.language( script )


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### Getting POST data
command = cgi['command']
mode = cgi['mode']
category = cgi['category']
mvcategory = cgi['mvcategory']
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
	puts "mvcategory:#{mvcategory}<br>\n"
	puts "pointer:#{pointer}<br>\n"
	puts "rank:#{rank}<br>\n"
	puts "post_process:#{post_process}<br>\n"
#	puts "memory:#{memory}<br>\n"
#	puts "memory_solid:#{memory_solid}<br>\n"
	puts "<hr>\n"
end


memory_html = ''
new_html = ''
case command
when 'init'
	new_html, memory_html = init()

when 'list_pointer'
	new_html, memory_html = list( category )

when 'new_category'
	memory_html = <<-"MEMORY"
	<div class='row'>
		<div class='input-group input-group-sm'>
  			<div class='input-group-prepend'>
    			<span class='input-group-text' id='inputGroup-sizing-sm'>新規カテゴリー</span>
  			</div>
 			<input type='text' class='form-control' id='category'>
		</div>
	</div><br>
	<div class='row'>
		<div class='col-2'><button type='button' class='btn btn-success btn-sm' onclick="saveCategory()">登録</button></div>
	</div>
MEMORY

when 'save_category'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false, @debug )
	mdb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='', memory='', category='#{category}', rank='1', date='#{$DATETIME}';", false, @debug ) unless r.first

	new_html, memory_html = init()

when 'delete_category'
	mdb( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}';", false, @debug )
	new_html, memory_html = init()

when 'new_bat'
	memory_html = <<-"MEMORY"
	<div class='row'>
		<textarea class='form-control' aria-label='memory' id='memory'></textarea>
	※タブもしくはカンマ区切りで、キー、記憶、カテゴリ、ランク。複数行可。
	</div>
	</div><br>
	<div class='row'>
	<div class='col-2'><button type='button' class='btn btn-success btn-sm' onclick="saveMemoryBat( 'insert' )">記憶追加</button></div>
	<div class='col-2'><button type='button' class='btn btn-warning btn-sm' onclick="saveMemoryBat( 'update' )">記憶置換</button></div>
	</div>
MEMORY

when 'save_bat'
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
			mdb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='#{pointer}', memory='#{memory}', category='#{category}', rank='#{rank}', date='#{$DATETIME}';", false, @debug ) if pointer != ''
		else
			r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )
			if r.first
				mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{memory}', category='#{category}', rank='#{rank}', date='#{$DATETIME}' WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug ) if pointer != ''
			else
				mdb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='#{pointer}', memory='#{memory}', category='#{category}', rank='#{rank}', date='#{$DATETIME}';", false, @debug ) if pointer != ''
			end
		end
	end

	new_html, memory_html = init()

when 'new_pointer'
	if pointer != ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )
		pointer = r.first['pointer']
		memory = r.first['memory']
		rank = r.first['rank']
	end

	category_set = []
	r = mdb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY};", false, @debug )
	r.each do |e| category_set << e['category'] end

	new_html, memory_html = new_pointer( category, pointer, memory, rank, category_set, post_process )

when 'delete_pointer'
	mdb( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )
	if post_process == 'front'
		new_html, memory_html = list( category )
	else
		exit()
	end

when 'save_pointer'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false , @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{memory_solid}', category='#{category}', rank='#{rank}', date='#{$DATETIME}' WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='#{pointer}', memory='#{memory_solid}', category='#{category}', rank='#{rank}', date='#{$DATETIME}';", false, @debug )
	end

	new_html, memory_html = list( category )

when 'move_pointer'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MEMORY} WHERE category='#{mvcategory}' AND pointer='#{pointer}';", false , @debug )
	if r.first
		t = r.first['memory']
		t << memory
		mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{t}', rank='#{rank}', date='#{$DATETIME}' WHERE category='#{mvcategory}' AND pointer='#{pointer}';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_MEMORY} SET user='#{user.name}', pointer='#{pointer}', memory='#{memory_solid}', category='#{mvcategory}', rank='#{rank}', date='#{$DATETIME}';", false, @debug )
	end
	mdb( "DELETE FROM #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )
	if post_process == 'front'
		new_html, memory_html = list( category )
	else
		exit()
	end
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
