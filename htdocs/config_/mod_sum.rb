# Config module for FCTB sum 0.00
#encoding: utf-8

def config_module( cgi )
	uname, uid, status = login_check( cgi )
	step = cgi['step']

	if step == 'reset'
		query = "UPDATE sum set sum='', name='', code='' WHERE user='#{uname}';"
		db_err = 'UPDATE sum'
		db_process( query, db_err, false )
	end
	html = <<-"HTML"
     <div class="container">
      	<div class='row'>
    		まな板を初期化する場合は、まな板初期化ボタンを押してください。<br>
    	</div><br>
		<button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="sum_cfg( 'reset' )">まな板初期化</button>
	</div>
HTML
	return html
end