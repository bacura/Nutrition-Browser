#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser config 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20180411, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'config'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================
#### 初期画面
def init( lp, user )
	bio = ''
	bio = "<button type='button' class='btn btn-info btn-sm nav_button' onclick=\"configForm( 'bio' )\">#{lp[11]}</button>" if user.status >= 2
	koyomiex = ''
	koyomiex = "<button type='button' class='btn btn-info btn-sm nav_button' onclick=\"configForm( 'koyomi' )\">#{lp[9]}</button>" if user.status >= 2
	schoolm = ''
	schoolm = "<button type='button' class='btn btn-info btn-sm nav_button' onclick=\"configForm( 'school' )\">#{lp[71]}</button>" if user.status >= 5 && user.status != 6
	html = <<-"HTML"
<button type="button" class="btn btn-info btn-sm nav_button" onclick="configForm( 'account' )">#{lp[1]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="configForm( 'display' )">#{lp[10]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="configForm( 'palette' )">#{lp[2]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="configForm( 'history' )">#{lp[6]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="configForm( 'sum' )">#{lp[7]}</button>
#{bio}
#{koyomiex}
#{schoolm}
<button type="button" class="btn btn-danger btn-sm nav_button" onclick="configForm( 'release' )">#{lp[8]}</button>
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
	puts"mod: #{mod}"
	puts"<hr>"
end


####
html = ''
if mod == ''
	html = init( lp, user )
else
	require "#{$HTDOCS_PATH}/config_/mod_#{mod}.rb"
	html = config_module( cgi, user, lp )
end


#### 画面表示
puts html
