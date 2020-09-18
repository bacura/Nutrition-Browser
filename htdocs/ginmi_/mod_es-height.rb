# Ginmi module for Estimated height 0.00
#encoding: utf-8

def ginmi_module( cgi, user )
	module_js()

	command = cgi['command']
	html = ''

	case command
	when 'form'
		sex = 0
		age = 18
		knee_height = 0

		sex_select = []
		if sex = 0
			sex_select[0] = 'SELECTED'
		else
			sex_select[1] = 'SELECTED'
		end


html = <<-"HTML"
		<div class='row'>
		<h5>推定身長 計算フォーム（Knee height法）</h5>
		</div>
		<br>

		<div class='row'>
			<div class='col-3'>
				<div class="input-group input-group-sm">
					<label class="input-group-text">身体的性別</label>
					<select class="form-select form-select-sm" id="sex">
						<option value='0' #{sex_select[0]}>男性</option>
						<option value='1' #{sex_select[1]}>女性</option>
					</select>
				</div>
			</div>

			<div class='col-3'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>年齢</span>
					<input type='number' class='form-control' id='age' min='18' value='#{age}'>
				</div>
			</div>

			<div class='col-3'>
				<div class='input-group input-group-sm'>
					<span class='input-group-text'>膝下高(cm)</span>
					<input type='text' class='form-control' id='knee_height' value='#{knee_height}'>
				</div>
			</div>

		</div>
		<br>

		<div class='row'>
			<div class='col-2'>
				<button class='btn btn-sm btn-primary' onclick="Calculate()">計算</button>
			</div>
		</div>
HTML
	when 'result'
		sex = cgi['sex'].to_i
		age = cgi['age'].to_i
		knee_height = BigDecimal( cgi['knee_height'] )

		if false
			puts "sex:#{sex}<br>\n"
			puts "age:#{age}<br>\n"
			puts "knee_height:#{knee_height}<br>\n"
			puts "<hr>\n"
		end

		result = 0.0
		formula = ''
		if sex == 0
			result = ( 64.19 - 0.04 * age + 2.02 * knee_height ).round( 1 )
			formula = "64.19 - 0.04 * #{age} + 2.02 * #{knee_height.to_f} "
		else
			result = ( 84.88 - 0.24 * age + 1.83 * knee_height ).round( 1 )
			formula = "84.88 - 0.24 * #{age} + 1.83 * #{knee_height.to_f}"
		end

html = <<-"HTML"
		<div class='row'>
			<div class='col-3'>推定身長(cm)</div>
			<div class='col-2'>#{result.to_f}</div>
			<div class='col-1'>計算式</div>
			<div class='col-6'>#{formula}</div>
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
// Ginmi Estimated height //////////////////////////////////////////////////////////////

var Calculate = function(){
	var sex = document.getElementById( "sex" ).value;
	var age = document.getElementById( "age" ).value;
	var knee_height = document.getElementById( "knee_height" ).value;
	$.post( "ginmi.cgi", { mod:"es-height", command:'result', age:age, sex:sex, knee_height:knee_height }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};

</script>
JS
	puts js
end
