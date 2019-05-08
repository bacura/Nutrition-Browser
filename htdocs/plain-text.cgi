#! /usr/bin/ruby
#encoding: utf-8
#fct browser plain text 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171018, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'plain-text.cgi'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
puts "Content-type: text/text\n\n"

lp = lp_init( 'plain-text', $DEFAULT_LP )

#### GETデータの取得
get_data = get_data()
frct_mode = get_data['frct_mode'].to_i
food_weight = get_data['food_weight']
food_no = get_data['food_no']


#### 食品重量の決定
food_weight = 100 if food_weight == nil || food_weight == ''
food_weight = food_weight.to_i


r = mariadb( "SELECT * FROM #{$MYSQL_TB_FCT} WHERE FN='#{food_no}';", false )

fct_opt = Hash.new
# 全ての栄養素を取得
$FCT_ITEM.each do |e| fct_opt[e] = num_opt( r.first[e], food_weight, frct_mode, $FCT_FRCT[e] ) end


fraction = ''
if frct_mode == 1
	fraction = lp[1]
elsif frct_mode == 2
	fraction = lp[2]

elsif frct_mode == 3
	fraction = lp[3]
else
	fraction = lp[4]
end
weight = "#{lp[5]} #{food_weight} #{lp[6]} （#{fraction}）\n"

item_name = "#{$FCT_NAME['FN']}\t#{$FCT_NAME['SID']}\t#{$FCT_NAME['Tagnames']}\t"
item_name << "#{$FCT_NAME['REFUSE']}\t#{$FCT_NAME['ENERC_KCAL']}\t#{$FCT_NAME['ENERC']}\t#{$FCT_NAME['WATER']}\t#{$FCT_NAME['PROT']}\t#{$FCT_NAME['PROTCAA']}\t#{$FCT_NAME['FAT']}\t#{$FCT_NAME['FATNLEA']}\t#{$FCT_NAME['FASAT']}\t#{$FCT_NAME['FAMS']}\t#{$FCT_NAME['FASAT']}\t#{$FCT_NAME['FAPU']}\t#{$FCT_NAME['CHOLE']}\t#{$FCT_NAME['CHO']}\t#{$FCT_NAME['CHOAVLM']}\t#{$FCT_NAME['FIBSOL']}\t#{$FCT_NAME['FIBINS']}\t#{$FCT_NAME['FIBTG']}\t"
item_name << "#{$FCT_NAME['ASH']}\t#{$FCT_NAME['NA']}\t#{$FCT_NAME['K']}\t#{$FCT_NAME['CA']}\t#{$FCT_NAME['MG']}\t#{$FCT_NAME['P']}\t#{$FCT_NAME['FE']}\t#{$FCT_NAME['ZN']}\t#{$FCT_NAME['CU']}\t#{$FCT_NAME['MN']}\t#{$FCT_NAME['ID']}\t#{$FCT_NAME['SE']}\t#{$FCT_NAME['CR']}\t#{$FCT_NAME['MO']}\t"
item_name << "#{$FCT_NAME['RETOL']}\t#{$FCT_NAME['CARTA']}\t#{$FCT_NAME['CARTB']}\t#{$FCT_NAME['CRYPXB']}\t#{$FCT_NAME['CARTBEQ']}\t#{$FCT_NAME['VITA_RAE']}\t#{$FCT_NAME['VITD']}\t#{$FCT_NAME['TOCPHA']}\t#{$FCT_NAME['TOCPHB']}\t#{$FCT_NAME['TOCPHG']}\t#{$FCT_NAME['TOCPHD']}\t#{$FCT_NAME['VITK']}\t"
item_name << "#{$FCT_NAME['THIAHCL']}\t#{$FCT_NAME['RIBF']}\t#{$FCT_NAME['NIA']}\t#{$FCT_NAME['VITB6A']}\t#{$FCT_NAME['VITB12']}\t#{$FCT_NAME['FOL']}\t#{$FCT_NAME['PANTAC']}\t#{$FCT_NAME['BIOT']}\t#{$FCT_NAME['VITC']}\t"
item_name << "#{$FCT_NAME['NACL_EQ']}\t#{$FCT_NAME['ALC']}\t#{$FCT_NAME['NITRA']}\t#{$FCT_NAME['THEBRN']}\t#{$FCT_NAME['CAFFN']}\t#{$FCT_NAME['TAN']}\t#{$FCT_NAME['POLYPHENT']}\t#{$FCT_NAME['ACEAC']}\t#{$FCT_NAME['COIL']}\t#{$FCT_NAME['OA']}\t#{$FCT_NAME['WCR']}\t#{$FCT_NAME['Notice']}\n"

