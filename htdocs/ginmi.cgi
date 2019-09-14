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
require 'cgi'
require 'date'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = true


#==============================================================================
#DEFINITION
#==============================================================================

#### 初期画面
def init( lp, status )
	html = <<-"HTML"
	<div class='row'>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="ginmiBMI()">BMI</button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="">MNA</button></div>
		<div class='col-2'><button class='btn btn-sm btn-outline-info' onclick="">SGA</button></div>
	</div>
HTML

	return html
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomi', language )
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
