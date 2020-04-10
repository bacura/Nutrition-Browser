#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser recipe photo 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171109, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'
require 'nkf'

#==============================================================================
#STATIC
#==============================================================================
script = 'photo'
$SIZE_MAX = 20000000
$TN_SIZE = 400
$TNS_SIZE = 40
$PHOTO_SIZE_MAX = 2000

$WM_FONT = 'さざなみゴシック'

@debug = false
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


#### POSTデータの取得
command = cgi['command']
code = cgi['code']
slot = cgi['slot']
slot_no = slot[-1]
if @debug
	puts "command: #{command}<br>"
	puts "code: #{code}<br>"
	puts "slot: #{slot}<br>"
	puts "slot_no: #{slot_no}<br>"
	puts "PHOTO_PATH: #{$PHOTO_PATH}<br>"
	puts "PHOTO_PATH_TMP: #{$PHOTO_PATH_TMP}<br>"
	puts "<hr>"
end


#### レシピのfigフラグ読み込み
# 通常
if code == ''
	r = mdb( "SELECT code FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
	code = r.first['code']
end


case command
when 'form'
	if slot_no == '0'
		5.times do |c|
			break if File.exist?( "#{$PHOTO_PATH}/#{code}-#{slot_no}tn.jpg" )
			sleep( 2 )
		end
	end

	r = mdb( "SELECT fig1, fig2, fig3 FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' AND code='#{code}';", false, @debug )
	if r.first
		fig1 = r.first['fig1']
		fig2 = r.first['fig2']
		fig3 = r.first['fig3']
	else
		puts "No code."
		exit
	end

	# 写真ファイルと削除ボタン
	photo_file = []
	photo_del_button = []
	if fig1 == 1
		photo_file[1] = "photo/#{code}-1tn.jpg"
		photo_del_button[1] = "<button class='btn btn-outline-danger' type='button' onclick=\"photoDel_BWL2( '1', '#{code}' )\">#{lp[1]}</button>"
	else
		photo_file[1] = "photo/no_image.png"
		photo_del_button[1] = ''
	end

	if fig2 == 1
		photo_file[2] = "photo/#{code}-2tn.jpg"
		photo_del_button[2] = "<button class='btn btn-outline-danger' type='button' onclick=\"photoDel_BWL2( '2', '#{code}' )\">#{lp[1]}</button>"
	else
		photo_file[2] = "photo/no_image.png"
		photo_del_button[2] = ''
	end

	if fig3 == 1
		photo_file[3] = "photo/#{code}-3tn.jpg"
		photo_del_button[3] = "<button class='btn btn-outline-danger' type='button' onclick=\"photoDel_BWL2( '3', '#{code}' )\">#{lp[1]}</button>"
	else
		photo_file[3] = "photo/no_image.png"
		photo_del_button[3] = ''
	end

	html = ''
	html = <<-"HTML"
	<form class='row' method="post" enctype="multipart/form-data" id='photo_form'>
		<div class='col' align="center">
			<div class="form-group">
				<label for="photo1">#{lp[2]}</label><br>
				<input type="file" name="photo1" id="photo1" class="custom-control-file" onchange="photoSave_BWL3( 'photo1', '#{code}' )">
			</div>
			<img src="#{photo_file[1]}" width="200px" class="img-thumbnail"><br>
			<br>
			#{photo_del_button[1]}
		</div>
		<div class='col' align="center">
			<div class="form-group">
				<label for="photo2">#{lp[3]}</label><br>
				<input type="file" name="photo2" id="photo2" class="custom-control-file" onchange="photoSave_BWL3( 'photo2', '#{code}' )">
			</div>
			<img src="#{photo_file[2]}" width="200px" class="img-thumbnail"><br>
			<br>
			#{photo_del_button[2]}
		</div>
		<div class='col' align="center">
			<div class="form-group">
				<label for="photo3">#{lp[4]}</label><br>
				<input type="file" name="photo3" id="photo3" class="custom-control-file" onchange="photoSave_BWL3( 'photo3', '#{code}' )">
			</div>
			<img src="#{photo_file[3]}" width="200px" class="img-thumbnail"><br>
			<br>
			#{photo_del_button[3]}
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

	# デバッグ用
	if @debug
		puts "tmp:#{$PHOTO_PATH_TMP}/#{photo_name}<br>"
		puts "photo:#{$PHOTO_PATH}/#{code}-#{slot_no}.jpg<br>"
		puts "tn:#{$PHOTO_PATH}/#{code}-#{slot_no}tn.jpg<br>"
		puts "tns:#{$PHOTO_PATH}/#{code}-#{slot_no}tns.jpg<br>"
		puts "<hr>"
	end

	if photo_size < $SIZE_MAX && ( photo_type == 'image/jpeg' || photo_type == 'image/jpg' )
		require 'rmagick'

		# 一時ファイルを作る
		f = open( "#{$PHOTO_PATH_TMP}/#{photo_name}", 'w' )
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
			photo_ratio = $PHOTO_SIZE_MAX / photo_x if photo_x >= $PHOTO_SIZE_MAX
		else
			tn_ratio = $TN_SIZE / photo_y
			tns_ratio = $TNS_SIZE / photo_y
			photo_ratio = $PHOTO_SIZE_MAX / photo_y if photo_y >= $PHOTO_SIZE_MAX
		end
		puts "Image magick resize" if @debug

		# サムネイル中のサイズ変更と保存
		tn_file = photo.thumbnail( tn_ratio )
		tn_file.write( "#{$PHOTO_PATH}/#{code}-#{slot_no}tn.jpg" )

		# サムネイル小のサイズ変更と保存
		tns_file = photo.thumbnail( tns_ratio )
		tns_file.write( "#{$PHOTO_PATH}/#{code}-#{slot_no}tns.jpg" )

		# 2Kサイズ変更と保存
		photo = photo.thumbnail( photo_ratio ) if photo_ratio != 1.0

		# ウォーターマーク合成
		wm_text = "BN2015 #{code} by #{user.name}"
#		wm_text = "食品成分表ブラウザ 2015\nPhoto by #{user.name} in #{#DATETIME.year}"
		wm_img = Magick::Image.new( photo.columns, photo.rows )
		wm_drew = Magick::Draw.new
		wm_drew.annotate( wm_img, 0, 0, 0, 0, wm_text ) do
			self.gravity = Magick::SouthWestGravity
			self.pointsize = 72
			self.font_family = $WM_FONT
			self.font_weight = Magick::BoldWeight
			self.stroke = "none"
		end
		wm_img = wm_img.shade( true, 315 )
		photo.composite!( wm_img, Magick::CenterGravity, Magick::HardLightCompositeOp )
		photo.write( "#{$PHOTO_PATH}/#{code}-#{slot_no}.jpg" )

		#一時ファイルの削除
		File.unlink "#{$PHOTO_PATH_TMP}/#{photo_name}"

		# レシピデータベースの更新
		mdb( "UPDATE #{$MYSQL_TB_RECIPE} SET fig#{slot_no}='1' WHERE code='#{code}';", false, @debug )
	end

#### 写真を削除
when 'delete'
	#写真ファイルの削除
	File.unlink "#{$PHOTO_PATH}/#{code}-#{slot_no}tns.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-#{slot_no}tns.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{code}-#{slot_no}tn.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-#{slot_no}tn.jpg" )
	File.unlink "#{$PHOTO_PATH}/#{code}-#{slot_no}.jpg" if File.exist?( "#{$PHOTO_PATH}/#{code}-#{slot_no}.jpg" )

	# レシピデータベースの更新
	mdb( "UPDATE #{$MYSQL_TB_RECIPE} SET fig#{slot_no}=0 WHERE code='#{code}';", false, @debug )
else
end

puts "	<div align='right' class='code'>#{code}</div>"
