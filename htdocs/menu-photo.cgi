#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser menu photo 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171214, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'menu-photo.cgi'
$SIZE_MAX = 20000000
$TN_SIZE = 400
$TNS_SIZE = 40
$PHOTO_SIZE_MAX = 2000

$WM_FONT = 'さざなみゴシック'

$DEBUG = false
#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'menu-photo', language )
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "<hr>"
end


#### POSTデータの取得
command = cgi['command']
code = cgi['code']
slot = cgi['slot']
if $DEBUG
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "slot: #{slot}<br>"
	puts "PHOTO_PATH: #{$PHOTO_PATH}<br>"
	puts "PHOTO_PATH_TMP: #{$PHOTO_PATH_TMP}<br>"
	puts "<hr>"
end


#### レシピのfigフラグ読み込み
# 通常
if code == ''
	r = mariadb( "SELECT code FROM #{$MYSQL_TB_MEAL} WHERE user='#{uname}';", false )
	code = r.first['code']
end


case command
when 'form'
	if slot == 'photo'
		5.times do |c|
			break if File.exist?( "#{$PHOTO_PATH}/#{code}-tn.jpg" )
			sleep( 2 )
		end
	end

	res = mariadb( "SELECT fig FROM #{$MYSQL_TB_MENU} WHERE user='#{uname}' AND code='#{code}';", false )

	if res.first
		fig = res.first['fig']
	else
		puts "No code."
		exit
	end

	# 写真ファイルと削除ボタン
	photo_file = "photo/no_image.png"
	photo_del_button = ''
	if fig == 1
		photo_file = "photo/#{code}-tn.jpg"
		photo_del_button = "<button class='btn btn-outline-danger' type='button' onclick=\"menu_photoDel_BWL3( '#{code}' )\">#{lp[1]}</button>"
	end

	html = ''
	html = <<-"HTML"
	<form class='row' method="post" enctype="multipart/form-data" id='photo_form'>
		<div class='col' align="center">
			<div class="form-group">
				<label for="photom">#{lp[2]}</label><br>
				<input type="file" name="photo1" id="photom" class="custom-control-file" onchange="menu_photoSave_BWL3( '#{code}' )">
			</div>
			<img src="#{photo_file}" width="200px" class="img-thumbnail"><br>
			<br>
			#{photo_del_button}
		</div>
	</form>
HTML
	puts html

#### 写真を保存
when 'upload'
	photo_name = cgi[slot].original_filename
	photo_type = cgi[slot].content_type
	photo_body = cgi[slot].read
	photo_size = photo_body.size.to_i

	if photo_size < $SIZE_MAX && ( photo_type == 'image/jpeg' || photo_type == 'image/jpg' )
		require 'rmagick'

		# 一時ファイルを作る
		f =open( "#{$PHOTO_PATH_TMP}/#{photo_name}", 'w' )
			f.puts photo_body
		f.close

		photo = Magick::ImageList.new( "#{$PHOTO_PATH_TMP}/#{photo_name}" )

		# 写真のサイズを変更
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

		# 写真の保存
		tns_file.write( "#{$PHOTO_PATH}/#{code}-tns.jpg" )
		tn_file.write( "#{$PHOTO_PATH}/#{code}-tn.jpg" )
		photo_file.write( "#{$PHOTO_PATH}/#{code}.jpg" )

		#一時ファイルの削除
		File.unlink "#{$PHOTO_PATH_TMP}/#{photo_name}"

		# 献立更新
		mariadb( "UPDATE #{$MYSQL_TB_MENU} SET fig=1 WHERE code='#{code}';", false )
	else
	end

#### 写真を削除
when 'delete'
	#写真ファイルの削除
	if File.exist?( "#{$PHOTO_PATH}/#{code}.jpg" )
		File.unlink "#{$PHOTO_PATH}/#{code}-tns.jpg"
		File.unlink "#{$PHOTO_PATH}/#{code}-tn.jpg"
		File.unlink "#{$PHOTO_PATH}/#{code}.jpg"

		# レシピデータベースの更新
		mariadb( "UPDATE #{$MYSQL_TB_MENU} SET fig='0' WHERE code='#{code}';", false )
	end
else
end
