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

#### Memory extender
def extend_linker( memory, depth )
	depth += 1 if depth < 5
	link_pointer = memory.scan( /\{\{[^\}\}]+\}\}/ )
	link_pointer.uniq!

	memory_ = memory
	link_pointer.each do |e|
		pointer = e.sub( '{{', "" ).sub( '}}', "" )
		pointer.gsub!( '<', "&lt;" )
		pointer.gsub!( '>', "&gt;" )

		pointer_ = e.sub( '{{', "<span class='memory_link' onclick=\"memoryOpenLink( '#{pointer}', '#{depth}' )\">" )
		pointer_.sub!( '}}', "</span>" )
		memory_.gsub!( e, pointer_ )
	end
	memory_.gsub!( "\n", "<br>\n" )

	return memory_
end


#### Alike pointer
def alike_pointer( key )
	pointer = ''

	begin
		pointer_h = Hash.new
		normal = key.tr( 'ぁ-ん０-９A-ZA-Z', 'ァ-ン0-9a-za-z' )
		normal.gsub!( '一', '1' )
		normal.gsub!( '二', '2' )
		normal.gsub!( '三', '3' )
		normal.gsub!( '四', '4' )
		normal.gsub!( '五', '5' )
		normal.gsub!( '六', '6' )
		normal.gsub!( '七', '7' )
		normal.gsub!( '八', '8' )
		normal.gsub!( '九', '9' )
		normal.gsub!( '（', '(' )
		normal.gsub!( '）', ')' )
		normal.gsub!( '％', '%' )
		normal.gsub!( '．', '.' )
		normal.gsub!( '＝', '=' )
		normal.gsub!( '＋', '+' )
		normal.gsub!( '－', '-' )
		r = mdb( "SELECT pointer from #{$MYSQL_TB_MEMORY};", false, @debug )
		r.each do |e|
			normal_pointer = e['pointer'].tr( 'ぁ-ん０-９A-ZA-Z', 'ァ-ン0-9a-za-z' )
			normal_pointer.gsub!( '一', '1' )
			normal_pointer.gsub!( '二', '2' )
			normal_pointer.gsub!( '三', '3' )
			normal_pointer.gsub!( '四', '4' )
			normal_pointer.gsub!( '五', '5' )
			normal_pointer.gsub!( '六', '6' )
			normal_pointer.gsub!( '七', '7' )
			normal_pointer.gsub!( '八', '8' )
			normal_pointer.gsub!( '九', '9' )
			normal_pointer.gsub!( '（', '(' )
			normal_pointer.gsub!( '）', ')' )
			normal_pointer.gsub!( '％', '%' )
			normal_pointer.gsub!( '．', '.' )
			normal_pointer.gsub!( '＝', '=' )
			normal_pointer.gsub!( '＋', '+' )
			normal_pointer.gsub!( '－', '-' )
			small = ''
			large = ''
			large_size = 1
			score = 0.0
			if normal.size <= normal_pointer.size
				small = normal
				large = normal_pointer
				large_size = normal_pointer.size
			else
				small = normal_pointer
				large = normal
				large_size = normal.size
			end
			a = small.split( '' )
			follower = ''
			a.each do |ee|
				if ee != '+'
					if /#{follower}#{ee}/ =~ large
						score += 3 if /#{follower}#{ee}/ =~ large
						follower = ee
					elsif /#{ee}/ =~ large
						score += 1 if /#{ee}/ =~ large
						follower = ee
					else
						follower = ''
					end
				end
			end
			pointer_h[e['pointer']] = score / large_size
		end

		ap = pointer_h.max do |k, v| k[1] <=> v[1] end
		pointer = ap[0] if ap[1] >= 1.5
	rescue
	end

	return pointer
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
			count = r.first['count'].to_i + 1
			mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET count='#{count}' WHERE pointer='#{e}';", false, @debug )
		else
			a_pointer = alike_pointer( e )
			unless a_pointer == ''
				rr = mdb( "SELECT * from #{$MYSQL_TB_MEMORY} WHERE pointer='#{a_pointer}';", false, @debug )
				pointer = ''
				memory_html << "<span class='memory_pointer'>#{a_pointer}&nbsp;??</span>&nbsp;&nbsp;<span class='badge badge-pill badge-dark' onclick=\"memoryOpenLink( '#{e}', '1' )\">再検索</span><br><br>"
				rr.each do |ee|
					edit_button = ''
					edit_button = "&nbsp;<button type='button' class='btn btn-outline-danger btn-sm nav_button' onclick=\"newPMemory_BWLF( '#{ee['category']}', '#{ee['pointer']}', 'back' )\">#{lp[3]}</button>" if user.status >= 8
					memory_html << extend_linker( ee['memory'], depth )
					memory_html << "<div align='right'>#{ee['category']} / #{ee['date'].year}/#{ee['date'].month}/#{ee['date'].day}#{edit_button}</div>"
				end
				count = rr.first['count'].to_i + 1
				mdb( "UPDATE #{$MYSQL_TB_MEMORY} SET count='#{count}' WHERE pointer='#{a_pointer}';", false, @debug )
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
