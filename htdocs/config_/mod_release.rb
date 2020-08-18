# Config module for release 0.00b
#encoding: utf-8

def config_module( cgi, user, lp )
	module_js()

	step = cgi['step']
	password = cgi['password']
	html =''

	if step ==  ''
		html = <<-"HTML"
      	<div class="container">
      		<div class='row'>
	    		#{lp[34]}<br>
    			#{lp[35]}<br>
				#{lp[36]}<br>
			</div><br>
      		<div class='row'>
				<div class='col-4'><input type="password" id="password" class="form-control login_input" placeholder="#{lp[37]}"></div>
				<div class='col-4'><button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="release_cfg()">#{lp[38]}</button></div>
			</div>
		</div>
HTML
	else
		if user.status == 3 || user.status == 9
			html = <<-"HTML"
      		<div class="container">
      			<div class='row'>
	    			#{lp[39]}
				</div>
			</div>
HTML

			# Updating user table
			query = "UPDATE #{$MYSQL_TB_USER} SET status='0' WHERE user='#{user.name}' AND cookie='#{uid}';"
			db_err = 'SELECT user'
			db_process( query, db_err, false )

			# Deleting indivisual data
			# History
			query = "DELETE FROM #{$MYSQL_TB_HIS} WHERE user='#{user.name}';"
			db_err = 'SELECT his'
			db_process( query, db_err, false )

			# SUM
			query = "DELETE FROM #{$MYSQL_TB_SUM} WHERE user='#{user.name}';"
			db_err = 'SELECT sum'
			db_process( query, db_err, false )

			# Config
			query = "DELETE FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';"
			db_err = 'SELECT cfg'
			db_process( query, db_err, false )

			# meal
			query = "DELETE FROM #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';"
			db_err = 'SELECT meal'
			db_process( query, db_err, false )

			# Master price
			query = "DELETE FROM #{$MYSQL_TB_PRICEM} WHERE user='#{user.name}';"
			db_err = 'SELECT pricem'
			db_process( query, db_err, false )

			# Palette
			query = "DELETE FROM #{$MYSQL_TB_PALETTE} WHERE user='#{user.name}';"
			db_err = 'SELECT palette'
			db_process( query, db_err, false )
		else
			html = <<-"HTML"
      		<div class="container">
      			<div class='row'>
	    			#{lp[40]}
				</div>
			</div>
HTML
		end

		return html
	end
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var release_cfg = function(){
	var password = document.getElementById( "password" ).value;
	closeBroseWindows( 2 );

	$.post( "config.cgi", { mod:'release', step:step, password:password }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
};

</script>
JS
	puts js
end
