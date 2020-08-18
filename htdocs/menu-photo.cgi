#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser menu photo 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'
require 'rmagick'


#==============================================================================
#STATIC
#==============================================================================
$SIZE_MAX = 20000000
$TN_SIZE = 400
$TNS_SIZE = 40
$PHOTO_SIZE_MAX = 2000
@debug = false
script = 'menu-photo'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
user = User.new( cgi )
user.debug if @debug
lp = user.language( script )

#### Geeting POST
command = cgi['command']
code = cgi['code']
slot = cgi['slot']
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "slot: #{slot}<br>"
	puts "PHOTO_PATH: #{$PHOTO_PATH}<br>"
	puts "PHOTO_PATH_TMP: #{$PHOTO_PATH_TMP}<br>"
	puts "<hr>"
end


meal = Meal.new( user.name )
menu = Menu.new( user.name )


case command
when 'form'

	if slot == 'photo'
		5.times do |c|
			break if File.exist?( "#{$PHOTO_PATH}/#{menu.code}-tn.jpg" )
			sleep( 2 )
		end
	end

	if meal.code == ''
		puts "No code."
		exit
	end

	# 写真ファイルと削除ボタン
	photo_file = "photo/no_image.png"
	photo_del_button = ''
	if menu.fig == 1
		photo_file = "photo/#{menu.code}-tn.jpg"
		photo_del_button = "<button class='btn btn-outline-danger' type='button' onclick=\"menu_photoDel( '#{menu.code}' )\">#{lp[1]}</button>"
	end

	html = ''
	html = <<-"HTML"
	<form class='row' method="post" enctype="multipart/form-data" id='photo_form'>
		<div class='col' align="center">
			<div class="form-group">
				<label for="photom">#{lp[2]}</label><br>
				<input type="file" name="photo1" id="photom" class="custom-control-file" onchange="menu_photoSave( '#{menu.code}' )">
			</div>
			<img src="#{photo_file}" width="200px" class="img-thumbnail"><br>
			<br>
			#{photo_del_button}
		</div>
	</form>
HTML
	puts html


when 'upload'
	photo_name = cgi[slot].original_filename
	photo_type = cgi[slot].content_type
	photo_body = cgi[slot].read
	photo_size = photo_body.size.to_i

	if photo_size < $SIZE_MAX && ( photo_type == 'image/jpeg' || photo_type == 'image/jpg' )

		# Creating tmo file
		f =open( "#{$PHOTO_PATH_TMP}/#{photo_name}", 'w' )
			f.puts photo_body
		f.close

		photo = Magick::ImageList.new( "#{$PHOTO_PATH_TMP}/#{photo_name}" )

		# Changing photo size
		photo_x = photo.columns.to_f
		photo_y = photo.rows.to_f
		photo_ratio = 1.0
		if photo_x >= photo_y
			tn_ratio = $TN_SIZE / photo_x
			tns_ratio = $TNS_SIZE / photo_x
			photo_ratio = $PHOTO_SIZE_MAX / photo_x if photo_x <= $PHOTO_SIZE_MAX
		else
			tn_ratio = $TN_SIZE / photo_y
			tns_ratio = $TNS_SIZE / photo_y
			photo_ratio = $PHOTO_SIZE_MAX / photo_y if photo_y <= $PHOTO_SIZE_MAX
		end
		tns_file = photo.thumbnail( tns_ratio )
		tn_file = photo.thumbnail( tn_ratio )
		photo_file = photo.thumbnail( photo_ratio )

		# Weiting photos
		tns_file.write( "#{$PHOTO_PATH}/#{code}-tns.jpg" )
		tn_file.write( "#{$PHOTO_PATH}/#{code}-tn.jpg" )
		photo_file.write( "#{$PHOTO_PATH}/#{code}.jpg" )

		# Deleting tmp file
		File.unlink "#{$PHOTO_PATH_TMP}/#{photo_name}"

		# Updating menu
		mdb( "UPDATE #{$MYSQL_TB_MENU} SET fig=1 WHERE code='#{code}';", false, @debug )
	else
	end


when 'delete'
	# Deleting photo file
	if File.exist?( "#{$PHOTO_PATH}/#{code}.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{code}-tns.jpg"
		File.unlink "#{$PHOTO_PATH}/#{code}-tn.jpg"
		File.unlink "#{$PHOTO_PATH}/#{code}.jpg"

		# Updating menu
		mdb( "UPDATE #{$MYSQL_TB_MENU} SET fig='0' WHERE code='#{code}';", false, @debug )
	end
else
end
