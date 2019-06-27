# Config module for Nutorition browser koyomiex 0.00
#encoding: utf-8

def config_module( cgi )
	uname, uid, status, aliasu, language = login_check( cgi )
	step = cgi['step']
	del_no = cgi['del_no'].to_i
	item_set = [cgi['item0'], cgi['item1'], cgi['item2'], cgi['item3'], cgi['item4'], cgi['item5'], cgi['item6'], cgi['item7'], cgi['item8'], cgi['item9']]
	if $DEBUG
		puts "step: #{step}<br>"
		puts "del_no: #{del_no}<br>"
		puts "item_set: #{item_set[0]}<br>"
		puts "<hr>"
	end


	case step
	when 'update'
		0.upto( 9 ) do |c|//
			item_set[c] == "\t" if cgi["item#{c}"] == ""
		end
		mariadb( "UPDATE #{$MYSQL_TB_CFG} SET koyomiex='#{item_set.join( ':' )}' WHERE user='#{uname}';", false )

	when 'delete'
		r = mariadb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
		item_set = r.first['koyomiex'].split( ':' )
		0.upto( 9 ) do |c|//
			if del_no == c
				item_set[c] = "\t"
				mariadb( "UPDATE #{$MYSQL_TB_CFG} SET koyomiex='#{item_set.join( ':' )}' WHERE user='#{uname}';", false )
				mariadb( "UPDATE #{$MYSQL_TB_KOYOMIEX} SET item#{c}='' WHERE user='#{uname}';", false )
				item_set[c] = '' if item_set[c] == "\t"
			end
		end

	else
		r = mariadb( "SELECT koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false )
		if r.first['koyomiex'] == '' || r.first['koyomiex'] == nil
			mariadb( "UPDATE #{$MYSQL_TB_CFG} SET koyomiex='\t:\t:\t:\t:\t:\t:\t:\t:\t:\t' WHERE user='#{uname}';", false )
		else
			item_set = r.first['koyomiex'].split( ':' )
			0.upto( 9 ) do |c|
				item_set[c] = '' if item_set[c] == "\t"
			end
		end
	end


	html = '<div class="container">'
	html << "<h5>こよみ拡張・項目設定:</h5><br>"

	0.upto( 9 ) do |c|
		html << "<div class='row'>"
		html << "<div class='col-2'>項目名#{c}</div>"
		html << "<div class='col-3'><input type='text' maxlength='32' id='item#{c}' class='form-control form-control-sm' value='#{item_set[c]}'></div>"
		html << "<div class='col-1'></div>"
		html << "<div class='col-2'><input type='checkbox' id='kex_del#{c}'>&nbsp;<button type='button' class='btn btn-outline-danger btn-sm' onclick=\"koyomiex_cfg( 'delete', 'kex_del#{c}', '#{c}' )\">初期化</button></div>"
		html << "</div><br>"
	end

  	html << "<div class='row'>"
	html << "<div class='col-2'></div>"
	html << "<div class='col-4'><button type='button' class='btn btn-outline-warning btn-sm nav_button' onclick=\"koyomiex_cfg( 'update' )\">保存</button></div>"
	html << "</div>"
	html << "</div>"

	return html
end
