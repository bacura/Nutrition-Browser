#! /usr/bin/ruby
# coding: UTF-8
#Nutrition browser index page 0.00b

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
@debug = false
script = 'index'

#==============================================================================
#DEFINITION
#==============================================================================

#### HTML top
def html_top( user )
  user_name = user.name
  user_name = user.aliasu if user.aliasu != '' && user.aliasu != nil
  uid = user.uid
  mid = user.mid

  case user.status
  when 1
    login_color = "primary"
  when 3, 6
    login_color = "warning"
  when 2, 4
    login_color = "info"
  when 5
    login_color = "success"
  when 8, 9
    login_color = "danger"
  else
    login_color = "secondary"
  end

  mom = ''
  mom_a = ''
  daughters = []
  daughters_a = []
  mom_flag = false

  if user.mom == user.name
    r = mdb( "SELECT * FROM user WHERE mom='#{user.name}' AND status='6';", false, false )
    r.each do |e|
      if e['switch'] == 1
        daughters << e['user']
        daughters_a << e['aliasu'].to_s
      end
    end
    mom = user.name
    mom_a = user.aliasu
  else
    r = mdb( "SELECT * FROM user WHERE user='#{user.mom}';", false, false )
    if r.first
      if r.first['cookie_m'] == mid
        mom = r.first['user']
        mom_a = r.first['aliasu']
        mom_a = mom if mom_a == ''

        rr = mdb( "SELECT * FROM user WHERE mom='#{mom}' AND status='6';", false, false )
        rr.each do |e|
          if e['switch'] == 1
            daughters << e['user']
            daughters_a << e['aliasu'].to_s
          end
        end
      end
    end
  end

  login = ''
  if daughters.size > 0 || mom_flag
    login = "<div class='form-inline'>"
    login << "<SELECT style='background-color:#343a40' id='login_mv' class='custom-select text-#{login_color}' onchange=\"chageAccountM( '#{mid}' )\">"
    login << "<OPTION value='#{mom}'>#{mom_a}</OPTION>"
    daughters.size.times do |c|
      t = daughters[c]
      t = daughters_a[c] unless daughters_a[c] == ''
      if daughters[c] == user.name
        login << "<OPTION value='#{daughters[c]}' SELECTED>#{t}</OPTION>"
      else
        login << "<OPTION value='#{daughters[c]}'>#{t}</OPTION>"
      end
    end
    login << "</SELECT>"
    login << "&nbsp;さん&nbsp;|&nbsp;<a href=\"login.cgi?mode=logout\" class=\"text-#{login_color}\">ログアウト</a>"
    login << "</div>"
  else
    login = "#{user_name}&nbsp;さん&nbsp;|&nbsp;<a href=\"login.cgi?mode=logout\" class=\"text-#{login_color}\">ログアウト</a>"
  end
  login = "<a href='login.cgi' class=\"text-#{login_color}\">ログイン</a>&nbsp;|&nbsp;<a href=\"regist.cgi\" class=\"text-#{login_color}\">登録</a>" if user_name == nil

  html = <<-"HTML"
      <header class="navbar navbar-dark bg-dark" id="header">
        <h4><a href="index.cgi" class="text-#{login_color}">栄養ブラウザ</a></h4>
        <span class="text-#{login_color} login_msg"><h5>#{login}</h5></span>
        <a href='http://neg.bacura.jp/?p=523' target='manual'><span class="text-#{login_color} login_msg"><h5>手引き</h5></span></a>
        <span class="form-inline form-inline-sm">
          <div class="input-group mb-3">
            <div class="input-group-prepend">
              <select class="form-control form-control-sm" id="qcate">
                <option value='0'>食品</option>
                <option value='1'>レシピ</option>
                <option value='2'>記憶</option>
              </select>
            </div>
            <input class="form-control form-control-sm" type="text" maxlength="100" id="words" onchange="searchBWL1()">
            <div class="input-group-append">
              <button class="btn btn-outline-#{login_color} btn-sm" onclick="searchBWL1()">検索</button>
            </div>
          </div>
        </span>
      </header>
HTML

  puts html
end

