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

category = []
pointer_list = []
memory = []

#### Lording all pointer
puts "Lording all pointer.\n"
r = db.query( "SELECT * FROM #{$MYSQL_TB_MEMORY};" )
r.each do |e|
	pointer_list << e['pointer']
end
pointer_list.uniq!


#### Adding pointer mark
puts "Adding pointer mark.\n"
r.each do |e|
	memory = e['memory']

	pointer_sub_list = []
	pointer_list.each do |ee| pointer_sub_list << memory.scan( ee ) end
	pointer_sub_list.flatten!
	pointer_sub_list.uniq!
	pointer_sub_list_ = Array.new( pointer_sub_list )

	# Removing smaller pointer & number
	pointer_sub_list.size.times do |c|
		pointer_sub_list_.each do |e|
			begin
				pointer_sub_list[c] = nil if /#{pointer_sub_list[c]}/ =~ e && pointer_sub_list[c] != e || /\d+/ =~ e || e.size < 2
			rescue
				pointer_sub_list[c] = nil
				puts "ERROR.\n"
			end
		end
	end

	pointer_sub_list.each do |ee|
		memory.gsub!( ee, "{{#{ee}}}" ) if ee != nil && ee != e['pointer']
	end
	memory.gsub!( '{{{{', '{{' )
	memory.gsub!( '}}}}', '}}' )
	db.query( "UPDATE #{$MYSQL_TB_MEMORY} SET memory='#{memory}' WHERE category='#{e['category']}' AND pointer='#{e['pointer']}';" )
end


puts "Done.\n"
