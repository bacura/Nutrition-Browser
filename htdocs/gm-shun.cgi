#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM Shun editor 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190210, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'gm-shun.cgi'
$DEBUG = false


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'gm-shun', language )
if $DEBUG
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


#### POSTデータの取得
command = cgi['command']
shun1s = cgi['shun1s'].to_i
shun1e = cgi['shun1e'].to_i
shun2s = cgi['shun2s'].to_i
shun2e = cgi['shun2e'].to_i
code = +cgi['code']
code.gsub!( /\s/, ',' )
code.gsub!( '　', ',' )
if $DEBUG
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"
	puts "shun1s:#{shun1s}<br>\n"
	puts "shun1e:#{shun1e}<br>\n"
	puts "shun2s:#{shun2s}<br>\n"
	puts "shun2e:#{shun2e}<br>\n"
	puts "<hr>\n"
end

case command
when 'on'
	fn = code.split( ',' )
	fn.each do |e|
		if /\d\d\d\d\d/ =~ e
			mariadb( "UPDATE #{$MYSQL_TB_EXT} SET shun1s='#{shun1s}', shun1e='#{shun1e}', shun2s='#{shun2s}', shun2e='#{shun2e}' WHERE FN='#{code}';", false )
		end
	end
when 'off'
	fn = code.split( ',' )
	fn.each do |e|
		if /\d\d\d\d\d/ =~ e
			mariadb( "UPDATE #{$MYSQL_TB_EXT} SET shun1s='0', shun1e='0', shun2s='0', shun2e='0' WHERE FN='#{code}';", false )
		end
	end
end

food_name = ''
unless code == ''
	r = mariadb( "SELECT name from #{$MYSQL_TB_TAG} WHERE FN='#{code}';", false )
	food_name = r.first['name']
end

list_html = ''
r = mariadb( "SELECT FN FROM #{$MYSQL_TB_EXT} WHERE shun1s>='1' and shun1s<='12';", false )
if r.size != 0
	code_list = []
	name_tag_list = []
	r.each do |e|
		rr = mariadb( "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e['FN']}';", false )
		code_list << rr.first['FN']
		name_tag_list << "#{rr.first['name']}・#{rr.first['tag1']} #{rr.first['tag2']} #{rr.first['tag3']} #{rr.first['tag4']} #{rr.first['tag5']}"
	end
	code_list.reverse!
	name_tag_list.reverse!

	c = 0
	code_list.each do |e|
		rr = mariadb( "SELECT * from #{$MYSQL_TB_EXT} WHERE FN='#{e}';", false )
		list_html << "<div class='row'>"
		list_html << "<div class='col-1'><button class='btn btn-sm btn-outline-danger' type='button' onclick=\"offShun_BWL1( '#{e}' )\">x</button></div>"
		list_html << "<div class='col-2'>#{e}</div>"
		list_html << "<div class='col-4'>#{name_tag_list[c]}</div>"
		list_html << "<div class='col-1'>#{rr.first['shun1s']}</div>"
		list_html << "<div class='col-1'>#{rr.first['shun1e']}</div>"
		list_html << "<div class='col-1'>#{rr.first['shun2s']}</div>"
		list_html << "<div class='col-1'>#{rr.first['shun2e']}</div>"
		list_html << '</div>'
		c += 1
	end
else
	list_html << 'no item listed.'
end

html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: #{food_name}</h5></div>
	</div>
	<div class='row'>
		<div class='col-10'>
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="weight">#{lp[2]}</label>
				</div>
				<input type="text" maxlength="5" class="form-control" id="code" value="#{code}">
			</div>
		</div>
		<div class='col-1'></div>
		<div class='col-1'>
			<button class="btn btn-sm btn-outline-primary" type="button" onclick="onShun_BWL1()">#{lp[3]}</button>
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-5'>
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="shun1s">#{lp[4]}</label>
				</div>
				<select class="custom-select custom-select-sm" id="shun1s">
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
					<option value="4">4</option>
					<option value="5">5</option>
					<option value="6">6</option>
					<option value="7">7</option>
					<option value="8">8</option>
					<option value="9">9</option>
					<option value="10">10</option>
					<option value="11">11</option>
					<option value="12">12</option>
				</select>
				　～　
				<div class="input-group-prepend">
					<label class="input-group-text" for="shun1e">#{lp[5]}</label>
				</div>
				<select class="custom-select custom-select-sm" id="shun1e">
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
					<option value="4">4</option>
					<option value="5">5</option>
					<option value="6">6</option>
					<option value="7">7</option>
					<option value="8">8</option>
					<option value="9">9</option>
					<option value="10">10</option>
					<option value="11">11</option>
					<option value="12">12</option>
				</select>
			</div>
		</div>
		<div class='col-1'></div>
		<div class='col-5'>
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="shun1s">#{lp[6]}</label>
				</div>
				<select class="custom-select custom-select-sm" id="shun2s">
					<option value="0">-</option>
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
					<option value="4">4</option>
					<option value="5">5</option>
					<option value="6">6</option>
					<option value="7">7</option>
					<option value="8">8</option>
					<option value="9">9</option>
					<option value="10">10</option>
					<option value="11">11</option>
					<option value="12">12</option>
				</select>
				　～　
				<div class="input-group-prepend">
					<label class="input-group-text" for="shun1e">#{lp[7]}</label>
				</div>
				<select class="custom-select custom-select-sm" id="shun2e">
					<option value="0">-</option>
					<option value="1">1</option>
					<option value="2">2</option>
					<option value="3">3</option>
					<option value="4">4</option>
					<option value="5">5</option>
					<option value="6">6</option>
					<option value="7">7</option>
					<option value="8">8</option>
					<option value="9">9</option>
					<option value="10">10</option>
					<option value="11">11</option>
					<option value="12">12</option>
				</select>
			</div>
		</div>
	</div>
	<br>
	<hr>
	#{list_html}
	<div class='row'>
		<div class='col-10'></div>
		<div class='col-2' align='center'>
			<a href='gm-export.cgi?extag=shun' download='shun.txt'><button type='button' class='btn btn-outline-primary'>#{lp[8]}</button></a>
		</div>
	</div>
HTML

puts html
