#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser meta data viewer 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20180402, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'meta'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

def meta_food( lp )
	fct_num = 0
	fctu_num = 0
	fctp_num = 0

	r = mdb( "SELECT * FROM #{$MYSQL_TB_FCT};", false, @debug )
	fct_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_FCTP};", false, @debug )
	r.each do |e|
		if /U/ =~ e['FN']
			fctu_num += 1
		elsif /P/ =~ e['FN']
			fctp_num += 1
		end
	end

	html = <<-"HTML"
<h5>#{lp[1]}</h5>
<table class="table">
	<thead>
		<tr>
			<th scope="col">#{lp[2]}</th>
			<th scope="col">#{lp[3]}</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>#{lp[4]}</td>
			<td>#{fct_num}</td>
		</tr>
		<tr>
			<td>#{lp[5]}</td>
			<td>#{fctu_num}</td>
		</tr>
		<tr>
			<td>#{lp[6]}</td>
			<td>#{fctp_num}</td>
		</tr>
	</tbody>
</table>
HTML
	return html
end


def meta_user( lp )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER};", false, @debug )
	cumulative_user_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE status=1;", false, @debug )
	general_user_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE status=2;", false, @debug )
	guild_member_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE status=4;", false, @debug )
	guild_moe_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE status=5;", false, @debug )
	guild_shun_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE status=6;", false, @debug )
	children_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE status=3 OR status=8 OR status=9;", false, @debug )
	admin_user_num = r.size

	html = <<-"HTML"
<h5>#{lp[7]}</h5>
<table class="table">
	<thead>
		<tr>
			<th scope="col">#{lp[8]}</th>
			<th scope="col">#{lp[9]}</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>#{lp[26]}</td>
			<td>#{cumulative_user_num - 1}</td>
		</tr>
		<tr>
			<td>#{lp[10]}</td>
			<td>#{general_user_num - 1}</td>
		</tr>
		<tr>
			<td>#{lp[11]}</td>
			<td>#{guild_member_num}</td>
		</tr>
		<tr>
			<td>#{lp[27]}</td>
			<td>#{guild_moe_num}</td>
		</tr>
		<tr>
			<td>#{lp[28]}</td>
			<td>#{guild_shun_num}</td>
		</tr>
		<tr>
			<td>#{lp[12]}</td>
			<td>#{admin_user_num}</td>
		</tr>
		<tr>
			<td>#{lp[29]}</td>
			<td>#{children_num}</td>
		</tr>
	</tbody>
</table>
HTML

	return html
end


def meta_recipe( lp, user )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE};", false, @debug )
	recipe_total_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE role!=100;", false, @debug )
	recipe_real_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE public=1;", false, @debug )
	recipe_public_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE public=1 AND role!=100;", false, @debug )
	recipe_real_public_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}';", false, @debug )
	recipe_user_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_RECIPE} WHERE user='#{user.name}' and public=1;", false, @debug )
	recipe_user_public_num = r.size

	html = <<-"HTML"
<h5>#{lp[13]}</h5>
<table class="table">
	<thead>
		<tr>
			<th scope="col">#{lp[14]}</th>
			<th scope="col">#{lp[15]}</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>#{lp[16]}</td>
			<td>#{recipe_total_num}</td>
		</tr>
		<tr>
			<td>#{lp[30]}</td>
			<td>#{recipe_real_num}</td>
		</tr>
		<tr>
			<td>#{lp[17]}</td>
			<td>#{recipe_public_num}</td>
		</tr>
		<tr>
			<td>#{lp[31]}</td>
			<td>#{recipe_real_public_num}</td>
		</tr>
		<tr>
			<td>#{user.name}#{lp[18]}</td>
			<td>#{recipe_user_num}</td>
		</tr>
		<tr>
			<td>#{user.name}#{lp[19]}</td>
			<td>#{recipe_user_public_num}</td>
		</tr>
	</tbody>
</table>
HTML

	return html
end


def meta_menu( lp, user )
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU};", false, @debug )
	menu_total_num = r.size

	r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE public=1;", false, @debug )
	menu_public_num = r.size

	html = <<-"HTML"
<h5>#{lp[20]}</h5>
<table class="table">
	<thead>
		<tr>
			<th scope="col">#{lp[21]}</th>
			<th scope="col">#{lp[22]}</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>#{lp[23]}</td>
			<td>#{menu_total_num}</td>
		</tr>
		<tr>
			<td>#{lp[24]}</td>
			<td>#{menu_public_num}</td>
		</tr>
	</tbody>
</table>
HTML

	return html
end

#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )


#### Getting POST data
command = cgi['command']
if @debug
	puts "command:#{command}<br>"
	puts "<hr>"
end


html = ''
case command
when 'food'
	html = meta_food( lp )

when 'user'
	html = meta_user( lp )

when 'recipe'
	html = meta_recipe( lp, user )

when 'menu'
	html = meta_menu( lp, user )

else
	html = "#{lp[25]}"
end

puts html
