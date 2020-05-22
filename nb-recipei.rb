#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe search index builder 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190319, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'
require 'natto'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
#$UDIC = '/usr/local/share/mecab/dic/ipadic/sys.dic'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================

mecab = Natto::MeCab.new()
words = Hash.new

db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
db.query( "update #{$MYSQL_TB_RECIPEI} SET f=0;" )


#### Makeing alias dictionary
puts "Makeing alias dictionary."
dic = Hash.new
res = db.query( "SELECT org_name, alias FROM #{$MYSQL_TB_DIC};" )
res.each do |e|
	dic[e['alias']] = e['org_name']
end


#### Lording all recipe list
puts "Analyzing recipe data.\n"
res = db.query( "SELECT code, name, sum, protocol, public, user FROM #{$MYSQL_TB_RECIPE};" )
res.each do |e|
	print "#{e['code']}\r"
	target = []

	#recipe name
	target << e['name']

	#comment 1st line
	a = e['protocol'].split( "\n" )
	unless a[0] == nil
		if /^\#.+/ =~ a[0]
			target << a[0]
		end
	end

	target.each do |ee|
		mecab.parse( ee ) do |n|
			a = n.feature.force_encoding( 'utf-8' ).split( ',' )
		 	if a[0] == '名詞' && ( a[1] == '一般' || a[1] == '固有名詞' )
				res2 = db.query( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE user='#{e['user']}' AND code='#{e['code']}' AND word='#{n.surface}';" )
				if res2.first
					db.query( "UPDATE #{$MYSQL_TB_RECIPEI} SET public='#{e['public']}', f=1 WHERE user='#{e['user']}' AND code='#{e['code']}' AND word='#{n.surface}';" )
				else
					db.query( "INSERT INTO #{$MYSQL_TB_RECIPEI}  SET public='#{e['public']}', f=1, user='#{e['user']}', code='#{e['code']}', word='#{n.surface}';" )
				end

		 		if dic[n.surface]
					res2 = db.query( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE user='#{e['user']}' AND code='#{e['code']}' AND word='#{dic[n.surface]}';" )
					if res2.first
						db.query( "UPDATE #{$MYSQL_TB_RECIPEI} SET public='#{e['public']}', f=1 WHERE user='#{e['user']}' AND code='#{e['code']}' AND word='#{dic[n.surface]}';" )
					else
						db.query( "INSERT INTO #{$MYSQL_TB_RECIPEI}  SET public='#{e['public']}', f=1, user='#{e['user']}', code='#{e['code']}', word='#{dic[n.surface]}';" )
					end
				end
		 	end
		end
	end

	#foods
	a = e['sum'].split( "\t" )
	sum_code = []
	target_food = []
	a.each do |ee| sum_code << ee.split( ':' ).first end
	sum_code.each do |ee|
		res2 = db.query( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{ee}';" )
		target_food << res2.first['name'] if res2.first
	end

	target_food.each do |ee|
		res2 = db.query( "SELECT * FROM #{$MYSQL_TB_RECIPEI} WHERE user='#{e['user']}' AND code='#{e['code']}' AND word='#{ee}';" )
		if res2.first
			db.query( "UPDATE #{$MYSQL_TB_RECIPEI} SET public='#{e['public']}', f=1 WHERE user='#{e['user']}' AND code='#{e['code']}' AND word='#{ee}';" )
		else
			db.query( "INSERT INTO #{$MYSQL_TB_RECIPEI}  SET public='#{e['public']}', f=1, user='#{e['user']}', code='#{e['code']}', word='#{ee}';" )
		end
	end
end


#### Deleting non-existent recipe
puts "\nDeleting non-existent recipe."
db.query( "DELETE FROM #{$MYSQL_TB_RECIPEI} WHERE f=0;" )


puts "Done."

