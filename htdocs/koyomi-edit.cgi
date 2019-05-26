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
$SCRIPT = 'koyomie.cgi'
$DEBUG = false
$TDIVL = [ 'breakfast', 'lunch', 'dinner', 'supple' ]

#==============================================================================
#DEFINITION
#==============================================================================
def meals( r, tdiv, lp )
	mb_html = "<table class='table table-sm table-hover'>"
	mb_html << "<thead>"
	mb_html << "<tr>"
	mb_html << "<td>#{lp[8]}</td>"
	mb_html << "<td>#{lp[9]}</td>"
	mb_html << "<td>#{lp[10]}</td>" if tdiv == 3
	mb_html << "<td></td>"
	mb_html << "</tr>"
	mb_html << "</thead>"

	a = r.first[$TDIVL[tdiv]].split( "\t" )
	a.each do |e|
		mb_html << '<tr>'
		aa = e.split( ':' )
		item_name = ''
		if /\-m\-/ =~ aa[0]
			rr = mariadb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{aa[0]}';", false )
			item_name = rr.first['name']
		elsif /\-f\-/ =~ aa[0]
			rr = mariadb( "SELECT name FROM #{$MYSQL_TB_FCS} WHERE code='#{aa[0]}';", false )
			item_name = rr.first['name']
		elsif /\-/ =~ aa[0]
			rr = mariadb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{aa[0]}';", false )
			item_name = rr.first['name']
		elsif /\?/ =~ aa[0]
			item_name = '?'
		else
			rr = mariadb( "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}';", false )
			item_name = rr.first['name']
		end
		mb_html << "<td>#{item_name}</td>"
		mb_html << "<td>#{aa[1]}#{aa[2]}</td>"
		if tdiv == 3
			if aa[3] == '99'
				mb_html << "<td>-</td>"
			else
				mb_html << "<td>#{aa[3]}:00</td>"
			end
		end

		mb_html << "<td><button class='btn btn-sm btn-outline-danger' onclick=\"deleteKoyomi_BW2( '#{r.first['date'].year}', '#{r.first['date'].month}', '#{r.first['date'].day}', '#{tdiv}', '#{aa[0]}' )\">削除</button></td>"
		mb_html << '</tr>'
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
if $DEBUG
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
if $DEBUG
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "tdiv:#{tdiv}<br>\n"
	puts "code:#{code}<br>\n"
	puts "memo:#{memo}<br>\n"
	puts "<hr>\n"
end


#### Delete
if command == 'delete'
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
	a = r.first[$TDIVL[tdiv]].split( "\t" )
	code_ = []
	vol_ = []
	unit_ = []
	hh_ = []
	a.each do |e|
		aa = e.split( ':' )
		code_ << aa[0]
		vol_ << aa[1]
		unit_ << aa[2]
		hh_ << aa[3]
	end

	new_meal = ''
	code_.size.times do |c|
		new_meal << "#{code_[c]}:#{vol_[c]}:#{unit_[c]}:#{hh_[c]}\t" if code_[c] != code
	end
	new_meal.chop!
	mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET #{$TDIVL[tdiv]}='#{new_meal}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
	mariadb( "DELETE FROM #{$MYSQL_TB_FCS} WHERE user='#{uname}' AND code='#{code}';", false ) 	if /\-f\-/ =~ code
end

#### Updating memo
if command == 'memo'
	mariadb( "UPDATE #{$MYSQL_TB_KOYOMI} SET memo='#{memo}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
end


#### Deleting empty entry
mariadb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND breakfast='' AND lunch='' AND dinner='' AND supple='' AND memo='' AND date='#{yyyy}-#{mm}-#{dd}';", false )


####
r = mariadb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false )
if r.first
 	breakfast_html = meals( r, 0, lp )
 	lunch_html = meals( r, 1, lp )
 	dinner_html = meals( r, 2, lp )
 	supple_html = meals( r, 3, lp )
 	memo = r.first['memo']
else
 	breakfast_html = ''
 	lunch_html = ''
 	dinner_html = ''
 	supple_html = ''
 	memo = ''
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{yyyy} / #{dd} / #{dd}</h5></div>
		<div class='col-8'></div>
		<div class='col-1'>
			<button class='btn btn-success' onclick="editKoyomiR_BW1( '#{yyyy}', '#{mm}' )">#{lp[7]}</button>
		</div>
	</div>
	<div class='row'>
		<div class='col-4'>
			<h5>#{lp[1]}</h5>
			#{breakfast_html}
			<button class='btn btn-sm btn-primary' onclick="fixKoyomi_BW3( 'init', '#{yyyy}', '#{mm}', '#{dd}', 0 )">＋</button>
		</div>
		<div class='col-4'>
			<h5>#{lp[2]}</h5>
			#{lunch_html}
			<button class='btn btn-sm btn-primary' onclick="fixKoyomi_BW3( 'init', '#{yyyy}', '#{mm}', '#{dd}', 1 )">＋</button>
		</div>
		<div class='col-4'>
			<h5>#{lp[3]}</h5>
			#{dinner_html}
			<button class='btn btn-sm btn-primary' onclick="fixKoyomi_BW3( 'init', '#{yyyy}', '#{mm}', '#{dd}', 2 )">＋</button>
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-6'>
			<h5>#{lp[4]}</h5>
			#{supple_html}
			<button class='btn btn-sm btn-primary' onclick="fixKoyomi_BW3( 'init', '#{yyyy}', '#{mm}', '#{dd}', 3 )">＋</button>
		</div>
		<div class='col-5'>
			<h5>メモ</h5>
			<textarea class="form-control" id="memo" rows="3">#{memo}</textarea>
		</div>
		<div class='col-1'>
			<br>
			<br>
			<br>
			<button class='btn btn-sm btn-outline-primary' onclick="memoKoyomi( '#{yyyy}', '#{mm}', '#{dd}' )">#{lp[11]}</button>
		</div>
	</div>
</div>

HTML

puts html
