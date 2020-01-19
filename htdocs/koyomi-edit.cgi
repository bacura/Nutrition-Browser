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
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
@tdiv_set = [ 'breakfast', 'lunch', 'dinner', 'supple', 'memo' ]

@size_max = 20000000
@tn_size = 400
@tns_size = 40
@photo_size_max = 2000


#==============================================================================
#DEFINITION
#==============================================================================
def meals( e, lp, uname, freeze_flag )
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

#### Temporary ####
	if aa[2] == 'g'
		aa[2] == 0
	elsif aa[2] == '%'
		aa[2] == 99
	end
#### Temporary ####

	if aa[2].to_i == 99
		unit = '%'
	else
		unit = $UNIT[aa[2].to_i]
	end

		item_name = ''
		onclick = ''
		if aa[0] == '?-'
			item_name = lp[21]
		elsif aa[0] == '?--'
			item_name = lp[22]
		elsif aa[0] == '?='
			item_name = lp[23]
		elsif aa[0] == '?+'
			item_name = lp[24]
		elsif aa[0] == '?++'
			item_name = lp[25]
		elsif /\-m\-/ =~ aa[0]
			rr = mdb( "SELECT name FROM #{$MYSQL_TB_MENU} WHERE code='#{aa[0]}';", false, @debug )
			item_name = rr.first['name']
			onclick = ""
		elsif /\-f\-/ =~ aa[0]
			rr = mdb( "SELECT name FROM #{$MYSQL_TB_FCS} WHERE code='#{aa[0]}';", false, @debug )
			item_name = rr.first['name']
			onclick = " onclick=\"modifyKoyomif( '#{aa[0]}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[3]}', '#{c}' )\"" if freeze_flag == 0
		elsif /\-/ =~ aa[0]
			rr = mdb( "SELECT name FROM #{$MYSQL_TB_RECIPE} WHERE code='#{aa[0]}';", false, @debug )
			item_name = rr.first['name']
			onclick = " onclick=\"modifyKoyomi( '#{aa[0]}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[3]}', '#{aa[1]}', '#{aa[2]}', '#{c}' )\"" if freeze_flag == 0
		else
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}';"
			q = "SELECT name FROM #{$MYSQL_TB_TAG} WHERE FN='#{aa[0]}' AND user='#{uname}';" if /^U\d{5}/ =~ aa[0]
			rr = mdb( q, false, @debug )
			item_name = rr.first['name']
			onclick = " onclick=\"modifyKoyomi( '#{aa[0]}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[3]}', '#{aa[1]}', '#{aa[2]}', '#{c}' )\"" if freeze_flag == 0
		end
		mb_html << "<tr>"
		mb_html << "<td#{onclick}>#{item_name}</td>"

		if /\-f\-/ =~ aa[0] || aa[0] == '?-' || aa[0] == '?=' || aa[0] == '?+' || aa[0] == '?++'  || aa[0] == '?--'
			mb_html << "<td#{onclick}>-</td>"
		elsif /\-m\-/ =~ aa[0] || /\-/ =~ aa[0]
			mb_html << "<td#{onclick}>#{aa[1]}&nbsp;#{unit}</td>"
		else
			uw = ''
			uw = "&nbsp;(#{unit_weight( aa[1], aa[2], aa[0] ).to_f} g)" if aa[2] != '0'
			mb_html << "<td#{onclick}>#{aa[1]}&nbsp;#{unit}#{uw}</td>"
		end

		if aa[3] == '99'
			mb_html << "<td#{onclick}>-</td>"
		else
			mb_html << "<td#{onclick}>#{aa[3]}:00</td>"
		end

		if freeze_flag == 0
			mb_html << "<td><button class='btn btn-sm btn-outline-danger' onclick=\"deleteKoyomi_BW2( '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[0]}', '#{c}' )\">削除</button></td>"
		else
			mb_html << "<td></td>"
		end
		mb_html << '</tr>'
		c += 1
	end
	mb_html << '</table>'

	return mb_html
end


# Getting start year & standard meal time
def get_starty( uname )
	start_year = $TIME_NOW.year
	breakfast_st = 0
	lunch_st = 0
	dinner_st = 0
	r = mdb( "SELECT koyomiy FROM #{$MYSQL_TB_CFG} WHERE user='#{uname}';", false, @debug )
	if r.first['koyomiy']
		a = r.first['koyomiy'].split( ':' )
		start_year = a[0].to_i if a[0].to_i != 0
		breakfast_st = a[1].to_i if a[1].to_i != 0
		lunch_st = a[2].to_i if a[2].to_i != 0
		dinner_st = a[3].to_i if a[3].to_i != 0
	end
	st_set = [ breakfast_st, lunch_st, dinner_st ]

	return start_year, st_set
end

#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status, aliaseu, language = login_check( cgi )
lp = lp_init( 'koyomi-edit', language )
start_year, st_set = get_starty( uname )
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
hh = cgi['hh'].to_i
tdiv = cgi['tdiv'].to_i
code = cgi['code']
memo = cgi['memo']
order = cgi['order'].to_i
some = cgi['some']

if @debug
	puts "command:#{command}<br>\n"
	puts "yyyy:#{yyyy}<br>\n"
	puts "mm:#{mm}<br>\n"
	puts "dd:#{dd}<br>\n"
	puts "hh:#{hh}<br>\n"
	puts "tdiv:#{tdiv}<br>\n"
	puts "code:#{code}<br>\n"
	puts "memo:#{memo}<br>\n"
	puts "order:#{order}<br>\n"
	puts "some: #{some}<br>\n"
	puts "<hr>\n"
end


