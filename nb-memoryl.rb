#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser memory linker 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190319, 0.00, start


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

db = Mysql2::Client.new(:host => "#{$MYSQL_HOST}", :username => "#{$MYSQL_USER}", :password => "#{$MYSQL_PW}", :database => "#{$MYSQL_DB}", :encoding => "utf8" )

pointer_h = Hash.new

#### Lording all pointer
puts "Lording all memories.\n"
r = db.query( "SELECT * FROM #{$MYSQL_TB_MEMORY};" )
r.each do |e|
	pointer_h[e['pointer']] = e['pointer'].size if e['pointer'].size > 2
end


memory_size = r.size
puts "#{pointer_h.size} pointers.\n"
puts "#{memory_size} memories.\n"


c = 0
r.each do |e|
	sub_pointer = []
	memory = e['memory']
	memory.gsub!( '{{', '' )
	memory.gsub!( '}}', '' )

	# 記憶に存在するポインタの抽出
	pointer_h.each_key do |k|
		begin
			if /#{k}/ =~ memory
				sub_pointer << k
			end
		rescue
		end
	end
	sub_pointer.flatten!
	sub_pointer.uniq!

	opt_pointer_h = Hash.new
	sub_pointer.each do |ee| opt_pointer_h[ee] = true end

	#ポインタ in ポインタのフラグ折り
	sub_pointer.each do |ee|
		sub_pointer.each do |eee|
			opt_pointer_h[eee] = false if /#{eee}/ =~ ee && eee != ee
			opt_pointer_h[eee] = false if /^\d+$/ =~ eee
		end
	end

	# ポインターの拡張タグ
	opt_pointer_h.each do |k, v|
		memory.gsub!( k, "{{#{k}}}") if v
	end

	db.query( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{memory}' WHERE category='#{e['category']}' AND pointer='#{e['pointer']}';" )

	c += 1
	print( "#{c}/#{memory_size}\r" )
end

puts "\nDone."
