# Config module for sum 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']

	if step == 'reset'
		query = "UPDATE sum set sum='', name='', code='' WHERE user='#{user.name}';"
		db_err = 'UPDATE sum'
		db_process( query, db_err, false )
	end
	html = <<-"HTML"
     <div class="container">
      	<div class='row'>
    		#{lp[32]}<br>
    	</div><br>
		<button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="sum_cfg( 'reset' )">#{lp[33]}</button>
	</div>
HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// Chopping board initialisation
var sum_cfg = function( step ){
	closeBroseWindows( 2 );
	$.post( "config.cgi", { com:'sum', step:step }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	if( step == 'clear' ){
		displayVideo( 'Initialized' );
	}

	var fx = function(){
		refreshCB();
	};
	setTimeout( fx, 1000 );
};

</script>
JS
	puts js
end
