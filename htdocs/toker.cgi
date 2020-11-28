#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser statistics tools 0.00

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
script = 'toker'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================


#### Initial screen menu
def init( lp )
	html = <<-"HTML"
	<button class='btn btn-sm btn-outline-info nav_button' onclick="tokerForm( 'test' )">#{lp[1]}</button>
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
	require "#{$HTDOCS_PATH}/toker_/mod_#{mod}.rb"
	html = toker_module( cgi, user )
end
html << "</div>"


####
puts html
