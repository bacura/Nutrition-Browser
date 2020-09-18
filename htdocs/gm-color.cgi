#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM color editor 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20180113, 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-color'


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
code = cgi['code']
code = '' if code == nil
code.gsub!( /\s/, ',' )
code.gsub!( '　', ',' )
if @debug
	puts "user.name:#{user.name}<br>\n"
	puts "uid:#{uid}<br>\n"
	puts "status:#{status}<hr>\n"
	puts "command:#{command}<br>\n"
	puts "code:#{code}<hr>\n"
end

color1 = 0
color2 = 0
color1h = 0
color2h = 0


case command
when 'update'
	color1 = cgi['color1'].to_i
	color2 = cgi['color2'].to_i
	color1h = cgi['color1h'].to_i
	color2h = cgi['color2h'].to_i

	# 加熱補完
	color1h = color1 if color1 != 0 && color1h == 0
	color2h = color1 if color2 != 0 && color2h == 0
	fn = code.split( ',' )
	if @debug
		puts "color1: #{color1}<br>\n"
		puts "color2: #{color2}<br>\n"
		puts "color1h: #{color1h}<br>\n"
		puts "color2h: #{color2h}<br>\n"
		puts "fn: #{fn}<hr>\n"
	end

	fn.each do |e|
		if /\d\d\d\d\d/ =~ e
			r = mdb( "UPDATE #{$MYSQL_TB_EXT} SET color1='#{color1}', color2='#{color2}', color1h='#{color1h}', color2h='#{color2h}' WHERE FN='#{e}';", false, @debug )
		end
	end
end


#### 未設定選択モード
if command == 'undefine'
	r = mdb( "SELECT FN from #{$MYSQL_TB_EXT} WHERE color1='0';", false, @debug )
	code = r.first['FN'] if r.first
end


#### コードが未設定モード
unless code == ''
	r = mdb( "SELECT name from #{$MYSQL_TB_TAG} WHERE FN='#{code}';", false, @debug )
	food_name = r.first['name']

	r = mdb( "SELECT * from #{$MYSQL_TB_EXT} WHERE FN='#{code}';", false, @debug )
	if r.first
		color1 = r.first['color1'].to_i
		color2 = r.first['color2'].to_i
		color1h = r.first['color1h'].to_i
		color2h = r.first['color2h'].to_i
	end
end


#### 色のフォーム
color_html = ''
$COLOR.each do |e| color_html << "<div class='col-1'>#{e}</div>\n" end

color1_html = ''
$COLOR.size.times do |c|
	checked = ''
	checked = 'CHECKED' if color1 == c
	color1_html << "<div class='col-1'><input type='radio' value='#{c}' name='color1' id='color1_#{c}' #{checked}></div>\n"
end

color2_html = ''
$COLOR.size.times do |c|
	checked = ''
	checked = 'CHECKED' if color2 == c
	color2_html << "<div class='col-1'><input type='radio' value='#{c}' name='color2' id='color2_#{c}' #{checked}></div>\n"
end

color1h_html = ''
$COLOR.size.times do |c|
	checked = ''
	checked = 'CHECKED' if color1h == c
	color1h_html << "<div class='col-1'><input type='radio' value='#{c}' name='color1h' id='color1h_#{c}' #{checked}></div>\n"
end

color2h_html = ''
$COLOR.size.times do |c|
	checked = ''
	checked = 'CHECKED' if color2h == c
	color2h_html << "<div class='col-1'><input type='radio' value='#{c}' name='color2h' id='color2h_#{c}' #{checked}></div>\n"
end


#### HTML
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: #{food_name}</h5></div>
	</div><br>

	<div class='row'>
		<div class='col-9'>
			<div class='input-group input-group-sm'>
				<label class="input-group-text">#{lp[2]}</label>
  				<input type="text" class="form-control" id="food_no" value="#{code}">
        		<button class='btn btn-outline-primary' type='button' onclick=\"initColor_BWLF()\">#{lp[3]}</button>
			</div>
		</div>
		<div class='col-3'>
        	<button class='btn btn-outline-primary btn-sm' type='button' onclick=\"initColor_BWLF( 'undefine' )\">#{lp[4]}</button>
		</div>
	</div><br>

	<div class='row'>
		#{color_html}
	</div>
	<div class='row'>
		<div class='col-1'>×</div>
		<div class='col-1' style='color:red;'>#{lp[5]}</div>
		<div class='col-1' style='color:pink;'>#{lp[5]}</div>
		<div class='col-1' style='color:orange;'>#{lp[5]}</div>
		<div class='col-1' style='color:yellow;'>#{lp[5]}</div>
		<div class='col-1' style='color:green;'>#{lp[5]}</div>
		<div class='col-1' style='color:blue;'>#{lp[5]}</div>
		<div class='col-1' style='color:purple;'>#{lp[5]}</div>
		<div class='col-1' style='color:brown;'>#{lp[5]}</div>
		<div class='col-1' style='color:black;'>#{lp[6]}</div>
		<div class='col-1' style='color:black;'>#{lp[5]}</div>
		<div class='col-1' style='color:lightgray;'>#{lp[6]}</div>
	</div><hr>


	<h6>#{lp[7]}</h6>
	<div class='row'>
		#{color1_html}
	</div>
	<br>
	<h6>#{lp[8]}</h6>
	<div class='row'>
		#{color2_html}
	</div>

	<hr>

	<h6>#{lp[9]}</h6>
	<div class='row'>
		#{color1h_html}
	</div>
	<br>
	<h6>#{lp[10]}</h6>
	<div class='row'>
		#{color2h_html}
	</div><hr>

	<div class='row'>
		<div class='col-10' align='center'><button class='btn btn-outline-danger' type='button' onclick=\"updateColor_BWL1()\">#{lp[11]}</button></div>
		<div class='col-2' align='center'>
			<a href='gm-export.cgi?extag=color' download='color.txt'><button type='button' class='btn btn-outline-primary'>#{lp[12]}</button></a>
		</div>
	</div>
</div>
HTML

puts html
