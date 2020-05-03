#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser cutting board 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171026, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'cboard'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================
class Food
	def initialize( no, weight, unit, unitv, check, init, rr, ew )
		@no = no
		@weight = weight
		@unit = unit
		@unitv = unitv
		@check = check
		@init = init
		@rr = rr
		@ew = ew
	end

	def sum_load( food )
		t = food.split( ':' )
		@no = t[0]
		@weight = t[1]
		@unit = t[2]
		@unitv = t[3]
		@check = t[4]
		@init = t[5]
		if t[6] == nil || t[6] == ''
			@rr = 1.0
		elsif t[6].to_f > 1
			@rr = 1.0
		elsif t[6].to_f < 0
			@rr = 0.0
		else
			@rr = t[6]
		end
		@ew = t[7]
	end

	attr_accessor :no, :weight, :unit, :unitv, :check, :init, :rr, :ew
end

#### Easy weight calc
def weight_calc( food_list, dish_num )
	weight = BigDecimal( '0' )
	weight_checked = BigDecimal( '0' )

	check_all = true
	food_list.each do |e|
		check_all = false if e.check == '1'
	end

	food_list.each do |e|
		unless e.no == '-' || e.no == '+'
			weight += BigDecimal( e.weight.to_s )
			weight_checked +=  BigDecimal( e.weight.to_s ) if e.check == '1' || check_all
		end
	end
	weight = ( weight / dish_num.to_i ).to_i
	weight_checked = ( weight_checked / dish_num.to_i ).to_i

	return weight, weight_checked, check_all
end


#### Easy energy calc
def energy_calc( food_list, uname, dish_num )
	energy = BigDecimal( '0' )
	energy_checked = BigDecimal( '0' )

	check_all = true
	food_list.each do |e|
		check_all = false if e.check == '1'
	end

	food_list.each do |e|
		unless e.no == '-' || e.no == '+'
			q = "SELECT ENERC_KCAL from #{$MYSQL_TB_FCT} WHERE FN='#{e.no}';"
			q = "SELECT ENERC_KCAL from #{$MYSQL_TB_FCTP} WHERE FN='#{e.no}' AND ( user='#{uname}' OR user='#{$GM}' );" if /P|U/ =~ e.no
			r = mdb( q, false, @debug )
			t = convert_zero( r.first['ENERC_KCAL'] )
			energy += ( t * BigDecimal( e.weight.to_s ) / 100 )
			energy_checked += ( t * BigDecimal( e.weight.to_s ) / 100 ) if e.check == '1' || check_all
		end
	end
	energy = ( energy / dish_num.to_i ).to_i
	energy_checked = ( energy_checked / dish_num.to_i ).to_i

	return energy, energy_checked, check_all
end


#### Processing weight fraction
def proc_wf( weight )
	weight_ = BigDecimal( 0 )
	if weight <= 0.01
		weight_ = 0.01
	elsif weight >= 0.01 && weight < 0.10
		weight_ = weight.round( 2 )

	elsif weight >= 0.10 && weight < 0.5
		weight_ = weight.round( 2 )
	elsif weight >= 0.5 && weight < 1.0
		weight_ = weight.floor( 1 )
		t = weight - weight_
		if t >= 0.075
			weight_ += 0.1
		elsif t >= 0.025 && t > 0.075
			weight_ += 0.05
		end

	elsif weight >= 1.0 && weight < 5.0
		weight_ = weight.round( 1 )
	elsif weight >= 5 && weight < 10
		weight_ = weight.floor( 0 )
		t = weight - weight_
		if t >= 0.75
			weight_ += 1
		elsif t >= 0.25 && t > 0.75
			weight_ += 0.5
		end

	elsif weight >= 10 && weight < 50
		weight_ = weight.round( 0 )
	elsif weight >= 50 && weight < 100
		weight_ = weight.floor( -1 )
		t = weight - weight_
		if t >= 7.5
			weight_ += 10
		elsif t >= 2.5 && t > 7.5
			weight_ += 5
		end

	elsif weight >= 100 && weight < 500
		weight_ = weight.round( -1 )
	elsif weight >= 500
		weight_ = weight.floor( -2 )
		t = weight - weight_
		if t >= 75
			weight_ += 100
		elsif t >= 25 && t > 75
			weight_ += 50
		end
	end

	return weight_
