#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser fctb meal monitor 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171207, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'mealm.cgi'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status = login_check( cgi )


#### Getting POST data
recipe_code = cgi['recipe_code']


#### Updating MEAL and Reflashing
unless recipe_code == ''
	if uname
		recipe_num = 0
		r = mariadb( "SELECT meal from #{$MYSQL_TB_MEAL} WHERE user='#{uname}';", false )
 		if r.first['meal']
			a = r.first['meal'].split( "\t" )
			recipe_num = a.size
			if recipe_num == 0
				new_meal = "#{recipe_code}"
			else
				new_meal = "#{r.first['meal']}\t#{recipe_code}"
			end
		else
			new_meal = recipe_code
 		end
		mariadb( "UPDATE #{$MYSQL_TB_MEAL} SET meal='#{new_meal}' WHERE user='#{uname}';", false )

		recipe_num += 1
		puts recipe_num
	else
		puts = '-'
	end


#### Reflashing
else
	if uname
		r = mariadb( "SELECT meal from #{$MYSQL_TB_MEAL} WHERE user='#{uname}';", false )
		t = r.first['meal'].split( "\t" )
		puts t.size
	else
		puts = '-'
	end
end
