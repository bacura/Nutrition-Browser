#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171105, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'recipe'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### Fig copy method
def copy_fig( slot, code, source_code )
	FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-#{slot}tns.jpg", "#{$PHOTO_PATH}/#{code}-#{slot}tns.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-#{slot}tns.jpg" )
	FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-#{slot}tn.jpg", "#{$PHOTO_PATH}/#{code}-#{slot}tn.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-#{slot}tn.jpg" )
	FileUtils.cp( "#{$PHOTO_PATH}/#{source_code}-#{slot}.jpg", "#{$PHOTO_PATH}/#{code}-#{slot}.jpg" ) if File.exist?( "#{$PHOTO_PATH}/#{source_code}-#{slot}.jpg" )
end


#### Recipe class
class Recipe
	attr_accessor :code, :user, :public, :protect, :draft, :name, :dish, :type, :role, :tech, :time, :cost, :sum, :protocol, :fig1, :fig2, :fig3, :date

	def initialize( uname )
		@code = ''
		@user = uname
		@branch = nil
		@root = nil
		@public = 0
		@protect = 0
		@draft = 1
		@name = ''
		@dish = 1
		@type = 0
		@role = 0
		@tech = 0
		@time = 0
		@cost = 0
		@sum = ''
		@protocol = ''
		@fig1 = 0
		@fig2 = 0
		@fig3 = 0
		@date = $DATETIME
	end

	def load_cgi( cgi )
		@code = cgi['code']
		@public = cgi['public'].to_i
		@protect = cgi['protect'].to_i
		@draft = cgi['draft'].to_i
		@name = cgi['recipe_name']
		@type = cgi['type'].to_i
		@role = cgi['role'].to_i
		@tech = cgi['tech'].to_i
		@time = cgi['time'].to_i
		@cost = cgi['cost'].to_i
		@protocol = cgi['protocol']
	end

	def load_db()
		r = mdb( "SELECT * from #{$MYSQL_TB_RECIPE} WHERE user='#{@user}' and code='#{@code}';", false, false )
		if r.first
			@public = r.first['public'].to_i
			@protect = r.first['protect'].to_i
			@draft = r.first['draft'].to_i
			@name = r.first['name'].to_i
			@dish = r.first['dish'].to_i
			@type = r.first['type'].to_i
			@role = r.first['role'].to_i
			@tech = r.first['tech'].to_i
			@time = r.first['time'].to_i
			@cost = r.first['cost'].to_i
			@protocol = r.first['protocol']
			@fig1 = r.first['fig1'].to_i
			@fig2 = r.first['fig2'].to_i
			@fig3 = r.first['fig3'].to_i
			@date = r.first['date']
		end


		# Reset name
		r = mdb( "SELECT name from #{$MYSQL_TB_SUM} WHERE user='#{@user}';", false, false )
		@name = r.first['name']
	end

	def insert_db()
  		mdb( "INSERT INTO #{$MYSQL_TB_RECIPE} SET code='#{@code}', user='#{@user}',draft=#{@draft}, protect=#{@protect}, public=#{@public}, name='#{@name}', type=#{@type}, role=#{@role}, tech=#{tech}, time=#{@time}, cost=#{@cost}, sum='#{@sum}', protocol='#{@protocol}', fig1=#{@fig1}, fig2=#{@fig2}, fig3=#{@fig3}, date='#{@date}';", false, false )
	end

	def update_db()
		mdb( "UPDATE #{$MYSQL_TB_RECIPE} SET name='#{@name}', dish=#{@dish},type=#{@type}, role=#{@role}, tech=#{@tech}, time=#{@time}, cost=#{@cost}, sum='#{@sum}', protocol='#{@protocol}', public=#{@public}, protect=#{@protect}, draft=#{@draft}, fig1=#{@fig1}, fig2=#{@fig2}, fig3=#{@fig3}, date='#{@date}' WHERE user='#{@user}' and code='#{@code}';", false, false )
	end

	def debug
		puts "Recipe.code:#{@code}<br>"
		puts "Recipe.name:#{@name}<br>"
		puts "Recipe.public:#{@public}<br>"
		puts "Recipe.protect:#{@protect}<br>"
		puts "Recipe.draft:#{@draft}<br>"
		puts "Recipe.type:#{@type}<br>"
		puts "Recipe.role:#{@role}<br>"
		puts "Recipe.tech:#{@tech}<br>"
		puts "Recipe.dish:#{@dish}<br>"
		puts "Recipe.time:#{@time}<br>"
		puts "Recipe.cost:#{@cost}<br>"
		puts "Recipe.sum:#{@sum}<br>"
		puts "Recipe.protocol:#{@protocol}<br>"
		puts "Recipe.date:#{@date}<br>"
		puts "Recipe.fig1:#{@fig1}<br>"
		puts "Recipe.fig2:#{@fig2}<br>"
		puts "Recipe.fig3:#{@fig3}<br>"
	end
