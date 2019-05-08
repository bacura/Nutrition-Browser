#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser cutting board monitor 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171026, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'fctb-cbm.cgi'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
uname, uid, status = login_check( cgi )


#### POSTデータの取得
food_no = cgi['food_no']
food_weight = cgi['food_weight']
food_check = cgi['food_check']
base_fn = cgi['base_fn']
mode = cgi['mode']

food_weight = BigDecimal( food_weight_check( food_weight ).first )

#### データと表示の更新
if uname
	# まな板データの読み込み
	r = mariadb( "SELECT sum from #{$MYSQL_TB_SUM} WHERE user='#{uname}';", false )
	sum = r.first['sum'].split( "\t" )
	cb_num = sum.size
	new_sum = ''

	if mode == 'add'
		# 新しいSUMの生成
		if cb_num == 0
			new_sum = "#{food_no}:#{food_weight}:g:#{food_weight}:#{food_check}::1.0:#{food_weight}"
		else
			new_sum = "#{r.first['sum']}\t#{food_no}:#{food_weight}:g:#{food_weight}:#{food_check}::1.0:#{food_weight}"
		end

		# まな板データ更新
		mariadb( "UPDATE #{$MYSQL_TB_SUM} SET sum='#{new_sum}' WHERE user='#{uname}';", false )
		cb_num += 1
		puts cb_num

		# 履歴データ更新
		add_his( uname, food_no )
	elsif mode == 'change'
		sum.each do |e|
			t = e.split( ':' )
			if t[0] == base_fn
				new_sum << "#{food_no}:#{t[1]}:#{food_weight}:#{t[3]}:#{t[4]}:#{t[5]}:#{t[6]}:#{t[7]}\t"
			else
				new_sum << "#{e}\t"
			end
		end
		new_sum.chop!

		# まな板データ更新
		mariadb( "UPDATE #{$MYSQL_TB_SUM} SET sum='#{new_sum}' WHERE user='#{uname}';", false )
		puts cb_num
	elsif mode == 'refresh'

		puts cb_num
	end
else
	puts = '-'
end
