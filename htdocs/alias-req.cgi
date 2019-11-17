#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser search alias request 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190224, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil ) if $DEBUG

cgi = CGI.new
uname, uid, status = login_check( cgi )
if @debug
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "<hr>"
end

#### POSTデータの取得
food_no = cgi['food_no']
request_alias = cgi['alias']
if @debug
	puts "food_no: #{food_no}<br>"
	puts "request_alias: #{request_alias}<br>"
	puts "<hr>"
end

#### 別名リクエストの記録
if request_alias != '' && request_alias != nil
	mariadb( "INSERT INTO #{$MYSQL_TB_SLOGF} SET code='#{food_no}', user='#{uname}', words='#{request_alias}', date='#{$DATETIME}';", false )
end