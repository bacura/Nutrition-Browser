# Config module for NB bio 0.00
#encoding: utf-8

def config_module( cgi )
	uname, uid, status = login_check( cgi )
	step = cgi['step']

	r = mdb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, false )
	sex = r.first['sex'].to_i
	age = r.first['age'].to_i
	height = r.first['height'].to_f
	weight = r.first['weight'].to_f

	if step ==  'change'
		sex = cgi['sex'].to_i
		age = cgi['age'].to_i
		height = cgi['height'].to_f
		weight = cgi['weight'].to_f

		# アカウント内容変更の保存
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET sex='#{sex}', age='#{age}', height='#{height}', weight='#{weight}' WHERE user='#{uname}';", false, false )
	end

	male_check = ''
	female_check = ''
	if sex == 0
		male_check = 'CHECKED'
	else
		female_check = 'CHECKED'
	end

	html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-2'>代謝的性別</div>
			<div class='col-3'>
				<div class='form-check form-check-inline'>
					<input class='form-check-input' type='radio' name='sex' id='male' value='0' #{male_check}>
					<label class='form-check-label' for='male'>男性</label>
				</div>
				<div class='form-check form-check-inline'>
					<input class='form-check-input' type='radio' name='sex' id='female' value='1' #{female_check}>
					<label class='form-check-label' for='female'>女性</label>
				</div>
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-2'>年齢</div>
			<div class='col-3'><input type="number" min="0" id="age" class="form-control login_input" value="#{age}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>身長(m)</div>
			<div class='col-3'><input type="text" maxlength="5" id="height" class="form-control login_input" value="#{height}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>体重(kg)</div>
			<div class='col-3'><input type="text" maxlength="5" id="weight" class="form-control login_input" value="#{weight}"></div>
		</div>

		<hr>

    	<div class='row'>
	    	<div class='col-2'></div>
			<div class='col-4'><button type="button" class="btn btn-outline-warning btn-sm nav_button" onclick="bio_cfg( 'change' )">保存</button></div>
		</div>
	</div>
HTML
	return html
end

