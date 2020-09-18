#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser detail viewer 0.00

#==============================================================================
# CHANGE LOG
#==============================================================================
#20171006, 0.00a, start


#==============================================================================
# LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
# STATIC
#==============================================================================
@debug = false
script = 'detail'


#==============================================================================
# DEFINITION
#==============================================================================
#### 端数処理の設定
def frct_check( frct_mode )
	frct_mode = 1 if frct_mode == nil
	fs = []
	0.upto( 3 ) do |c|
		if frct_mode.to_i == c
			fs << 'selected'
		else
			fs << ''
		end
	end

	return frct_mode, fs
end


#### 検索インデックスの飛ばし処理
def sid_skip( sid, dir )
	r = []
	c = 0
	until r.first
		if dir == 'fwd'
			sid = sid.to_i + 1
			sid = 1 if sid > 2198
		else
			sid = sid.to_i - 1
			sid = 2198 if sid < 1
		end
		r = mdb( "SELECT FN, SID FROM #{$MYSQL_TB_TAG} WHERE SID='#{sid}';", false, @debug )
		c += 1
		break if c > 10
	end
	food_no = r.first['FN']

	return food_no
end

#==============================================================================
# Main
#==============================================================================

html_init( nil )

cgi = CGI.new
user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### GETデータの取得
get_data = get_data()
frct_mode = get_data['frct_mode']
food_weight = CGI.unescape( get_data['food_weight'] ) if get_data['food_weight'] != '' && get_data['food_weight'] != nil
food_no = get_data['food_no']
dir = get_data['dir']
sid = get_data['sid']
sid_flag = true if sid
if @debug
	puts "frct_mode: #{frct_mode}<br>"
	puts "food_weight: #{food_weight}<br>"
	puts "food_no: #{food_no}<br>"
	puts "dir: #{dir}<br>"
	puts "sid: #{sid}<br>"
	puts "<hr>"
end


#### 食品重量の決定
food_weight = BigDecimal( food_weight_check( food_weight ).first )


#### 端数処理の設定
frct_mode, frct_select = frct_check( frct_mode )


#### 検索インデックスの処理
food_no = sid_skip( sid, dir ) if sid


#### 全ての栄養素を取得
fct_opt = Hash.new
r = mdb( "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_no}';", false, @debug )
sid = r.first['SID']
food_no = r.first['FN']
$FCT_ITEM.each do |e| fct_opt[e] = num_opt( r.first[e], food_weight, frct_mode, $FCT_FRCT[e] ) end


#### 追加ボタンの生成
add_button = ''
add_button = "<spqn onclick=\"addingCB( '#{food_no}', 'detail_weight' )\">#{lp[1]}</span>" if user.name


#### 検索キーの生成
search_key = ''
r = mdb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{food_no}';", false, @debug )
food_name = r.first['name']

r = mdb( "SELECT alias FROM #{$MYSQL_TB_DIC} WHERE org_name='#{food_name}';", false, @debug )
r.each do |e| search_key << "#{e['alias']}," end
search_key.chop!


#### 別名リクエストボタンの生成
alias_button = ''
if user.status > 0
	alias_button << '<div class="input-group input-group-sm">'
	alias_button << "<label class='input-group-text' for='alias'>#{lp[3]}</label>"
	alias_button <<	'<input type="text" class="form-control" id="alias">'
	alias_button <<	"<div class='input-group-prepend'><button class='btn btn-outline-primary' type='button' onclick=\"aliasRequest( '#{food_no}' )\">#{lp[4]}</button></div>"
	alias_button << '</div>'
end


#### html部分
html = <<-"HTML"
<div class='container-fluid'>
	<div class="row">
		<div class="col-2" align='center'>
			<span class='h6'>#{lp[5]}：#{food_no}<br>
			<span onclick="detailPage( 'rev', '#{sid}' )">#{lp[7]}</span>
			#{lp[6]}：#{sid}</span>
			<span onclick="detailPage( 'fwd', '#{sid}' )">#{lp[8]}</span>
		</div>
	  	<div class="col-2"><h5>#{food_weight.to_f} g</h5></div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="detail_fraction">#{lp[9]}</label>
				<select class="form-select form-select-sm" id="detail_fraction" onchange="detailWeight( '#{food_no}' )">
					<option value="1"#{frct_select[1]}>#{lp[10]}</option>
					<option value="2"#{frct_select[2]}>#{lp[11]}</option>
					<option value="3"#{frct_select[3]}>#{lp[12]}</option>
				</select>
			</div>
		</div>
		<div class="col-2">
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="weight">#{lp[13]}</label>
				<input type="number" min='0' class="form-control" id="detail_weight" value="#{food_weight.to_f}" onchange="detailWeight( '#{food_no}' )">
				<button class="btn btn-outline-primary" type="button" onclick="detailWeight( '#{food_no}' )">g</button>
			</div>
		</div>
		<div class="col-1">
		</div>
		<div class="col-1">
			#{add_button}
		</div>
		<div class="col-1">
			<a href='plain-text.cgi?food_no=#{food_no}&food_weight=#{food_weight}&frct_mode=#{frct_mode}' download='detail_#{fct_opt['FN']}.txt'><span>#{lp[14]}</span></a>
		</div>
		<div class="col-1" align='right'>
			<span onclick='detailReturn()'>#{lp[15]}</span>
		</div>
	</div>