end

#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### Getting POST
command = cgi['command']
code = cgi['code']
if @debug
	puts "commnad:#{command}<br>"
	puts "code:#{code}<br>"
end

recipe = Recipe.new( user.name )
recipe.code = code
recipe.debug if @debug

case command
when 'view'
	# Loading recipe from DB
	recipe.load_db

when 'save'
	recipe.load_cgi( cgi )


	# excepting for tags
	recipe.protocol.gsub!( '<', '&lt;')
	recipe.protocol.gsub!( '>', '&gt;')
	recipe.protocol.gsub!( ';', '；')

	r = mdb( "SELECT sum, name, dish from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )

	# Inserting new recipe
	if r.first['name'] == ''
		recipe.code = generate_code( user.name, 'r' )
		recipe.sum = r.first['sum']
		recipe.dish = r.first['dish'].to_i
  		recipe.insert_db

	# Updating recipe
	else
		pre_recipe = Recipe.new( user.name )
		pre_recipe.code = recipe.code
		pre_recipe.load_db
		recipe.sum = r.first['sum']
		recipe.dish = r.first['dish'].to_i
		recipe.fig1 = pre_recipe.fig1
		recipe.fig2 = pre_recipe.fig2
		recipe.fig3 = pre_recipe.fig3

		copy_flag = false

		# Canceling public mode of recipe using puseudo user foods
		a = recipe.sum.split( "\t" )
		a.each do |e|
			sum_items = e.split( ':' )
			recipe.public = 0 if /^U/ =~ sum_items[0]
		end

		# Draft mode
		if recipe.draft == 1
			recipe.protect = 0
			recipe.public = 0
			recipe.update_db

		# Normal mode
		elsif recipe.draft == 0 && recipe.protect == 0
			if recipe.name == pre_recipe.name
				recipe.update_db
			else
				recipe.protect = 1 if recipe.public == 1
				copy_flag = true
			end

		# Protect mode
		else
			recipe.protect = 1 if recipe.public == 1
			if pre_recipe.protect == 0 && recipe.name == pre_recipe.name
				recipe.update_db
			else
				copy_flag = true
			end
		end

		if copy_flag == true
			recipe.code = generate_code( user.name, 'r' )

			# Copying name
			if recipe.name == pre_recipe.name
				t = pre_recipe.name.match( /\((\d+)\)$/ )
				sn = 1
				sn = t[1].to_i + 1 if t != nil
				pre_recipe.name.sub!( /\((\d+)\)$/, '' )
				recipe.name = "#{pre_recipe.name}(#{sn})"
			end

			# Cocying figs
			if recipe.fig1 == 1 || recipe.fig2 == 1 || recipe.fig3 == 1
			require 'fileutils'
				copy_fig( 1, recipe.code, pre_recipe.code )if recipe.fig1 == 1
				copy_fig( 2, recipe.code, pre_recipe.code )if recipe.fig2 == 1
				copy_fig( 3, recipe.code, pre_recipe.code )if recipe.fig3 == 1
			end
			recipe.insert_db
		end
	end

	mdb( "UPDATE #{$MYSQL_TB_SUM} SET name='#{recipe.name}', code='#{recipe.code}', protect='#{recipe.protect}' WHERE user='#{user.name}';", false, @debug )
end


# HTML SELECT Recipe attribute
check_public = ''
check_public = 'CHECKED' if recipe.public == 1

check_protect = ''
check_protect = 'CHECKED' if recipe.protect == 1

check_draft = ''
check_draft = 'CHECKED' if recipe.draft == 1


# HTML SELECT Recipe type
html_type = lp[1]
html_type << '<select class="form-control form-control-sm" id="type">'
$RECIPE_TYPE.size.times do |c|
	if recipe.type == c
		html_type << "<option value='#{c}' SELECTED>#{$RECIPE_TYPE[c]}</option>"
	else
		html_type << "<option value='#{c}'>#{$RECIPE_TYPE[c]}</option>"
	end
end
html_type << '</select>'


# HTML SELECT Recipe role
html_role = lp[2]
html_role << '<select class="form-control form-control-sm" id="role">'
$RECIPE_ROLE.size.times do |c|
	if recipe.role == c
		html_role << "<option value='#{c}' SELECTED>#{$RECIPE_ROLE[c]}</option>"
	else
		html_role << "<option value='#{c}'>#{$RECIPE_ROLE[c]}</option>"
	end
end
if recipe.role == 100
	html_role << "<option value='100' SELECTED>[ 調味％ ]</option>"
else
	html_role << "<option value='100'>[ 調味％ ]</option>"
end
html_role << '</select>'


# HTML SELECT Recipe technique
html_tech = lp[3]
html_tech << '<select class="form-control form-control-sm" id="tech">'
$RECIPE_TECH.size.times do |c|
	if recipe.tech == c
		html_tech << "<option value='#{c}' SELECTED>#{$RECIPE_TECH[c]}</option>"
	else
		html_tech << "<option value='#{c}'>#{$RECIPE_TECH[c]}</option>"
	end
end
html_tech << '</select>'


# HTML SELECT Recipe time
html_time = lp[4]
html_time << '<select class="form-control form-control-sm" id="time">'
$RECIPE_TIME.size.times do |c|
	if recipe.time == c
		html_time << "<option value='#{c}' SELECTED>#{$RECIPE_TIME[c]}</option>"
	else
		html_time << "<option value='#{c}'>#{$RECIPE_TIME[c]}</option>"
	end
end
html_time << '</select>'


# HTML SELECT Recipe cost
html_cost = lp[5]
html_cost << '<select class="form-control form-control-sm" id="cost">'
$RECIPE_COST.size.times do |c|
	if recipe.cost == c
		html_cost << "<option value='#{c}' SELECTED>#{$RECIPE_COST[c]}</option>"
	else
		html_cost << "<option value='#{c}'>#{$RECIPE_COST[c]}</option>"
	end
end
html_cost << '</select>'


#### HTML FORM recipe
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{lp[6]}</h5></div>
		<div class="col-3">
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="public" #{check_public} onchange="recipeBit_public()"> #{lp[7]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="protect" #{check_protect} onchange="recipeBit_protect()"> #{lp[8]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="draft" #{check_draft} onchange="recipeBit_draft()"> #{lp[9]}
  				</label>
			</div>
		</div>
		<div class="col-1">
    	</div>
  		<div class="col-5">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="recipe_name">#{lp[10]}</label>
				</div>
      			<input type="text" class="form-control" id="recipe_name" value="#{recipe.name}" required>
				<div class="input-group-append">
      				<button class="btn btn-outline-primary" type="button" onclick="recipeSave_BWL2( '#{recipe.code}' )">#{lp[11]}</button>
				</div>
    		</div>
    	</div>
    </div>
    <br>
	<div class='row'>
		<div class='col'>#{html_type}</div>
		<div class='col'>#{html_role}</div>
		<div class='col'>#{html_tech}</div>
		<div class='col'>#{html_time}</div>
		<div class='col'>#{html_cost}</div>
	</div>
	<br>
	<div class='row'>
		<div class="col form-group">
			<div class="col">
    			<label for="exampleFormControlTextarea1">#{lp[12]}</label>
				<textarea class="form-control" id="protocol" rows="10">#{recipe.protocol}</textarea>
			</div>
  		</div>
	</div>
	<div align='right' class='code'>#{recipe.code}</div>
</div>
HTML

puts html
