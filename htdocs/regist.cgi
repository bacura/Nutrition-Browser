#! /usr/bin/ruby
#encoding: utf-8
#Nutrition browser regist 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20170927, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require 'cgi'
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = false


#==============================================================================
#DEFINITION
#==============================================================================

#### HTML regist
def html_regist_form( id, mail, pass, msg, aliasu, lp )
    html = <<-"HTML"
      <div class="container">
        <form action="#{$SCRIPT}?mode=confirm" method="post" class="form-signin login_form">
          #{msg}
          <p class="msg_small">#{lp[4]}</p>
          <input type="text" name="id" value="#{id}" maxlength="30" id="inputID" class="form-control login_input" placeholder="#{lp[5]}" required autofocus>
          <input type="text" name="alias" value="#{aliasu}" maxlength="60" id="inputAlias" class="form-control login_input" placeholder="#{lp[6]}">
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

#### GETデータの取得
get_data = get_data()

#### POSTデータの取得
post_data = CGI.new

html_head( nil, 0, nil )
html_top( nil, nil, nil )

case get_data['mode']
#### 入力内容の確認
when 'confirm'

  # 入力されたIDは英数字以外があるか？
  if /[^0-9a-zA-Z\-\_]/ =~ post_data['id']
    msg = '<p class="msg_small_red">#{lp[1]}</p>'
    html_regist_form( nil, post_data['mail'], nil, msg, post_data['aliasu'], lp )

  # 入力されたIDは文字制限を超えているか？
  elsif post_data['id'].size > 30
    msg = '<p class="msg_small_red">#{lp[2]}</p>'
    html_regist_form( nil, post_data['mail'], nil, msg, post_data['aliasu'], lp )

  # 入力されたIDでユーザーテーブルから抽出
  else
    r = mariadb( "SELECT user FROM #{$MYSQL_TB_USER} WHERE user='#{post_data['id']}';", false )

    #### データベースに同じIDが存在するか？
    # 存在しない
    unless r.first
      html_regist_confirm( post_data['id'], post_data['mail'], post_data['pass'], post_data['aliasu'], lp )
    # 存在する
    else
      msg = '<p class="msg_small_red">#{lp[3]}</p>'
      html_regist_form( nil, post_data['mail'], nil, msg, post_data['aliasu'], lp )
    end
  end


#### 入力内容の登録
when 'finish'
  #ユーザーテーブルの登録
  aliasu = post_data['alias']
  aliasu = post_data['id'] if aliasu == ''

  mariadb( "INSERT INTO #{$MYSQL_TB_USER} SET user='#{post_data['id']}', pass='#{post_data['pass']}', mail='#{post_data['mail']}',aliasu='#{aliasu}', status=1, reg_date='#{$DATETIME}', count=0;", false )

  #パレットテーブルの登録
  mariadb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{post_data['id']}', name='簡易表示用', count='5', palette='00000100101000001000000000000000000000000000000000000000100000000000';", false )
  mariadb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{post_data['id']}', name='基本の5成分', count='5', palette='00000100101000001000000000000000000000000000000000000000100000000000';", false )
  mariadb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{post_data['id']}', name='基本の14成分', count='14', palette='0000010010100000100010111011000000000000100000011000000110000000000';", false )
  mariadb( "INSERT INTO #{$MYSQL_TB_PALETTE} SET user='#{post_data['id']}', name='全て', count='63', palette='0000011111111111111111111111111111111111111111111111111111111111110';", false )

  #履歴テーブルの登録
  mariadb( "INSERT INTO #{$MYSQL_TB_HIS} SET user='#{post_data['id']}', his='';", false )

  #合計テーブルの登録
  mariadb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{post_data['id']}', sum='';", false )

  #食事テーブルの登録
  mariadb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{post_data['id']}', meal='';", false )

  #コンフィグテーブルの登録
  mariadb( "INSERT INTO #{$MYSQL_TB_CFG} SET user='#{post_data['id']}', recipel='1:0:99:99:99:99:99';", false )

  html_regist_finish( lp )

#### 初期入力フォーム
else
  html_regist_form( nil, nil, nil, nil, nil, lp )
end

html_foot()
