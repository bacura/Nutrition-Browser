#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser nutrition assessment tools 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190910, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'date'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### 初期画面
def init( lp, status )
	html = <<-"HTML"
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'bmi' )">BMI</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'kaupi' )">カウプ指数</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'laureli' )">ローレル指数</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'energy-ref' )">E・参照</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'energy-hn' )">E・国立健栄</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'energy-hb' )">E・ハリベネ</button>
	<button class='btn btn-sm btn-outline-light nav_button' onclick="">推定身長</button>
	<button class='btn btn-sm btn-outline-light nav_button' onclick="">推定骨格筋量</button>
	<button class='btn btn-sm btn-outline-light nav_button' onclick="">MNA</button>
	<button class='btn btn-sm btn-outline-light nav_button' onclick="">MNA-SF</button>
	<button class='btn btn-sm btn-outline-light nav_button' onclick="">SGA</button>
HTML

	return html
end


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomi', language )

html_init( nil )
if @debug
	puts "uname:#{uname}<br>\n"
	puts "status:#{status}<br>\n"
	puts "aliaseu:#{aliaseu}<br>\n"
	puts "language:#{language}<br>\n"
	puts "<hr>\n"
end


#### Getting POST
mod = cgi['mod']
if @debug
	puts "mod:#{mod}<br>\n"
	puts "<hr>\n"
end


####
html = "<div class='container-fluid'>"
if mod == ''
	html = init( lp, status )
else
	require "#{$HTDOCS_PATH}/ginmi_/mod_#{mod}.rb"
	html = ginmi_module( cgi )
end
html << "</div>"


####
puts html
