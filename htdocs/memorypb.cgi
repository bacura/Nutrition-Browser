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
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'memorypb', language )
if @debug
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
open_res = cgi['open_res'].to_i
if @debug
	puts "command:#{command}<br>"
	puts "category:#{category}<br>"
	puts "operation:#{operation}<br>"
	puts "open_res:#{open_res}<br>"
	puts "<hr>"
end


memory_html = ''
onclick = ''
checked = ''
case command
when 'init'
	checked = 'CHECKED' if open_res == 1
	r = mariadb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY} ORDER BY category ASC;", false )
	memory_html << "<div class='row'>"
	memory_html << "<div class='col-1'>"
	memory_html << "	<button type='button' class='btn btn-primary btn-sm nav_button' onclick=\"nextMemoryPB()\">#{lp[4]}</button>\n"
	memory_html << "</div>"
	memory_html << "<div class='col-5'>"
	memory_html << "	<div class='input-group input-group-sm'>"
	memory_html << "		<div class='input-group-prepend'>"
	memory_html << "			<label class='input-group-text'>#{lp[1]}</label>"
	memory_html << "		</div>"
	memory_html << "		<select class='form-control form-control-sm' id='category'>"
	memory_html << "			<option value='all'>#{lp[2]}</option>"
	r.each do |e| memory_html << "<option value='#{e['category']}'>#{e['category']}</option>" end
	memory_html << "		</select>"
	memory_html << "	</div>"
	memory_html << "</div>"
	memory_html << "<div class='col-2'>"
	memory_html << "	<div class='form-group form-check'>"
	memory_html << "	<input type='checkbox' class='form-check-input' id='open_res' #{checked}>"
	memory_html << "	<label class='form-check-label'>#{lp[3]}</label>"
	memory_html << "	</div>"
	memory_html << "</div>"
	memory_html << "</div>"

when 'category'
	require 'securerandom'
	edit_button = ''

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
	if open_res == 1
		memory_html << "<h6 id='close_memory' style='visibility:visible;'>"
	else
		memory_html << "<h6 id='close_memory' style='visibility:hidden;'>"
	end
	memory_html << "#{memory[n]}</h6>"
	memory_html << "#{edit_button}" if status >= 8
	memory_html << "</div>"
end


html = <<-"HTML"
<div class='container-fluid'>
#{memory_html}
</div>
HTML

puts html