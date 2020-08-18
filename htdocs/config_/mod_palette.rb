# Config module for Palette 0.00
#encoding: utf-8

#### displying palette
def listing( uname, lp )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{uname}';", false, @debug )

	list_body = ''
	r.each do |e|
		list_body << "<tr><td>#{e['name']}</td><td>#{e['count']}</td>"
		list_body << "<td><button class='btn btn-outline-primary btn-sm' type='button' onclick='palette_cfg( \"edit_palette\", \"#{e['name']}\" )'>#{lp[41]}</button></td>"
		list_body << "<td>"
		list_body << "<input type='checkbox' id=\"#{e['name']}\">&nbsp;<button class='btn btn-outline-danger btn-sm' type='button' onclick='palette_cfg( \"delete_palette\", \"#{e['name']}\" )'>#{lp[42]}</button></td></tr>\n" unless e['name'] == '簡易表示用'
		list_body << "</td></tr>"
	end

	html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-8'><h5>#{lp[43]}</h5></div>
		<div class='col-2'><button class="btn btn-outline-primary btn-sm" type="button" onclick="palette_cfg( 'new_palette' )">#{lp[44]}</button></div>
		<div class='col-2'><button class="btn btn-outline-danger btn-sm" type="button" onclick="palette_cfg( 'reset_palette' )">#{lp[45]}</button></div>
	</div>
	<br>

	<table class="table table-sm table-hover">
	<thead>
		<tr>
			<td>#{lp[46]}</td>
			<td>#{lp[47]}</td>
			<td>#{lp[48]}</td>
			<td></td>
		</tr>
	</thead>
	#{list_body}

	</table>
</div>
HTML

	return html
end


def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']
	html = ''

	case step
	when ''
		html = listing( user.name, lp )

	when 'new_palette', 'edit_palette'
		checked = []
		if step == 'edit_palette'
			r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}' AND name='#{cgi['palette_name']}';", false, @debug )
			palette = r.first['palette']
			palette.size.times do |c|
				if palette[c] == '1'
					checked << 'checked'
				else
					checked << ''
				end
			end
		end

		fc_table = ['', '', '', '', '', '', '']
		4.upto( 7 ) do |i| fc_table[0] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		8.upto( 20 ) do |i| fc_table[1] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		21.upto( 34 ) do |i| fc_table[2] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		35.upto( 46 ) do |i| fc_table[3] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		47.upto( 55 ) do |i| fc_table[4] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end
		56.upto( 67 ) do |i| fc_table[5] << "<tr><td><input type='checkbox' id='#{$FCT_ITEM[i]}' #{checked[i]}>&nbsp;#{$FCT_NAME[$FCT_ITEM[i]]}</td></tr>" end

		html = <<-"HTML"
	<div class="container-fluid">
		<div class="row">
			<div class="col-6">
				<div class="input-group mb-3">
  					<div class="input-group-prepend"><span class="input-group-text">#{lp[49]}</span></div>
  					<input type="text" class="form-control" id="palette_name" value="#{cgi['palette_name']}" maxlength="60">
  				</div>
			</div>
			<div class="col-5"></div>
			<div class="col-1"><button class="btn btn-outline-primary btn-sm" type="button" onclick="palette_cfg( 'regist' )">#{lp[50]}</button></div>
		</div>
		<br>
		<div class="row">
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[0]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[1]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[2]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[3]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[4]}</table></div>
			<div class="col-2"><table class='table-sm table-striped' width='100%'>#{fc_table[5]}</table></div>
		</div>
	</div>
