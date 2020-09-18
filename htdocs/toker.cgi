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
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'ginmi'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### 初期画面
def init( lp )
	html = <<-"HTML"
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'bmi' )">#{lp[1]}</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'kaupi' )">#{lp[2]}</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'laureli' )">#{lp[3]}</button>
	<button class='btn btn-sm btn-outline-light nav_button' onclick="ginmiForm( 'obesity' )">#{lp[4]}</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'energy-ref' )">#{lp[5]}</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'energy-hn' )">#{lp[6]}</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'energy-hb' )">#{lp[7]}</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'energy-ath' )">#{lp[8]}</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'energy-mets' )">#{lp[9]}</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'es-height' )">#{lp[10]}</button>
	<button class='btn btn-sm btn-outline-info nav_button' onclick="ginmiForm( 'es-muscle' )">#{lp[11]}</button>
	<button class='btn btn-sm btn-outline-light nav_button' onclick="">#{lp[12]}</button>
	<button class='btn btn-sm btn-outline-light nav_button' onclick="">#{lp[13]}</button>
	<button class='btn btn-sm btn-outline-light nav_button' onclick="">#{lp[14]}</button>
HTML

	return html
end


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### Getting POST
mod = cgi['mod']
if @debug
	puts "mod:#{mod}<br>\n"
	puts "<hr>\n"
end


####
html = "<div class='container-fluid'>"
if mod == ''
	html = init( lp )
else
	require "#{$HTDOCS_PATH}/ginmi_/mod_#{mod}.rb"
	html = ginmi_module( cgi, user )
end
html << "</div>"


####
puts html
