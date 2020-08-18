#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser school 0.00b


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script = 'school-menu'
@debug = true
label_school = '[料理教室]'


#==============================================================================
#DEFINITION
#==============================================================================


#==============================================================================
# Main
#==============================================================================
cgi = CGI.new

html_init( nil )

user = User.new( cgi )
user.debug if @debug
lp = user.language( script )

#### Guild member check
if user.status < 5
	puts "Guild member shun error."
	exit
end


#### Getting POST
command = cgi['command']
if @debug
	puts "command:#{command}<br>\n"
	puts "<hr>\n"
end


#### HTML school menu
html_school_menu = "<table class='table table-hover table-sm'>"
		html_school_menu << "<thead><tr>"
		html_school_menu << "<th>#{lp[5]}</th>"
		html_school_menu << "<th>#{lp[6]}</th>"
		html_school_menu << "<th>#{lp[7]}</th>"
		html_school_menu << "<th>#{lp[8]}</th>"
		html_school_menu << "</tr></thead>"
r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE user='#{user.name}' AND label='#{label_school}';", false, @debug)
menu_list = []
r.each do |e|
	html_school_menu << "<tr>"
	html_school_menu << "<td>#{e['name']}</td>"
	html_school_menu << "<td>#{e['memo']}</td>"

	rr = mdb( "SELECT * FROM #{$MYSQL_TB_SCHOOLM} WHERE user='#{user.name}' AND code='#{e['code']}';", false, @debug)
	if rr.first
		html_school_menu << "<td>#{rr.first['course']}</td>"
	else
		html_school_menu << "<td>#{lp[9]}</td>"
	end
	html_school_menu << '</tr>'

end
html_school_menu << '</table>'


html = <<-"HTML"
<div class='container-fluid'>
	<div class='row'>
		<div class='col-3'><h5>#{lp[1]}</h5></div>
	</div>
	<div class='row'>
		<div class='col-3'><h6>#{lp[2]}</h6></div>
	</div>
	<hr>
	<div class='row'>
		<div class='col-3'><h6>#{lp[3]}</h6></div>
	</div>
	<hr>
	<div class='row'>
		<div class='col-3'><h6>#{lp[4]}</h6></div>
	</div>
	#{html_school_menu}

HTML

puts html