#### HTML nav
def html_nav( user, lp )
  cb_num = ''
  meal_num = ''
  # まな板カウンター
  if user.name
    r = mdb( "SELECT sum from #{$MYSQL_TB_SUM} WHERE user='#{user.name}';", false, @debug )
    if r.first
      t = []
      t = r.first['sum'].split( "\t" ) if r.first['sum']
      cb_num = t.size
    else
      mdb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{user.name}';", false, @debug )
      cb_num = 0
    end
    # 献立カウンター
    r = mdb( "SELECT meal from #{$MYSQL_TB_MEAL} WHERE user='#{user.name}';", false, @debug )
    if r.first
      t = []
      t = r.first['meal'].split( "\t" ) if r.first['meal']
      meal_num = t.size
    else
      mdb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{user.name}';", false, @debug )
      meal_num = 0
    end
  else
    cb_num = '-'
    meal_num = '-'
  end

  # 履歴ボタンとまな板ボタンの設定
  if user.status >= 1
    cb = "#{lp[1]} <span class=\"badge badge-pill badge-warning\" id=\"cb_num\">#{cb_num}</span>"
    mb = "#{lp[2]} <span class=\"badge badge-pill badge-warning\" id=\"mb_num\">#{meal_num}</span>"
    special_button = "<button type=\"button\" class=\"btn btn-outline-dark btn-sm nav_button\" id=\"category0\" onclick=\"summonBWL1( 0 )\">#{lp[3]}</button>"
    his_button = "<button type=\"button\" class=\"btn btn-dark btn-sm nav_button\" onclick=\"historyBWL1( 'recent', '100', '1', 'all' )\">#{lp[4]}</button>"
    sum_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"initCB_BWL1( '' )\">#{cb}</button>"
    recipe_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"recipeList( 'init' )\">#{lp[5]}</button>"
    menu_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"initMeal_BWL1( '' )\">#{mb}</button>"
    set_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"menuList()\">#{lp[6]}</button>"
    config_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"configInit( '' )\">#{lp[7]}</button>"
  else
    cb = "#{lp[1]} <span class=\"badge badge-pill badge-secondary\" id=\"cb_num\">#{cb_num}</span>"
    mb = "#{lp[2]} <span class=\"badge badge-pill badge-secondary\" id=\"mb_num\">#{meal_num}</span>"
    special_button = "<button type=\"button\" class=\"btn btn-outline-secondary btn-sm nav_button\" onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[3]}</button>"
    his_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[4]}</button>"
    sum_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{cb}</button>"
    recipe_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[5]}</button>"
    menu_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{mb}</button>"
    set_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[6]}</button>"
    config_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[7]}</button>"
  end

  if user.status >= 3
    g_button = "<button type='button' class='btn btn btn-warning btn-sm nav_button text-warning guild_color' onclick=\"changeMenu( '#{user.status}' )\">G</button>"
  else
    g_button = "<button type='button' class='btn btn btn-warning btn-sm nav_button text-dark guild_color' onclick=\"displayVideo( '#{lp[9]}' )\">G</button>"
  end

  gm_account = ''
  gm_account = "<button type='button' class='btn btn-warning btn-sm nav_button text-warning guild_color' onclick=\"initAccount_BWL1( 'init' )\">#{lp[34]}</button>" if user.status == 9

	html = <<-"HTML"
      <nav class='container-fluid'>
          #{g_button}
          <button type="button" class="btn btn-info btn-sm nav_button" id="category1" onclick="summonBWL1( 1 )">#{lp[10]}</button>
          <button type="button" class="btn btn-info btn-sm nav_button" id="category2" onclick="summonBWL1( 2 )">#{lp[11]}</button>
          <button type="button" class="btn btn-info btn-sm nav_button" id="category3" onclick="summonBWL1( 3 )">#{lp[12]}</button>
          <button type="button" class="btn btn-danger btn-sm nav_button" id="category4" onclick="summonBWL1( 4 )">#{lp[13]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button" id="category5" onclick="summonBWL1( 5 )">#{lp[14]}</button>
          <button type="button" class="btn btn-success btn-sm nav_button" id="category6" onclick="summonBWL1( 6 )">#{lp[15]}</button>
          <button type="button" class="btn btn-info btn-sm nav_button" id="category7" onclick="summonBWL1( 7 )">#{lp[16]}</button>
          <button type="button" class="btn btn-success btn-sm nav_button" id="category8" onclick="summonBWL1( 8 )">#{lp[17]}</button>
          <button type="button" class="btn btn-success btn-sm nav_button" id="category9" onclick="summonBWL1( 9 )">#{lp[18]}</button>
          <button type="button" class="btn btn-danger btn-sm nav_button" id="category10" onclick="summonBWL1( 10 )">#{lp[19]}</button>
          <button type="button" class="btn btn-danger btn-sm nav_button" id="category11" onclick="summonBWL1( 11 )">#{lp[20]}</button>
          <button type="button" class="btn btn-danger btn-sm nav_button" id="category12" onclick="summonBWL1( 12 )">#{lp[21]}</button>
          <button type="button" class="btn btn-outline-secondary btn-sm nav_button" id="category13" onclick="summonBWL1( 13 )">#{lp[22]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button" id="category14" onclick="summonBWL1( 14 )">#{lp[23]}</button>
          <button type="button" class="btn btn-secondary btn-sm nav_button" id="category15" onclick="summonBWL1( 15 )">#{lp[24]}</button>
          <button type="button" class="btn btn-secondary btn-sm nav_button" id="category16" onclick="summonBWL1( 16 )">#{lp[25]}</button>
          <button type="button" class="btn btn-outline-secondary btn-sm nav_button" id="category17" onclick="summonBWL1( 17 )">#{lp[26]}</button>
          <button type="button" class="btn btn-secondary btn-sm nav_button" id="category18" onclick="summonBWL1( 18 )">#{lp[27]}</button>
          #{special_button}
          #{his_button}
          #{sum_button}
          #{recipe_button}
          #{menu_button}
          #{set_button}
          <button type="button" class="btn btn-outline-secondary btn-sm nav_button" onclick="bookOpen( 'books/books.html', 1 )">#{lp[28]}</button>
          #{config_button}
      </nav>
      <nav class='container-fluid' id='guild_menu' style='display:none;'>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initKoyomi()">#{lp[37]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initGinmi()">#{lp[40]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initGinmi()">#{lp[42]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initGinmi()">#{lp[43]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initGinmi()">#{lp[44]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initGinmi()">#{lp[45]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initGinmi()">#{lp[46]}</button>
      </nav>
      </nav>
      <nav class='container-fluid' id='gs_menu' style='display:none;'>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initAccountM()">#{lp[48]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initSchool()">#{lp[47]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="">#{lp[49]}</button>
      </nav>
      <nav class='container-fluid' id='gm_menu' style='display:none;'>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initUnitc_BWLF( 'init' )">#{lp[29]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initColor_BWLF( 'init' )">#{lp[30]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initAllergen_BWLF( 'init' )">#{lp[31]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initGYCV_BWLF( 'init' )">#{lp[35]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initShun_BWLF( 'init' )">#{lp[36]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initDic_BWL1( 'init' )">#{lp[32]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initSlogf_BWL1( 'init' )">#{lp[33]}</button>
          #{gm_account}
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initMemory_BWLF( 'init' )">#{lp[39]}</button>
          <button type="button" class="btn btn-warning btn-sm nav_button text-warning guild_color" onclick="initImport_BWL1( 'init' )">#{lp[38]}</button>
      </nav>