HTML

	when 'regist'
		fct_bits = '0000'
		fct_count = 0
		palette_name = cgi['palette_name']

		4.upto( 67 ) do |i|
			fct_bits << cgi[$FCT_ITEM[i]].to_i.to_s
			fct_count += 1 if cgi[$FCT_ITEM[i]] == '1'
		end

		r = mdb( "SELECT * FROM #{$MYSQL_TB_PALETTE} WHERE name='#{palette_name}' AND user='#{user.name}';", false, @debug )
		if r.first
			mdb( "UPDATE #{$MYSQL_TB_PALETTE} SET palette='#{fct_bits}', count='#{fct_count}' WHERE name='#{palette_name}' AND user='#{user.name}';", false, @debug )
		else
			mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET name='#{palette_name}', user='#{user.name}', palette='#{fct_bits}', count='#{fct_count}';", false, @debug )
		end

		html = listing( user.name, lp )

	when 'delete_palette'
		mdb( "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE name='#{cgi['palette_name']}' AND user='#{user.name}';", false, @debug )

		html = listing( user.name, lp )

	when 'reset_palette'
		mdb( "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}';", false, @debug )
 		mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{lp[51]}', count='5', palette='00000100101000001000000000000000000000000000000000000000100000000000';", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{lp[52]}', count='5', palette='00000100101000001000000000000000000000000000000000000000100000000000';", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{lp[53]}', count='14', palette='0000010010100000100010111011000000000000100000011000000110000000000';", false, @debug )
		mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{user.name}', name='#{lp[54]}', count='63', palette='0000011111111111111111111111111111111111111111111111111111111111110';", false, @debug )

		html = listing( user.name, lp )
	end

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Sending FC palette
var palette_cfg = function( step, id ){
	if( step == 'new_palette' ){
		$.post( "config.cgi", { mod:'palette', step:step }, function( data ){ $( "#bw_level3" ).html( data );});
		document.getElementById( "bw_level3" ).style.display = 'block';
	}

	switch( step ){
	case 'reset_palette':
		$.post( "config.cgi", { mod:'palette', step:step }, function( data ){ $( "#bw_level2" ).html( data );});
		document.getElementById( "bw_level2" ).style.display = 'block';
		displayVideo( 'Palette reset' );
		break;
	}

	if( step == 'regist' ){
		var palette_name = document.getElementById( "palette_name" ).value;

		if( palette_name != '' ){
			if( document.getElementById( "REFUSE" ).checked ){ var REFUSE = 1 }
			if( document.getElementById( "ENERC_KCAL" ).checked ){ var ENERC_KCAL = 1 }
			if( document.getElementById( "ENERC" ).checked ){ var ENERC = 1 }
			if( document.getElementById( "WATER" ).checked ){ var WATER = 1 }

			if( document.getElementById( "PROT" ).checked ){ var PROT = 1 }
			if( document.getElementById( "PROTCAA" ).checked ){ var PROTCAA = 1 }
			if( document.getElementById( "FAT" ).checked ){ var FAT = 1 }
			if( document.getElementById( "FATNLEA" ).checked ){ var FATNLEA = 1 }
			if( document.getElementById( "FASAT" ).checked ){ var FASAT = 1 }
			if( document.getElementById( "FAMS" ).checked ){ var FAMS = 1 }
			if( document.getElementById( "FAPU" ).checked ){ var FAPU = 1 }
			if( document.getElementById( "CHOLE" ).checked ){ var CHOLE = 1 }
			if( document.getElementById( "CHO" ).checked ){ var CHO = 1 }
			if( document.getElementById( "CHOAVLM" ).checked ){ var CHOAVLM = 1 }
			if( document.getElementById( "FIBSOL" ).checked ){ var FIBSOL = 1 }
			if( document.getElementById( "FIBINS" ).checked ){ var FIBINS = 1 }
			if( document.getElementById( "FIBTG" ).checked ){ var FIBTG = 1 }

			if( document.getElementById( "ASH" ).checked ){ var ASH = 1 }
			if( document.getElementById( "NA" ).checked ){ var NA = 1 }
			if( document.getElementById( "K" ).checked ){ var K = 1 }
			if( document.getElementById( "CA" ).checked ){ var CA = 1 }
			if( document.getElementById( "MG" ).checked ){ var MG = 1 }
			if( document.getElementById( "P" ).checked ){ var P = 1 }
			if( document.getElementById( "FE" ).checked ){ var FE = 1 }
			if( document.getElementById( "ZN" ).checked ){ var ZN = 1 }
			if( document.getElementById( "CU" ).checked ){ var CU = 1 }
			if( document.getElementById( "MN" ).checked ){ var MN = 1 }
			if( document.getElementById( "ID" ).checked ){ var ID = 1 }
			if( document.getElementById( "SE" ).checked ){ var SE = 1 }
			if( document.getElementById( "CR" ).checked ){ var CR = 1 }
			if( document.getElementById( "MO" ).checked ){ var MO = 1 }

			if( document.getElementById( "RETOL" ).checked ){ var RETOL = 1 }
			if( document.getElementById( "CARTA" ).checked ){ var CARTA = 1 }
			if( document.getElementById( "CARTB" ).checked ){ var CARTB = 1 }
			if( document.getElementById( "CRYPXB" ).checked ){ var CRYPXB = 1 }
			if( document.getElementById( "CARTBEQ" ).checked ){ var CARTBEQ = 1 }
			if( document.getElementById( "VITA_RAE" ).checked ){ var VITA_RAE = 1 }
			if( document.getElementById( "VITD" ).checked ){ var VITD = 1 }
			if( document.getElementById( "TOCPHA" ).checked ){ var TOCPHA = 1 }
			if( document.getElementById( "TOCPHB" ).checked ){ var TOCPHB = 1 }
			if( document.getElementById( "TOCPHG" ).checked ){ var TOCPHG = 1 }
			if( document.getElementById( "TOCPHD" ).checked ){ var TOCPHD = 1 }
			if( document.getElementById( "VITK" ).checked ){ var VITK = 1 }

			if( document.getElementById( "THIAHCL" ).checked ){ var THIAHCL = 1 }
			if( document.getElementById( "RIBF" ).checked ){ var RIBF = 1 }
			if( document.getElementById( "NIA" ).checked ){ var NIA = 1 }
			if( document.getElementById( "VITB6A" ).checked ){ var VITB6A = 1 }
			if( document.getElementById( "VITB12" ).checked ){ var VITB12 = 1 }
			if( document.getElementById( "FOL" ).checked ){ var FOL = 1 }
			if( document.getElementById( "PANTAC" ).checked ){ var PANTAC = 1 }
			if( document.getElementById( "BIOT" ).checked ){ var BIOT = 1 }
			if( document.getElementById( "VITC" ).checked ){ var VITC = 1 }

			if( document.getElementById( "NACL_EQ" ).checked ){ var NACL_EQ = 1 }
			if( document.getElementById( "ALC" ).checked ){ var ALC = 1 }
			if( document.getElementById( "NITRA" ).checked ){ var NITRA = 1 }
			if( document.getElementById( "THEBRN" ).checked ){ var THEBRN = 1 }
			if( document.getElementById( "CAFFN" ).checked ){ var CAFFN = 1 }
			if( document.getElementById( "TAN" ).checked ){ var TAN = 1 }
			if( document.getElementById( "POLYPHENT" ).checked ){ var POLYPHENT = 1 }
			if( document.getElementById( "ACEAC" ).checked ){ var ACEAC = 1 }
			if( document.getElementById( "COIL" ).checked ){ var COIL = 1 }
			if( document.getElementById( "OA" ).checked ){ var OA = 1 }
			if( document.getElementById( "WCR" ).checked ){ var WCR = 1 }

			if( document.getElementById( "Notice" ).checked ){ var Notice = 1 }

			$.post( "config.cgi", {
				mod:'palette', step:step, palette_name:palette_name,
				REFUSE:REFUSE, ENERC_KCAL:ENERC_KCAL, ENERC:ENERC, WATER:WATER,
				PROT:PROT, PROTCAA:PROTCAA, FAT:FAT, FATNLEA:FATNLEA, FASAT:FASAT, FAMS:FAMS, FAPU:FAPU, CHOLE:CHOLE, CHO:CHO, CHOAVLM:CHOAVLM, FIBSOL:FIBSOL, FIBINS:FIBINS, FIBTG:FIBTG,
				ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
				RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
				THIAHCL:THIAHCL, RIBF:RIBF, NIA:NIA, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
				NACL_EQ:NACL_EQ, ALC:ALC, NITRA:NITRA, THEBRN:THEBRN, CAFFN:CAFFN, TAN:TAN, POLYPHENT:POLYPHENT, ACEAC:ACEAC, COIL:COIL, OA:OA, WCR:WCR,
				Notice:Notice
			}, function( data ){ $( "#bw_level2" ).html( data );});
			displayVideo( palette_name + 'saved' );

//			$.post( "config.cgi", { command:"palette", step:'list' }, function( data ){ $( "#bw_level2" ).html( data );});
			closeBroseWindows( 2 );
		} else{
			displayVideo( 'Palette name!(>_<)' );
		}
	}

	// Edit FC palette
	if( step == 'edit_palette' ){
		$.post( "config.cgi", { mod:'palette', step:step, palette_name:id }, function( data ){ $( "#bw_level3" ).html( data );});
		document.getElementById( "bw_level3" ).style.display = 'block';
	}

	// Deleting FC palette
	if( step == 'delete_palette' ){
		if( document.getElementById( id ).checked ){
			$.post( "config.cgi", { mod:'palette', step:step, palette_name:id }, function( data ){ $( "#bw_level2" ).html( data );});
			closeBroseWindows( 2 );
		} else{
			displayVideo( 'Check!(>_<)' );
		}
	}

};

</script>
JS
	puts js
end
