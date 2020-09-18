# Ginmi module for Kaup index 0.00b
#encoding: utf-8

def ginmi_module( cgi, user )
	module_js()

	command = cgi['command']
	html = ''

	case command
	when 'form', 'koyomiex'
		#importing from config

		age = 0.0
		height = 0.0
		weight = 0.0
		r = mdb( "SELECT age, height, weight, koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, true )
		if r.first
			age = r.first['age']
			age = 0.0 unless r.first['age']
			height = r.first['height'].to_f * 100
			height = 0.0 unless r.first['height']
			weight = r.first['weight'].to_f * 1000
			weight = 0.0 unless r.first['weight']
		end

		# inporting from koyomiex
		if command == 'koyomiex' && r.first['koyomiex']
			a = r.first['koyomiex'].split( ':' )
			a.size.times do |c|
				aa = a[c].split( "\t" )
				if aa[0] == '2'
					rr = mdb( "SELECT item#{aa[0]} FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND item#{aa[0]}!='' ORDER BY date DESC LIMIT 1;", false, true )
					if rr.first
						height = rr.first["item#{aa[0]}"].to_f
					end
				end

				if aa[0] == '3'
					rr = mdb( "SELECT item#{aa[0]} FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND item#{aa[0]}!='' ORDER BY date DESC LIMIT 1;", false, true )
					if rr.first
						weight = rr.first["item#{aa[0]}"].to_f * 1000
					end
				end
			end
		end

		age_select = []
		if age < 1.0
			age_select[0] = 'SELECTED'
		elsif age <= 1.5
			age_select[1] = 'SELECTED'
		elsif age < 2
			age_select[2] = 'SELECTED'
		elsif age < 3
			age_select[3] = 'SELECTED'
		elsif age < 4
			age_select[4] = 'SELECTED'
		elsif age < 5
			age_select[5] = 'SELECTED'
		else
			age_select[6] = 'SELECTED'
		end


html = <<-"HTML"
		<div class='row'>
		<h5>カウプ指数 計算フォーム</h5>
		</div>
		<br>

		<div class='row'>
			<div class='col-6'>
				<button class='btn btn-sm btn-outline-primary' onclick="ginmiKaupkex()">拡張こよみ適用</button>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">年齢</label>
					<select class="form-select form-select-sm" id="age">
						<option value='0.3' #{age_select[0]}>3ヶ月-1歳</option>
						<option value='1' #{age_select[1]}>満1歳</option>
						<option value='1.6' #{age_select[2]}>1歳6ヶ月</option>
						<option value='2' #{age_select[3]}>満2歳</option>
						<option value='3' #{age_select[4]}>満3歳</option>
						<option value='4' #{age_select[5]}>満4歳</option>
						<option value='5' #{age_select[6]}>満5歳</option>
					</select>
				</div>
			</div>

			<div class='col-2'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>身長(cm)</span>
					<input type='text' class='form-control' id='height' maxlength='6' value='#{height}'>
				</div>
			</div>

			<div class='col-2'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>体重(g)</span>
					<input type='text' class='form-control' id='weight' maxlength='6' value='#{weight}'>
				</div>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="ginmiKaupres()">計算</button>
			</div>
		</div>
HTML
	when 'result'
		age = cgi['age'].to_i
		weight = BigDecimal( cgi['weight'] )
		height = BigDecimal( cgi['height'] )
		if false
			puts "age:#{age}<br>\n"
			puts "height:#{height}<br>\n"
			puts "weight:#{weight}<br>\n"
			puts "<hr>\n"
		end

		result = ( weight / ( height * height ) * 10 ).round( 1 )

		age_1 = []
		age_2 = []
		age_3 = []
		age_4 = []
		age_5 = []
		age_6 = []
		age_7 = []
		ibw_index = 0.0
		hit_bg = [age_1, age_2, age_3, age_4, age_5, age_6, age_7]
		if age < 1.0
			if result < 14.5
				hit_bg[0][0] = 'bg-warning'
			elsif result < 16
				hit_bg[0][1] = 'bg-warning'
			elsif result < 18
				hit_bg[0][2] = 'bg-warning'
			elsif result < 20
				hit_bg[0][3] = 'bg-warning'
			else
				hit_bg[0][4] = 'bg-warning'
			end
			ibw_index = 17
		elsif age <= 1.5
			if result < 14.5
				hit_bg[1][0] = 'bg-warning'
			elsif result < 15.5
				hit_bg[1][1] = 'bg-warning'
			elsif result < 17.5
				hit_bg[1][2] = 'bg-warning'
			elsif result < 19.5
				hit_bg[1][3] = 'bg-warning'
			else
				hit_bg[1][4] = 'bg-warning'
			end
			ibw_index = 16.5
		elsif age < 2
			if result < 14
				hit_bg[2][0] = 'bg-warning'
			elsif result < 15
				hit_bg[2][1] = 'bg-warning'
			elsif result < 17
				hit_bg[2][2] = 'bg-warning'
			elsif result < 19
				hit_bg[2][3] = 'bg-warning'
			else
				hit_bg[2][4] = 'bg-warning'
			end
			ibw_index = 16
		elsif age < 3
			if result < 13.5
				hit_bg[3][0] = 'bg-warning'
			elsif result < 15
				hit_bg[3][1] = 'bg-warning'
			elsif result < 16.5
				hit_bg[3][2] = 'bg-warning'
			elsif result < 18.5
				hit_bg[3][3] = 'bg-warning'
			else
				hit_bg[3][4] = 'bg-warning'
			end
			ibw_index = 15.75
		elsif age < 4
			if result < 13.5
				hit_bg[4][0] = 'bg-warning'
			elsif result < 14.5
				hit_bg[4][1] = 'bg-warning'
			elsif result < 16.5
				hit_bg[4][2] = 'bg-warning'
			elsif result < 18
				hit_bg[4][3] = 'bg-warning'
			else
				hit_bg[4][4] = 'bg-warning'
			end
			ibw_index = 15
		elsif age < 5
			if result < 13
				hit_bg[5][0] = 'bg-warning'
			elsif result < 14.5
				hit_bg[5][1] = 'bg-warning'
			elsif result < 16.5
				hit_bg[5][2] = 'bg-warning'
			elsif result < 18
				hit_bg[5][3] = 'bg-warning'
			else
				hit_bg[5][4] = 'bg-warning'
			end
			ibw_index = 15
		else
			if result < 13
				hit_bg[6][0] = 'bg-warning'
			elsif result < 14.5
				hit_bg[6][1] = 'bg-warning'
			elsif result < 16.5
				hit_bg[6][2] = 'bg-warning'
			elsif result < 18.5
				hit_bg[6][3] = 'bg-warning'
			else
				hit_bg[6][4] = 'bg-warning'
			end
			ibw_index = 15
		end

		ibw = ( ibw_index * ( height * height ) / 10 ) .round( 1 )

		#Degree of obesity
		obesity = (( weight - ibw ) / ibw * 100 ).round( 1 )
		obesity_hit_bg = []
		if obesity < -20
			obesity_hit_bg[0] = 'bg-warning'
		elsif obesity < -15
			obesity_hit_bg[1] = 'bg-warning'
		elsif obesity < 15
			obesity_hit_bg[2] = 'bg-warning'
		elsif obesity < 20
			obesity_hit_bg[3] = 'bg-warning'
		elsif obesity < 30
			obesity_hit_bg[4] = 'bg-warning'
		else
			obesity_hit_bg[5] = 'bg-warning'
		end

html = <<-"HTML"
		<div class='row'>
			<div class='col-2'>カウプ指数</div>
			<div class='col-2'>#{result.to_f}</div>
			<div class='col-2'>計算式</div>
			<div class='col-6'>#{weight.to_f} / ( #{height.to_f} * #{height.to_f} ) * 10</div>
		</div>
		<br>

		<table width='50%' class='table table-sm table-bordered'>
			<thead class='thead-light'>
				<tr>
					<th scope='col'>年齢</th>
					<th scope='col'>やせすぎ</th>
					<th scope='col'>やせ気味</th>
					<th scope='col'>標準</th>
					<th scope='col'>太り気味</th>
					<th scope='col'>太りすぎ</th>
				</tr>
			</thead>
			<tbody>
				<tr>
					<th scope='row'>3ヶ月-1歳</th>
					<td class='#{hit_bg[0][0]}'> - 14.4</td>
					<td class='#{hit_bg[0][1]}'>14.5 - 15.9</td>
					<td class='#{hit_bg[0][2]}'>16.0 - 17.9</td>
					<td class='#{hit_bg[0][3]}'>18.0 - 19.9</td>
					<td class='#{hit_bg[0][4]}'>20.0 - </td>
				</tr>
				<tr>
					<th scope='row'>満1歳</th>
					<td class='#{hit_bg[1][0]}'> - 14.4</td>
					<td class='#{hit_bg[1][1]}'>14.5 - 15.4</td>
					<td class='#{hit_bg[1][2]}'>15.0 - 17.4</td>
					<td class='#{hit_bg[1][3]}'>17.5 - 19.4</td>
					<td class='#{hit_bg[1][4]}'>19.5 - </td>
				</tr>
				<tr>
					<th scope='row'>1歳6ヶ月</th>
					<td class='#{hit_bg[2][0]}'> - 13.9</td>
					<td class='#{hit_bg[2][1]}'>14.0 - 14.9</td>
					<td class='#{hit_bg[2][2]}'>15.0 - 16.9</td>
					<td class='#{hit_bg[2][3]}'>17.0 - 18.9</td>
					<td class='#{hit_bg[2][4]}'>19.0 - </td>
				</tr>
				<tr>
					<th scope='row'>満2歳</th>
					<td class='#{hit_bg[3][0]}'> - 13.4</td>
					<td class='#{hit_bg[3][1]}'>13.5 - 14.9</td>
					<td class='#{hit_bg[3][2]}'>15.0 - 16.4</td>
					<td class='#{hit_bg[3][3]}'>16.5 - 18.4</td>
					<td class='#{hit_bg[3][4]}'>18.5 - </td>
				</tr>
				<tr>
					<th scope='row'>満3歳</th>
					<td class='#{hit_bg[4][0]}'> - 13.4</td>
					<td class='#{hit_bg[4][1]}'>13.5 - 14.4</td>
					<td class='#{hit_bg[4][2]}'>15.0 - 16.4</td>
					<td class='#{hit_bg[4][3]}'>16.5 - 17.9</td>
					<td class='#{hit_bg[4][4]}'>18.0 - </td>
				</tr>
				<tr>
					<th scope='row'>満4歳</th>
					<td class='#{hit_bg[5][0]}'> - 12.9</td>
					<td class='#{hit_bg[5][1]}'>13.0 - 14.4</td>
					<td class='#{hit_bg[5][2]}'>14.5 - 16.4</td>
					<td class='#{hit_bg[5][3]}'>16.5 - 17.9</td>
					<td class='#{hit_bg[5][4]}'>18.0 - </td>
				</tr>
				<tr>
					<th scope='row'>満5歳</th>
					<td class='#{hit_bg[6][0]}'> - 12.9</td>
					<td class='#{hit_bg[6][1]}'>13.0 - 14.4</td>
					<td class='#{hit_bg[6][2]}'>14.5 - 16.4</td>
					<td class='#{hit_bg[6][3]}'>16.5 - 18.4</td>
					<td class='#{hit_bg[6][4]}'>18.5 - </td>
				</tr>
			</tbody>
		</table>
		<br>
		<div class='row'>
			<div class='col-2'>標準体重 (g)</div>
			<div class='col-2'>#{ibw.to_f}</div>
			<div class='col-2'>計算式</div>
			<div class='col-6'>#{ibw_index} * #{height.to_f} * #{height.to_f} / 10</div>
		</div>
		<br>
		<div class='row'>
			<div class='col-2'>肥満度 (%)</div>
			<div class='col-2'>#{obesity.to_f}</div>
			<div class='col-2'>計算式</div>
			<div class='col-6'>( #{weight.to_f} - #{ibw.to_f} ) / #{ibw.to_f} * 100</div>
		</div>
		<br>

		<table class='table table-sm table-bordered'>
		<thead class='thead-light'>
			<tr>
				<th scope='col'>やせすぎ</th>
				<th scope='col'>やけ</th>
				<th scope='col'>標準</th>
				<th scope='col'>ふとりぎみ</th>
				<th scope='col'>ややふとりすぎ</th>
				<th scope='col'>ふとりすぎ</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td class='#{obesity_hit_bg[0]}'>-20%未満</td>
				<td class='#{obesity_hit_bg[1]}'>-15%未満</td>
				<td class='#{obesity_hit_bg[2]}'>-15%以上 +15%未満</td>
				<td class='#{obesity_hit_bg[3]}'>+15%以上</td>
				<td class='#{obesity_hit_bg[4]}'>+20%以上</td>
				<td class='#{obesity_hit_bg[5]}'>+30%以上</td>
			</tr>
		</tbody>
	</table>
※区分は目安です。
HTML
	when 'save'

	end

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var ginmiKaupres = function(){
	var age = document.getElementById( "age" ).value;
	var height = document.getElementById( "height" ).value;
	var weight = document.getElementById( "weight" ).value;
	$.post( "ginmi.cgi", { mod:"kaupi", command:'result', age:age, height:height, weight:weight }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};

var ginmiKaupkex = function(){
	$.post( "ginmi.cgi", { mod:"kaupi", command:'koyomiex' }, function( data ){ $( "#bw_level2" ).html( data );});
};

</script>
JS
	puts js
end
