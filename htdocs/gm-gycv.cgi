#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM yellow green color vegetable editor 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190210, 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'gm-gycv.cgi'
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
lp = lp_init( 'gm-gycv', language )
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
food_no = cgi['food_no']
if $DEBUG
	puts "command:#{command}<br>\n"
	puts "food_no:#{food_no}<br>\n"
	puts "<hr>\n"
end

case command
when 'on'
	mariadb( "UPDATE #{$MYSQL_TB_EXT} SET gycv='1' WHERE FN='#{food_no}';", false )
when 'off'
	mariadb( "UPDATE #{$MYSQL_TB_EXT} SET gycv ='0' WHERE FN='#{food_no}';", false )
end

list_html = ''
r = mariadb( "SELECT FN FROM #{$MYSQL_TB_EXT} WHERE gycv ='1';", false )
if r.size != 0
	food_no_list = []
	r.each do |e|
		rr = mariadb( "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e['FN']}';", false )
		food_no_list << rr.first['FN']
	end
	food_no_list.reverse.each do |e|
		rr = mariadb( "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e}';", false )
		list_html << "<div class='row'>"
		list_html << "<div class='col-1'><button class='btn btn-sm btn-outline-danger' type='button' onclick=\"offGYCV_BWL1( '#{e}' )\">x</button></div>"
		list_html << "<div class='col-2'>#{e}</div>"
		list_html << "<div class='col-4'>#{rr.first['name']}・#{rr.first['tag1']} #{rr.first['tag2']} #{rr.first['tag3']} #{rr.first['tag4']} #{rr.first['tag5']}</div>"
		list_html << '</div>'
	end
else
	list_html << 'no item listed.'
end

html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: </h5></div>
	</div>
	<div class='row'>
		<div class='col-3'>
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="weight">#{lp[2]}</label>
				</div>
				<input type="text" maxlength="5" class="form-control" id="food_no" value="#{food_no}" onchange="onGYCV_BWL1()">
				<div class="input-group-append">
					<button class="btn btn-outline-primary" type="button" onclick="onGYCV_BWL1()">#{lp[3]}</button>
				</div>
			</div>
		</div>
	</div>
	<br>
	<hr>
	#{list_html}
	<div class='row'>
		<div class='col-10'></div>
		<div class='col-2' align='center'>
			<a href='gm-export.cgi?extag=gycv' download='gycv.txt'><button type='button' class='btn btn-outline-primary'>#{lp[4]}</button></a>
		</div>
	</div>
HTML

puts html