#### Delete
if command == 'delete'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
	a = r.first['koyomi'].split( "\t" )
	new_meal = ''
	a.size.times do |c|
		new_meal << "#{a[c]}\t" if c != order
	end
	new_meal.chop!

	mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{new_meal}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
	mdb( "DELETE FROM #{$MYSQL_TB_FCS} WHERE user='#{uname}' AND code='#{code}';", false, @debug ) 	if /\-f\-/ =~ code
end


#### Updating memo
if command == 'memo'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", false, @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{memo}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET fzcode='', freeze='0', koyomi='#{memo}', user='#{uname}', date='#{yyyy}-#{mm}-#{dd}', tdiv='4';", false, @debug )
	end
end


#### Saving Something
if command == 'some'
	hh = st_set[tdiv] if hh == 99
	koyomi = "#{some}:100:99:#{hh}"
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug)
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug)
	else
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{uname}', fzcode='', freeze='0', koyomi='#{koyomi}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", false, @debug)
	end
end


#### Deleting empty entry
mdb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND freeze=0 AND ( koyomi='' OR koyomi IS NULL OR DATE IS NULL );", false, @debug )


####
freeze_flag = 0
koyomi_html = []
r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
freeze_flag = r.first['freeze'].to_i if r.first

r.each do |e|
	if e['tdiv'] == 4
		koyomi_html[e['tdiv']] = e['koyomi']
	else
		koyomi_html[e['tdiv']] = meals( e, lp, uname, freeze_flag )
	end
end


####
some_html = [ '', '', '', '' ]
if freeze_flag == 0
	0.upto( 3 ) do |c|
		some_html[c] = <<-"SOME"
		<select class='custom-select custom-select-sm' id='some#{c}' onchange="koyomiSaveSome( '#{yyyy}', '#{mm}', '#{dd}', #{c}, 'some#{c}' )">
			<option value='' selected>#{lp[20]}</option>
			<option value='?--'>#{lp[15]}</option>
			<option value='?-'>#{lp[12]}</option>
			<option value='?='>#{lp[13]}</option>
			<option value='?+'>#{lp[14]}</option>
			<option value='?++'>#{lp[16]}</option>
		</select>
SOME
	end
end

####
cmm_html = [ '', '', '', '' ]
if freeze_flag == 0
	0.upto( 3 ) do |c|
			cmm_html[c]	<< "<button class='btn btn-sm btn-dark' onclick=\"fixKoyomi( 'init', '#{yyyy}', '#{mm}', '#{dd}', '#{c}' )\">#{lp[17]}</button>&nbsp;"
		if koyomi_html[c] == nil
			cmm_html[c] << "<button class='btn btn-sm btn-secondary'>#{lp[18]}</button>&nbsp;"
			cmm_html[c] << "<button class='btn btn-sm btn-secondary'>#{lp[19]}</button>&nbsp;"
		else
			cmm_html[c] << "<button class='btn btn-sm btn-primary' onclick=\"cmmKoyomi( 'copy', '#{yyyy}', '#{mm}', '#{dd}', #{c} )\">#{lp[18]}</button>&nbsp;"
			cmm_html[c] << "<button class='btn btn-sm btn-primary' onclick=\"cmmKoyomi( 'move', '#{yyyy}', '#{mm}', '#{dd}', #{c} )\">#{lp[19]}</button>&nbsp;"
		end
	end
end


####
photo_html = [ '', '', '', '' ]
if freeze_flag == 0
	0.upto( 3 ) do |c|
		photo_html[c] = <<-"PHOTO"
		<form class='row' method="post" enctype="multipart/form-data" id='photo_form'>
			<div class='col'>
				<div class="form-group">
					<label for="photom">####</label>
					<input type="file" name="photo1" id="photom" class="custom-control-file" onchange="">
				</div>
				<img src="" width="100px" class="img-thumbnail"><br>
				<br>
			</div>
		</form>
PHOTO
	end
end


####
memo_html = ''
if freeze_flag == 0
	memo_html = <<-"MEMO1"
	<div class='col-10'>
		<textarea class='form-control' id='memo' rows='2'>#{koyomi_html[4]}</textarea>
	</div>
	<div class='col-1'><br>
		<button class='btn btn-sm btn-outline-primary' onclick="memoKoyomi( '#{yyyy}', '#{mm}', '#{dd}' )">#{lp[11]}</button>
	</div>
MEMO1
else
	memo_html = <<-"MEMO2"
	<div class='col-10'>
		#{koyomi_html[4]}
	</div>
MEMO2
end


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{yyyy} / #{mm} / #{dd}</h5></div>
		<div class='col-8'></div>
		<div class='col-1'>
			<button class='btn btn-sm btn-success' onclick="editKoyomiR_BW1( '#{yyyy}', '#{mm}' )">#{lp[7]}</button>
		</div>
	</div>
	<div class='row'>
		<div class='col-6'>
			<h5>#{lp[1]}</h5>
			#{koyomi_html[0]}
			<div class="form-inline">
				#{cmm_html[0]}
				#{some_html[0]}
			</div>
			<br><br>
			#{photo_html[0]}
		</div>
		<div class='col-6'>
			<h5>#{lp[2]}</h5>
			#{koyomi_html[1]}
			<div class="form-inline">
				#{cmm_html[1]}
				#{some_html[1]}
			</div>
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-6'>
			<h5>#{lp[3]}</h5>
			#{koyomi_html[2]}
			<div class="form-inline">
				#{cmm_html[2]}
				#{some_html[2]}
			</div>
		</div>
		<div class='col-6'>
			<h5>#{lp[4]}</h5>
			#{koyomi_html[3]}
			<div class="form-inline">
				#{cmm_html[3]}
				#{some_html[3]}
			</div>
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-1'>
			<br>
			<h5>メモ</h5>
		</div>
		#{memo_html}
	</div>
</div>

HTML

puts html
