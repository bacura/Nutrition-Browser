# Config module for FCTB history 0.00
#encoding: utf-8

def config_module( cgi, user )
	module_js()

	case cgi['step']
	when 'max'
		his_max = cgi['his_max'].to_i
		his_max = 200 if his_max == nil || his_max == 0 || his_max > 500
		mariadb( "UPDATE #{$MYSQL_TB_CFG} SET his_max='#{his_max}' WHERE user='#{user.name}';", false )
	when 'clear'
		mariadb( "UPDATE #{$MYSQL_TB_HIS} SET his='' WHERE user='#{user.name}';", false )
	end


	####
	checked_max2 = ''
	checked_max5 = ''
	r = mariadb( "SELECT his_max FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false )
	if r.first
		if r.first['his_max'].to_i == 200
			checked_max2 = 'checked'
			checked_max5 = ''

		else
			checked_max2 = ''
			checked_max5 = 'checked'
		end
	else
		checked_max2 = 'checked'
		checked_max5 = ''
	end



	html = <<-"HTML"
     <div class="container">

      	<div class='row'>
      		<h5>履歴保存量</h5>
      	</div>
       	<div class='row'>
			<div class="form-check form-check-inline">
  				<input class="form-check-input" type="radio" name="max" onChange="history_cfg( 'max', '200' )" #{checked_max2}>
  				<label class="form-check-label" for="max2">200</label>
			</div>
			<div class="form-check form-check-inline">
  				<input class="form-check-input" type="radio" name="max" onChange="history_cfg( 'max', '500' )" #{checked_max5}>
  				<label class="form-check-label" for="max5">500</label>
			</div>
		</div>
		<br>
     	※増やすとレスポンスが悪くなるかもしれません。

     	<hr>
      	<div class='row'>
    		履歴を初期化する場合は、履歴初期化ボタンを押してください。<br>
    	</div>
    	<br>
		<button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="history_cfg( 'clear', '' )">履歴初期化</button>
	</div>
HTML
	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

// History initialisation
var history_cfg = function( step, his_max ){
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
