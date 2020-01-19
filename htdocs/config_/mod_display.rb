# Config module for NB display 0.00
#encoding: utf-8

def config_module( cgi )
	uname, uid, status = login_check( cgi )
	step = cgi['step']

	r = mdb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, false )
	icache = r.first['icache'].to_i

	if step ==  'change'
		icache = cgi['icache'].to_i

		# アカウント内容変更の保存
#		mdb( "UPDATE #{$MYSQL_TB_CFG} SET icache='#{icache}' WHERE user='#{uname}';", false, false )
	end

	icache_check = ''
	icache_check = 'CHECKED' if icache == 1


	html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-2'>画像キャッシュ</div>
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

