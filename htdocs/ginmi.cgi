#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser nutrition assessment tools 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190807, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require 'date'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'ginmi.cgi'
$DEBUG = true

#==============================================================================
#DEFINITION
#==============================================================================

#### BMI
def bmi( cgi, uname, lp )
	html = ''
	case cgi['step']
	when 'form'
		html << "<div class='row'>"
		html << "<h5>BMI計算フォーム</h5>"
		html << "</div>"

		html << "<div class='row'>"

		html << "<div class='col-2'>"
		html << "<div class='input-group input-group-sm'>"
		html << "<div class='input-group-prepend'><span class='input-group-text' maxlength='3' value='18'>年齢</span></div>"
		html << "<input type='number' min='18' class='form-control' id='age'>"
		html << "</div></div>"

		html << "<div class='col-2'>"
		html << "<div class='input-group input-group-sm'>"
		html << "<div class='input-group-prepend'><span class='input-group-text' maxlength='3' value='1.0'>身長(m)</span></div>"
		html << "<input type='text' class='form-control' id='height'>"
		html << "</div></div>"

		html << "<div class='col-2'>"
		html << "<div class='input-group input-group-sm'>"
		html << "<div class='input-group-prepend'><span class='input-group-text' maxlength='3' value='1.0'>体重(kg)</span></div>"
		html << "<input type='text' class='form-control' id='weight'>"
		html << "</div></div></div>"
		html << "<br>"
		html << "<div class='row'>"
		html << "<div class='col-2'>"
		html << "<button class='btn btn-sm btn-primary' onclick=\"ginmiBMIres()\">計算</button>"
		html << "</div>"
		html << "</div>"
	when 'result'
		age = cgi['age'].to_i
		weight = BigDecimal( cgi['weight'] )
		height = BigDecimal( cgi['height'] )
		if $DEBUG
			puts "age:#{age}<br>\n"
			puts "height:#{height}<br>\n"
			puts "weight:#{weight}<br>\n"
			puts "<hr>\n"
		end
		result = ( weight / ( height * height )).round( 1 )
		html << "<div class='row'>"
		html << "<div class='col-2'>計算式</div>"
		html << "<div class='col-2'>#{weight.to_f} / ( #{height.to_f} * #{height.to_f} )</div>"
		html << "</div>"

		html << "<div class='row'>"
		html << "<div class='col-2'>BMI値</div>"
		html << "<div class='col-2'>#{result.to_f}</div>"
		html << "</div>"
	when 'save'

	end

	return html
end









#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomi', language )
if $DEBUG
	puts "uname:#{uname}<br>\n"
	puts "status:#{status}<br>\n"
	puts "aliaseu:#{aliaseu}<br>\n"
	puts "language:#{language}<br>\n"
	puts "<hr>\n"
end


#### POSTデータの取得
command = cgi['command']
step = cgi['step']
if $DEBUG
	puts "command:#{command}<br>\n"
	puts "step:#{step}<br>\n"
	puts "<hr>\n"
end


#### General menu
if command == 'menu'
html = <<-"MENU"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="ginmiBMI()">BMI</button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="">MNA</button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="">SGA</button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick=""></button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick=""></button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick=""></button></div>
	</div>
</div>

MENU
	puts html
	exit()
end


#### Getting Date
date = Date.today


####
html = "<div class='container-fluid'>"
case command
when 'bmi'
	html = bmi( cgi, uname, lp )

when 'mna'

when 'sga'

end

html << '</div>'

puts html