HTML
  puts html
end


#### HTML working space
def html_working( dummy )
  html = <<-"HTML"
      <div class="bw_frame" id='bw_frame' aligh="center">
        <div class="browse_window" id='bw_level1' style="display: none;"></div>
        <div class="browse_window" id='bw_level2' style="display: none;"></div>
        <div class="browse_window" id='bw_level3' style="display: none;"></div>
        <div class="browse_window" id='bw_level4' style="display: none;"></div>
        <div class="browse_window" id='bw_level5' style="display: none;"></div>
        <div class="browse_window" id='bw_levelF' style="display: none;"></div>
        <div class="video" id='video' style="display: none;"></div>
      </div>
HTML

  puts html
end


#==============================================================================
# Main
#==============================================================================

#### Getting Cookie
cgi = CGI.new

html_init( nil )
user = User.new( cgi )
user.status = 0 unless user.name

lp = user.language( script )

r = mdb( "SELECT ifix FROM cfg WHERE user='#{user.name}';", false, @debug )
ifix = r.first['ifix'].to_i if r.first

html_head( nil, user.status, nil )

puts "<div style='position:fixed; z-index:100; background-color:white'>" if ifix == 1

html_top( user )
html_nav( user, lp )

if ifix == 1
  puts '</div>'
  puts '<header class="navbar navbar-dark bg-dark"><h4> </h4></header>'
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
end
if user.status >= 3 && ifix == 1
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
  puts "<button type='button' class='btn btn btn-outline-light btn-sm nav_button'> </button><br>"
end

html_working( nil )

html_foot
