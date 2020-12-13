#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser regist 0.00b

#==============================================================================
#CHANGE LOG
#==============================================================================
#20170927, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
script='regist'
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### HTML top
def html_top_regist( lp )
  login_color = "secondary"
  login = "<a href='login.cgi' class=\"text-#{login_color}\">#{lp[17]}</a>&nbsp;|&nbsp;<a href=\"regist.cgi\" class=\"text-#{login_color}\">#{lp[24]}</a>"

  html = <<-"HTML"
      <header class="navbar navbar-dark bg-dark" id="header">
        <div class='row'>
          <div class='col-3'><h2><a href="index.cgi" class="text-#{login_color}">#{lp[25]}</a></h2></div>
          <div class='col-4'><span class="text-#{login_color} login_msg"><h3>#{login}</h3></span></div>
          <div class='col-1'><a href='https://neg.bacura.jp/?page_id=1154' target='manual'>#{lp[26]}</a></div>
          <div class='col-4'>
            <div class="input-group">
              <select class="form-select" id="qcate">
                <option value='0'>#{lp[28]}</option>
                <option value='1'>#{lp[29]}</option>
                <option value='2'>#{lp[20]}</option>
              </select>
              <input class="form-control" type="search" maxlength="100" id="words" onchange="searchBWL1()">
              <btton class='btn btn-sm' onclick="searchBWL1()">#{lp[27]}</button>
            </div>
          </div>
        </div>
      </header>
HTML

  puts html
end


#### Language init
def lp_init( script, language_set )
  f = open( "#{$HTDOCS_PATH}/language_/#{script}.#{language_set}", "r" )
  lp = [nil]
  f.each do |line|
    lp << line.chomp.force_encoding( 'UTF-8' )
  end
  f.close

  return lp
end


#### HTML regist
def html_regist_form( id, mail, pass, msg, aliasu, lp )
    html = <<-"HTML"
      <div class="container">
        <form action="regist.cgi?mode=confirm" method="post" class="form-signin login_form">
          #{msg}
          <p class="msg_small">#{lp[4]}</p>
          <input type="text" name="id" value="#{id}" maxlength="30" id="inputID" class="form-control login_input" placeholder="#{lp[5]}" required autofocus>
          <input type="text" name="aliasu" value="#{aliasu}" maxlength="60" id="inputAlias" class="form-control login_input" placeholder="#{lp[6]}">
          <input type="email" name="mail" value="#{mail}" maxlength="60" id="inputMail" class="form-control login_input" placeholder="#{lp[7]}">
          <input type="text" name="pass" value="#{pass}" maxlength="30" id="inputPassword" class="form-control login_input" placeholder="#{lp[8]}" required>
          <input type="submit" value="#{lp[9]}" class="btn btn-lg btn-success btn-block"></input>
        </form>
      </div>

      <hr>
      <div  class="container" id='rule'></div>
      <script>$( function(){ $( "#rule" ).load( "books/guide/rule.html" );} );</script>
HTML

  puts html
end


#### HTML regist confirm
def html_regist_confirm( id, mail, pass, aliasu, lp )
    html = <<-"HTML"
      <div class="container">
        <form action="regist.cgi?mode=finish" method="post" class="form-signin login_form">
          <p class="msg_small">#{lp[10]}</p>
          <table class="table">
              <tr>
                <td>#{lp[11]}</td>
                <td>#{id}</td>
              </tr>
              <tr>
                <td>#{lp[12]}</td>
                <td>#{aliasu}</td>
              </tr>
              <tr>
                <td>#{lp[13]}</td>
                <td>#{mail}</td>
              </tr>
              <tr>
                <td>#{lp[14]}</td>
                <td>#{pass}</td>
              </tr>
          </table>
          <input type="hidden" name="id" value="#{id}" id="inputID" class="form-control login_input" placeholder="#{lp[11]}">
          <input type="hidden" name="alias" value="#{aliasu}" id="inputAlias" class="form-control login_input" placeholder="#{lp[12]}">
          <input type="hidden" name="mail" value="#{mail}" id="inputMail" class="form-control login_input" placeholder="#{lp[13]}">
          <input type="hidden" name="pass" value="#{pass}" id="inputPassword" class="form-control login_input" placeholder="#{lp[14]}">
          <input type="submit" value="#{lp[15]}" class="btn btn-lg btn-warning btn-block"></input>
          <input type="button" value="#{lp[19]}" class="btn btn-lg btn-secondary btn-block" onclick="history.back()"></input>
        </form>
      </div>
