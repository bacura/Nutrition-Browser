#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser meal 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'meal'


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
lp = user.language( script )


#### Getting POST data
command = cgi['command']
code = cgi['code']
order = cgi['order']
if @debug
	puts "command:#{command}<br>"
	puts "code:#{code}<br>"
	puts "order:#{order}<br>"
	puts "<hr>"
end


#### Reading MEAL
meal = Meal.new( user.name )
meal.load_menu( code ) if command == 'load'
meal.debug if @debug


#### 食品と付随成分の抽出
recipe_list = []
if meal.meal
	meal.meal.split( "\t" ).each do |e|
		recipe = Recipe.new( user.name )
		recipe.load_db( e )
		recipe_list << recipe
	end
end


case command
# Deleting recipe from meal
when 'clear'
	# All
	if order == 'all'
		recipe_list = []
		meal.name = ''
		meal.code = ''
	# One by one
	else
		recipe_list.delete_at( order.to_i )
		update = '*'
	end

# 食品の順番を１つ上げる
when 'upper'
	if order.to_i == 0
		t = recipe_list.shift
		recipe_list << t
	else
		t = recipe_list.delete_at( order.to_i )
		recipe_list.insert( order.to_i - 1, t )
	end
	update = '*'

# 食品の順番を１つ下げる
when 'lower'
	if order.to_i == recipe_list.size - 1
		t = recipe_list.pop
		recipe_list.unshift( t )
	else
		t = recipe_list.delete_at( order.to_i )
		recipe_list.insert( order.to_i + 1, t )
	end
	update = '*'
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-10'><h5>#{lp[1]}: #{meal.name}</h5></div>
		<div class='col-2'>
			<input type='checkbox' id='meal_all_check'>&nbsp;
			<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"clear_meal( 'all', '#{meal.code}' )\">#{lp[2]}</button>
		</div>
	</div>
	<hr>

	<div class='row'>
		<div class='col-2 meal_header'>#{lp[3]}</div>
		<div class='col-1 meal_header'>#{lp[4]}</div>
		<div class='col-4 meal_header'>#{lp[5]}</div>
		<div class='col-2 meal_header'>#{lp[6]}</div>
	</div>
	<br>
HTML

c = 0
recipe_list.each do |e|
	html << "	<div class='row'>"
 	html << "		<div class='col-2'>"
 	html << "			<button type='button' class='btn btn-outline-danger btn-sm del_button' onclick=\"clear_meal( '#{c}', '#{e.code}' )\">X</button>&nbsp;&nbsp;"
 	html << "			<button type='button' class='btn btn-outline-primary btn-sm ctl_button' onclick=\"upper_meal( '#{c}', '#{e.code}' )\">↑</button>"
 	html << "			<button type='button' class='btn btn-outline-primary btn-sm ctl_button' onclick=\"lower_meal( '#{c}', '#{e.code}' )\">↓</button>"
 	html << "		</div>"
  	if e.fig1 == 0
  		html << "		<div class='col-1' align='center'>-</div>"
  	else
  		html << "		<div class='col-1' align='center'><img src='photo/#{e.code}-1tns.jpg'></div>"
  	end
  	html << "		<div class='col-4' onclick=\"initCB_BWL1( 'load', '#{e.code}' )\">#{e.name}</div>"
  	html << "		<div class='col-1'>"
  	html << "			#{$RECIPE_TYPE[e.type]}&nbsp;" unless e.type == 0
  	html << "		</div>"
  	html << "		<div class='col-1'>"
  	html << "			#{$RECIPE_ROLE[e.role]}&nbsp;" unless e.role == 0
  	html << "		</div>"
  	html << "		<div class='col-1'>"
  	html << "			#{$RECIPE_TECH[e.tech]}&nbsp;" unless e.tech == 0
  	html << "		</div>"
  	html << "		<div class='col-1'>"
  	html << "		</div>"
  	html << "		<div class='col-1'>"
  	html << "		</div>"
	html << "	</div>"
	c += 1
end


html << "	<br>"
html << "	<div class='row'>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuEdit( 'view', '#{meal.code}' )\">#{lp[7]}</button></div>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuCalcView( '#{meal.code}' )\">#{lp[8]}</button></div>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuAnalysis( '#{meal.code}' )\">#{lp[9]}</button></div>"
html << "	</div>"
html << "	<div class='code'>#{meal.code}</div>"
html << "</div>"

puts html

#### Updating MEAL
meal_new = ''
recipe_list.each do |e| meal_new << "#{e.code}\t" end
meal.meal = meal_new.chop!
meal.update_db
