# Ginmi module for BMI 0.00
#encoding: utf-8

def ginmi_module( cgi )
	uname, uid, status = login_check( cgi )
	command = cgi['command']

	html = ''
	case cgi['command']
	when 'form'
		html << "<div class='row'>"
		html << "<h5>BMI計算フォーム</h5>"
		html << "</div>"

		html << "<div class='row'>"

		html << "<div class='col-2'>"
		html << "<div class='input-group input-group-sm'>"
		html << "<div class='input-group-prepend'><span class='input-group-text' maxlength='3' value='18'>年齢</span></div>"
		html << "<input type='number' min='18' class='form-control' id='age'>"
		html << "</div></div>"

		html << "<div class='col-2'>"
		html << "<div class='input-group input-group-sm'>"
		html << "<div class='input-group-prepend'><span class='input-group-text' maxlength='3' value='1.0'>身長(m)</span></div>"
		html << "<input type='text' class='form-control' id='height'>"
		html << "</div></div>"

		html << "<div class='col-2'>"
		html << "<div class='input-group input-group-sm'>"
		html << "<div class='input-group-prepend'><span class='input-group-text' maxlength='3' value='1.0'>体重(kg)</span></div>"
		html << "<input type='text' class='form-control' id='weight'>"
		html << "</div></div></div>"
		html << "<br>"
		html << "<div class='row'>"
		html << "<div class='col-2'>"
		html << "<button class='btn btn-sm btn-primary' onclick=\"ginmiBMIres()\">計算</button>"
		html << "</div>"
		html << "</div>"

	when 'result'
		age = cgi['age'].to_i
		weight = BigDecimal( cgi['weight'] )
		height = BigDecimal( cgi['height'] )
		if $DEBUG
			puts "age:#{age}<br>\n"
			puts "height:#{height}<br>\n"
			puts "weight:#{weight}<br>\n"
			puts "<hr>\n"
		end
		result = ( weight / ( height * height )).round( 1 )
		html << "<div class='row'>"
		html << "<div class='col-2'>BMI値</div>"
		html << "<div class='col-2'>#{result.to_f}</div>"
		html << "<div class='col-2'>計算式</div>"
		html << "<div class='col-2'>#{weight.to_f} / ( #{height.to_f} * #{height.to_f} )</div>"
		html << "</div>"

		html << "<br>"

		ibw = ( 22 * height * height ).round( 1 )
		html << "<div class='row'>"
		html << "<div class='col-2'>標準体重</div>"
		html << "<div class='col-2'>#{ibw.to_f}&nbsp;kg</div>"
		html << "<div class='col-2'>計算式</div>"
		html << "<div class='col-2'>22 * #{height.to_f} * #{height.to_f}</div>"
		html << "</div>"

		html << "<br>"
		html << "<table class='table table-sm table-bordered'>"
		html << "<thead class='thead-light'>"
		html << "<tr>"
		html << "	<th scope='col'>年齢</th>"
		html << "	<th scope='col'>目標BMI</th>"
		html << "</tr>"
		html << "</thead>"
		html << "<tbody>"
		html << "<tr>"
		html << "	<th scope='row'>18歳-49歳</th>"
		html << "	<td>18.5 - 24.9</td>"
		html << "</tr>"
		html << "<tr>"
		html << "	<th scope='row'>50歳-69歳</th>"
		html << "	<td>20.0 - 24.9</td>"
		html << "</tr>"
		html << "<tr>"
		html << "	<th scope='row'>70歳-</th>"
		html << "	<td>21.5 - 24.9</td>"
		html << "</tr>"
		html << "</tbody>"
		html << "</table>"

	when 'save'

	end

	return html
end
