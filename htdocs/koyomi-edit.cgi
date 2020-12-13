#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser koyomi edit 0.02b


#==============================================================================
# LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
# STATIC
#==============================================================================
script = 'koyomi-edit'
@debug = false
@tdiv_set = [ 'breakfast', 'lunch', 'dinner', 'supple', 'memo' ]

@size_max = 20000000
@tn_size = 400
@tns_size = 40
@photo_size_max = 2000


#==============================================================================
# DEFINITION
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
		if aa[2].to_i == 99
			unit = '%'
		else
			unit = $UNIT[aa[2].to_i]
		end

		item_name = ''
		onclick = ''
		fix_copy_button = ''
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
			if rr.first
				item_name = rr.first['name']
				origin = "#{e['date'].year}:#{e['date'].month}:#{e['date'].day}:#{e['tdiv']}:#{c}"
				onclick = " onclick=\"modifysaveKoyomiFC( '#{aa[0]}', '#{origin}' )\"" if freeze_flag == 0
				fix_copy_button = "<button class='btn btn-sm btn-primary' onclick=\"modifyKoyomif( '#{aa[0]}', '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[3]}', '#{c}' )\">編</button>&nbsp;"
			else
				item_name = "Error: #{aa[0]}"
				onclick = ''
			end
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
			mb_html << "<td>"
			mb_html << fix_copy_button unless fix_copy_button == ''
			mb_html << "<span onclick=\"deleteKoyomi( '#{e['date'].year}', '#{e['date'].month}', '#{e['date'].day}', '#{e['tdiv']}', '#{aa[0]}', '#{c}' )\">#{lp[27]}</span>"
			mb_html << "</td>"
		else
			mb_html << "<td></td>"
		end
		mb_html << '</tr>'
		c += 1
	end
	mb_html << '</table>'

	return mb_html
end


#### Multi calc_subset
def multi_calc_sub( uname, yyyy, mm, dd, tdiv, fc_items )
	results = ''
	fct_total = Hash.new
	fct_total.default = BigDecimal( 0 )

	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{uname}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
	if r.first
  		r.each do |e|
			menu_set = []
			code_set = []
			rate_set = []
			unit_set = []

			a = e['koyomi'].split( "\t" )
			a.each do |ee|
				( koyomi_code, koyomi_rate, koyomi_unit, z ) = ee.split( ':' )
				code_set << koyomi_code
				rate_set << koyomi_rate
				unit_set << koyomi_unit
			end

			code_set.size.times do |c|
				code = code_set[c]
				rate = BigDecimal( rate_set[c] )
				unit = unit_set[c].to_i

				if /\?/ =~ code
				elsif /\-f\-/ =~ code
					rr = mdb( "SELECT * FROM #{$MYSQL_TB_FCS} WHERE user='#{uname}' AND code='#{code}';", false, @debug )
					if rr.first
						5.upto( 65) do |cc|
							fct_total[$FCT_ITEM[cc]] += BigDecimal( num_opt( rr.first[$FCT_ITEM[cc]], 100, 1, $FCT_FRCT[$FCT_ITEM[cc]] + 3 ))
						end
					end
				else
					recipe_set = []
					fn_set = []
					weight_set = []
					if /\-m\-/ =~ code
						rr = mdb( "SELECT meal FROM #{$MYSQL_TB_MENU} WHERE user='#{uname}' AND code='#{code}';", false, @debug )
						a = rr.first['meal'].split( "\t" )
						a.each do |e| recipe_set << e end
					end

					if recipe_set.size == 0
						recipe_set << code
					end
					recipe_set.size.times do |cc|
						recipe_total_weight = BigDecimal( 0 )

						if /\-r\-/ =~ recipe_set[cc] || /\w+\-\h{4}\-\h{4}/ =~ recipe_set[cc]
