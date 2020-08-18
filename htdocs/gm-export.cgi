#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM extag export 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190315, 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'gm-export.cgi'

#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil ) if @debug

puts "Content-type: text/text\n\n"

#### GETデータの取得
get_data = get_data()
extag = get_data['extag']
puts "extag:#{extag}\n" if @debug

cgi = CGI.new
user = User.new( cgi )

#### GMチェック
if user.status < 8
	puts "GM error."
	exit
end

export = ''
case extag
when 'unitc'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_EXT};", false, @debug )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['unitc']}\t#{e['unitn']}\n" end
when 'color'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_EXT};", false, @debug )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['color1']}\t#{e['color2']}\t#{e['color1h']}\t#{e['color2h']}\n" end

when 'allergen'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_EXT};", false, @debug )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['allergen']}\n" end

when 'gycv'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_EXT};", false, @debug )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['gycv']}\n" end

when 'shun'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_EXT};", false, @debug )
	r.each do |e| export << "#{e['FN']}\t#{e['user']}\t#{e['shun1s']}\t#{e['shun1e']}\t#{e['shun2s']}\t#{e['shun2e']}\n" end

when 'dic'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_DIC};", false, @debug )
#	r.each do |e| export << "#{e['tn']}\t#{e['org_name']}\t#{e['alias']}\t#{e['user']}\n" end

else
	export_extag << 'Extag error.'
end

puts export.encode( 'Shift_JIS' )
