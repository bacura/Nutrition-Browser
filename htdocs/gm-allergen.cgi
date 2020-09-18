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
script = 'gm-allergen'


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
allergen = cgi['allergen']
code = +cgi['code']
code.gsub!( /\s/, ',' )
code.gsub!( '　', ',' )

if @debug
	puts "command:#{command}<br>\n"
	puts "code:#{code}<br>\n"
	puts "allergen:#{allergen}<br>\n"
	puts "<hr>\n"
end

case command
when 'on'
	fn = code.split( ',' )
	fn.each do |e|
		if /\d\d\d\d\d/ =~ e
			mdb( "UPDATE #{$MYSQL_TB_EXT} SET allergen='#{allergen}' WHERE FN='#{code}';", false, @debug )
		end
	end
when 'off'
	fn = code.split( ',' )
	fn.each do |e|
		if /\d\d\d\d\d/ =~ e
			mdb( "UPDATE #{$MYSQL_TB_EXT} SET allergen='0' WHERE FN='#{code}';", false, @debug )
		end
	end
end

food_name = ''
unless code == ''
	r = mdb( "SELECT name from #{$MYSQL_TB_TAG} WHERE FN='#{code}';", false, @debug )
	food_name = r.first['name']
end

list_html = ''
r = mdb( "SELECT FN FROM #{$MYSQL_TB_EXT} WHERE allergen>='1';", false, @debug )
if r.size != 0
	code_list = []
	r.each do |e|
		rr = mdb( "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e['FN']}';", false, @debug)
		code_list << rr.first['FN']
	end
	code_list.reverse.each do |e|
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
		<div class='col'><h5>#{lp[1]}: #{food_name}</h5></div>
	</div>
	<div class='row'>
		<div class='col-7'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="weight">#{lp[2]}</label>
				<input type="text" maxlength="5" class="form-control" id="code" value="#{code}">
			</div>
		</div>
		<div class='col-4'>
			<div class="form-check form-check-inline">
  				<input class="form-check-input" type="radio" id="ag_class1" CHECKED>
				<label class="form-check-label" for="inlineRadio1">#{lp[3]}</label>
			</div>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" id="ag_class2">
				<label class="form-check-label" for="inlineRadio2">#{lp[4]}</label>
			</div>
			<div class="form-check form-check-inline">
				<input class="form-check-input" type="radio" id="ag_class3">
				<label class="form-check-label" for="inlineRadio3">#{lp[5]}</label>
			</div>
		</div>
		<div class='col-1'>
				<button class="btn btn-sm btn-outline-primary" type="button" onclick="onAllergen_BWL1()">#{lp[6]}</button>
		</div>
	</div>

	<br>
	<hr>
	#{list_html}
	<div class='row'>
		<div class='col-10'></div>
		<div class='col-2' align='center'>
			<a href='gm-export.cgi?extag=allergen' download='allergen.txt'><button type='button' class='btn btn-outline-primary'>#{lp[7]}</button></a>
		</div>
	</div>
HTML

puts html
