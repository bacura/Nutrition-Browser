#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser menu 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'menu'
school = '[料理教室]'


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
if @debug
	puts "commnad:#{command}<br>"
	puts "code:#{code}<br>"
	puts "<hr>"
end


menu = Menu.new( user.name )
meal = Meal.new( user.name )
meal.debug if @debug


case command
#### Displaing menu
when 'view'
	if code == ''
		# 献立データベースの仮登録チェック
  		r = mdb( "SELECT code FROM #{$MYSQL_TB_MENU} WHERE user='#{user.name}' AND name='' AND code!='';", false, @debug )
  		if r.first
			meal.load_menu( r.first['code'] )
  		else
		  	# 献立データベースに仮登録
			menu.code = generate_code( user.name, 'm' )
			menu.insert_db
 	 		meal.code = menu.code
  			meal.update_db
  		end
  	end
	menu.load_db( meal.code )

#### Saving menu
when 'save'
	menu.load_cgi( cgi )
	menu.label = menu.new_label unless menu.new_label == ''
	menu.protect = 1 if menu.label == school
	menu.protect = 1 if menu.public == 1

	menu_old = Menu.new( user.name )
	menu_old.load_db( code )

	if menu.name != menu_old.name
		# 名前が一致しなければ、新規コードとメニューを登録
		# バグに近い仕様：名前を変えて新規コードになるけど、写真はコピーされない
		menu.code = generate_code( user.name, 'm' )
		menu.insert_db
  		meal.code = menu.code
  		meal.name = menu.name
	end
	# Updating menu & meal
	menu.meal = meal.meal
	menu.debug if @debug
	menu.update_db
  	meal.update_db
end

# 写真ファイルと削除ボタン
photo_file = "no_image.png"
photo_del_button = ''
if menu.fig == 1
	photo_file = "photo/#{menu.code}-tn.jpg"
	photo_del_button = "<button class='btn btn-outline-danger' type='button' onclick=\"menu_photoDel( '#{menu.code}' )\">#{lp[1]}</button>"
end


# Label HTML
r = mdb( "SELECT label from #{$MYSQL_TB_MENU} WHERE user='#{user.name}' AND name!='';", false, @debug )
label_list = []
r.each do |e| label_list << e['label'] end
label_list.uniq!


html_label = '<select class="form-control form-control-sm" id="label">'
html_label << "<option value='#{lp[2]}'>#{lp[2]}</option>"
label_list.each do |e|
	html_label << "<option value='#{e}' #{selected( menu.label, e )}>#{e}</option>" unless e == lp[2] || e == school
end
html_label << "<option value='#{school}' #{selected( menu.label, school )}>#{school}</option>" if user.status >= 5 && user.status != 6
html_label << '</select>'


#### HTML
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{lp[3]}</h5></div>
		<div class="col-4">
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="public" #{checked( menu.public )}> #{lp[4]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="protect" #{checked( menu.protect )}> #{lp[5]}
  				</label>
			</div>
		</div>
		<div class="col-6">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="menu_name">#{lp[6]}</label>
				</div>
      			<input type="text" class="form-control" id="menu_name" value="#{menu.name}" required>
				<div class="input-group-append">
      				<button class="btn btn-outline-primary" type="button" onclick="menuSave( '#{menu.code}' )">#{lp[7]}</button>
				</div>
    		</div>
    	</div>
    </div>
    <br>
	<div class='row'>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="menu_name">#{lp[9]}</label>
				</div>
				#{html_label}
			</div>
		</div>
		<div class="col-4">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="menu_name">#{lp[10]}</label>
				</div>
      			<input type="text" class="form-control" id="new_label" value="">
	   		</div>
    	</div>
	</div>
    <br>
	<div class='row'>
		<div class="col">
			<div class="form-group">
    			<label for='memo'>メモ</label>
				<textarea class="form-control" id='memo' rows="2"></textarea>
   			</div>
		</div>
	</div>

	<div align='right' class='code'>#{menu.code}</div>
</div>
HTML

puts html