#							p 'recipe'
							rr = mdb( "SELECT sum, dish FROM #{$MYSQL_TB_RECIPE} WHERE user='#{uname}' AND code='#{recipe_set[cc]}';", false, @debug )
							a = rr.first['sum'].split( "\t" )
							a.each do |eee|
								( sum_no, sum_weight, z, z, z, z, z, sum_ew ) = eee.split( ':' )

								if sum_no != '+' && sum_no != '-'
									fn_set << sum_no
									sum_ew = sum_weight if sum_ew == nil
									weight_set << ( BigDecimal( sum_ew ) / rr.first['dish'].to_i )
									recipe_total_weight += ( BigDecimal( sum_ew ) / rr.first['dish'].to_i )
								end
							end

							if unit == 99
								weight_set.map! do |x| x * rate / 100 end
							else
								weight_set.map! do |x| x * rate / recipe_total_weight end
							end
						end
					end

					# food
					if fn_set.size == 0
						fn_set << code
						weight_set << rate
					end

					#
					if unit != 0 && unit != 99
						fn_set.size.times do |cc|
							weight_set[cc] = unit_weight( weight_set[cc], unit, fn_set[cc] )
						end
					end

					fn_set.size.times do |cc|
						query = ''
						if /^P/ =~ fn_set[cc]
							query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{fn_set[cc]}';"
						elsif /^U/ =~ fn_set[cc]
							query = "SELECT * FROM #{$MYSQL_TB_FCTP} WHERE FN='#{fn_set[cc]}' AND user='#{uname}';"
						else
							query = "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{fn_set[cc]}';"
						end

						rr = mdb( query, false, @debug )
						if rr.first
							5.upto( 65) do |ccc|
								t = convert_zero( rr.first[$FCT_ITEM[ccc]] )
								fct_total[$FCT_ITEM[ccc]] += BigDecimal( num_opt( t, weight_set[cc], 1, $FCT_FRCT[$FCT_ITEM[ccc]] + 3 ))
							end
						end
					end
				end
			end
		end
	end

	fct_total.each do |k, v| fct_total[k] = v.round( $FCT_FRCT[k] ) end
	fc_items.each do |e| results << "#{$FCT_NAME[e]}[#{fct_total[e].to_f}]&nbsp;&nbsp;&nbsp;&nbsp;" end

	return results
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
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )

start_year, st_set = get_starty( user.name )

#### Getting POST
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
yyyy_mm = cgi['yyyy_mm']
unless yyyy_mm == ''
	a = yyyy_mm.split( '-' )
	yyyy = a[0].to_i
	mm = a[1].to_i
end
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
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
	a = r.first['koyomi'].split( "\t" )
	new_meal = ''
	a.size.times do |c|
		new_meal << "#{a[c]}\t" if c != order
	end
	new_meal.chop!

	mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{new_meal}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug )
#	mdb( "DELETE FROM #{$MYSQL_TB_FCS} WHERE user='#{user.name}' AND code='#{code}';", false, @debug ) 	if /\-f\-/ =~ code
end


#### Updating memo
if command == 'memo'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", false, @debug )
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{memo}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='4';", false, @debug )
	else
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET fzcode='', freeze='0', koyomi='#{memo}', user='#{user.name}', date='#{yyyy}-#{mm}-#{dd}', tdiv='4';", false, @debug )
	end
end


#### Saving Something
if command == 'some'
	hh = st_set[tdiv] if hh == 99
	koyomi = "#{some}:100:99:#{hh}"
	r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug)
	if r.first
		mdb( "UPDATE #{$MYSQL_TB_KOYOMI} SET koyomi='#{koyomi}' WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}' AND tdiv='#{tdiv}';", false, @debug)
	else
		mdb( "INSERT INTO #{$MYSQL_TB_KOYOMI} SET user='#{user.name}', fzcode='', freeze='0', koyomi='#{koyomi}', date='#{yyyy}-#{mm}-#{dd}', tdiv='#{tdiv}';", false, @debug)
	end
end


#### Deleting empty entry
mdb( "DELETE FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND freeze=0 AND ( koyomi='' OR koyomi IS NULL OR DATE IS NULL );", false, @debug )


####
freeze_flag = 0
koyomi_html = []
fc_items = []
r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}' AND name='簡易表示用';", false, @debug )
if r.first
	palette = r.first['palette']
	palette.size.times do |c|
		fc_items << $FCT_ITEM[c] if palette[c] == '1'
	end