end

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
order = cgi['order']
dish_num = cgi['dish_num']
food_init_ = cgi['food_init']
food_rr_ = cgi['food_rr']
option1 = cgi['option1']
option2 = cgi['option2']
option3 = cgi['option3']
code = cgi['code']
if @debug
	puts "command:#{command}<br>"
	puts "code:#{code}<br>"
	puts "order:#{order}<br>"
	puts "dish_num:#{dish_num}<br>"
	puts "food_init_:#{food_init_}<br>"
	puts "food_rr_:#{food_rr_}<br>"
	puts "opt1:#{option1}<br>"
	puts "opt2:#{option2}<br>"
	puts "opt3:#{option3}<br>"
	puts "<hr>"
end


#### CBの読み込み
q = "SELECT code, name, sum, dish, protect from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';"
q = "SELECT code, name, sum, dish, protect from #{$MYSQL_TB_RECIPE} WHERE code='#{code}';" if command == 'load'
r = mdb( q, false, @debug )


code = r.first['code']
recipe_name = r.first['name']
dish_num = r.first['dish'].to_i if dish_num == '' || dish_num == nil
dish_num = 1 if dish_num == 0
protect = r.first['protect'].to_i
sum = r.first['sum']
if @debug
	puts "code:#{code}<br>"
	puts "recipe_name:#{recipe_name}<br>"
	puts "dish_num:#{dish_num}<br>"
	puts "protect:#{protect}<br>"
	puts "sum:#{sum}<br>"
	puts "<hr>"
end


#### 食品と付随成分の抽出
food_list = []
if sum
	sum.split( "\t" ).each do |e|
		t = Food.new( nil, nil, nil, nil, nil, nil, nil, nil )
		t.sum_load( e )
		food_list << t
	end
end


update = ''
all_check = ''
case command
# リストから食品を削除
when 'clear'
	# まとめて削除
	if option1 == 'all'
		food_list = []
		recipe_name = ''
		code = ''
		dish_num = 1
	# 1つずつ削除
	else
		food_list.delete_at( order.to_i )
		update = '*'
	end

# 食品の順番を１つ上げる
when 'upper'
	if order.to_i == 0
		t = food_list.shift
		food_list << t
	else
		t = food_list.delete_at( order.to_i )
		food_list.insert( order.to_i - 1, t )
	end
	update = '*'

# 食品の順番を１つ下げる
when 'lower'
	if order.to_i == food_list.size - 1
		t = food_list.pop
		food_list.unshift( t )
	else
		t = food_list.delete_at( order.to_i )
		food_list.insert( order.to_i + 1, t )
	end
	update = '*'

#### 食品の重量の変更
when 'weight'
	order_no = order.to_i
	unit_value = BigDecimal( 0 )
	food_list[order_no].unit = option3
	food_list[order_no].init = food_init_
	food_list[order_no].rr = food_rr_
	food_weight, unit_value = food_weight_check( option2 )
	food_list[order_no].unitv = food_weight

	# 食品ごとの単位読み込み
	r = mdb( "SELECT unitc from #{$MYSQL_TB_EXT} WHERE FN='#{food_list[order_no].no}';", false, @debug )
	uk = BigDecimal( '1' )
	if food_list[order_no].unit.to_i == 1
		# カロリー換算
		puts 'カロリー' if @debug
		rr = mdb( "SELECT ENERC_KCAL FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_list[order_no].no}';", false, @debug )
		if rr.first['ENERC_KCAL']
			uk = BigDecimal( '100' ) / rr.first['ENERC_KCAL']
		end
	elsif food_list[order_no].unit.to_i == 15
		# 廃棄前g
		puts '廃棄前g' if @debug
		rr = mdb( "SELECT REFUSE FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_list[order_no].no}';", false, @debug )
		if rr.first['REFUSE']
			uk = BigDecimal(( 100 - rr.first['REFUSE'].to_i ).to_s ) / 100
		end
	elsif r.first['unitc']
		# 単位変換
		puts 'その他' if @debug
		a = r.first['unitc'].split( ':' )
		t = a[food_list[order_no].unit.to_i]
		t = '1' if t == ''
		uk = BigDecimal( t )
	end

	# 換算重量の小数点処理
	food_list[order_no].weight = unit_value * uk
	if food_list[order_no].weight >= 10
		food_list[order_no].weight = food_list[order_no].weight.round( 0 ).to_i
	elsif food_list[order_no].weight >= 1
		food_list[order_no].weight = food_list[order_no].weight.round( 1 ).to_f
	else
		food_list[order_no].weight = food_list[order_no].weight.round( 2 ).to_f
	end

	# 調理後重量の小数点処理
	food_list[order_no].ew = BigDecimal( food_list[order_no].weight.to_s ) * BigDecimal( food_list[order_no].rr.to_s )
	if food_list[order_no].ew >= 10
		food_list[order_no].ew = food_list[order_no].ew.round( 0 ).to_i
	elsif food_list[order_no].ew >= 1
		food_list[order_no].ew = food_list[order_no].ew.round( 1 ).to_f
	else
		food_list[order_no].ew = food_list[order_no].ew.round( 2 ).to_f
	end
	update = '*'

