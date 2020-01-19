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
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================
#### 初期画面
def config_init( lp, status )
	html = <<-"HTML"
<button type="button" class="btn btn-info btn-sm nav_button" onclick="account_cfg()">#{lp[1]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="bio_cfg()">#{lp[11]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="display_cfg()">#{lp[10]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="palette_cfg( 'list' )">#{lp[2]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="history_cfg()">#{lp[6]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="sum_cfg()">#{lp[7]}</button>
<button type="button" class="btn btn-info btn-sm nav_button" onclick="koyomiex_cfg( 'init' )">#{lp[9]}</button>
<button type="button" class="btn btn-danger btn-sm nav_button" onclick="release_cfg()">#{lp[8]}</button>
HTML

	return html
end

#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'config', language )

html_init( nil )
if @debug
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
end


command = cgi['command']
if @debug
	puts"command: #{command}"
	puts"<hr>"
end


#### モジュール選択
html = ''
if command == 'init'
	html = config_init( lp, status )
else
	require "#{$HTDOCS_PATH}/config_/mod_#{command}.rb"
	html = config_module( cgi )
end


#### 画面表示
puts html
