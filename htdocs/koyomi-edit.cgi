#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190516, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require 'date'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
@tdiv_set = [ 'breakfast', 'lunch', 'dinner', 'supple', 'memo' ]


#==============================================================================
#DEFINITION
#==============================================================================
def meals( e, lp, uname )
	mb_html = "<table class='table table-sm table-hover'>"
	mb_html << "<thead>"
	mb_html << "<tr>"
	mb_html << "<td>#{lp[8]}</td>"
	mb_html << "<td>#{lp[9]}</td>"
	mb_html << "<td>#{lp[10]}</td>"
	mb_html << "<td></td>"
	mb_html << "</tr>"
	mb_html << "</thead>"

	a = e['koyomi'].split( "\t" )
	c = 0
	a.each do |ee|
		aa = ee.split( ':' )
		item_name = ''
		onclick = ''
		if aa[0] == '?-'
			item_name = "何か食べた（小盛）"
		elsif aa[0] == '?--'
			item_name = "何か食べた（微盛）"
		elsif aa[0] == '?='
			item_name = "何か食べた（並盛）"
		elsif aa[0] == '?+'
			item_name = "何か食べた（大盛）"
		elsif aa[0] == '?++'
			item_name = "何か食べた（特盛）"
		elsif /\-m\-/ =~ aa[0]
			rr = mariadb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{aa[0]}';", false )
			item_name = rr.first['name']
			onclick = ""
		elsif /\-f\-/ =~ aa[0]
			rr = mariadb( "SELECT name FROM #{$MYSQL_TB_FCS} WHERE code='#{aa[0]}';", false )
			item_name = rr.first['name']
			onclick = " onclick=\"modifyKoyomif( '#{aa[0]}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[3]}', '#{c}' )\""
		elsif /\-/ =~ aa[0]
			rr = mariadb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{aa[0]}';", false )
			item_name = rr.first['name']
			onclick = " onclick=\"modifyKoyomi( '#{aa[0]}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[3]}', '#{aa[1]}', '#{aa[2]}', '#{c}' )\""
		else
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}';"
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}' AND user='#{uname}';" if /^U\d{5}/ =~ aa[0]
			rr = mariadb( q, false )
			item_name = rr.first['name']
			onclick = " onclick=\"modifyKoyomi( '#{aa[0]}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[3]}', '#{aa[1]}', '#{aa[2]}', '#{c}' )\""
		end
		mb_html << "<tr>"
		mb_html << "<td#{onclick}>#{item_name}</td>"

		if /\-f\-/ =~ aa[0] || aa[0] == '?-' || aa[0] == '?=' || aa[0] == '?+' || aa[0] == '?++'  || aa[0] == '?--'
			mb_html << "<td#{onclick}>-</td>"
		else
			mb_html << "<td#{onclick}>#{aa[1]}#{aa[2]}</td>"
		end

		if aa[3] == '99'
			mb_html << "<td#{onclick}>-</td>"
		else
			mb_html << "<td#{onclick}>#{aa[3]}:00</td>"
		end

		mb_html << "<td><button class='btn btn-sm btn-outline-danger' onclick=\"deleteKoyomi_BW2( '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[0]}', '#{c}' )\">削除</button></td>"
		mb_html << '</tr>'
		c += 1
	end
	mb_html << '</table>'

	return mb_html
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomi-edit', language )
if @debug
	puts "uname:#{uname}<br>\n"
	puts "status:#{status}<br>\n"
	puts "aliaseu:#{aliaseu}<br>\n"
	puts "language:#{language}<br>\n"
	puts "<hr>\n"
end


#### Getting POST
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
tdiv = cgi['tdiv'].to_i
code = cgi['code']
memo = cgi['memo']
order = cgi['order'].to_i
if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "tdiv:#{tdiv}<br>\n"
	puts "code:#{code}<br>\n"
	puts "memo:#{memo}<br>\n"
	puts "order:#{order}<br>\n"
	puts "<hr>\n"
end


#### Delete
if command == 'delete'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
	a = r.first['koyomi'].split( "\t" )
	new_meal = ''
	a.size.times do |c|
		new_meal << "#{a[c]}\t" if c != order
	end
	new_meal.chop!

	mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{new_meal}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false )
	mariadb( "DELETE FROM #{$MYSQL_TB_FCS} WHERE user='#{uname}' AND code='#{code}';", false ) 	if /\-f\-/ =~ code
end

#### Updating memo
if command == 'memo'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", false )
	if r.first
		mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{memo}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", false )
	else
		mariadb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET fix='', koyomi='#{memo}', user='#{uname}', date='#{yyyy}-#{mm}-#{dd}', tdiv='4';", false )
	end
end


#### Deleting empty entry
mariadb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND ( koyomi='' OR koyomi IS NULL OR DATE IS NULL );", false )


####
koyomi_html = []
r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
r.each do |e|
	if e['tdiv'] == 4
		koyomi_html[e['tdiv']] = e['koyomi']
	else
		koyomi_html[e['tdiv']] = meals( e, lp, uname )
	end

end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{yyyy} / #{dd} / #{dd}</h5></div>
		<div class='col-8'></div>
		<div class='col-1'>
			<button class='btn btn-sm btn-success' onclick="editKoyomiR_BW1( '#{yyyy}', '#{mm}' )">#{lp[7]}</button>
		</div>
	</div>
	<div class='row'>
		<div class='col-6'>
			<h5>#{lp[1]}</h5>
			#{koyomi_html[0]}
			<button class='btn btn-sm btn-primary' onclick="fixKoyomi( 'init', '#{yyyy}', '#{mm}', '#{dd}', 0 )">＋</button>
		</div>
		<div class='col-6'>
			<h5>#{lp[2]}</h5>
			#{koyomi_html[1]}
			<button class='btn btn-sm btn-primary' onclick="fixKoyomi( 'init', '#{yyyy}', '#{mm}', '#{dd}', 1 )">＋</button>
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-6'>
			<h5>#{lp[3]}</h5>
			#{koyomi_html[2]}
			<button class='btn btn-sm btn-primary' onclick="fixKoyomi( 'init', '#{yyyy}', '#{mm}', '#{dd}', 2 )">＋</button>
		</div>
		<div class='col-6'>
			<h5>#{lp[4]}</h5>
			#{koyomi_html[3]}
			<button class='btn btn-sm btn-primary' onclick="fixKoyomi( 'init', '#{yyyy}', '#{mm}', '#{dd}', 3 )">＋</button>
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-1'>
			<br>
			<h5>メモ</h5>
		</div>
		<div class='col-10'>
			<textarea class="form-control" id="memo" rows="2">#{koyomi_html[4]}</textarea>
		</div>
		<div class='col-1'>
			<br>
			<button class='btn btn-sm btn-outline-primary' onclick="memoKoyomi( '#{yyyy}', '#{mm}', '#{dd}' )">#{lp[11]}</button>
		</div>
	</div>
</div>

HTML

puts html