#### 食品番号による食品の追加、または空白の追加
when 'add'
	option1 = '' if option1 == nil
	option1.gsub!( /　+/, ' ' )
	option1.gsub!( /\s+/, ' ' )
	option1.tr!( "０-９", "0-9" ) if /[０-９]/ =~ option2
	option1.sub!( '．', '.')
	p option1 if @debug

	t = option1.split( ' ' )
	add_food_no = t[0]
	add_food_weight = 100
	add_food_weight = t[1] unless t[1] == nil
	add_food_weight = 100 unless /[0-9\.]+/ =~ t[1]
	add_food_no = '00000' if add_food_no == '0'
	p add_food_no if @debug

	insert_posi = 0
	check_flag = false
	food_list.size.times do |c|
		if food_list[c].check == "1"
			insert_posi = c
			check_flag = true
		end
	end
	insert_posi = food_list.size - 1 unless check_flag
	food_list_ = []
	0.upto( insert_posi ) do |c| food_list_ << food_list[c] end

	if add_food_no == nil
		food_list_ << Food.new( '-', '-', '-', '-', 0, '-', '-', '-' )
	elsif /\d{5}/ =~ add_food_no
		r = mdb( "SELECT FN from #{$MYSQL_TB_TAG} WHERE FN='#{add_food_no}';", false, @debug )
		food_list_ << Food.new( add_food_no, add_food_weight, '0', add_food_weight, '0', '', '1.0', add_food_weight ) if r.first
	elsif /[PU]?\d{5}/ =~ add_food_no
		r = mdb( "SELECT FN from #{$MYSQL_TB_TAG} WHERE FN='#{add_food_no}' AND (( user='#{user.name}' AND public!='#{2}' ) OR public='1' );", false, @debug )
		food_list_ << Food.new( add_food_no, add_food_weight, '0', add_food_weight, '0', '', '1.0', add_food_weight ) if r.first
	else
		food_list_ << Food.new( '+', '-', '-', '-', '0', add_food_no, '-', '-' )
	end

	if check_flag
		insert_posi += 1
		insert_posi.upto( food_list.size - 1 ) do |c| food_list_ << food_list[c] end
	end
	food_list = food_list_

	update = '*'


#### 食品チェックボックススの更新
when 'check_box'
	order_no = order.to_i
	check_status = option2
	food_list[order_no].check = check_status


#### Switching all check box
when 'allSwitch'
	allSwitch = cgi['allSwitch']
	puts "allSwitch:#{allSwitch}<br>" if @debug

	food_list.size.times do |c|
		food_list[c].check = allSwitch
	end
	all_check = 'CHECKED' if allSwitch == '1'

#### 皿数の更新
when 'dish'
	dish_num = 1 if dish_num == nil || dish_num == ''
	dish_num = 1 unless dish_num =~ /\d+/
	dish_num.tr!( "０-９", "0-9" ) if /[０-９]/ =~ dish_num.to_s
	update = '*'


#### レシピデータのクイック保存
when 'quick_save'
	 mdb( "UPDATE #{$MYSQL_TB_RECIPE} SET sum='#{sum}', date='#{$DATETIME}', dish='#{dish_num}' WHERE user='#{user.name}' and code='#{code}';", false, @debug )


#### GN変換
when 'gn_exchange'
	c = 0
	food_list.each do |e|
		unless e.no == '-' || e.no == '+'
			weight_gn = proc_wf( BigDecimal( e.weight ) / dish_num )
			food_list[c].weight = weight_gn
			food_list[c].unit = '0'
			food_list[c].unitv = weight_gn
			food_list[c].ew = weight_gn * BigDecimal( e.rr )
		end
		c += 1
	end
	dish_num = 1
	update = '*'

