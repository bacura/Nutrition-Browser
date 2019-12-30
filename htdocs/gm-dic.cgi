#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser GM food alias dictionary editor 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20180508, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'gm-dic', language )

html_init( nil )
if @debug
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "aliasu: #{aliasu}<br>"
	puts "language: #{language}<br>"
	puts "<hr>"
end


#### GM check
if status < 8
	puts "GM error."
	exit
end


#### POSTデータの取得
command = cgi['command']
org_name = cgi['org_name']
tn = cgi['tn']
aliases = cgi['aliases']
if @debug
	puts "command:#{command}<br>\n"
	puts "org_name:#{org_name}<br>\n"
	puts "aliases:#{aliases}<br>\n"
	puts "<hr>\n"
end

list_html = ''
case command
when 'save'
	# オリジナル以外の旧データを削除
	mdb( "DELETE FROM #{$MYSQL_TB_DIC} WHERE org_name='#{org_name}' AND tn='0';", false, @debug )

	# オリジナル以外の新データを登録
	aliases.gsub!( '、', ',' )
	aliases.gsub!( '，', ',' )
	a = aliases.split( ',' ).uniq

	a.each do |e|
		unless e == org_name
			mdb( "INSERT INTO #{$MYSQL_TB_DIC} SET tn='0', org_name='#{org_name}', alias='#{e}', user='#{uname}';", false, @debug )
		end
	end
	list_html = 'ok'
else
	r = mdb( "SELECT DISTINCT tn, org_name FROM #{$MYSQL_TB_DIC} WHERE tn !='0';", false, @debug )

	r.each do |e|
		rr = mdb( "SELECT tn, alias from #{$MYSQL_TB_DIC} WHERE org_name='#{e['org_name']}';", false, @debug )
		list_html << "<div class='row'>"
		list_html << "<div class='col-2'>"
		list_html << "#{e['org_name']}"
		list_html << '</div>'
		list_html << "<div class='col-10'>"
		alias_value = ''
		rr.each do |ee|
			alias_value << "#{ee['alias']},"
		end
		alias_value.chop!
		list_html << "<input type='text' class='form-control' id=\"tn#{e['tn']}\" value='#{alias_value}' onchange=\"saveDic_BWL1( '#{e['org_name']}', '#{e['tn']}' )\">"
		list_html << '</div>'
		list_html << '</div>'
	end
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col'><h5>#{lp[1]}: </h5></div>
	</div><br>

	#{list_html}
	<div class='row'>
		<div class='col-10'></div>
		<div class='col-2' align='center'>
<!--			<a href='gm-export.cgi?extag=dic' download='dic.txt'><button type='button' class='btn btn-outline-primary'>エクスポート</button></a>-->
		</div>
	</div>
HTML

puts html
