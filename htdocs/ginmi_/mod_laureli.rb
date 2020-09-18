# Ginmi module for Laurel index 0.00
#encoding: utf-8

def ginmi_module( cgi, user )
	module_js()

	command = cgi['command']
	html = ''

	case command
	when 'form', 'koyomiex'
		#importing from config

		r = mdb( "SELECT height, weight, koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, true )
		height = 0.0
		weight = 0.0
		if r.first
			age = r.first['age']
			height = r.first['height'].to_f
			weight = r.first['weight']
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
						weight = rr.first["item#{aa[0]}"].to_f
					end
				end
			end
		end


html = <<-"HTML"
		<div class='row'>
		<h5>ローレル指数 計算フォーム</h5>
		</div>
		<br>

		<div class='row'>
			<div class='col-6'>
				<button class='btn btn-sm btn-outline-primary' onclick="gginmiLaurelkex()">拡張こよみ適用</button>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>身長(m)</span>
					<input type='text' class='form-control' id='height' maxlength='6' value='#{height}'>
				</div>
			</div>

			<div class='col-2'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>体重(kg)</span>
					<input type='text' class='form-control' id='weight' maxlength='6' value='#{weight}'>
				</div>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="ginmiLaurelres()">計算</button>
			</div>
		</div>
HTML
	when 'result'
		weight = BigDecimal( cgi['weight'] )
		height = BigDecimal( cgi['height'] )
		if false
			puts "height:#{height}<br>\n"
			puts "weight:#{weight}<br>\n"
			puts "<hr>\n"
		end

		result = ( weight / ( height * height * height ) * 10 ).round( 0 )

		ibw_index = 0.0
		hit_bg = ['', '', '', '', '', '', '']
		if result < 100
			hit_bg[0] = 'bg-warning'
		elsif result < 115
			hit_bg[1] = 'bg-warning'
		elsif result < 145
			hit_bg[2] = 'bg-warning'
		elsif result < 160
			hit_bg[3] = 'bg-warning'
		else
			hit_bg[4] = 'bg-warning'
		end

		ibw_index = 130
		ibw = ( ibw_index * ( height * height * height ) / 10 ) .round( 1 )

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
			<div class='col-2'>ローレル指数</div>
			<div class='col-2'>#{result.to_f}</div>
			<div class='col-2'>計算式</div>
			<div class='col-6'>#{weight.to_f} / ( #{height.to_f} * #{height.to_f} * #{height.to_f} ) * 10</div>
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
					<th scope='row'>6歳-17歳</th>
					<td class='#{hit_bg[0]}'> - 99</td>
					<td class='#{hit_bg[1]}'>100 - 114</td>
					<td class='#{hit_bg[2]}'>115 - 144</td>
					<td class='#{hit_bg[3]}'>145 - 159</td>
					<td class='#{hit_bg[4]}'>160 - </td>
				</tr>

			</tbody>
		</table>
		<br>

		<div class='row'>
			<div class='col-2'>標準体重</div>
			<div class='col-2'>#{ibw.to_f}&nbsp;kg</div>
			<div class='col-2'>計算式</div>
			<div class='col-6'>#{ibw_index} * #{height.to_f} * #{height.to_f} * #{height.to_f} / 10</div>
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

var ginmiLaurelres = function(){
	var height = document.getElementById( "height" ).value;
	var weight = document.getElementById( "weight" ).value;
	$.post( "ginmi.cgi", { mod:"laureli", command:'result', height:height, weight:weight }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};

var ginmiLaurelkex = function(){
	$.post( "ginmi.cgi", { mod:"laureli", command:'koyomiex' }, function( data ){ $( "#bw_level2" ).html( data );});
};

</script>
JS
	puts js
end
