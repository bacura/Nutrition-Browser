#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser fctb meal monitor 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171207, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'mealm'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug


#### Getting POST data
recipe_code = cgi['recipe_code']


#### Updating MEAL and Reflashing
unless recipe_code == ''
	if user.name
		recipe_num = 0
		r = mdb( "SELECT meal from #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';", false, @debug )
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
		mdb( "UPDATE #{$MYSQL_TB_MEAL} SET meal='#{new_meal}' WHERE user='#{user.name}';", false, @debug )

		recipe_num += 1
		puts recipe_num
	else
		puts '-'
	end


#### Reflashing
else
	if user.name
		r = mdb( "SELECT meal from #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';", false, @debug )
		t = r.first['meal'].split( "\t" )
		puts t.size
	else
		puts '-'
	end
end
