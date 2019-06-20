#! /usr/bin/ruby
# coding: UTF-8
#Nutrition browser index page 0.00

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
$SCRIPT = 'index.cgi'


#==============================================================================
#DEFINITION
#==============================================================================

#### HTML nav
def html_nav( user_name, status, lp )
  # まな板カウンター
  if user_name
    r = mariadb( "SELECT sum from #{$MYSQL_TB_SUM} WHERE user='#{user_name}';", false )
    if r.first
      t = []
      t = r.first['sum'].split( "\t" ) if r.first['sum']
      @cb_num = t.size
    else
      mariadb( "INSERT INTO #{$MYSQL_TB_SUM} SET user='#{user_name}';", false )
      @cb_num = 0
    end
    # 献立カウンター
    r = mariadb( "SELECT meal from #{$MYSQL_TB_MEAL} WHERE user='#{user_name}';", false )
    if r.first
      t = []
      t = r.first['meal'].split( "\t" ) if r.first['meal']
      @meal_num = t.size
    else
      mariadb( "INSERT INTO #{$MYSQL_TB_MEAL} SET user='#{user_name}';", false )
      @meal_num = 0
    end
  else
    @cb_num = '-'
    @meal_num = '-'
  end


  # 履歴ボタンとまな板ボタンの設定
  if status >= 1
    cb = "#{lp[1]} <span class=\"badge badge-pill badge-warning\" id=\"cb_num\">#{@cb_num}</span>"
    mb = "#{lp[2]} <span class=\"badge badge-pill badge-warning\" id=\"mb_num\">#{@meal_num}</span>"
    special_button = "<button type=\"button\" class=\"btn btn-outline-dark btn-sm nav_button\" id=\"category0\" onclick=\"summonBWL1( 0 )\">#{lp[3]}</button>"
    his_button = "<button type=\"button\" class=\"btn btn-dark btn-sm nav_button\" onclick=\"historyBWL1( 'recent', '100', '1', 'all' )\">#{lp[4]}</button>"
    sum_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"initCB_BWL1( '' )\">#{cb}</button>"
    recipe_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"recipeList_BWL1( 'init' )\">#{lp[5]}</button>"
    menu_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"initMeal_BWL1( '' )\">#{mb}</button>"
    set_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"menuList_BWL1()\">#{lp[6]}</button>"
    config_button = "<button type='button' class='btn btn-dark btn-sm nav_button' onclick=\"configInit( '' )\">#{lp[7]}</button>"
  else
    cb = "#{lp[1]} <span class=\"badge badge-pill badge-secondary\" id=\"cb_num\">#{@cb_num}</span>"
    mb = "#{lp[2]} <span class=\"badge badge-pill badge-secondary\" id=\"mb_num\">#{@meal_num}</span>"
    special_button = "<button type=\"button\" class=\"btn btn-outline-secondary btn-sm nav_button\" onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[3]}</button>"
    his_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[4]}</button>"
    sum_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{cb}</button>"
    recipe_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[5]}</button>"
    menu_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{mb}</button>"
    set_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[6]}</button>"
    config_button = "<button type='button' class='btn btn btn-dark btn-sm nav_button text-secondary' onclick=\"displayVideo( '#{lp[8]}' )\">#{lp[7]}</button>"
  end

if status >= 3
    g_button = "<button type='button' class='btn btn btn-warning btn-sm nav_button text-warning guild_color' onclick=\"changeMenu()\">G</button>"
else
    g_button = "<button type='button' class='btn btn btn-warning btn-sm nav_button text-dark guild_color' onclick=\"displayVideo( '#{lp[9]}' )\">G</button>"
end

	html = <<-"HTML"
      <nav class='container-fluid'>
          #{g_button}
          <span id='normal_menu' style="display:inline;">
          <button id=''type="button" class="btn btn-info btn-sm nav_button" id="category1" onclick="summonBWL1( 1 )">#{lp[10]}</button>
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
          </span>

          <span id='guild_menu' style="display:none;">
          #{his_button}
          #{sum_button}
          #{recipe_button}
          #{menu_button}
          #{set_button}
          <button type="button" class="btn btn-info btn-sm nav_button" onclick="initKoyomi()">#{lp[37]}</button>
          </span>
          <button type="button" class="btn btn-outline-secondary btn-sm nav_button" onclick="bookOpen( 'books/books.html', 1 )">#{lp[28]}</button>
          #{config_button}
			</nav>
HTML
  puts html


  # Guild master menu
  if status == 9
    html = <<-"HTML"
      <nav class='container-fluid'>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initUnitc_BWLF( 'init' )">#{lp[29]}</button>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initColor_BWLF( 'init' )">#{lp[30]}</button>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initAllergen_BWLF( 'init' )">#{lp[31]}</button>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initGYCV_BWLF( 'init' )">#{lp[35]}</button>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initShun_BWLF( 'init' )">#{lp[36]}</button>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initDic_BWL1( 'init' )">#{lp[32]}</button>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initSlogf_BWL1( 'init' )">#{lp[33]}</button>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initAccount_BWL1( 'init' )">#{lp[34]}</button>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initMemory_BWLF( 'init' )">#{lp[39]}</button>
          <button type="button" class="btn btn-outline-danger btn-sm nav_button" onclick="initImport_BWL1( 'init' )">#{lp[38]}</button>
      </nav>
HTML
    puts html
  end

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
uname, uid, status, aliasu, language = login_check( cgi )
status = 0 unless uname
lp = lp_init( 'index', language )

html_init( nil )
html_head( nil, status, nil )

html_top( uname, status, aliasu )
html_nav( uname, status, lp )
html_working( nil )

html_foot