#### 調味％
when 'seasoning'
	seasoning = cgi['seasoning']
	puts "seasoning:#{seasoning}<br>" if @debug

	total_weight = BigDecimal( 0 )
	target_weight = BigDecimal( 0 )
	food_list.each do |e|
		unless e.no == '-' || e.no == '+'
			if e.check == '1'
				target_weight += BigDecimal( e.weight )
			end
			total_weight += BigDecimal( e.weight )
		end
	end
	target_weight = total_weight if target_weight == 0
	seasoning_rate = target_weight / 100

	r = mdb( "SELECT sum from #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' AND code='#{seasoning}';", false, @debug )
	if r.first
		 r.first['sum'].split( "\t" ).each do |e|
			t = Food.new( nil, nil, nil, nil, nil, nil, nil, nil )
			t.sum_load( e )
			t.weight = BigDecimal( t.weight ) * seasoning_rate
			t.unitv = t.weight
			t.ew = t.weight * BigDecimal( t.rr )
			food_list << t
		end
	end
	update = '*'


#### Adjusting tootal food weight
when 'wadj'
	weight_adj = cgi['weight_adj'].to_i
	puts "weight_adj:#{weight_adj}<br>" if @debug

	weight_ctrl, weight_checked, check_all = weight_calc( food_list, dish_num )
#	break if ( weight_ctrl - weight_checked ) < 10
	wadj_rate = BigDecimal( weight_adj - ( weight_ctrl - weight_checked )) / ( weight_checked )
	food_list.size.times do |c|
		if ( food_list[c].check == '1' || check_all ) && food_list[c].weight != '-' && food_list[c].weight != '+'
			food_list[c].weight = proc_wf( BigDecimal( food_list[c].weight ) * wadj_rate )
			food_list[c].unitv = proc_wf( BigDecimal( food_list[c].unitv ) * wadj_rate )
			food_list[c].ew = proc_wf( BigDecimal( food_list[c].ew ) * wadj_rate )
		end
	end
	update = '*'


#### Adjusting tootal food energy
when 'eadj'
	energy_adj = cgi['energy_adj'].to_i
	puts "energy_adj:#{energy_adj}<br>" if @debug

	energy_ctrl, energy_checked, check_all = energy_calc( food_list, user.name, dish_num )
#	break if ( energy_ctrl - energy_checked ) < 10
	eadj_rate = BigDecimal( energy_adj - ( energy_ctrl - energy_checked )) / ( energy_checked )
	food_list.size.times do |c|
		if food_list[c].check == '1' || check_all && food_list[c].weight != '-' && food_list[c].weight != '+'
			food_list[c].weight = proc_wf( BigDecimal( food_list[c].weight ) * eadj_rate )
			food_list[c].unitv = proc_wf( BigDecimal( food_list[c].unitv ) * eadj_rate )
			food_list[c].ew = proc_wf( BigDecimal( food_list[c].ew ) * eadj_rate )
		end
	end
	update = '*'


#### Adjusting feeding rate by food loss
when 'ladj'
	loss_adj = cgi['loss_adj'].to_i
	puts "loss_adj:#{loss_adj}<br>" if @debug

	weight_ctrl, weight_checked = weight_calc( food_list, dish_num )
	ladj_rate = ( BigDecimal( weight_checked - loss_adj ) / ( weight_checked )).round( 2 ).to_f
	food_list.size.times do |c|
		if food_list[c].weight != '-' && food_list[c].weight != '+'
			if food_list[c].check == '1'
				food_list[c].rr = ladj_rate
				food_list[c].ew = BigDecimal( food_list[c].weight ) * ladj_rate
			else
				food_list[c].rr = "1.0"
				food_list[c].ew = food_list[c].weight
			end
		end
	end
	update = '*'
end


#### 更新チェック
update = '' if recipe_name == ''
if @debug
	puts "update:#{update}<br>"
	puts "<hr>"
end


#### Getting food weight & food energy
weight_ctrl, weight_checked = weight_calc( food_list, dish_num )
energy_ctrl, energy_checked = energy_calc( food_list, user.name, dish_num )
weitht_adj = weight_ctrl if weitht_adj == 0
energy_adj = energy_ctrl if energy_adj == 0


