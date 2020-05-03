#Generating METs tablw from 2012.4.11 version 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20200109, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================


#==============================================================================
#STATIC
#==============================================================================


#==============================================================================
#DEFINITION
#==============================================================================

f = open( "mets.txt", "r" )
mets_solid = []
f.each do |l|
	mets_solid << l.chomp.force_encoding( 'UTF-8' )
end
f.close

code_set = []
mets_set = []
cate_set = []
en_set = []
en_cate_set = []
ja_set = []
flip = true
mets_solid.each do |e|
	if /^\d{5}/ =~ e
		( code, mets, cate ) = e.split( "\s" )
		code_set << code
		mets_set << mets
		cate_set << cate
	elsif /^\(/ =~ e
		if flip
			en_cate_set << e
			flip = false
		else
			en_set << e
			flip = true
		end
	else
		unless e == 'コード' || e == 'メッツ' || e == 'METS' || e == '大項目' || e == 'MAJOR HEADING' || e == '個別活動' || e == 'CODE'  || e == 'SPECIFIC ACTIVITIES' || /^\d{1,2}/ =~ e || /\s\d{4}/ =~ e || /※/ =~ e
			ja_set << e
		end
	end
end

4.times do code_set.shift end
4.times do mets_set.shift end
4.times do cate_set.shift end
6.times do en_set.shift end
7.times do en_cate_set.shift end
19.times do ja_set.shift end

puts "code:#{code_set.size}"
puts "mets:#{mets_set.size}"
puts "cate:#{cate_set.size}"
puts "ja:#{ja_set.size}"
puts "en:#{en_set.size}"
puts "en_cate:#{en_cate_set.size}"

f = open( "mets_.txt", "w" )
ja_set.size.times do |c|
	f.puts "#{code_set[c]}\t#{mets_set[c]}\t#{cate_set[c]}\t#{ja_set[c]}\t#{en_cate_set[c]}\t#{en_set[c]}\n"
end
f.close
