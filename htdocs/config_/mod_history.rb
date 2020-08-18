# Config module for history 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()

	case cgi['step']
	when 'max'
		his_max = cgi['his_max'].to_i
		his_max = 200 if his_max == nil || his_max == 0 || his_max > 1000
		mdb( "UPDATE #{$MYSQL_TB_CFG} SET his_max='#{his_max}' WHERE user='#{user.name}';", false, @debug )
	when 'clear'
		mdb( "UPDATE #{$MYSQL_TB_HIS} SET his='' WHERE user='#{user.name}';", false, @debug )
	end

	####
	his_max = 200
	r = mdb( "SELECT his_max FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
	his_max = r.first['his_max'].to_i if r.first

	html = <<-"HTML"
     <div class="container">

      	<div class='row'>
      		<h5>#{lp[27]}</h5>
      	</div>
     	<div class='row'>
			<div class='col-2'>#{his_max} #{lp[31]}</div>
			<div class='col-1' align='right'>200</div>
			<div class='col-8'>
				<input type="range" class="custom-range" min="200" max="1000" step="100" value='#{his_max}' id="his_max" onclick="history_cfg( 'max' )">
			</div>
			<div class='col-1'>1000</div>
		</div>
		<br>
     	#{lp[28]}

     	<hr>
      	<div class='row'>
    		#{lp[29]}<br>
    	</div>
    	<br>
		<button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="history_cfg( 'clear' )">#{lp[30]}</button>
	</div>
HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// History initialisation
var history_cfg = function( step ){
	var his_max = document.getElementById( "his_max" ).value;
	closeBroseWindows( 2 );
	$.post( "config.cgi", { mod:'history', step:step, his_max:his_max }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	if( step == 'clear' ){
		displayVideo( 'Initialized' );
	}
	if( step == 'max' ){
		displayVideo( 'History max -> '+ his_max );
	}
};


</script>
JS
	puts js
end
