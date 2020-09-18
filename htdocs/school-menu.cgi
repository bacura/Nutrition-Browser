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
if user.status < 5 && user.status != 6
	puts "Guild member shun error."
	exit
end


#### Getting POST
command = cgi['command']
if @debug
	puts "command:#{command}<br>\n"
	puts "<hr>\n"
end


####
label_set = []
r = mdb( "SELECT schooll FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, @debug )
if r.first
	a =  r.first['schooll'].split( ':' )
	a.each do |e|
		label_set << e if e != '' &&  e != nil
	end
end


html_school_menu = ""
#### HTML school menu
html_school_menu << "<table class='table table-hover table-sm'>"
html_school_menu << "<thead><tr>"
html_school_menu << "<th>#{lp[2]}</th>"
html_school_menu << "<th>#{lp[7]}</th>"
html_school_menu << "<th>#{lp[5]}</th>"
html_school_menu << "<th>#{lp[6]}</th>"
html_school_menu << "<th>#{lp[8]}</th>"
html_school_menu << "</tr></thead>"
label_set.each do |e|
	html_school_menu << "<tr><td>#{e}</td></tr>"
	r = mdb( "SELECT * FROM #{$MYSQL_TB_MENU} WHERE user='#{user.name}' AND label='#{e}';", false, @debug)
	r.each do |ee|
		html_school_menu << "<tr>"
		html_school_menu << "<td></td>"
		html_school_menu << "<td>-</td>"
		html_school_menu << "<td>#{ee['name']}</td>"
		html_school_menu << "<td>#{ee['memo']}</td>"
		html_school_menu << "<td></td>"
		html_school_menu << "<td></td>"
		html_school_menu << '</tr>'
	end
end
html_school_menu << '</table>'

html = <<-"HTML"
<div class='container-fluid'>

	#{html_school_menu}
</div>
HTML

puts html