</div>
<br>

<div class='container-fluid'>
	<div class="row">
		<div class="col-7"><h5 onclick='detailReturn()'>#{fct_opt['Tagnames']}</h5></div>
	</div>
	<br>

	<div class="container-fluid">
		<div class="row">
			<div class="col-4">
			<table class="table-sm table-striped" width="100%">
				<tr><td>#{$FCT_NAME['REFUSE']}</td><td align="right">#{fct_opt['REFUSE']} #{$FCT_UNIT['REFUSE']}</td></tr>
				<tr><td>#{$FCT_NAME['ENERC_KCAL']}</td><td align="right">#{fct_opt['ENERC_KCAL']} #{$FCT_UNIT['ENERC_KCAL']}</td></tr>
				<tr><td>#{$FCT_NAME['ENERC']}</td><td align="right">#{fct_opt['ENERC']} #{$FCT_UNIT['ENERC']}</td></tr>
				<tr><td>#{$FCT_NAME['WATER']}</td><td align="right">#{fct_opt['WATER']} #{$FCT_UNIT['WATER']}</td></tr>
			</table>
			<div style='border: solid gray 1px; margin: 0.5em; padding: 0.5em;'>
				#{lp[17]}<br>
				#{fct_opt['Notice']}
			</div>
			</div>

			<div class="col-4">
			<table class="table-sm table-striped" width="100%">
				<tr><td>#{$FCT_NAME['PROT']}</td><td align="right">#{fct_opt['PROT']} #{$FCT_UNIT['PROT']}</td></tr>
				<tr><td>#{$FCT_NAME['PROTCAA']}</td><td align="right">#{fct_opt['PROTCAA']} #{$FCT_UNIT['PROTCAA']}</td></tr>
				<tr><td>#{$FCT_NAME['FAT']}</td><td align="right">#{fct_opt['FAT']} #{$FCT_UNIT['FAT']}</td></tr>
				<tr><td>#{$FCT_NAME['FATNLEA']}</td><td align="right">#{fct_opt['FATNLEA']} #{$FCT_UNIT['FATNLEA']}</td></tr>
				<tr><td>#{$FCT_NAME['FASAT']}</td><td align="right">#{fct_opt['FASAT']} #{$FCT_UNIT['FASAT']}</td></tr>
				<tr><td>#{$FCT_NAME['FAMS']}</td><td align="right">#{fct_opt['FAMS']} #{$FCT_UNIT['FAMS']}</td></tr>
				<tr><td>#{$FCT_NAME['FAPU']}</td><td align="right">#{fct_opt['FAPU']} #{$FCT_UNIT['FAPU']}</td></tr>
				<tr><td>#{$FCT_NAME['CHOLE']}</td><td align="right">#{fct_opt['CHOLE']} #{$FCT_UNIT['CHOLE']}</td></tr>
				<tr><td>#{$FCT_NAME['CHO']}</td><td align="right">#{fct_opt['CHO']} #{$FCT_UNIT['CHO']}</td></tr>
				<tr><td>#{$FCT_NAME['CHOAVLM']}</td><td align="right">#{fct_opt['CHOAVLM']} #{$FCT_UNIT['CHOAVLM']}</td></tr>
				<tr><td>#{$FCT_NAME['FIBSOL']}</td><td align="right">#{fct_opt['FIBSOL']} #{$FCT_UNIT['FIBSOL']}</td></tr>
				<tr><td>#{$FCT_NAME['FIBINS']}</td><td align="right">#{fct_opt['FIBINS']} #{$FCT_UNIT['FIBINS']}</td></tr>
				<tr><td>#{$FCT_NAME['FIBTG']}</td><td align="right">#{fct_opt['FIBTG']} #{$FCT_UNIT['FIBTG']}</td></tr>
			</table>
			</div>

			<div class="col-4">
			<table class="table-sm table-striped" width="100%">
				<tr><td>#{$FCT_NAME['ASH']}</td><td align="right">#{fct_opt['ASH']} #{$FCT_UNIT['ASH']}</td></tr>
				<tr><td>#{$FCT_NAME['NA']}</td><td align="right">#{fct_opt['NA']} #{$FCT_UNIT['NA']}</td></tr>
				<tr><td>#{$FCT_NAME['K']}</td><td align="right">#{fct_opt['K']} #{$FCT_UNIT['K']}</td></tr>
				<tr><td>#{$FCT_NAME['CA']}</td><td align="right">#{fct_opt['CA']} #{$FCT_UNIT['CA']}</td></tr>
				<tr><td>#{$FCT_NAME['MG']}</td><td align="right">#{fct_opt['MG']} #{$FCT_UNIT['MG']}</td></tr>
				<tr><td>#{$FCT_NAME['P']}</td><td align="right">#{fct_opt['P']} #{$FCT_UNIT['P']}</td></tr>
				<tr><td>#{$FCT_NAME['FE']}</td><td align="right">#{fct_opt['FE']} #{$FCT_UNIT['FE']}</td></tr>
				<tr><td>#{$FCT_NAME['ZN']}</td><td align="right">#{fct_opt['ZN']} #{$FCT_UNIT['ZN']}</td></tr>
				<tr><td>#{$FCT_NAME['CU']}</td><td align="right">#{fct_opt['CU']} #{$FCT_UNIT['CU']}</td></tr>
				<tr><td>#{$FCT_NAME['MN']}</td><td align="right">#{fct_opt['MN']} #{$FCT_UNIT['MN']}</td></tr>
				<tr><td>#{$FCT_NAME['ID']}</td><td align="right">#{fct_opt['ID']} #{$FCT_UNIT['ID']}</td></tr>
				<tr><td>#{$FCT_NAME['SE']}</td><td align="right">#{fct_opt['SE']} #{$FCT_UNIT['SE']}</td></tr>
				<tr><td>#{$FCT_NAME['CR']}</td><td align="right">#{fct_opt['CR']} #{$FCT_UNIT['CR']}</td></tr>
				<tr><td>#{$FCT_NAME['MO']}</td><td align="right">#{fct_opt['MO']} #{$FCT_UNIT['MO']}</td></tr>
			</table>
			</div>
		</div>

		<hr>

		<div class="row">
			<div class="col-4">
				<table class="table-sm table-striped" width="100%">
				<tr><td>#{$FCT_NAME['RETOL']}</td><td align="right">#{fct_opt['RETOL']} #{$FCT_UNIT['RETOL']}</td></tr>
				<tr><td>#{$FCT_NAME['CARTA']}</td><td align="right">#{fct_opt['CARTA']} #{$FCT_UNIT['CARTA']}</td></tr>
				<tr><td>#{$FCT_NAME['CARTB']}</td><td align="right">#{fct_opt['CARTB']} #{$FCT_UNIT['CARTB']}</td></tr>
				<tr><td>#{$FCT_NAME['CRYPXB']}</td><td align="right">#{fct_opt['CRYPXB']} #{$FCT_UNIT['CRYPXB']}</td></tr>
				<tr><td>#{$FCT_NAME['CARTBEQ']}</td><td align="right">#{fct_opt['CARTBEQ']} #{$FCT_UNIT['CARTBEQ']}</td></tr>
				<tr><td>#{$FCT_NAME['VITA_RAE']}</td><td align="right">#{fct_opt['VITA_RAE']} #{$FCT_UNIT['VITA_RAE']}</td></tr>
				<tr><td>#{$FCT_NAME['VITD']}</td><td align="right">#{fct_opt['VITD']} #{$FCT_UNIT['VITD']}</td></tr>
				<tr><td>#{$FCT_NAME['TOCPHA']}</td><td align="right">#{fct_opt['TOCPHA']} #{$FCT_UNIT['TOCPHA']}</td></tr>
				<tr><td>#{$FCT_NAME['TOCPHB']}</td><td align="right">#{fct_opt['TOCPHB']} #{$FCT_UNIT['TOCPHB']}</td></tr>
				<tr><td>#{$FCT_NAME['TOCPHG']}</td><td align="right">#{fct_opt['TOCPHG']} #{$FCT_UNIT['TOCPHG']}</td></tr>
				<tr><td>#{$FCT_NAME['TOCPHD']}</td><td align="right">#{fct_opt['TOCPHD']} #{$FCT_UNIT['TOCPHD']}</td></tr>
				<tr><td>#{$FCT_NAME['VITK']}</td><td align="right">#{fct_opt['VITK']} #{$FCT_UNIT['VITK']}</td></tr>
				</table>
			</div>

			<div class="col-4">
			<table class="table-sm table-striped" width="100%">
				<tr><td>#{$FCT_NAME['THIAHCL']}</td><td align="right">#{fct_opt['THIAHCL']} #{$FCT_UNIT['THIAHCL']}</td></tr>
				<tr><td>#{$FCT_NAME['RIBF']}</td><td align="right">#{fct_opt['RIBF']} #{$FCT_UNIT['RIBF']}</td></tr>
				<tr><td>#{$FCT_NAME['NIA']}</td><td align="right">#{fct_opt['NIA']} #{$FCT_UNIT['NIA']}</td></tr>
				<tr><td>#{$FCT_NAME['VITB6A']}</td><td align="right">#{fct_opt['VITB6A']} #{$FCT_UNIT['VITB6A']}</td></tr>
				<tr><td>#{$FCT_NAME['VITB12']}</td><td align="right">#{fct_opt['VITB12']} #{$FCT_UNIT['VITB12']}</td></tr>
				<tr><td>#{$FCT_NAME['FOL']}</td><td align="right">#{fct_opt['FOL']} #{$FCT_UNIT['FOL']}</td></tr>
				<tr><td>#{$FCT_NAME['PANTAC']}</td><td align="right">#{fct_opt['PANTAC']} #{$FCT_UNIT['PANTAC']}</td></tr>
				<tr><td>#{$FCT_NAME['BIOT']}</td><td align="right">#{fct_opt['BIOT']} #{$FCT_UNIT['BIOT']}</td></tr>
				<tr><td>#{$FCT_NAME['VITC']}</td><td align="right">#{fct_opt['VITC']} #{$FCT_UNIT['VITC']}</td></tr>
			</table>
			</div>

			<div class="col-4">
			<table class="table-sm table-striped" width="100%">
				<tr><td>#{$FCT_NAME['NACL_EQ']}</td><td align="right">#{fct_opt['NACL_EQ']} #{$FCT_UNIT['NACL_EQ']}</td></tr>
				<tr><td>#{$FCT_NAME['ALC']}</td><td align="right">#{fct_opt['ALC']} #{$FCT_UNIT['ALC']}</td></tr>
				<tr><td>#{$FCT_NAME['NITRA']}</td><td align="right">#{fct_opt['NITRA']} #{$FCT_UNIT['NITRA']}</td></tr>
				<tr><td>#{$FCT_NAME['THEBRN']}</td><td align="right">#{fct_opt['THEBRN']} #{$FCT_UNIT['THEBRN']}</td></tr>
				<tr><td>#{$FCT_NAME['CAFFN']}</td><td align="right">#{fct_opt['CAFFN']} #{$FCT_UNIT['CAFFN']}</td></tr>
				<tr><td>#{$FCT_NAME['TAN']}</td><td align="right">#{fct_opt['TAN']} #{$FCT_UNIT['TAN']}</td></tr>
				<tr><td>#{$FCT_NAME['POLYPHENT']}</td><td align="right">#{fct_opt['POLYPHENT']} #{$FCT_UNIT['POLYPHENT']}</td></tr>
				<tr><td>#{$FCT_NAME['ACEAC']}</td><td align="right">#{fct_opt['ACEAC']} #{$FCT_UNIT['ACEAC']}</td></tr>
				<tr><td>#{$FCT_NAME['COIL']}</td><td align="right">#{fct_opt['COIL']} #{$FCT_UNIT['COIL']}</td></tr>
				<tr><td>#{$FCT_NAME['OA']}</td><td align="right">#{fct_opt['OA']} #{$FCT_UNIT['OA']}</td></tr>
				<tr><td>#{$FCT_NAME['WCR']}</td><td align="right">#{fct_opt['WCR']} #{$FCT_UNIT['WCR']}</td></tr>
			</table>
			</div>
		</div>
	</div>

	<hr>

	<div class="row">
		<div class="col-8">
			#{lp[16]}：#{search_key}
		</div>
		<div class="col-4">
			#{alias_button}
		</div>
	</div>
</div>
HTML
puts html


#### 登録ユーザーで直接参照の場合は履歴に追加
add_his( user.name, food_no ) unless sid_flag || user.status == 0
