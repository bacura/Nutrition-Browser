#encoding: utf-8
#fct browser Lucky input for general data 0.00

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

	new_sum = ''
	if mode == 'add'
		# まな板データの読み込み
		q = "SELECT sum from #{$MYSQL_TB_SUM} WHERE user='#{uname}';"
		puts "#{q}<br>" if $DEBUG
		err = 'sum select'
		r = db_process( q, err, false )
		new_sum << "#{r.first['sum']}\t" if r.first
	end

	lucky_solid.each do |e|
		if e.food_no[0] == nil
			new_sum << "-:-:-:-:0:-:-:-\t"
		else
			# まな板データ更新
			q = "SELECT FN FROM #{$MYSQL_TB_TAG} WHERE FN='#{e.food_no[0]}';"
			err = 'tag select FN'
			r = db_process( q, err, false )
			if r.first
				if e.food_no[0] != nil && e.weight[0] == nil
					new_sum << "#{e.food_no[0]}:100:0:100:0::1.0:100\t"
				elsif e.food_no[0] != nil && e.weight[0] != nil && e.unit[0] == nil
					new_sum << "#{e.food_no[0]}:#{e.weight[0]}:0:#{e.weight[0]}:0::1.0:#{e.weight[0]}\t"
				elsif e.food_no[0] != nil && e.weight[0] != nil && e.unit[0] != nil
					new_sum << "#{e.food_no[0]}:#{e.weight[0]}:0:#{e.weight[0]}:0:#{e.unit[0]}:1.0:#{e.weight[0]}\t"
				else
					new_sum << "+:-:-:-:0:ERROR:-:-\t"
				end
			else
				new_sum << "+:-:-:-:0:ERROR FN(#{e.food_no[0]}):-:-\t"
			end
		end
	end
	new_sum.chop!

	# まな板データ更新
	q = "UPDATE #{$MYSQL_TB_SUM} SET sum='#{new_sum}' WHERE user='#{uname}';"
	puts "#{q}<br>" if $DEBUG
	err = 'sum update'
	db_process( q, err, false )

	return true
end