#### CBタグの読み込み
food_tag = []
db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )
if false
	food_list.each do |e|
		q = "SELECT Tagnames from #{$MYSQL_TB_FCT} WHERE FN='#{e.no}';"
		r = db.query( q )
		if r.first
			food_tag << r.first['Tagnames']
		end
		food_tag << '' if e.no == '-' || e.no == '+'
	end
else
	food_list.each do |e|
		q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e.no}';"
		q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e.no}' AND user='#{user.name}';" if /^U\d{5}/ =~ e.no
		r = db.query( q )
		food_tag << bind_tags( r ) if r.first
		food_tag << '' if e.no == '-' || e.no == '+'
	end
end
db.close


#### 調味％セット
seasoning_html = ''
r = mdb( "SELECT code, name FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' and role='100';", false, @debug )
seasoning_html << "<div class='input-group input-group-sm'>"
seasoning_html << "<div class='input-group-prepend'>"
seasoning_html << "<label class='input-group-text' for='seasoning'>#{lp[6]}</label>"
seasoning_html << "</div>"
seasoning_html << "<select class='form-control form-control-sm' id='seasoning'>"
r.each do |e|
	seasoning_html << "<option value='#{e['code']}'>#{e['name']}</option>"
end
seasoning_html << "</select>"
seasoning_html << "<div class='input-group-append'>"
seasoning_html << "<button type='button' class='btn btn-outline-primary btn-sm' onclick=\"seasoningAdd_BWL1( '#{code}' )\">#{lp[7]}</button>"
seasoning_html << "</div>"
seasoning_html << "</div>"


#### Sasshi button
html_sasshi = ''
html_sasshi = "<button class='btn btn-outline-light btn-sm' type='button' onclick=\"\">#{lp[28]}</button>" if user.status >= 3


#### 新しいまな板表示
html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-8'>
			<h5>#{lp[1]}: #{update}#{recipe_name}</h5>
		</div>
		<div class='col-2'>
			<div class='input-group input-group-sm'>
				<div class="input-group-prepend">
					<label class="input-group-text" for="dish_num">#{lp[2]}</label>
				</div>
  				<input type="number" min='1' class="form-control" id="dish_num" value="#{dish_num}" onchange=\"dishCB( '#{code}' )\">
				<div class="input-group-append">
	        		<button class='btn btn-outline-primary' type='button' onclick=\"dishCB( '#{code}' )\">#{lp[3]}</button>
	        	</div>
			</div>
		</div>
		<div class='col-2' align='center'>
			<input type='checkbox' id='all_check'>&nbsp;
			<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"clear_BWL1( 'all', '#{code}' )\">#{lp[8]}</button>
		</div>
	</div>

	<div class='row'>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<div class="input-group-prepend">
					<label class="input-group-text" for="food_add">#{lp[4]}</label>
				</div>
  				<input type="text" class="form-control" maxlength='12' placeholder="00000 100" id="food_add">
				<div class="input-group-append">
	        		<button class='btn btn-outline-primary' type='button' onclick=\"recipeAdd_BWL1( '#{code}' )\">#{lp[5]}</button>
        		</div>
			</div>
		</div>
		<div class='col-5'>
			#{seasoning_html}
		</div>
		<div class='col-1'>
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<div class="input-group-prepend">
					<label class="input-group-text" for="weight_ctrl">#{lp[25]}</label>
				</div>
  				<input type="number" min='1' class="form-control" id="weight_adj" value="#{weight_ctrl}">
				<div class="input-group-append">
	        		<button class='btn btn-outline-primary' type='button' onclick=\"weightAdj( '#{code}' )\">#{lp[27]}</button>
	        	</div>
			</div>
		</div>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<div class="input-group-prepend">
					<label class="input-group-text" for="energy_ctrl">#{lp[26]}</label>
				</div>
  				<input type="number" min='1' class="form-control" id="energy_adj" value="#{energy_ctrl}">
				<div class="input-group-append">
	        		<button class='btn btn-outline-primary' type='button' onclick=\"energyAdj( '#{code}' )\">#{lp[27]}</button>
	        	</div>
			</div>
		</div>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<div class="input-group-prepend">
					<label class="input-group-text" for="energy_ctrl">#{lp[29]}</label>
				</div>
  				<input type="number" min='0' class="form-control" id="loss_adj" value="0">
				<div class="input-group-append">
	        		<button class='btn btn-outline-primary' type='button' onclick=\"lossAdj( '#{code}' )\">#{lp[27]}</button>
	        	</div>
			</div>
		</div>
		<div class='col-1'>
	        #{html_sasshi}
		</div>
		<div class='col-2'>
			<input type='checkbox' id='gn_check'>&nbsp;
			<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"gnExchange( '#{code}' )\">#{lp[22]}</button>
		</div>
	</div>
	<hr>

