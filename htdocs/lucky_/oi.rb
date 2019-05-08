#encoding: utf-8
#fct browser Lucky input for OI 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20190120, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================


#==============================================================================
#STATIC
#==============================================================================
$DEBUG = false


#==============================================================================
#DEFINITION
#==============================================================================

def add2cb( lucky_solid, uname, mode )
	if $DEBUG
		puts "uname: #{uname}"
		puts "mode: #{mode}"
		puts "lucky_solid: #{lucky_solid}"
	end

	new_sum = "+:-:-:-:0:UNLUCKY!:-:-\t"

	if mode == 'add'
		# まな板データの読み込み
		q = "SELECT sum from #{$MYSQL_TB_SUM} WHERE user='#{uname}';"
		puts q if $DEBUG
		err = 'sum select'
		r = db_process( q, err, false )
		new_sum << "#{r.first['sum']}\t" if r.first
	end

	lucky_solid.each do |e|
		# dummy
	end
	new_sum.chop!

	# まな板データ更新
	q = "UPDATE #{$MYSQL_TB_SUM} SET sum='#{new_sum}' WHERE user='#{uname}';"
	puts q if $DEBUG
	err = 'sum update'
	db_process( q, err, false )

	return true
end
