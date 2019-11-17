#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser login 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20170928, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require 'securerandom'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### HTML login
def html_login_form( msg, lp )
  html = <<-"HTML"
    <div class="container">
      <div class="row">
        <div class="col-6">
          <form action="#{$SCRIPT}?mode=check" method="post" class="form-signin login_form">
          #{msg}
          <p class="msg_small">#{lp[1]}</p>
          <input type="text" name="id" id="inputID" class="form-control login_input" placeholder="ID" required autofocus>
          <input type="password" name="pass" id="inputPassword" class="form-control login_input" placeholder="#{lp[2]}" required>
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


#==============================================================================
# Main
#==============================================================================

#### Getting GET data
get_data = get_data()


#### Getting POST date
cgi = CGI.new
uname, uid, status, aliasu, language = login_check( cgi )
lp = lp_init( 'login', $DEFAULT_LP )

case get_data['mode']
when 'check'
  #### 入力されたIDとパスワードでユーザーテーブルから抽出
  r = mariadb( "SELECT user, status, count FROM #{$MYSQL_TB_USER} WHERE user='#{cgi['id']}' AND pass='#{cgi['pass']}' AND status>'0';", true )

  # データベースに該当ユーザーが存在するか？
  # 存在しない
  unless r.first
      html_init( nil )
      html_head( nil, 0, nil )
      html_top( nil, nil, nil )
      msg = "<p class='msg_small_red'>#{lp[4]}</p>"
      html_login_form( msg, lp )

  # 存在する
  else
    status = r.first['status'].to_i
    # Cookieの発行
    uid = SecureRandom.hex(16)
    cookie = "Set-Cookie: NAME=#{cgi['id']}\nSet-Cookie: UID=#{uid}\n"

    #### ユーザー情報の更新
    count = r.first['count'] += 1
    mariadb( "UPDATE #{$MYSQL_TB_USER} SET cookie='#{uid}', login_date='#{$DATETIME}', count=#{count} WHERE user='#{cgi['id']}';", true )

    html_init( cookie )
    html_head( 'refresh', status, nil )

    #### 基本テーブルのチェック＆修復
    # 履歴テーブルの修復
    r = mariadb( "SELECT user FROM #{$MYSQL_TB_HIS} WHERE user='#{cgi['id']}';", false )
    unless r.first
      mariadb( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{cgi['id']}', his='';", false )
    end

    # 合計テーブルののチェック＆修復
    r = mariadb( "SELECT user FROM #{$MYSQL_TB_SUM} WHERE user='#{cgi['id']}';", false )
    unless r.first
      mariadb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{cgi['id']}', sum='';", false )
    end

    # 食事テーブルののチェック＆修復
    r = mariadb( "SELECT user FROM #{$MYSQL_TB_MEAL} WHERE user='#{cgi['id']}';", false )
    unless r.first
      mariadb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{cgi['id']}', meal='';", false )
    end

    # コンフィグテーブルののチェック＆修復
    r = mariadb( "SELECT user FROM #{$MYSQL_TB_CFG} WHERE user='#{cgi['id']}';", false )
    unless r.first
      mariadb( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{cgi['id']}', recipel='1:0:0:0:0:0:0';", false )
    end
  end

when 'logout'
    # Meaningless Cookie
    cookie = "Set-Cookie: NAME=NULL\nSet-Cookie: UID=NULL\n"
    html_init( cookie )
    html_head( 'refresh', 0, nil )

# Input form init
else
  html_init( nil )
  html_head( nil, 0, nil )
  html_top( nil, nil, nil )
  html_login_form( nil, lp )
end

html_foot()