<div class='row cb_header'>
	<div class='col-2'>#{lp[9]}</div>
	<div class='col-1'><input type='checkbox' id='switch_all' #{all_check} onclick=\"allSwitch( '#{code}' )\">&nbsp;#{lp[10]}</div>
	<div class='col-3'>#{lp[11]}</div>
	<div class='col-3'>
  		<div class='row'>
			<div class='col-6'>#{lp[12]}</div>
			<div class='col-3'>#{lp[13]}</div>
			<div class='col-3'>#{lp[14]}</div>
		</div>
	</div>
	<div class='col-3'>
  		<div class='row'>
			<div class='col-3'>#{lp[15]}</div>
			<div class='col-4'>#{lp[16]}</div>
			<div class='col-3'>#{lp[17]}</div>
		</div>
	</div>
</div>
<br>
HTML

c = 0
food_list.each do |e|
	p e.no if @debug

	# フードチェック
	if e.check == '1'
		check = 'CHECKED'
	else
		check = ''
	end

	# 単位の生成と選択
  	unless e.no == '-' || e.no == '+'
		unit_set = []
		unit_select = []
		r = mdb( "SELECT unitc FROM #{$MYSQL_TB_EXT} WHERE FN='#{e.no}';", false, @debug )
		unless r.first['unitc'] == nil
			t = r.first['unitc'].split( ':' )
#### Temporary
			if t.size == 14
				t << '0.0'
				t << ''
			end

			t.size.times do |cc|
				unless t[cc] == '0.0'
					unit_set << cc
					if cc == e.unit.to_i
						unit_select << 'SELECTED'
					else
						unit_select << ''
					end
				end
			end
		else
			unit_set = [ 0, 1, 15 ]
			if e.unit == '15'
				unit_select = [ '', '', 'SELECTED' ]
			elsif e.unit == '1'
				unit_select = [ '', 'SELECTED', '' ]
			else
				unit_select = [ 'SELECTED', '', '' ]
			end
		end
	end

	# フードキーの生成
	food_key = ''
  	unless e.no == '-' || e.no == '+'
  		q = "SELECT * FROM #{$MYSQL_TB_TAG} WHERE FN='#{e.no}';"
		q = "SELECT * from #{$MYSQL_TB_TAG} WHERE FN='#{e.no}' AND user='#{user.name}';" if /^U\d{5}/ =~ e.no
		r = mdb( q, false, @debug )

		if r.first
			food_key = "#{r.first['FG']}:#{r.first['class1']}:#{r.first['class2']}:#{r.first['class3']}:#{r.first['name']}"
		end
	end

	html << "<div class='row'>"
 	html << "	<div class='col-2'>"
 	html << " 		<button type='button' class='btn btn-outline-danger btn-sm del_button' onclick=\"clear_BWL1( '#{c}', '#{code}' )\">X</button>&nbsp;&nbsp;"
 	html << "		<button type='button' class='btn btn-outline-primary btn-sm ctl_button' onclick=\"upper_BWL1( '#{c}', '#{code}' )\">↑</button>"
 	html << "		<button type='button' class='btn btn-outline-primary btn-sm ctl_button' onclick=\"lower_BWL1( '#{c}', '#{code}' )\">↓</button>"
 	html << "	</div>"

 	if e.no == '-'
		html << "<div class='col-10'><hr></div>"
 	elsif e.no == '+'
		html << "<div class='col-3 text-secondary cb_food_label'>#{e.init}</div>"
		html << "<div class='col-7'><hr></div>"
  	else

	  	html << "	<div class='col-1 fct_value'><input class='form-check-input' type='checkbox' id='food_cb#{c}' onchange=\"checkCB_BWL1( '#{c}', '#{code}', 'food_cb#{c}' )\" #{check}>#{e.no}</div>"
  		html << "	<div class='col-3 fct_value' onclick=\"cb_summonBWL5( '#{food_key}', '#{e.weight}', '#{e.no}' )\">#{food_tag[c]}</div>"
  		html << "	<div class='col-3'>"
  		html << "		<div class='form-group form-row cb_form'>"
  		html << "			<div class='col-6'><input type='text'  maxlength='8' class='form-control form-control-sm' id='food_init_#{c}' value='#{e.init}' onchange=\"initCB_SS( '#{c}', 'unitv_#{c}', 'unit_#{c}', 'food_init_#{c}', 'food_rr_#{c}', '#{code}' )\"></div>"
  		html << "			<div align='right' class='col-3 fct_value'>#{e.weight.to_f}</div>"
  		html << "			<div align='right' class='col-3 fct_value'>#{e.ew.to_f}</div>"
		html << "		</div>"
		html << "	</div>"
  		html << "	<div class='col-3'>"
  		html << "		<div class='form-group form-row cb_form'>"
  		if /\// =~ e.unitv.to_s
  			html << "			<div class='col-3'><input type='text' maxlength='5' class='form-control form-control-sm' id='unitv_#{c}' value='#{e.unitv}' onchange=\"weightCB_BWL1( '#{c}', 'unitv_#{c}', 'unit_#{c}', 'food_init_#{c}', 'food_rr_#{c}', '#{code}' )\"></div>"
  		else
  			html << "			<div class='col-3'><input type='text' maxlength='5' class='form-control form-control-sm' id='unitv_#{c}' value='#{e.unitv.to_f}' onchange=\"weightCB_BWL1( '#{c}', 'unitv_#{c}', 'unit_#{c}', 'food_init_#{c}', 'food_rr_#{c}', '#{code}' )\"></div>"
  		end
  		html << "			<div class='col-4'><select class='form-control form-control-sm' id='unit_#{c}' onchange=\"weightCB_BWL1( '#{c}', 'unitv_#{c}', 'unit_#{c}', 'food_init_#{c}', 'food_rr_#{c}', '#{code}' )\">"
  		unit_set.size.times do |cc|
  			html << "				<option value='#{unit_set[cc]}' #{unit_select[cc]}>#{$UNIT[unit_set[cc]]}</option>"
  		end
		html << "				</select>"
		html << "			</div>"
  		html << "			<div class='col-3'><input type='text' maxlength='3' class='form-control form-control-sm' id='food_rr_#{c}' value='#{e.rr}' onchange=\"weightCB_BWL1( '#{c}', 'unitv_#{c}', 'unit_#{c}', 'food_init_#{c}', 'food_rr_#{c}', '#{code}' )\"></div>"
		html << "		</div>"
		html << "	</div>"
	end
	html << "</div>"
	c += 1
