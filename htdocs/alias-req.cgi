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
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'alias-req'

#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### Geeting POST
food_no = cgi['food_no']
request_alias = cgi['alias']
if @debug
	puts "food_no: #{food_no}<br>"
	puts "request_alias: #{request_alias}<br>"
	puts "<hr>"
end

#### Update alias
if request_alias != '' && request_alias != nil
	mdb( "INSERT INTO #{$MYSQL_TB_SLOGF} SET code='#{food_no}', user='#{user.name}', words='#{request_alias}', date='#{$DATETIME}';", false, @debug )
end