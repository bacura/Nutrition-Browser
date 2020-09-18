#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM yellow green color vegetable editor 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190210, 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-gycv'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### GM check
if user.status < 8
	puts "GM error."
	exit
end


#### POSTデータの取得
command = cgi['command']
food_no = cgi['food_no']
if @debug
	puts "command:#{command}<br>\n"
	puts "food_no:#{food_no}<br>\n"
	puts "<hr>\n"
end

case command
when 'on'
	mdb( "UPDATE #{$MYSQL_TB_EXT} SET gycv='1' WHERE FN='#{food_no}';", false, @debug )
when 'off'
	mdb( "UPDATE #{$MYSQL_TB_EXT} SET gycv ='0' WHERE FN='#{food_no}';", false, @debug )
end

list_html = ''
r = mdb( "SELECT FN FROM #{$MYSQL_TB_EXT} WHERE gycv ='1';", false, @debug )
if r.size != 0
	food_no_list = []
	r.each do |e|
		rr = mdb( "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e['FN']}';", false, @debug )
		food_no_list << rr.first['FN']
	end
	food_no_list.reverse.each do |e|
		rr = mdb( "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e}';", false, @debug )
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
				<label class="input-group-text" for="weight">#{lp[2]}</label>
				<input type="text" maxlength="5" class="form-control" id="food_no" value="#{food_no}" onchange="onGYCV_BWL1()">
				<button class="btn btn-outline-primary" type="button" onclick="onGYCV_BWL1()">#{lp[3]}</button>
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
