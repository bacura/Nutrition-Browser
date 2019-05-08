# Config module for FCTB history 0.00
#encoding: utf-8

def config_module( cgi )
	uname, uid, status = login_check( cgi )
	step = cgi['step']

	if step == 'clear'
		query = "UPDATE his set his='' WHERE user='#{uname}';"
		db_err = 'history UPDATE'
		db_process( query, db_err, false )
	end
	html = <<-"HTML"
     <div class="container">
      	<div class='row'>
    		履歴を初期化する場合は、履歴初期化ボタンを押してください。<br>
    	</div>
    	<br>
		<button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="history_cfg( 'clear' )">履歴初期化</button>
	</div>
HTML
	return html
end
