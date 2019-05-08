#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser meal 0.00

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
$SCRIPT = 'fctb-meal.cgi'
$DEBUG = false


#==============================================================================
#DEFINITION
#==============================================================================
class Recipe
	def initialize( no )
		@no = no
		@recipe_name = ''
		@type = 0
		@role = 0
		@tech = 0
		@fig1 = 0
	end

	def meal_load( recipe )
		t = recipe.split( ':' )
		@no = t[0]
	end

	attr_accessor :no, :recipe_name, :type, :role, :tech, :fig1
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'meal', language )
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
end


#### Getting POST data
command = cgi['command']
code = cgi['code']
order = cgi['order']
if $DEBUG
	puts "command:#{command}<br>"
	puts "code:#{code}<br>"
	puts "order:#{order}<br>"
	puts "<hr>"
end


#### Reading MEAL
query = "SELECT code, name, meal from #{$MYSQL_TB_MEAL} WHERE user='#{uname}';"
if command == 'load'
	query = "SELECT code, name, meal from #{$MYSQL_TB_MENU} WHERE code='#{code}';"
end
r = mariadb( query, false )

code = r.first['code']
meal_name = r.first['name']
meal = r.first['meal']
protect = r.first['protect'].to_i
update = ''
if $DEBUG
	puts "code:#{code}<br>"
	puts "meal_name:#{meal_name}<br>"
	puts "protect:#{protect}<br>"
	puts "meal:#{meal}<br>"
	puts "<hr>"
end


#### 食品と付随成分の抽出
recipe_list = []
if meal
	meal.split( "\t" ).each do |e|
		t = Recipe.new( nil )
		t.meal_load( e )
		recipe_list << t
	end
end


case command
# リストから食品を削除
when 'clear'
	# All
	if order == 'all'
		recipe_list = []
		meal_name = ''
		code = ''
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


#### MEALの読み込み
db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
c = 0
recipe_list.each do |e|
	query = "SELECT code, name, type, role, tech, fig1 from #{$MYSQL_TB_RECIPE} WHERE code='#{e.no}';"
	res = db.query( query )
	if res.first
		recipe_list[c].recipe_name = res.first['name']
		recipe_list[c].type = res.first['type']
		recipe_list[c].role = res.first['role']
		recipe_list[c].tech = res.first['tech']
		recipe_list[c].fig1 = res.first['fig1']
	end
	c += 1
end
db.close


#### 新しいお膳表示
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-9'><h5>#{lp[1]}: #{meal_name}</h5></div>
		<div class='col-3'>
			<input type='checkbox' id='meal_all_check'>&nbsp;
			<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"clear_meal_BWL1( 'all', '#{code}' )\">#{lp[2]}</button>
		</div>
	</div>
	<hr>

	<div class='row'>
		<div class='col-2 meal_header'>#{lp[3]}</div>
		<div class='col-1 meal_header'>#{lp[4]}</div>
		<div class='col-5 meal_header'>#{lp[5]}</div>
		<div class='col-2 meal_header'>#{lp[6]}</div>
	</div>
	<br>
HTML

c = 0
recipe_list.each do |e|
	html << "	<div class='row'>"
 	html << "		<div class='col-2'>"
 	html << "			<button type='button' class='btn btn-outline-danger btn-sm del_button' onclick=\"clear_meal_BWL1( '#{c}', '#{code}' )\">X</button>&nbsp;&nbsp;"
 	html << "			<button type='button' class='btn btn-outline-primary btn-sm ctl_button' onclick=\"upper_meal_BWL1( '#{c}', '#{code}' )\">↑</button>"
 	html << "			<button type='button' class='btn btn-outline-primary btn-sm ctl_button' onclick=\"lower_meal_BWL1( '#{c}', '#{code}' )\">↓</button>"
 	html << "		</div>"
  	if e.fig1 == 0
  		html << "		<div class='col-1' align='center'>-</div>"
  	else
  		html << "		<div class='col-1' align='center'><img src='photo/#{e.no}-1tns.jpg'></div>"
  	end
  	html << "		<div class='col-5' onclick=\"initCB_BWL1( 'load', '#{e.no}' )\">#{e.recipe_name}</div>"
  	html << "		<div class='col-2'>"
  	html << "			#{$RECIPE_TYPE[e.type]}&nbsp;" unless e.type == 0
  	html << "			#{$RECIPE_ROLE[e.role]}&nbsp;" unless e.role == 0
  	html << "			#{$RECIPE_TECH[e.tech]}&nbsp;" unless e.tech == 0
  	html << "		</div>"
	html << "	</div>"
	c += 1
end

html << "	<div class='row'>"
recipe_list.each do |e|
	html << "	<div class='col'>"
	html << "	</div>"
end
html << "	</div><br>"

html << "	<div class='row'>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuEdit_BWL2( 'view', '#{code}' )\">#{lp[7]}</button></div>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuCalcView_BWL2( '#{code}' )\">#{lp[8]}</button></div>"
html << "		<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"menuAnalysis_BWL2( '#{code}' )\">#{lp[9]}</button></div>"
html << "	</div>"
html << "	<div class='code'>#{code}</div>"
html << "</div>"

puts html

#### Updating MEAL
meal_new = ''
recipe_list.each do |e| meal_new << "#{e.no}\t" end
meal_new.chop!
mariadb( "UPDATE #{$MYSQL_TB_MEAL} set code='#{code}', name='#{meal_name}', meal='#{meal_new}' WHERE user='#{uname}';", false )
