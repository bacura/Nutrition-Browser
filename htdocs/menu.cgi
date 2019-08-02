#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser menu 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171105, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'menu.cgi'
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
lp = lp_init( 'menu', language )
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
menu_name = cgi['menu_name']
public_bit = cgi['public'].to_i
protect = cgi['protect'].to_i
label = cgi['label']
new_label = cgi['new_label']
fig = 0
if $DEBUG
	puts "commnad:#{command}<br>"
	puts "code:#{code}<br>"
	puts "menu_name:#{menu_name}<br>"
	puts "public_bit:#{public_bit}<br>"
	puts "protect:#{protect}<br>"
	puts "<hr>"
end


case command
#### 献立の表示
when 'view'
	if code == ''
		# 献立データベースの仮登録チェック
  		r = mariadb( "SELECT code FROM #{$MYSQL_TB_MENU} WHERE user='#{uname}' AND name='' AND code!='';", false )
  		code = r.first['code'] if r.first
  		unless r.first
		  	# 献立データベースに仮登録
			code = generate_code( uname, 'm' )
		  	mariadb( "INSERT INTO #{$MYSQL_TB_MENU} SET code='#{code}', user='#{uname}',public=0, name='', meal='';", false )
  		end

  		# 食事データベースへ反映
		mariadb( "UPDATE #{$MYSQL_TB_MEAL} SET code='#{code}' WHERE user='#{uname}';", false )
  	end

	# 献立の読み込み
	r = mariadb( "SELECT * from #{$MYSQL_TB_MENU} WHERE user='#{uname}' and code='#{code}';", false )
	if r.first
		public_bit = r.first['public'].to_i
		protect = r.first['protect'].to_i
		label = r.first['label']
		fig = r.first['fig'].to_i
	end

	# リセットネーム処理
	r = mariadb( "SELECT name from #{$MYSQL_TB_MEAL} WHERE user='#{uname}';", false )
	menu_name = r.first['name']


#### 献立の保存
when 'save'
	r = mariadb( "SELECT name, meal from #{$MYSQL_TB_MEAL} WHERE user='#{uname}';", false )
	meal = r.first['meal']
	meal_name = r.first['name']
	p meal if $DEBUG

	label = new_label unless new_label == ''

	# レシピ名の確認
	unless meal_name == ''
		r = mariadb( "SELECT code from #{$MYSQL_TB_MENU} WHERE user='#{uname}' and code='#{code}' and name='#{menu_name}';", false )

		# 名前が一致しなければ、新規コードとメニューを登録
		# バグに近い仕様：名前を変えて新規コードになるけど、写真はコピーされない
		unless r.first
			code = generate_code( uname, 'm' )
	  		mariadb( "INSERT INTO #{$MYSQL_TB_MENU} SET code='#{code}', user='#{uname}';", false )
		end
	end

	# 上書き保存
	mariadb( "UPDATE #{$MYSQL_TB_MENU} SET name='#{menu_name}', public='#{public_bit}', protect='#{protect}', meal='#{meal}', label='#{label}', date='#{Time.now}' WHERE user='#{uname}' and code='#{code}';", false )
	mariadb( "UPDATE #{$MYSQL_TB_MEAL} SET name='#{menu_name}', code='#{code}' WHERE user='#{uname}';", false )
end


# 公開チェック
p public_bit if $DEBUG
check_public = ''
check_public = 'CHECKED' if public_bit == 1


# 保護チェック
p protect if $DEBUG
check_protect = ''
check_protect = 'CHECKED' if protect == 1


# 写真ファイルと削除ボタン
photo_file = "no_image.png"
photo_del_button = ''
if fig == 1
	photo_file = "photo/#{code}-tn.jpg"
	photo_del_button = "<button class='btn btn-outline-danger' type='button' onclick=\"menu_photoDel_BWL2( '#{code}' )\">#{lp[1]}削除</button>"
end


# ラベル抽出とhtml
r = mariadb( "SELECT label from #{$MYSQL_TB_MENU} WHERE user='#{uname}';", false )
label_list = []
r.each do |e| label_list << e['label'] end
label_list.uniq!

html_label = '<select class="form-control form-control-sm" id="label">'
label_list.each do |e|
	if e == nil
		html_label << "<option value='#{lp[2]}'>#{lp[2]}</option>"
	elsif label == e
		html_label << "<option value='#{e}' SELECTED>#{e}</option>"
	else
		html_label << "<option value='#{e}'>#{e}</option>"
	end
end
html_label << '</select>'


#### レシピフォームの表示
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-2'><h5>#{lp[3]}</h5></div>
		<div class="col-2">
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="public" #{check_public}> #{lp[4]}
  				</label>
			</div>
			<div class="form-check form-check-inline">
  				<label class="form-check-label">
    				<input class="form-check-input" type="checkbox" id="protect" #{check_protect}> #{lp[5]}
  				</label>
			</div>
		</div>
		<div class="col-6">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="menu_name">#{lp[6]}</label>
				</div>
      			<input type="text" class="form-control" id="menu_name" value="#{menu_name}" required>
				<div class="input-group-append">
      				<button class="btn btn-outline-primary" type="button" onclick="menuSave_BWL2( '#{code}' )">#{lp[7]}</button>
				</div>
    		</div>
    	</div>
    	<div class="col-1">
    	</div>
    	<div class="col-1">
      		<button class="btn btn-sm btn-outline-warning" type="button" onclick="">#{lp[8]}</button>
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
		<div class="col-5">
			<div class="input-group input-group-sm">
				<div class="input-group-prepend">
					<label class="input-group-text" for="menu_name">#{lp[10]}</label>
				</div>
      			<input type="text" class="form-control" id="new_label" value="">
	   		</div>
    	</div>
	</div>

	<div align='right' class='code'>#{code}</div>
</div>
HTML

puts html
