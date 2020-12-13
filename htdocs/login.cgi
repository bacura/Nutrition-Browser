#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser login 0.00


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false
script = 'login'


#==============================================================================
#DEFINITION
#==============================================================================

#### HTML login
def html_login_form( msg, lp )
  html = <<-"HTML"
    <div class="container">
      <div class="row">
        <div class="col-6">
          <form action="login.cgi?mode=check" method="post" class="form-signin login_form">
          #{msg}
          <p class="msg_small">#{lp[1]}</p>
          <input type="text" name="id" id="inputID" class="form-control login_input" placeholder="ID" required autofocus>
          <input type="password" name="pass" id="inputPassword" class="form-control login_input" placeholder="#{lp[2]}">
          <input type="submit" value="#{lp[3]}" class="btn btn-lg btn-primary btn-block"></input>
          </form>
        </div>
        <div class="col-6">
          [空き地]
        </div>
      </div>
    </div>
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


#### HTML top
def html_top_login( lp )
  login_color = "secondary"
  login = "<a href='login.cgi' class=\"text-#{login_color}\">#{lp[3]}</a>&nbsp;|&nbsp;<a href=\"regist.cgi\" class=\"text-#{login_color}\">#{lp[8]}</a>"

  html = <<-"HTML"
      <header class="navbar navbar-dark bg-dark" id="header">
        <div class='row'>
          <div class='col-3'><h2><a href="index.cgi" class="text-#{login_color}">#{lp[7]}</a></h2></div>
          <div class='col-4'><span class="text-#{login_color} login_msg"><h3>#{login}</h3></span></div>
          <div class='col-1'><a href='https://neg.bacura.jp/?page_id=1154' target='manual'>#{lp[5]}</a></div>
          <div class='col-4'>
            <div class="input-group">
              <select class="form-select" id="qcate">
                <option value='0'>#{lp[9]}</option>
                <option value='1'>#{lp[10]}</option>
                <option value='2'>#{lp[11]}</option>
              </select>
              <input class="form-control" type="search" maxlength="100" id="words" onchange="searchBWL1()">
              <btton class='btn btn-sm' onclick="searchBWL1()">#{lp[6]}</button>
            </div>
          </div>
        </div>
      </header>
HTML

  puts html
end

#==============================================================================
# Main
#==============================================================================

#### Getting GET data
get_data = get_data()


#### Getting POST date
cgi = CGI.new
user = User.new( cgi )
user.debug if @debug
lp = lp_init( script, $DEFAULT_LP )

case get_data['mode']
when 'check'
  #### Checking user ID on DB
  r = mdb( "SELECT user, status, count FROM #{$MYSQL_TB_USER} WHERE user='#{cgi['id']}' AND pass='#{cgi['pass']}' AND status>'0';", true, @debug )
  unless r.first
      html_init( nil )
      html_head( nil, 0, nil )
      html_top_login( lp )
      msg = "<p class='msg_small_red'>#{lp[4]}</p>"
      html_login_form( msg, lp )

  else
    status = r.first['status'].to_i

    # Issuing cookies
    uid = SecureRandom.hex(16)
    mid = ''
    mid = uid if r.first['status'].to_i >= 5 && r.first['status'].to_i != 6

    cookie = "Set-Cookie: NAME=#{cgi['id']}\nSet-Cookie: UID=#{uid}\nSet-Cookie: MID=#{mid}\n"

    # Updating user information
    count = r.first['count'] += 1
    mdb( "UPDATE #{$MYSQL_TB_USER} SET cookie='#{uid}', cookie_m='#{mid}', login_date='#{$DATETIME}', count=#{count} WHERE user='#{cgi['id']}';", true, @debug )

    html_init( cookie )
    html_head( 'refresh', status, nil )

    # Checking & repairing history table
    r = mdb( "SELECT user FROM #{$MYSQL_TB_HIS} WHERE user='#{cgi['id']}';", false, @debug )
    unless r.first
      mdb( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{cgi['id']}', his='';", false, @debug )
    end

    # Checking & repairing SUM table
    r = mdb( "SELECT user FROM #{$MYSQL_TB_SUM} WHERE user='#{cgi['id']}';", false, @debug )
    unless r.first
      mdb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{cgi['id']}', sum='';", false, @debug )
    end

    # Checking & repairing meal table
    r = mdb( "SELECT user FROM #{$MYSQL_TB_MEAL} WHERE user='#{cgi['id']}';", false, @debug )
    unless r.first
      mdb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{cgi['id']}', meal='';", false, @debug )
    end

    # Checking & repairing config table
    r = mdb( "SELECT user FROM #{$MYSQL_TB_CFG} WHERE user='#{cgi['id']}';", false, @debug )
    unless r.first
      mdb( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{cgi['id']}', recipel='1:0:0:0:0:0:0';", false, @debug )
    end
  end

when 'logout'
  # Meaningless Cookie
  cookie = "Set-Cookie: NAME=NULL\nSet-Cookie: UID=NULL\nSet-Cookie: MID=NULL\n"
  html_init( cookie )
  html_head( 'refresh', 0, nil )

when 'daughter'
  cookie = ''
  uid = ''
  login_mv = get_data['login_mv']

  r = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user='#{login_mv}';", true, @debug )
  if r.first
    count = r.first['count'] += 1
    if r.first['mom'] == '' ||  r.first['mom'] == nil
        cookie = "Set-Cookie: NAME=#{login_mv}\nSet-Cookie: UID=#{r.first['cookie']}\n"
        uid = r.first['cookie']
    else
      rr = mdb( "SELECT * FROM #{$MYSQL_TB_USER} WHERE user=\"#{r.first['mom']}\";", true, @debug )
      if rr.first
        # Issuing cookies
        uid = SecureRandom.hex( 16 )
        cookie = "Set-Cookie: NAME=#{login_mv}\nSet-Cookie: UID=#{uid}\nSet-Cookie: MID=#{rr.first['cookie_m']}\n"
      end
    end
    mdb( "UPDATE #{$MYSQL_TB_USER} SET cookie='#{uid}', login_date='#{$DATETIME}', count=#{count} WHERE user='#{login_mv}';", true, @debug )
  end

  html_init( cookie )
  html_head( 'refresh', r.first['status'], nil )

# Input form init
else
  html_init( nil )
  html_head( nil, 0, nil )
  html_top_login( lp )
  html_login_form( nil, lp )
end

html_foot()
