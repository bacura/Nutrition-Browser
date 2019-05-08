#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM extag export 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190315, 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'gm-export.cgi'
$DEBUG = false

#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil ) if $DEBUG

puts "Content-type: text/text\n\n"

#### GETデータの取得
get_data = get_data()
extag = get_data['extag']
puts "extag:#{extag}\n" if $DEBUG

cgi = CGI.new
uname, uid, status = login_check( cgi )

#### GMチェック
if status < 9
	puts "GM error."
	exit
end

export = ''
case extag
when 'unitc'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_EXT};", false )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['unitc']}\t#{e['unitn']}\n" end
when 'color'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_EXT};", false )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['color1']}\t#{e['color2']}\t#{e['color1h']}\t#{e['color2h']}\n" end

when 'allergen'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_EXT};", false )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['allergen']}\n" end

when 'gycv'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_EXT};", false )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['gycv']}\n" end

when 'shun'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_EXT};", false )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['shun1s']}\t#{e['shun1e']}\t#{e['shun2s']}\t#{e['shun2e']}\n" end

when 'dic'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_DIC};", false )
#	r.each do |e| export << "#{e['tn']}\t#{e['org_name']}\t#{e['alias']}\t#{e['user']}\n" end

else
	export_extag << 'Extag error.'
end

puts export.encode( 'Shift_JIS' )
