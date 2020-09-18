# Ginmi module for basal metabolism reference 0.00
#encoding: utf-8

def ginmi_module( cgi, user )
	module_js()

	command = cgi['command']
	html = ''

	case command
	when 'form', 'koyomiex'
		#importing from config
		r = mdb( "SELECT age, sex, weight, koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, true )
		sex = 0
		age = 18
		weight = 0.0
		if r.first
			sex = r.first['sex'].to_i
			age = r.first['age'].to_i
			weight = r.first['weight']
		end

		# inporting from koyomiex
		if command == 'koyomiex' && r.first['koyomiex']
			a = r.first['koyomiex'].split( ':' )
			a.size.times do |c|
				aa = a[c].split( "\t" )
				if aa[0] == '3'
					rr = mdb( "SELECT item#{aa[0]} FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND item#{aa[0]}!='' ORDER BY date DESC LIMIT 1;", false, true )
					if rr.first
						weight = BigDecimal( rr.first["item#{aa[0]}"] )
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
		<h5>基礎代謝量 計算フォーム（参照値）</h5>
		</div>
		<br>

		<div class='row'>
			<div class='col-6'>
				<button class='btn btn-sm btn-outline-primary' onclick="ginmiEnergyRefkex()">拡張こよみ適用</button>
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
					<span class='input-group-text'>体重(kg)</span>
					<input type='text' class='form-control' id='weight' maxlength='6' value='#{weight.to_f}'>
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
			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">妊婦・授乳婦</label>
					<select class="form-select form-select-sm" id="pregnancy">
						<option value='0'>-</option>
						<option value='1'>妊娠・初期</option>
						<option value='2'>妊娠・中期</option>
						<option value='3'>妊娠・後期</option>
						<option value='4'>授乳婦</option>
					</select>
				</div>
			</div>
			<div class='col-9'>
				※体重を0に設定すると参照体重を使用します。
			</div>
		</div>
		<br>


		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="ginmiEnergyRefres()">計算</button>
			</div>
		</div>
HTML
	when 'result'
		sex = cgi['sex'].to_i
		weight = BigDecimal( cgi['weight'] )
		age = cgi['age'].to_i
		pal = BigDecimal( cgi['pal'] )
		pregnancy = cgi['pregnancy'].to_i

		if false
			puts "sex:#{sex}<br>\n"
			puts "weight:#{weight}<br>\n"
			puts "age:#{age}<br>\n"
			puts "pal:#{pal}<br>\n"
			puts "pregnancy:#{pregnancy}<br>\n"
			puts "<hr>\n"
		end

		age_class = 0
		if age < 2
			age_class = 0
		elsif age < 5
			age_class = 1
		elsif age < 7
			age_class = 2
		elsif age < 8
			age_class = 3
		elsif age < 11
			age_class = 4
		elsif age < 14
			age_class = 5
		elsif age < 17
			age_class = 6
		elsif age < 29
			age_class = 7
		elsif age < 49
			age_class = 8
		elsif age < 69
			age_class = 9
		else
			age_class = 10
		end

		standard_male   = [61.0, 54.8, 44.3, 40.8, 37.4, 31.0 , 27.0, 24.0, 22.3, 21.5, 21.5]
		standard_female = [59.7, 52.2, 41.9, 38.3, 34.8, 29.6 , 25.3, 22.1, 21.7, 20.7, 20.7]

		ref_weiht_male   = [11.5, 16.5, 22.2, 28.0, 35.6, 49.0 , 59.7, 63.2, 68.5, 65.3, 60.0]
		ref_weiht_female = [11.0, 16.1, 21.9, 27.4, 36.3, 47.5 , 51.9, 50.0, 53.1, 53.0, 49.5]

		addtional = [150, 250, 450, 350]

		if weight == 0
			if sex == 0
				weight = ref_weiht_male[age_class]
			else
				weight = ref_weiht_female[age_class]
			end
		end

		formula = ''
		result = 0
		eer_formula = ''
		eer_result = 0
		if sex == 0
			result = ( standard_male[age_class] * weight ).round( 0 )
			formula = "#{standard_male[age_class]} * #{weight.to_f}"
			eer_result = ( standard_male[age_class] * weight * pal ).round( 0 )
			eer_formula = "#{standard_male[age_class]} * #{weight.to_f} * #{pal.to_f}"
		else
			if pregnancy == 0
				result = ( standard_female[age_class] * weight ).round( 0 )
				formula = "#{standard_female[age_class]} * #{weight.to_f}"
				eer_result = ( standard_female[age_class] * weight * pal ).round( 0 )
				eer_formula = "#{standard_female[age_class]} * #{weight.to_f} * #{pal.to_f}"
			else
				result = ( standard_female[age_class] * weight ).round( 0 )
				formula = "#{standard_female[age_class]} * #{weight.to_f}"
				eer_result = ( standard_female[age_class] * weight * pal + addtional[pregnancy] ).round( 0 )
				eer_formula = "#{standard_female[age_class]} * #{weight.to_f} * #{pal.to_f} + #{addtional[pregnancy]}"
			end
		end

html = <<-"HTML"
		<div class='row'>
			<div class='col-3'>基礎代謝量(kcal/day)</div>
			<div class='col-2'>#{result.to_i}</div>
			<div class='col-1'>計算式</div>
			<div class='col-4'>#{formula}</div>
		</div>
		<br>
		<div class='row'>
			<div class='col-3'>推定エネルギー必要量(kcal/day)</div>
			<div class='col-2'>#{eer_result.to_i}</div>
			<div class='col-1'>計算式</div>
			<div class='col-4'>#{eer_formula}</div>
		</div>
		<br>

HTML
	when 'save'

	end

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var ginmiEnergyRefres = function(){
	var sex = document.getElementById( "sex" ).value;
	var age = document.getElementById( "age" ).value;
	var weight = document.getElementById( "weight" ).value;
	var pal = document.getElementById( "pal" ).value;
	var pregnancy = document.getElementById( "pregnancy" ).value;
	$.post( "ginmi.cgi", { mod:"energy-ref", command:'result', sex:sex, age:age, weight:weight, pal:pal, pregnancy:pregnancy }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};

var ginmiEnergyRefkex = function(){
	$.post( "ginmi.cgi", { mod:"energy-ref", command:'koyomiex' }, function( data ){ $( "#bw_level2" ).html( data );});
};

</script>
JS
	puts js
end
