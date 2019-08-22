#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser memory play backer 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190822, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
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
lp = lp_init( 'memory', language )
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
end


#### Getting POST data
command = cgi['command']
category = cgi['category']
operation = cgi['operation']
if $DEBUG
	puts "command:#{command}<br>"
	puts "category:#{category}<br>"
	puts "operation:#{operation}<br>"
	puts "<hr>"
end


memory_html = ''
onclick = ''
case command
when 'init'
	r = mariadb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY} ORDER BY category ASC;", false )
	memory_html << "<div class='row'>"
	memory_html << "<div class='col-5'>"
	memory_html << "	<div class='input-group input-group-sm'>"
	memory_html << "		<div class='input-group-prepend'>"
	memory_html << "			<label class='input-group-text'>カテゴリー</label>"
	memory_html << "		</div>"
	memory_html << "		<select class='form-control form-control-sm' id='category'>"
	memory_html << "			<option value='all'>全部</option>"
	r.each do |e| memory_html << "<option value='#{e['category']}'>#{e['category']}</option>" end
	memory_html << "		</select>"
	memory_html << "	</div>"
	memory_html << "</div>"
	memory_html << "<div class='col-7'>"
	memory_html << "	<button type='button' class='btn btn-primary btn-sm nav_button' onclick=\"nextMemoryPB()\">↓</button>\n"
	memory_html << "</div>"
	memory_html << "</div>"

when 'category'
	require 'securerandom'

	q = "SELECT * from #{$MYSQL_TB_MEMORY} WHERE category='#{category}' ORDER BY RAND() LIMIT 10;"
	q = "SELECT * from #{$MYSQL_TB_MEMORY} ORDER BY RAND() LIMIT 10;" if category == 'all'
	r = mariadb( q, false )

	pointer = []
	memory = []
	rank = []
	r.each do |e|
		pointer << e['pointer']
		memory << e['memory']
		rank << e['rank']
	end
	n = SecureRandom.random_number( r.size )

	memory_html << "<div class='row' onclick=\"document.getElementById( 'close_memory' ).style.visibility = 'visible';\">"
	memory_html << "<h4>#{pointer[n]}</h4>"
	memory_html << "</div>"
	memory_html << "<hr>"
	memory_html << "<div class='row'>"
	memory_html << "<h6 id='close_memory' style='visibility:hidden;'>#{memory[n]}</h6>"
	memory_html << "</div>"
end

html = <<-"HTML"
<div class='container-fluid'>

#{memory_html}

</div>
HTML

puts html
