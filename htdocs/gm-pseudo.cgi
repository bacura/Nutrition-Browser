#! /usr/bin/ruby
#encoding: utf-8
#fct browser fctb square 0.00

#==============================================================================
# CHANGE LOG
#==============================================================================
#20171006, 0.00a, start


#==============================================================================
# LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/fct_soul.rb'


#==============================================================================
# STATIC
#==============================================================================
$DEBUG = true


#==============================================================================
# DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new
uname, uid, status = login_check( cgi )
$DEBUG = false unless uname == $GM

html_init( nil )


#### GMチェック
if status < 9
	puts "GM error."
	exit
end

fct_opt = Hash.new

#### POSTデータの取得
command = cgi['command']
code = cgi['code']
food_name = cgi['food_name']
code = '' if code == nil
code = '' unless /P\d\d\d\d\d/ =~ code


#### デバッグ用
if $DEBUG
	puts "user:#{uname}<br>\n"
	puts "uid: #{uid}<br>\n"
	puts "status: #{status}<br>\n"
	puts "<hr>\n"
	puts "command: #{command}<br>\n"
	puts "food_name: #{food_name}<br>\n"
	puts "code: #{code}<br>\n"
	puts "<hr>\n"
end


#### 保存部分
if command == 'save'
	food_group = cgi['food_group']
	class1 = cgi['class1']
	class2 = cgi['class2']
	class3 = cgi['class3']
	tag1 = cgi['tag1']
	tag2 = cgi['tag2']
	tag3 = cgi['tag3']
	tag4 = cgi['tag4']
	tag5 = cgi['tag5']

	# 全成分読み込み
	4.upto( 66 ) do |i| fct_opt[$FCT_ITEM[i]] = cgi[$FCT_ITEM[i]] end
	4.upto( 66 ) do |i| fct_opt[$FCT_ITEM[i]] = '-' if fct_opt[$FCT_ITEM[i]] == '' end

	fct_opt['Notice'] = cgi['Notice']
end


#### デバッグ用
if $DEBUG
	puts "fct_opt: #{fct_opt}<br>\n"
	puts "<hr>\n"
end


#### html_fct_block
html_fct_block1 = '<table class="table-sm table-striped" width="100%">'
4.upto( 7 ) do |i| html_fct_block1 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]]}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block1 << '</table>'

html_fct_block2 = '<table class="table-sm table-striped" width="100%">'
8.upto( 20 ) do |i| html_fct_block2 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]]}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block2 << '</table>'

html_fct_block3 = '<table class="table-sm table-striped" width="100%">'
21.upto( 34 ) do |i| html_fct_block3 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]]}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block3 << '</table>'

html_fct_block4 = '<table class="table-sm table-striped" width="100%">'
35.upto( 46 ) do |i| html_fct_block4 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]]}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block4 << '</table>'

html_fct_block5 = '<table class="table-sm table-striped" width="100%">'
47.upto( 55 ) do |i| html_fct_block5 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]]}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block5 << '</table>'

html_fct_block6 = '<table class="table-sm table-striped" width="100%">'
56.upto( 66 ) do |i| html_fct_block6 << "<tr><td>#{$FCT_NAME[$FCT_ITEM[i]]}</td><td align='right' width='20%''><input type='text' class='form-control form-control-sm' id='#{$FCT_ITEM[i]}' value=\"#{fct_opt[$FCT_ITEM[i]]}\"></td><td>#{$FCT_UNIT[$FCT_ITEM[i]]}</td></tr>\n" end
html_fct_block6 << '</table>'


#### html部分
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-4">
			<input type="text" class="form-control form-control-sm" id="food_name" placeholder="食品名" value="#{food_name}">
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm" id="food_group">
				<span class="input-group-addon">食品群&nbsp;</span>
				<select class="form-control" id="fg">
					<option value="0">特殊</option>
					<option value="1">穀類</option>
					<option value="2">いも及びでん粉類</option>
					<option value="3">砂糖及び甘味類</option>
					<option value="4">豆類</option>
					<option value="5">種実類</option>
					<option value="6">野菜類</option>
					<option value="7">果実類</option>
					<option value="8">きのこ類</option>
					<option value="9">藻類</option>
					<option value="10">魚介類</option>
					<option value="11">肉類</option>
					<option value="12">卵類</option>
					<option value="13">乳類</option>
					<option value="14">油脂類</option>
					<option value="15">菓子類</option>
					<option value="16">し好飲料類</option>
					<option value="17">調味料及び香辛料類</option>
					<option value="18">調理加工食品類</option>
				</select>
			</div>
		</div>
		<div class="col-3"></div>
		<div class="col-1">
			<button class="btn btn-outline-primary btn-sm" type="button" onclick="savePseudo_BWL1( 'code' )">登録</button>
		</div>
	</div>

	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class1" placeholder="class1" value="#{class1}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class2" placeholder="class2" value="#{class2}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="class3" placeholder="class3" value="#{class3}"></div>
	</div>
	<br>
	<div class="row">
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag1" placeholder="tag1" value="#{tag1}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag2" placeholder="tag2" value="#{tag2}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag3" placeholder="tag3" value="#{tag3}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag4" placeholder="tag4" value="#{tag4}"></div>
		<div class="col-2"><input type="text" class="form-control form-control-sm" id="tag5" placeholder="tag5" value="#{tag5}"></div>
	</div>
	<hr>
	<div class="row">
		<div class="col-4">
			#{html_fct_block1}

			<div style='border: solid gray 1px; margin: 0.5em; padding: 0.5em;'>
				備考：<br>
				<textarea rows="6" cols="32" id="Notice">#{fct_opt['Notice']}</textarea>
			</div>
		</div>

		<div class="col-4">
			#{html_fct_block2}
		</div>

		<div class="col-4">
			#{html_fct_block3}
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="col-4">
			#{html_fct_block4}
		</div>

		<div class="col-4">
			#{html_fct_block5}
		</div>

		<div class="col-4">
			#{html_fct_block6}
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="col-8">
			検索キー：
		</div>
		<div class="col-4">
		</div>
	</div>
</div>

HTML


puts html
