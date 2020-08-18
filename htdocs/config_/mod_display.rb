# Config module for NB display 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']

	icache = 0
	ifix = 0
	ilist = 50
	icalc = 14
	icalcp = 14
	if step ==  'update'
		icache = cgi['icache'].to_i
		ifix = cgi['ifix'].to_i
		ilist = cgi['ilist'].to_i
		icalc = cgi['icalc'].to_i
		icalcp = cgi['icalcp'].to_i

		# Updating bio information
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET icache='#{icache}', ifix='#{ifix}', ilist='#{ilist}', icalc='#{icalc}', icalcp='#{icalcp}' WHERE user='#{user.name}';", false, false )
	else
		r = mdb( "SELECT * FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, false )
		icache = r.first['icache'].to_i
		ifix = r.first['ifix'].to_i
		ilist = r.first['ilist'].to_i
		icalc = r.first['icalc'].to_i
		icalcp = r.first['icalcp'].to_i
	end

	icache_checked = ''
	icache_checked = 'CHECKED' if icache == 1

	ifix_checked = ''
	ifix_checked = 'CHECKED' if ifix == 1

	ilist_10_selected = ''
	ilist_10_selected = 'SELECTED' if ilist == 10
	ilist_25_selected = ''
	ilist_25_selected = 'SELECTED' if ilist == 25
	ilist_50_selected = ''
	ilist_50_selected = 'SELECTED' if ilist == 50 ||  ilist == 0
	ilist_75_selected = ''
	ilist_75_selected = 'SELECTED' if ilist == 75
	ilist_100_selected = ''
	ilist_100_selected = 'SELECTED' if ilist == 100
	ilist_150_selected = ''
	ilist_150_selected = 'SELECTED' if ilist == 150
	ilist_200_selected = ''
	ilist_200_selected = 'SELECTED' if ilist == 200

	icalc = 14 if icalc == 0
	icalcp = 14 if icalcp == 0

	html = <<-"HTML"
    <div class="container">
    	<div class='row'>
	    	<div class='col-3'>#{lp[65]}</div>
			<div class='col-4'>
				<div class="custom-control custom-switch">
					<input type="checkbox" class="custom-control-input" id="icache" #{icache_checked} onchange="display_cfg()">
					<label class="custom-control-label" for="icache"></label>
				</div>
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-3'>#{lp[66]}</div>
			<div class='col-4'>
				<div class="custom-control custom-switch">
					<input type="checkbox" class="custom-control-input" id="ifix" #{ifix_checked} onchange="display_cfg()">
					<label class="custom-control-label" for="ifix">#{lp[67]}</label>
				</div>
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-3'>#{lp[68]}</div>
			<div class='col-2'>
				<select class="form-control" id='ilist' onchange="display_cfg()">
					<option value='10' #{ilist_10_selected}>10</option>
					<option value='25' #{ilist_25_selected}>25</option>
					<option value='50' #{ilist_50_selected}>50</option>
					<option value='75' #{ilist_75_selected}>75</option>
					<option value='100' #{ilist_100_selected}>100</option>
					<option value='150' #{ilist_150_selected}>150</option>
					<option value='200' #{ilist_200_selected}>200</option>
				</select>
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-3'>#{lp[69]}</div>
			<div class='col-1'>
				<input class="form-control form-control-sm" type="number" min='5' max='20' id='icalc' value='#{icalc}' onchange="display_cfg()">
			</div>
		</div>
		<br>
    	<div class='row'>
	    	<div class='col-3'>#{lp[70]}</div>
			<div class='col-1'>
				<input class="form-control form-control-sm" type="number" min='5' max='20' id='icalcp' value='#{icalcp}' onchange="display_cfg()">
			</div>
		</div>
	</div>
HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Updating bio information
var display_cfg = function(){
	var icache = 0
	var ifix = 0
	if( document.getElementById( "icache" ).checked ){ icache = 1; }else{ icache = 0; }
	if( document.getElementById( "ifix" ).checked ){ ifix = 1; }else{ ifix = 0; }
	var ilist = document.getElementById( "ilist" ).value;
	var icalc = document.getElementById( "icalc" ).value;
	var icalcp = document.getElementById( "icalcp" ).value;
	closeBroseWindows( 1 );

	$.post( "config.cgi", { mod:'display', step:'update', icache:icache, ifix:ifix, ilist:ilist, icalc:icalc, icalcp:icalcp }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
	displayVideo( 'Updated' );
};

</script>
JS
	puts js
end
