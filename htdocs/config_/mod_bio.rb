# Config module for NB bio 0.00
#encoding: utf-8

def bio_module( cgi )
	uname, uid, status = login_check( cgi )
	step = cgi['step']

	res = mdb( "SELECT * FROM #{$MYSQL_TB_BIO} WHERE user='#{uname}';", false, false )
	aliasu = res.first['aliasu']
	mail = res.first['mail']
	pass = res.first['pass']

	if step ==  'change'
		new_mail = cgi['new_mail']
		new_aliasu = cgi['new_aliasu']
		old_password = cgi['old_password']
		new_password1 = cgi['new_password1']
		new_password2 = cgi['new_password2']

		if pass == old_password
			mail = new_mail if new_mail != '' && new_mail != nil
			aliasu = new_aliasu if new_aliasu != '' && new_aliasu != nil
			if new_password1 == new_password2
				pass = new_password1 if new_password1 != '' && new_password1 != nil
			end

			# アカウント内容変更の保存
			mdb( "UPDATE #{$MYSQL_TB_USER} SET pass='#{pass}', mail='#{mail}', aliasu='#{aliasu}' WHERE user='#{uname}' AND cookie='#{uid}';", false, false )
		else
			puts "<span class='msg_small_red'>現在のパスワードが違うので、保存されませんでした。</span><br>"
		end
	end
	html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-2'>性別</div>
			<div class='col-4'><input type="text" maxlength="60" id="new_aliasu" class="form-control login_input" placeholder="二つ名" value="#{aliasu}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>生年月日</div>
			<div class='col-4'><input type="email" maxlength="60" id="new_mail" class="form-control login_input" placeholder="メールアドレス" value="#{mail}"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>身長(cm)</div>
			<div class='col-4'><input type="text" maxlength="30" id="new_password1" class="form-control login_input" placeholder="新しいパスワード (30文字まで)"></div>
		</div>

    	<div class='row'>
	    	<div class='col-2'>体重(kg)</div>
			<div class='col-4'><input type="text" maxlength="30" id="new_password2" class="form-control login_input" placeholder="新しいパスワード（確認）"></div>
		</div>

		<hr>

    	<div class='row'>
    		現在のパスワードを入力して保存してください。<br>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-2'>自動更新</div>
			<div class='col-4'><input type="password" id="old_password" class="form-control login_input" placeholder="現在のパスワード" required></div>
		</div>
    	<div class='row'>
	    	<div class='col-2'></div>
			<div class='col-4'><button type="button" class="btn btn-outline-warning btn-sm nav_button" onclick="account_cfg( 'change' )">保存</button></div>
		</div>
	</div>
HTML
	return html
end