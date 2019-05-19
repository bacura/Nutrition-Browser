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
$SCRIPT = 'fctb-recopei.cgi'
$DEBUG = false
$UDIC = '/usr/local/share/mecab/dic/mecab-user-dict-seed.20190307.dic'

#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================

mecab = Natto::MeCab.new( userdic: $UDIC )
words = Hash.new

#### Lording all recipe list
puts "Lording recipe data.\n"
r = mariadb( "SELECT code, name, sum, protocol FROM #{$MYSQL_TB_RECIPE};", false )
r.each do |e|
	target = []

	#recipe name
	target << e['name']

	#foods
	a = e['sum'].split( "\t" )
	sum_code = []
	a.each do |ee| sum_code << ee.split( ':' ).first end
	sum_code.each do |ee|
		rr = mariadb( "SELECT FG, name, class1, class2, class3 FROM #{$MYSQL_TB_TAG} WHERE FN='#{ee}' AND FG!='00' AND FG!='03' AND FG!='14' AND FG!='15' AND FG!='16' AND FG!='17' AND FG!='18';", false )
		if rr.first
			target << rr.first['name']
			target << rr.first['class1'] if rr.first['class1'] != ''
			target << rr.first['class2'] if rr.first['class2'] != ''
			target << rr.first['class3'] if rr.first['class3'] != ''
		end
	end

	#comment 1st line
	a = e['protocol'].split( "\n" )
	unless a[0] == nil
		target << a[0] if /^\#.+/ =~ a[0]
	end

	target_dic = []
	target.each do  |ee|
		rr = mariadb( "SELECT org_name FROM #{$MYSQL_TB_DIC} WHERE alias='#{ee}';", false )
		if rr.first
			target_dic << rr.first['org_name']
			target_dic << ee
		else
			target_dic << ee
		end
	end

	target_u = []
	target_dic.each do |e|
		mecab.parse( e ) do |n|
			a = n.feature.split( ',' )
		 	if a[0] == '名詞' && ( a[1] == '一般' || a[1] == '固有名詞' )
		 		target_u << n.surface
		 	end
		end
	end
	target_u.uniq!

	target_u.each do |ee|
		if words[ee]
			words[ee] = "#{words[ee]}:#{e['code']}"
		else
			words[ee] = e['code']
		end
	end
end


#### Removing no-exist recipe
puts "Removing no-exist recipe.\n"
r = mariadb( "SELECT words FROM #{$MYSQL_TB_RECIPEI};", false )
r.each do |e|
	 mariadb( "DELETE FROM #{$MYSQL_TB_RECIPEI} WHERE words='#{e['words']}';", false ) if words[e['words']] == nil
end


#### Updating recipei
puts "Updating recipei.\n"
words.each do |k, v|
	r = mariadb( "SELECT words FROM #{$MYSQL_TB_RECIPEI} WHERE words='#{k}'", false )
	if r.first
		mariadb( "UPDATE #{$MYSQL_TB_RECIPEI} SET codes='#{v}' WHERE words='#{k}';", false )
	else
		mariadb( "INSERT INTO #{$MYSQL_TB_RECIPEI} SET words='#{k}', codes='#{v}', count='0';", false )
	end
end


#### recipeif => recipei
puts "Copying recipeif => recipei.\n"
r = mariadb( "SELECT words, count FROM #{$MYSQL_TB_RECIPEIF};", false )
r.each do |e|
	rr = mariadb( "SELECT words, count FROM #{$MYSQL_TB_RECIPEI} WHERE words='#{e['words']}'", false )
	if rr.first
		if e['count'].to_i > rr.first['count'].to_i
			mariadb( "UPDATE #{$MYSQL_TB_RECIPEI} SET count='#{e['count']}' WHERE words='#{e['words']}';", false )
		end
	end
end

#### Flashing recipeif
puts "Flashing recipeif.\n"
mariadb( "DELETE FROM #{$MYSQL_TB_RECIPEIF};", false )


#### recipei => recipeif
puts "Copying recipei => recipeif.\n"
r = mariadb( "SELECT * FROM #{$MYSQL_TB_RECIPEI} ORDER BY 'count' LIMIT 1000;", false )
r.each do |e|
	mariadb( "INSERT INTO #{$MYSQL_TB_RECIPEIF} SET words='#{e['words']}', codes='#{e['codes']}', count='#{e['count']}';", false )
end

puts "Done.\n"