HTML

  puts html
end


#### HTML regist finish
def html_regist_finish( lp )
    html = <<-"HTML"
      <div class="container">
          <p class="reg_msg">#{lp[16]}<a href="login.cgi">#{lp[17]}<a/>#{lp[18]}</p>
      </div>
HTML

  puts html
end


#==============================================================================
# Main
#==============================================================================
html_init( nil )

lp = lp_init( 'regist', $DEFAULT_LP )

#### Getting GET data
get_data = get_data()

#### Getting POST data
post_data = CGI.new

html_head( nil, 0, nil )
html_top_regist( lp )

case get_data['mode']
# Confomation of user data
when 'confirm'

  # Checking improper characters
  if /[^0-9a-zA-Z\-\_]/ =~ post_data['id']
    msg = '<p class="msg_small_red">#{lp[1]}</p>'
    html_regist_form( nil, post_data['mail'], nil, msg, post_data['aliasu'], lp )

  # Checking character limit
  elsif post_data['id'].size > 30
    msg = '<p class="msg_small_red">#{lp[2]}</p>'
    html_regist_form( nil, post_data['mail'], nil, msg, post_data['aliasu'], lp )

  # OK
  else
    # Checking same ID
    r = mdb( "SELECT user FROM #{$MYSQL_TB_USER} WHERE user='#{post_data['id']}';", false, @debug )
    unless r.first
      html_regist_confirm( post_data['id'], post_data['mail'], post_data['pass'], post_data['aliasu'], lp )
    else
      msg = '<p class="msg_small_red">#{lp[3]}</p>'
      html_regist_form( nil, post_data['mail'], nil, msg, post_data['aliasu'], lp )
    end
  end


#### Finishing registration of new user
when 'finish'
  # Inserting user information
  aliasu = post_data['alias']
  aliasu = post_data['id'] if aliasu == ''

  mdb( "INSERT INTO #{$MYSQL_TB_USER} SET user='#{post_data['id']}', pass='#{post_data['pass']}', mail='#{post_data['mail']}',aliasu='#{aliasu}', status=1, reg_date='#{$DATETIME}', count=0;", false, @debug )

  # Inserting standard palettes
  mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{post_data['id']}', name='#{lp[20]}', count='5', palette='00000100101000001000000000000000000000000000000000000000100000000000';", false, @debug )
  mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{post_data['id']}', name='#{lp[21]}', count='5', palette='00000100101000001000000000000000000000000000000000000000100000000000';", false, @debug )
  mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{post_data['id']}', name='#{lp[22]}', count='14', palette='0000010010100000100010111011000000000000100000011000000110000000000';", false, @debug )
  mdb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{post_data['id']}', name='#{lp[23]}', count='63', palette='0000011111111111111111111111111111111111111111111111111111111111110';", false, @debug )

  # Inserting new history
  mdb( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{post_data['id']}', his='';", false, @debug )

  # Inserting new SUM
  mdb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{post_data['id']}', sum='';", false, @debug )

  # Inserting new meal
  mdb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{post_data['id']}', meal='';", false, @debug )

  # Inserting new config
  mdb( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{post_data['id']}', recipel='1:0:99:99:99:99:99', koyomiex='0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t:0\t\t';", false, @debug )

  html_regist_finish( lp )

#### Input form
else
  html_regist_form( nil, nil, nil, nil, nil, lp )
end

html_foot()
