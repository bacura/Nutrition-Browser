#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser memory viewer 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20180325, 0.00, start


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
pointer = cgi['pointer']
depth = cgi['depth']
if $DEBUG
	puts "command:#{command}<br>"
	puts "category:#{category}<br>"
	puts "pointer:#{pointer}<br>"
	puts "depth:#{depth}<br>"
	puts "<hr>"
end


memory_html = ''
onclick = ''
case command
when 'init'
	r = mariadb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY} ORDER BY category ASC;", false )
	r.each do |e|
		memory_html << "<button type='button' class='btn btn-outline-secondary btn-sm nav_button' onclick=\"memoryOpen( 'category', '#{e['category']}', '', 2 )\">#{e['category']}</button>\n"
	end

when 'category'
	r = mariadb( "SELECT pointer from #{$MYSQL_TB_MEMORY} WHERE category='#{category}' ORDER BY pointer ASC;", false )
	r.each do |e|
		memory_html << "<button type='button' class='btn btn-outline-secondary btn-sm nav_button' onclick=\"memoryOpen( 'pointer', '#{category}', '#{e['pointer']}', 2 )\">#{e['pointer']}</button>\n"
	end
	onclick = "onclick=\"memoryOpen( 'init', '', '', 2 )\""

when 'pointer'
	r = mariadb( "SELECT * from #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false )
	r.each do |e|
		edit_button = ''
		edit_button = "&nbsp<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"newPMemory_BWLF( '#{e['category']}', '#{e['pointer']}', 'back' )\">編集</button>" if status == 9
		raw_memory = e['memory']
		memory = raw_memory
		memory_html << "<div class='row'>"
		memory_html << "#{e['memory']}"
		memory_html << "</div>"
		memory_html << "<div align='right'>#{e['date'].year}/#{e['date'].month}/#{e['date'].day}#{edit_button}</div>"
	end
	onclick = "onclick=\"memoryOpen( 'category', '#{category}', '', 2 )\""

when 'refer'
	pointer.gsub!( '　', ' ' )
	pointer.gsub!( /\s+/, ' ' )
	a = pointer.split( ' ' )
	a.each do |e|
		r = mariadb( "SELECT * from #{$MYSQL_TB_MEMORY} WHERE pointer='#{e}';", false )
		if r.first
			pointer = ''
			r.each do |ee|
				edit_button = ''
				edit_button = "<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"newPMemory_BWLF( '#{e['category']}', '#{e['pointer']}')\">#{e['category']}</button>" if status == 9
				raw_memory = e['memory']
				memory = raw_memory
				memory_html << "<h5>#{ee['pointer']}</h5>"
				memory_html << "#{ee['memory']}"
				memory_html << "<div align='right'>#{ee['category']} / #{ee['date'].year}/#{ee['date'].month}/#{ee['date'].day}#{edit_button}</div>"
			end
		end
	end
	memory_html << lp[2] if memory_html == ''
end

html = <<-"HTML"
<div class='container-fluid'>
	<div class='col' #{onclick}><h5>#{lp[1]}: #{category} / #{pointer}</h5></div>
	<blockquote>
	#{memory_html}
	</blockquote>
</div>
HTML

puts html
