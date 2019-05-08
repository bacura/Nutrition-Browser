#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser food search 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20171024, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
$SCRIPT = 'search-food.cgi'
$DEBUG = false


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
html_init( nil )

cgi = CGI.new
rec_date = Time.new
uname, uid, status = login_check( cgi )
if $DEBUG
	puts "uname: #{uname}<br>"
	puts "uid: #{uid}<br>"
	puts "status: #{status}<br>"
	puts "<hr>"
end

#### POSTデータの取得
words = cgi['words']
words.gsub!( /\s+/, "\t")
words.gsub!( /　+/, "\t")
words.gsub!( /,+/, "\t")
words.gsub!( /、+/, "\t")
words.gsub!( /\t{2,}/, "\t")
query_word = words.split( "\t" )
query_word.uniq!
if $DEBUG
	puts "query_word: #{query_word}<br>"
	puts "<hr>"
end


#### 検索キーの記録と辞書変換
true_query = []
query_word.each do |e|
	# 記録
	mariadb( "INSERT INTO #{$MYSQL_TB_SLOGF} SET user='#{uname}', words='#{e}', date='#{rec_date}';", false )

	# 変換
	r = mariadb( "SELECT * FROM #{$MYSQL_TB_DIC} WHERE alias='#{e}';", false )
	true_query << r.first['org_name'] if r.first
end


#### 検索して食品キーを生成
result_keys = []
result_keys_hash = Hash.new
words_count = 0
if true_query.size > 0
	true_query.each do |e|
		# 名前で検索
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE name='#{e}';", false )
		r.each do |ee| result_keys << "#{ee['FG']}:#{ee['class1']}:#{ee['class2']}:#{ee['class3']}:#{ee['name']}" end

		# クラス3で検索
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE class3='#{e}';", false )
		r.each do |ee| result_keys << "#{ee['FG']}:#{ee['class1']}:#{ee['class2']}:#{ee['class3']}:#{ee['name']}" end

		# クラス2で検索
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE class2='#{e}';", false )
		r.each do |ee| result_keys << "#{ee['FG']}:#{ee['class1']}:#{ee['class2']}:#{ee['class3']}:#{ee['name']}" end

		# クラス1で検索
		r = mariadb( "SELECT * FROM #{$MYSQL_TB_TAG} WHERE class1='#{e}';", false )
		r.each do |ee| result_keys << "#{ee['FG']}:#{ee['class1']}:#{ee['class2']}:#{ee['class3']}:#{ee['name']}" end

		# 食品キーのカウント
		result_keys.uniq!
		result_keys.each do |e|
			result_keys_hash[e] = 0 if result_keys_hash[e] == nil
			result_keys_hash[e] += 1
		end

		# 検索結果コードの記録
		mariadb( "UPDATE #{$MYSQL_TB_SLOGF} SET code='#{result_keys.size}' WHERE user='#{uname}' AND words='#{query_word[words_count]}' AND date='#{rec_date}';", false )
		words_count += 1
	end
else
	# 検索結果無しコードの記録
	query_word.each do |e| mariadb( "UPDATE #{$MYSQL_TB_SLOGF} SET code='0' WHERE user='#{uname}' AND words='#{e}' AND date='#{rec_date}';", false ) end
end


#### 食品キーのソート
result_keys_sort = result_keys_hash.sort_by{|k, v| -v }


html = ''
if result_keys.size > 0
	html << "<h6>検索結果: #{words}: #{result_keys.size}件</h6>"
	result_keys_sort.each do |e|
		# サブクラス処理
		class1_sub = ''
		class2_sub = ''
		class3_sub = ''
		class_space = ''
		a = e[0].split( ':' )
		class1_sub = "<span class='tagc'>#{a[1].sub( '+', '' )}</span>" if /\+/ =~ a[1]
		class2_sub = "<span class='tagc'>#{a[2].sub( '+', '' )}</span>" if /\+/ =~ a[2]
		class3_sub = "<span class='tagc'>#{a[3].sub( '+', '' )}</span>" if /\+/ =~ a[3]
		class_space = ' ' unless class1_sub == '' and class2_sub == '' and class3_sub == ''

		button_class = "class='btn btn-outline-secondary btn-sm nav_button'"
		button_class = "class='btn btn-outline-primary btn-sm nav_button visited'" if e[1] == true_query.size

		html << "<button type='button' #{button_class} onclick=\"summonBWL5( '#{e[0]}', '1' )\">#{class1_sub}#{class2_sub}#{class3_sub}#{class_space}#{a[4]}</button>\n"
	end
else
	html << "<h6>検索結果: #{words}: 0 件</h6>"
	html << "<h6>該当する食品は見つかりませんでした。</h6>"

end

puts html
