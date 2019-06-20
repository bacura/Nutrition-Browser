# Config module for FCTB Palette 0.00
#encoding: utf-8

#### パレットリスト表示
def listing( uname )
	query = "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';"
	db_err = 'SELECT palette'
	res = db_process( query, db_err, false )

	# 操作ボタン準備
	list_body = ''
	res.each do |e|
		list_body << "<tr><td>#{e['name']}</td><td>#{e['count']}</td>"
		list_body << "<td><button class='btn btn-outline-primary btn-sm' type='button' onclick='palette_cfg( \"edit_palette\", \"#{e['name']}\" )'>編集</button></td>"
		list_body << "<td>"
		list_body << "<input type='checkbox' id=\"#{e['name']}\">&nbsp;<button class='btn btn-outline-danger btn-sm' type='button' onclick='palette_cfg( \"delete_palette\", \"#{e['name']}\" )'>削除</button></td></tr>\n" unless e['name'] == '簡易表示用'
		list_body << "</td></tr>"
	end

	html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-10'><h5>カスタム成分パレット一覧</h5></div>
		<div class='col-2'><button class="btn btn-outline-primary btn-sm" type="button" onclick="palette_cfg( 'new_palette' )">新規登録</button></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
		<tr>
			<td>パレット名</td>
			<td>成分数</td>
			<td>操作</td>
			<td></td>
		</tr>
	</thead>
	#{list_body}

	</table>
</div>
HTML

	return html
end


#### モジュールメイン
def config_module( cgi )
	uname, uid, status = login_check( cgi )
	step = cgi['step']
	html = ''

	case step
	when 'list'
		html = listing( uname )

	when 'new_palette', 'edit_palette'
		checked = []
		if step == 'edit_palette'
			query = "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{uname}' AND name='#{cgi['palette_name']}';"
			db_err = 'SELECT palette'
			res = db_process( query, db_err, false )
			palette = res.first['palette']
			palette.size.times do |c|
				if palette[c] == '1'
					checked << 'checked'
				else
					checked << ''
				end
			end
		end

		# 食品成分HTML準備
		fc_table = ['', '', '', '', '', '', '']
		4.upto( 7 ) do |i| fc_table[0] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		8.upto( 20 ) do |i| fc_table[1] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		21.upto( 34 ) do |i| fc_table[2] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		35.upto( 46 ) do |i| fc_table[3] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		47.upto( 55 ) do |i| fc_table[4] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		56.upto( 67 ) do |i| fc_table[5] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end

		html = <<-"HTML"
	<div class="container-fluid">
		<div class="row">
			<div class="col-6">
				<div class="input-group mb-3">
  					<div class="input-group-prepend"><span class="input-group-text">パレット名</span></div>
  					<input type="text" class="form-control" id="palette_name" value="#{cgi['palette_name']}" maxlength="60">
  				</div>
			</div>
			<div class="col-5"></div>
			<div class="col-1"><button class="btn btn-outline-primary btn-sm" type="button" onclick="palette_cfg( 'regist' )">登録</button></div>
		</div>
		<br>
		<div class="row">
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[0]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[1]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[2]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[3]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[4]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[5]}</table></div>
		</div>
	</div>
HTML

	when 'regist'
		fct_bits = '0000'
		fct_count = 0
		palette_name = cgi['palette_name']

		4.upto( 67 ) do |i|
			fct_bits << cgi[$FCT_ITEM[i]].to_i.to_s
			fct_count += 1 if cgi[$FCT_ITEM[i]] == '1'
		end

		# パレット名チェック
		query = "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE name='#{palette_name}' AND user='#{uname}';"
		db_err = 'select PALETTE'
		res = db_process( query, db_err, false )

		if res.first
			# 更新
			query = "UPDATE #{$MYSQL_TB_PALETTE} SET palette='#{fct_bits}', count='#{fct_count}' WHERE name='#{palette_name}' AND user='#{uname}';"
			db_err = 'select PALETTE'
			db_process( query, db_err, false )
		else
			# 追加
			query = "INSERT INTO #{$MYSQL_TB_PALETTE} SET name='#{palette_name}', user='#{uname}', palette='#{fct_bits}', count='#{fct_count}';"
			db_err = 'select PALETTE'
			db_process( query, db_err, false )
		end

		html = listing( uname )

	when 'delete_palette'
		query = "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE name='#{cgi['palette_name']}' AND user='#{uname}';"
		db_err = 'DELETE PALETTE'
		db_process( query, db_err, false )

		html = listing( uname )
	end

	return html
end