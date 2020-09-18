# Ginmi module for basal metabolism 0.00
#encoding: utf-8

def ginmi_module( cgi, user )
	module_js()

	command = cgi['command']
	html = ''

	case command
	when 'form', 'koyomiex'
		#importing from config
		r = mdb( "SELECT age, sex, height, weight, koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, true )
		sex = 0
		age = 18
		height = 0.0
		weight = 0.0
		if r.first
			sex = r.first['sex'].to_i
			age = r.first['age'].to_i
			height = r.first['height'].to_f * 100
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

		sex_select = []
		if sex = 0
			sex_select[0] = 'SELECTED'
		else
			sex_select[1] = 'SELECTED'
		end


html = <<-"HTML"
		<div class='row'>
		<h5>基礎代謝量 計算フォーム（国立健康・栄養研究所の式）</h5>
		</div>
		<br>

		<div class='row'>
			<div class='col-6'>
				<button class='btn btn-sm btn-outline-primary' onclick="ginmiEnergyHNkex()">拡張こよみ適用</button>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">代謝的性別</label>
					<select class="form-select form-select-sm" id="sex">
						<option value='0' #{sex_select[0]}>男性</option>
						<option value='1' #{sex_select[1]}>女性</option>
					</select>
				</div>
			</div>

			<div class='col-2'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>年齢</span>
					<input type='number' class='form-control' id='age' min='0' value='#{age}'>
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
					<span class='input-group-text'>体重(kg)</span>
					<input type='text' class='form-control' id='weight' maxlength='6' value='#{weight}'>
				</div>
			</div>

			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">身体活動レベル</label>
					<select class="form-select form-select-sm" id="pal">
						<option value='1.50'>I (1.50)</option>
						<option value='1.75' SELECTED>II (1.75)</option>
						<option value='2.00'>III (2.00</option>
					</select>
				</div>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="ginmiEnergyHNres()">計算</button>
			</div>
		</div>
HTML
	when 'result'
		sex = cgi['sex'].to_i
		age = cgi['age'].to_i
		weight = BigDecimal( cgi['weight'] )
		height = BigDecimal( cgi['height'] )
		pal = BigDecimal( cgi['pal'] )

		if false
			puts "sex:#{sex}<br>\n"
			puts "age:#{age}<br>\n"
			puts "height:#{height}<br>\n"
			puts "weight:#{weight}<br>\n"
			puts "pal:#{pal}<br>\n"
			puts "<hr>\n"
		end

		result = 0
		formula = ''
		if sex == 0
			result = (( 0.0481 * weight + 0.0234 * height - 0.0138 * age - 0.4235 ) * 1000 / 4.186 ).round( 0 )
			formula = "( 0.0481 * #{weight.to_f} + 0.0234 * #{height.to_f} - 0.0138 * #{age} - 0.4235 ) * 1000 / 4.186"
		else
			result = (( 0.0481 * weight + 0.0234 * height - 0.0138 * age - 0.9708 ) * 1000 / 4.186 ).round( 0 )
			formula = "( 0.0481 * #{weight.to_f} + 0.0234 * #{height.to_f} - 0.0138 * #{age} - 0.9708 ) * 1000 / 4.186"
		end
		eer_result = ( result * pal ).round( 0 )
		eer_formula = "#{result.to_i} * #{pal.to_f}"


		ibw = ( 22 * height * height / 10000 ).round( 1 )
		ibw_result = 0
		ibw_formula = ''
		if sex == 0
			ibw_result = (( 0.0481 * ibw + 0.0234 * height - 0.0138 * age - 0.4235 ) * 1000 / 4.186 ).round( 0 )
			ibw_formula = "( 0.0481 * #{ibw.to_f} + 0.0234 * #{height.to_f} - 0.0138 * #{age} - 0.4235 ) * 1000 / 4.186"
		else
			ibw_result = (( 0.0481 * ibw + 0.0234 * height - 0.0138 * age - 0.9708 ) * 1000 / 4.186 ).round( 0 )
			ibw_formula = "( 0.0481 * #{ibw.to_f} + 0.0234 * #{height.to_f} - 0.0138 * #{age} - 0.9708 ) * 1000 / 4.186"
		end
		ibw_eer_result = ( ibw_result * pal ).round( 0 )
		ibw_eer_formula = "#{ibw_result.to_i} * #{pal.to_f}"

html = <<-"HTML"
		<div class='row'>
			<div class='col-3'>基礎代謝量(kcal/day)</div>
			<div class='col-2'>#{result.to_i}</div>
			<div class='col-1'>計算式</div>
			<div class='col-6'>#{formula}</div>
		</div>
		<br>
		<div class='row'>
			<div class='col-3'>推定エネルギー必要量(kcal/day)</div>
			<div class='col-2'>#{eer_result.to_i}</div>
			<div class='col-1'>計算式</div>
			<div class='col-6'>#{eer_formula}</div>
		</div>
		<hr>

		<div class='row'>
			<div class='col-3'>標準体重(kg)</div>
			<div class='col-2'>#{ibw.to_f}</div>
		</div>
		<br>
		<div class='row'>
			<div class='col-3'>基礎代謝量(kcal/day)</div>
			<div class='col-2'>#{ibw_result.to_i}</div>
			<div class='col-1'>計算式</div>
			<div class='col-6'>#{ibw_formula}</div>
		</div>
		<br>
		<div class='row'>
			<div class='col-3'>推定エネルギー必要量(kcal/day)</div>
			<div class='col-2'>#{(ibw_eer_result.to_i)}</div>
			<div class='col-1'>計算式</div>
			<div class='col-6'>#{ibw_eer_formula}</div>
		</div>

HTML
	when 'save'

	end

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

/////////////////////////////////////////////////////////////////////////////////
// Ginmi enegry HN //////////////////////////////////////////////////////////////

var ginmiEnergyHNres = function(){
	var sex = document.getElementById( "sex" ).value;
	var age = document.getElementById( "age" ).value;
	var height = document.getElementById( "height" ).value;
	var weight = document.getElementById( "weight" ).value;
	var pal = document.getElementById( "pal" ).value;
	$.post( "ginmi.cgi", { mod:"energy-hn", command:'result', age:age, sex:sex, height:height, weight:weight, pal:pal }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};

var ginmiEnergyHNkex = function(){
	$.post( "ginmi.cgi", { mod:"energy-hn", command:'koyomiex' }, function( data ){ $( "#bw_level2" ).html( data );});
};

</script>
JS
	puts js
end
