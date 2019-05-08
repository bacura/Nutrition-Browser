# Config module for FCTB release 0.00
#encoding: utf-8

def config_module( cgi )
	uname, uid, status = login_check( cgi )
	step = cgi['step']
	password = cgi['password']
	html =''

	if step ==  ''
		html = <<-"HTML"
      	<div class="container">
      		<div class='row'>
	    		ユーザー登録を解除する場合は、パスワードを入力し登録解除ボタンを押してください。<br>
    			登録抹消ボタンを押すと、即時ユーザー登録の解除と蓄積データの消去が行われます。<br>
				消去されたデータを復元する手段はございません。<br>
			</div><br>
      		<div class='row'>
				<div class='col-4'><input type="password" id="password" class="form-control login_input" placeholder="パスワード"></div>
				<div class='col-4'><button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="release_cfg( 'release' )">登録解除</button></div>
			</div>
		</div>
HTML
	else
		html = <<-"HTML"
      	<div class="container">
      		<div class='row'>
	    		ユーザー登録を解除しました。ご利用ありがとうございました。
			</div>
		</div>
HTML

		# ユーザーステータスの変更
		query = "UPDATE #{$MYSQL_TB_USER} SET status='0' WHERE user='#{uname}' AND cookie='#{uid}';"
		db_err = 'SELECT user'
		db_process( query, db_err, false )

		# ヒストリーデータのの削除
		query = "DELETE FROM #{$MYSQL_TB_HIS} WHERE user='#{uname}';"
		db_err = 'SELECT his'
		db_process( query, db_err, false )

		# SUMデータのの削除
		query = "DELETE FROM #{$MYSQL_TB_SUM} WHERE user='#{uname}';"
		db_err = 'SELECT sum'
		db_process( query, db_err, false )

		# コンフィグデータのの削除
		query = "DELETE FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';"
		db_err = 'SELECT cfg'
		db_process( query, db_err, false )

		# mealデータのの削除
		query = "DELETE FROM #{$MYSQL_TB_MEAL} WHERE user='#{uname}';"
		db_err = 'SELECT meal'
		db_process( query, db_err, false )

		# マスター価格データの削除
		query = "DELETE FROM #{$MYSQL_TB_PRICEM} WHERE user='#{uname}';"
		db_err = 'SELECT pricem'
		db_process( query, db_err, false )

		# パレットデータの削除
		query = "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';"
		db_err = 'SELECT palette'
		db_process( query, db_err, false )
	end
	return html
end
