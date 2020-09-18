# Config module for school 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']
	label_set = [cgi['label0'], cgi['label1'], cgi['label2'], cgi['label3'], cgi['label4'], cgi['label5'], cgi['label6'], cgi['label7'], cgi['label8'], cgi['label9']]
	if @debug
		puts "step: #{step}<br>"
		puts "label_set: #{label_set}<br>"
		puts "<hr>"
	end


	case step
	when 'update'
		schooll_new = ''
		0.upto( 9 ) do |c| schooll_new << "#{label_set[c]}:" end
		schooll_new.chop!
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET schooll='#{schooll_new}' WHERE user='#{user.name}';", false, @debug )
	else
		r = mdb( "SELECT schooll FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
		if r.first['schooll'] == '' || r.first['schooll'] == nil
			mdb( "UPDATE #{$MYSQL_TB_CFG} SET schooll='::::::::::' WHERE user='#{user.name}';", false, @debug )
		end
	end

####
	r = mdb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	if r.first
		label_set = r.first['schooll'].split( ':' )
	end

	# HTML
	html = '<div class="container">'
	html << "<h5>#{lp[72]}</h5><br>"

	0.upto( 9 ) do |c|
		html << "<div class='row'>"
		html << "	<div class='col-5'>"
		html << "		<div class='input-group input-group-sm'>"
		html << "			<span class='input-group-text'>#{lp[74]}#{c}</span>"
		html << "			<input type='text' maxlength='32' id='label#{c}' class='form-control form-control-sm' value='#{label_set[c]}'>"
		html << "		</div>"
		html << "	</div>"
		html << "</div><br>"
	end

  	html << "<div class='row'>"
	html << "<div class='col-4'><button type='button' class='btn btn-outline-primary btn-sm nav_button' onclick=\"schooll_cfg( 'update' )\">#{lp[73]}</button></div>"
	html << "</div>"

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

//
var schooll_cfg = function( step ){
	closeBroseWindows( 2 );

	var label0 = document.getElementById( "label0" ).value;
	var label1 = document.getElementById( "label1" ).value;
	var label2 = document.getElementById( "label2" ).value;
	var label3 = document.getElementById( "label3" ).value;
	var label4 = document.getElementById( "label4" ).value;
	var label5 = document.getElementById( "label5" ).value;
	var label6 = document.getElementById( "label6" ).value;
	var label7 = document.getElementById( "label7" ).value;
	var label8 = document.getElementById( "label8" ).value;
	var label9 = document.getElementById( "label9" ).value;

	$.post( "config.cgi", {
		mod:'school', step:step,
		label0:label0, label1:label1, label2:label2, label3:label3, label4:label4, label5:label5, label6:label6, label7:label7, label8:label8, label9:label9
	}, function( data ){ $( "#bw_level2" ).html( data );});
	displayVideo( 'Saved' );

	document.getElementById( "bw_level2" ).style.display = 'block';
};

</script>
JS
	puts js
end