end

html << "	<br>"
html << "<div class='row'>"
html << "	<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"recipeEdit_BWL2( 'view', '#{code}' )\">#{lp[18]}</button></div>"
html << "	<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"calcView_BWL2( '#{code}' )\">#{lp[19]}</button></div>"

if recipe_name != '' && update == ''
	html << "	<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"priceView_BWL2( '#{code}' )\">#{lp[20]}</button></div>" if recipe_name != '' && update == ''
else
	html << "	<div class='col-2'><button type='button' class='btn btn-secondary btn-sm'\">#{lp[20]}</button></div>"
end

html << "	<div class='col-2'><button type='button' class='btn btn-primary btn-sm' onclick=\"luckyInput_BWL2()\">#{lp[21]}</button></div>"

html << "<div class='col-2'>"
html <<	"		<button class='btn btn-primary btn-sm' onclick='Pseudo_R2F_BWL3(\"#{code}\")'>#{lp[24]}</button>"
html << "</div>"

#### Quick保存
if recipe_name == '' || protect == 1
	html << "	<div class='col-2'></div>"
else
	html << "	<div class='col-2'><button type='button' class='btn btn-outline-danger btn-sm' onclick=\"quickSave( '#{code}' )\">#{lp[23]}</button></div>"
end

html << "</div>"
html << "<div class='code'>#{code}</div>"
html << "</div>"

puts html
#### まな板データ更新
sum_new = ''
food_list.each do |e| sum_new << "#{e.no}:#{e.weight}:#{e.unit}:#{e.unitv}:#{e.check}:#{e.init}:#{e.rr}:#{e.ew}\t" end
sum_new.chop!

mdb( "UPDATE #{$MYSQL_TB_SUM} set code='#{code}', name='#{recipe_name}', sum='#{sum_new}', dish='#{dish_num}', protect='#{protect}' WHERE user='#{user.name}';", false, @debug )
