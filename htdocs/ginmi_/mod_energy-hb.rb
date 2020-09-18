# Ginmi module for basal metabolism Harris-Benedict Equation 0.00
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
		<h5>基礎代謝量 計算フォーム（Harris-Benedict式）</h5>
		</div>
		<br>

		<div class='row'>
			<div class='col-6'>
				<button class='btn btn-sm btn-outline-primary' onclick="ginmiEnergyHBkex()">拡張こよみ適用</button>
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
		</div>
		<br>

		<div class='row'>
			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">活動係数</label>
					<select class="form-select form-select-sm" id="active">
						<option value='1.0'>寝たきり・意識低下 (1.0)</option>
						<option value='1.1'>寝たきり・覚醒 (1.1)</option>
						<option value='1.2'>ベッド上・安静 (1.2)</option>
						<option value='1.3'>ベッド上 (1.3)</option>
						<option value='1.4'>ベッド外活動あり (1.4)</option>
						<option value='1.5'>通常・軽労働L1 (1.5)</option>
						<option value='1.6'>通常・軽労働L2 (1.6)</option>
						<option value='1.7' SELECTED>通常・一般労働L1 (1.7)</option>
						<option value='1.8'>通常・一般労働L2 (1.8)</option>
						<option value='1.9'>通常・重労働L1 (1.9)</option>
						<option value='2.00'>通常・重労働L2 (2.0)</option>
					</select>
				</div>
			</div>
			<div class='col-4'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">ストレス係数</label>
					<select class="form-select form-select-sm" id="stress">
						<option value='0.6'>飢餓L2 (0.6)</option>
						<option value='0.8'>飢餓L1 (0.8)</option>
						<option value='1.0' SELECTED>なし (1.0)</option>
						<option value='1.1'>手術・軽度、がんL1 (1.1)</option>
						<option value='1.2'>手術・中度、感染症・軽度、がんL2、COPD (1.2)</option>
						<option value='1.3'>骨折、がんL3 (1.3)</option>
						<option value='1.5'>感染症・中度、熱傷・40% (1.5)</option>
						<option value='1.8'>手術・重度 (1.8)</option>
						<option value='1.9'>熱傷・100% (1.9)</option>
					</select>
				</div>
			</div>
			<div class='col-2'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">体温(℃)</label>
					<select class="form-select form-select-sm" id="btm">
						<option value='-0.05'>35.5</option>
						<option value='0.00' SELECTED>36.0</option>
						<option value='0.05'>36.5</option>
						<option value='0.10'>37.0</option>
						<option value='0.15'>37.5</option>
						<option value='0.20'>38.5</option>
						<option value='0.25'>39.0</option>
						<option value='0.30'>39.5</option>
						<option value='0.35'>40.0</option>
					</select>
				</div>
			</div>
		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="ginmiEnergyHBres()">計算</button>
			</div>
		</div>
HTML
	when 'result'
		sex = cgi['sex'].to_i
		age = cgi['age'].to_i
		active = BigDecimal( cgi['active'] )
		stress = BigDecimal( cgi['stress'] )
		btm = BigDecimal( cgi['btm'] )
		weight = BigDecimal( cgi['weight'] )
		height = BigDecimal( cgi['height'] )

		if false
			puts "sex:#{sex}<br>\n"
			puts "age:#{age}<br>\n"
			puts "height:#{height}<br>\n"
			puts "weight:#{weight}<br>\n"
			puts "active:#{active}<br>\n"
			puts "stress:#{stress}<br>\n"
			puts "btm:#{btm}<br>\n"
			puts "<hr>\n"
		end

		result = 0
		formula = ''
		if sex == 0
			result = ( 66.4730 + 13.7516 * weight + 5.0033 *  height - 6.7550 * age ).round( 0 )
			formula = "66.4730 + 13.7516 * #{weight.to_f} + 5.0033 *  #{height.to_f} - 6.7550 * #{age}"
		else
			result = ( 655.0955 + 9.5634 * weight + 1.8496 * height - 4.6756 * age ).round( 0 )
			formula = "655.0955 + 9.5634 * #{weight.to_f} + 1.8496 * #{height.to_f} - 4.6756 * #{age}"
		end
		eer_result = ( result * active * ( stress + btm )).round( 0 )
		eer_formula = "#{result.to_i} * #{active.to_f} * ( #{stress.to_f} + #{btm.to_f} )"

		ibw = ( 22 * height * height / 10000 ).round( 1 )
		ibw_result = 0
		ibw_formula = ''
		if sex == 0
			ibw_result = ( 66.4730 + 13.7516 * ibw + 5.0033 *  height - 6.7550 * age ).round( 0 )
			ibw_formula = "66.4730 + 13.7516 * #{ibw.to_f} + 5.0033 *  #{height.to_f} - 6.7550 * #{age}"
		else
			ibw_result = ( 655.0955 + 9.5634 * ibw + 1.8496 * height - 4.6756 * age ).round( 0 )
			ibw_formula = "655.0955 + 9.5634 * #{ibw.to_f} + 1.8496 * #{height.to_f} - 4.6756 * #{age}"
		end
		ibw_eer_result = ( ibw_result * active * ( stress + btm )).round( 0 )
		ibw_eer_formula = "#{ibw_result.to_i} * #{active.to_f} * ( #{stress.to_f} + #{btm.to_f} )"


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
			<div class='col-2'>#{(eer_result.to_f)}</div>
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
			<div class='col-2'>#{(ibw_eer_result.to_f)}</div>
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

var ginmiEnergyHBres = function(){
	var sex = document.getElementById( "sex" ).value;
	var age = document.getElementById( "age" ).value;
	var height = document.getElementById( "height" ).value;
	var weight = document.getElementById( "weight" ).value;
	var active = document.getElementById( "active" ).value;
	var stress = document.getElementById( "stress" ).value;
	var btm = document.getElementById( "btm" ).value;
	$.post( "ginmi.cgi", { mod:"energy-hb", command:'result', sex:sex, age:age, height:height, weight:weight, active:active, stress:stress, btm:btm }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};

var ginmiEnergyHBkex = function(){
	$.post( "ginmi.cgi", { mod:"energy-hb", command:'koyomiex' }, function( data ){ $( "#bw_level2" ).html( data );});
};

</script>
JS
	puts js
end