item_unit = "#{$FCT_UNIT['FN']}\t#{$FCT_UNIT['SID']}\t#{$FCT_UNIT['Tagnames']}\t"
item_unit << "#{$FCT_UNIT['REFUSE']}\t#{$FCT_UNIT['ENERC_KCAL']}\t#{$FCT_UNIT['ENERC']}\t#{$FCT_UNIT['WATER']}\t#{$FCT_UNIT['PROT']}\t#{$FCT_UNIT['PROTCAA']}\t#{$FCT_UNIT['FAT']}\t#{$FCT_UNIT['FATNLEA']}\t#{$FCT_UNIT['FASAT']}\t#{$FCT_UNIT['FAMS']}\t#{$FCT_UNIT['FASAT']}\t#{$FCT_UNIT['FAPU']}\t#{$FCT_UNIT['CHOLE']}\t#{$FCT_UNIT['CHO']}\t#{$FCT_UNIT['CHOAVLM']}\t#{$FCT_UNIT['FIBSOL']}\t#{$FCT_UNIT['FIBINS']}\t#{$FCT_UNIT['FIBTG']}\t"
item_unit << "#{$FCT_UNIT['ASH']}\t#{$FCT_UNIT['NA']}\t#{$FCT_UNIT['K']}\t#{$FCT_UNIT['CA']}\t#{$FCT_UNIT['MG']}\t#{$FCT_UNIT['P']}\t#{$FCT_UNIT['FE']}\t#{$FCT_UNIT['ZN']}\t#{$FCT_UNIT['CU']}\t#{$FCT_UNIT['MN']}\t#{$FCT_UNIT['ID']}\t#{$FCT_UNIT['SE']}\t#{$FCT_UNIT['CR']}\t#{$FCT_UNIT['MO']}\t"
item_unit << "#{$FCT_UNIT['RETOL']}\t#{$FCT_UNIT['CARTA']}\t#{$FCT_UNIT['CARTB']}\t#{$FCT_UNIT['CRYPXB']}\t#{$FCT_UNIT['CARTBEQ']}\t#{$FCT_UNIT['VITA_RAE']}\t#{$FCT_UNIT['VITD']}\t#{$FCT_UNIT['TOCPHA']}\t#{$FCT_UNIT['TOCPHB']}\t#{$FCT_UNIT['TOCPHG']}\t#{$FCT_UNIT['TOCPHD']}\t#{$FCT_UNIT['VITK']}\t"
item_unit << "#{$FCT_UNIT['THIAHCL']}\t#{$FCT_UNIT['RIBF']}\t#{$FCT_UNIT['NIA']}\t#{$FCT_UNIT['VITB6A']}\t#{$FCT_UNIT['VITB12']}\t#{$FCT_UNIT['FOL']}\t#{$FCT_UNIT['PANTAC']}\t#{$FCT_UNIT['BIOT']}\t#{$FCT_UNIT['VITC']}\t"
item_unit << "#{$FCT_UNIT['NACL_EQ']}\t#{$FCT_UNIT['ALC']}\t#{$FCT_UNIT['NITRA']}\t#{$FCT_UNIT['THEBRN']}\t#{$FCT_UNIT['CAFFN']}\t#{$FCT_UNIT['TAN']}\t#{$FCT_UNIT['POLYPHENT']}\t#{$FCT_UNIT['ACEAC']}\t#{$FCT_UNIT['COIL']}\t#{$FCT_UNIT['OA']}\t#{$FCT_UNIT['WCR']}\t#{$FCT_UNIT['Notice']}\n"

item_opt = "#{fct_opt['FN']}\t#{fct_opt['SID']}\t#{fct_opt['Tagnames']}\t"
item_opt << "#{fct_opt['REFUSE']}\t#{fct_opt['ENERC_KCAL']}\t#{fct_opt['ENERC']}\t#{fct_opt['WATER']}\t#{fct_opt['PROT']}\t#{fct_opt['PROTCAA']}\t#{fct_opt['FAT']}\t#{fct_opt['FATNLEA']}\t#{fct_opt['FASAT']}\t#{fct_opt['FAMS']}\t#{fct_opt['FASAT']}\t#{fct_opt['FAPU']}\t#{fct_opt['CHOLE']}\t#{fct_opt['CHO']}\t#{fct_opt['CHOAVLM']}\t#{fct_opt['FIBSOL']}\t#{fct_opt['FIBINS']}\t#{fct_opt['FIBTG']}\t"
item_opt << "#{fct_opt['ASH']}\t#{fct_opt['NA']}\t#{fct_opt['K']}\t#{fct_opt['CA']}\t#{fct_opt['MG']}\t#{fct_opt['P']}\t#{fct_opt['FE']}\t#{fct_opt['ZN']}\t#{fct_opt['CU']}\t#{fct_opt['MN']}\t#{fct_opt['ID']}\t#{fct_opt['SE']}\t#{fct_opt['CR']}\t#{fct_opt['MO']}\t"
item_opt << "#{fct_opt['RETOL']}\t#{fct_opt['CARTA']}\t#{fct_opt['CARTB']}\t#{fct_opt['CRYPXB']}\t#{fct_opt['CARTBEQ']}\t#{fct_opt['VITA_RAE']}\t#{fct_opt['VITD']}\t#{fct_opt['TOCPHA']}\t#{fct_opt['TOCPHB']}\t#{fct_opt['TOCPHG']}\t#{fct_opt['TOCPHD']}\t#{fct_opt['VITK']}\t"
item_opt << "#{fct_opt['THIAHCL']}\t#{fct_opt['RIBF']}\t#{fct_opt['NIA']}\t#{fct_opt['VITB6A']}\t#{fct_opt['VITB12']}\t#{fct_opt['FOL']}\t#{fct_opt['PANTAC']}\t#{fct_opt['BIOT']}\t#{fct_opt['VITC']}\t"
item_opt << "#{fct_opt['NACL_EQ']}\t#{fct_opt['ALC']}\t#{fct_opt['NITRA']}\t#{fct_opt['THEBRN']}\t#{fct_opt['CAFFN']}\t#{fct_opt['TAN']}\t#{fct_opt['POLYPHENT']}\t#{fct_opt['ACEAC']}\t#{fct_opt['COIL']}\t#{fct_opt['OA']}\t#{fct_opt['WCR']}\t#{fct_opt['Notice']}\n"

puts weight.encode( 'Shift_JIS' )
puts item_name.encode( 'Shift_JIS' )
puts item_unit.encode( 'Shift_JIS' )
puts item_opt.encode( 'Shift_JIS' )
