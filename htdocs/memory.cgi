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
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'memory'


#==============================================================================
#DEFINITION
#==============================================================================

def extend_linker( memory, depth )
	depth += 1 if depth < 5
	link_pointer = memory.scan( /\{\{[^\}\}]+\}\}/ )
	link_pointer.uniq!

	memory_ = memory
	link_pointer.each do |e|
		pointer = e.sub( '{{', "" ).sub( '}}', "" )
		pointer_ = e.sub( '{{', "<span class='memory_link' onclick=\"memoryOpenLink( '#{pointer}', '#{depth}' )\">" )
		pointer_.sub!( '}}', "</span>" )
		memory_.gsub!( e, pointer_ )
	end

	return memory_
end


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### Getting POST data
command = cgi['command']
category = cgi['category']
pointer = cgi['pointer']
depth = cgi['depth'].to_i
if @debug
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
	r = mdb( "SELECT DISTINCT category FROM #{$MYSQL_TB_MEMORY} ORDER BY category ASC;", false, @debug )
	if user.status.to_i >= 1
		memory_html << "<button type='button' class='btn btn-primary btn-sm nav_button' onclick=\"initMemoryPB()\">#{lp[4]}</button>"
	else
		memory_html << "<button type=\"button\" class=\"btn btn-dark text-secondary btn-sm nav_button\" onclick=\"displayVideo( '#{lp[5]}' )\">#{lp[4]}</button>"
	end
	r.each do |e|
		memory_html << "<button type='button' class='btn btn-outline-secondary btn-sm nav_button' onclick=\"memoryOpen( 'category', '#{e['category']}', '', 2 )\">#{e['category']}</button>\n"
	end

when 'category'
	r = mdb( "SELECT pointer from #{$MYSQL_TB_MEMORY} WHERE category='#{category}' ORDER BY pointer ASC;", false, @debug )
	r.each do |e|
		memory_html << "<button type='button' class='btn btn-outline-secondary btn-sm nav_button' onclick=\"memoryOpen( 'pointer', '#{category}', '#{e['pointer']}', 2 )\">#{e['pointer']}</button>\n"
	end
	onclick = "onclick=\"memoryOpen( 'init', '', '', 2 )\""

when 'pointer'
	r = mdb( "SELECT * from #{$MYSQL_TB_MEMORY} WHERE category='#{category}' AND pointer='#{pointer}';", false, @debug )
	r.each do |e|
		edit_button = ''
		edit_button = "&nbsp<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"newPMemory_BWLF( '#{e['category']}', '#{e['pointer']}', 'back' )\">#{lp[3]}</button>" if user.status >= 8
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
		r = mdb( "SELECT * from #{$MYSQL_TB_MEMORY} WHERE pointer='#{e}';", false, @debug )
		if r.first
			pointer = ''
			memory_html << "<span class='memory_pointer'>#{e}</span>&nbsp;&nbsp;<span class='badge badge-pill badge-dark' onclick=\"memoryOpenLink( '#{e}', '1' )\">再検索</span><br><br>"
			r.each do |ee|
				edit_button = ''
				edit_button = "&nbsp;<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"newPMemory_BWLF( '#{ee['category']}', '#{ee['pointer']}', 'back' )\">#{lp[3]}</button>" if user.status >= 8
				memory_html << extend_linker( ee['memory'], depth )
				memory_html << "<div align='right'>#{ee['category']} / #{ee['date'].year}/#{ee['date'].month}/#{ee['date'].day}#{edit_button}</div>"
			end
		end
	end
	memory_html << lp[2] if memory_html == ''
end

title = ''
title = "<div class='col' #{onclick}><h5>#{lp[1]}: #{category} / #{pointer}</h5></div>" if command != 'refer'

html = <<-"HTML"
<div class='container-fluid'>
	#{title}
	<blockquote>
	#{memory_html}
	</blockquote>
</div>
HTML

puts html