else
 	fc_items = ['ENERC_KCAL', 'PROT', 'FAT', 'CHO', 'NACL_EQ']
end

r = mdb( "SELECT * FROM #{$MYSQL_TB_KOYOMI} WHERE user='#{user.name}' AND date='#{yyyy}-#{mm}-#{dd}';", false, @debug )
freeze_flag = r.first['freeze'].to_i if r.first
r.each do |e|
	if e['tdiv'] == 4
		koyomi_html[e['tdiv']] = e['koyomi']
	else
		koyomi_html[e['tdiv']] = meals( e, lp, user.name, freeze_flag )
		koyomi_html[e['tdiv']] << multi_calc_sub(  user.name, yyyy, mm, dd, e['tdiv'], fc_items )
	end
end


####
some_html = [ '', '', '', '' ]
if freeze_flag == 0
	0.upto( 3 ) do |c|
		some_html[c] = <<-"SOME"
		<select class='form-select form-select-sm' id='some#{c}' onchange="koyomiSaveSome( '#{yyyy}', '#{mm}', '#{dd}', #{c}, 'some#{c}' )">
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
0.upto( 3 ) do |c|
	unless freeze_flag == 1
		cmm_html[c]	<< "<button class='btn btn-sm btn-dark' onclick=\"fixKoyomi( 'init', '#{yyyy}', '#{mm}', '#{dd}', '#{c}' )\">#{lp[17]}</button>&nbsp;"
	else
		cmm_html[c]	<< "<button class='btn btn-sm btn-secondary'>#{lp[17]}</button>&nbsp;"
	end
	if koyomi_html[c] == nil
		cmm_html[c] << "<button class='btn btn-sm btn-secondary'>#{lp[18]}</button>&nbsp;"
		cmm_html[c] << "<button class='btn btn-sm btn-secondary'>#{lp[19]}</button>&nbsp;"
	else
		cmm_html[c] << "<button class='btn btn-sm btn-primary' onclick=\"cmmKoyomi( 'copy', '#{yyyy}', '#{mm}', '#{dd}', #{c} )\">#{lp[18]}</button>&nbsp;"
		cmm_html[c] << "<button class='btn btn-sm btn-primary' onclick=\"cmmKoyomi( 'move', '#{yyyy}', '#{mm}', '#{dd}', #{c} )\">#{lp[19]}</button>&nbsp;" unless freeze_flag == 1
	end
end


####
photo_html = [ '', '', '', '' ]
if freeze_flag == 0
	0.upto( 3 ) do |c|
		photo_html[c] = <<-"PHOTO"
		<form method="post" enctype="multipart/form-data" id='photo_formm#{c}'>
			<label for="photom">&nbsp;&nbsp;#{lp[26]}</label>
			<input type="file" name="photo1" id="photom#{c}" class="custom-control-file" onchange="">
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
			<span onclick="editKoyomiR( '#{yyyy}', '#{mm}' )">#{lp[7]}</span>
		</div>
	</div>
	<div class='row'>
		<div class='col-6'>
			<h5>#{lp[1]}</h5>
			#{koyomi_html[0]}
			<br><br>
			<div class="input-group">
				#{cmm_html[0]}
				#{some_html[0]}
				#{photo_html[0]}
			</div>
		</div>
		<div class='col-6'>
			<h5>#{lp[2]}</h5>
			#{koyomi_html[1]}
			<br><br>
			<div class="input-group">
				#{cmm_html[1]}
				#{some_html[1]}
				#{photo_html[1]}
			</div>
		</div>
	</div>
	<br>
	<div class='row'>
		<div class='col-6'>
			<h5>#{lp[3]}</h5>
			#{koyomi_html[2]}
			<br><br>
			<div class="input-group">
				#{cmm_html[2]}
				#{some_html[2]}
				#{photo_html[2]}
			</div>
		</div>
		<div class='col-6'>
			<h5>#{lp[4]}</h5>
			#{koyomi_html[3]}
			<br><br>
			<div class="input-group">
				#{cmm_html[3]}
				#{some_html[3]}
				#{photo_html[3]}
			</div>
		</div>
	</div>
	<br>
	<div class='row'>
		#{memo_html}
	</div>
</div>

HTML

puts html
