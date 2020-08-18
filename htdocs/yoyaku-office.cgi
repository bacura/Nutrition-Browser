#! /usr/bin/ruby
# coding: UTF-8
#Nutrition browser cooking school yoyaku office 0.00

#==============================================================================
#CHANGE LOG
#==============================================================================
#20200620, 0.00, start


#==============================================================================
#LIBRARY
#==============================================================================
require '/var/www/nb-soul.rb'


#==============================================================================
#STATIC
#==============================================================================
@debug = true
script = 'yoyaku-office'


#==============================================================================
#DEFINITION
#==============================================================================

def html_header()
	html = <<-"HTML"
<!DOCTYPE html>
<head>
  <title>嵯峨お料理教室予約フォーム</title>
  <meta charset="UTF-8">
  <meta name="keywords" content="嵯峨お料理教室">
  <meta name="description" content="食品成分表の検索,栄養計算,栄養評価, analysis, calculation">
  <meta name="robots" content="index,follow">
  <meta name="author" content="Shinji Yoshiyama">
  <!-- bootstrap -->
  <link rel="stylesheet" href="bootstrap-dist/css/bootstrap.min.css">
  <link rel="stylesheet" href="#{$CSS_PATH}/core.css">
<!-- Jquery -->
  <script type="text/javascript" src="./jquery-3.2.1.min.js"></script>
<!-- bootstrap -->
  <script type="text/javascript" src="bootstrap-dist/js/bootstrap.min.js"></script>
  <script type="text/javascript" src="#{$JS_PATH}/core.js"></script>
  <script type="text/javascript" src="#{$JS_PATH}/shun.js"></script>
</head>

<body class="body">
  <span class="world_frame" id="world_frame">
HTML

	puts html
end


class Cals
	attr_accessor :yyyy, :mm, :dd, :available, :am, :pm

  def initialize( yyyy, mm, dd, available )
    @yyyy = yyyy
    @mm = mm
    @dd = dd
    @available = available
    @am = 2
    @pm = 2
  end
end

#==============================================================================
# Main
#==============================================================================
#### Getting Cookie
cgi = CGI.new

user = User.new( cgi )

#lp = lp_init( 'yoyaku', language )

html_init( nil )
#html_header()


#### Getting POST
command = cgi['command']
yyyy = cgi['yyyy'].to_i
mm = cgi['mm'].to_i
dd = cgi['dd'].to_i
ampm = cgi['ampm'].to_i
dd = 1 if dd == 0
if @debug
  puts "command:#{command}<br>\n"
  puts "yyyy:#{yyyy}<br>\n"
  puts "mm:#{mm}<br>\n"
  puts "dd:#{dd}<br>\n"
  puts "ampm:#{ampm}<br>\n"
  puts "<hr>\n"
end


#### Date & calendar config
calendar = Calendar.new( user.name, yyyy, mm, dd )
calendar.wf = 7 if calendar.wf == 0
calendar.debug if @debug
sql_ymd = "#{calendar.yyyy}-#{calendar.mm}-#{calendar.dd}"
sql_ym = "#{calendar.yyyy}-#{calendar.mm}"

case command
when 'new'
when 'edit'
when 'cancel'
when 'regular_set'
when 'original_set'
else
end


ampm_time = []
ampm_time[0] = '午前'
ampm_time[1] = '午後'


html = <<-"HTML"
<h1 align="center" class='month'>嵯峨お料理教室予約フォーム</h1>

<h2 align="center" class='month'>#{user.name} さん</h2>
<h2 align="center" class='month'>#{calendar.yyyy}年 #{calendar.mm}月 #{calendar.dd}日 #{ampm_time[ampm]}</h2>
<hr>

<div class='row'>
  <div class='col'>
    <h4 class='.scs_menu'>レギュラー献立</h4>
  </div>
</div>

<div class='row'>
  <div class='col-1'><input class="form-check-input" type="radio" name="menu" id="exam" value="option1"></div>
  <div class='col-11'>基本の和食</div>
</div>

<hr>
<div class='row'>
  <div class='col'>
    <h4 class='.scs_menu'>季節の献立（月替わり）</h4>
  </div>
</div>

<hr>
<div class='row'>
  <div class='col'>
    <h4 class='.scs_menu'>フリー献立</h4>
  </div>
</div>

<hr>
<div class='row'>
  <div class='col'>
    <h4 class='.scs_menu'>超フリー献立</h4>
  </div>
</div>





<hr>
<div class='row'>
  <div class='col-4'></div>
  <div class='col-2'>
    <div align='center' class="input-group mb-3 form-inline">
      <div class="input-group-prepend">
        <label class="input-group-text">人数</label>
      </div>
      <select class="custom-select" id="number">
        <option value="1">1</option>
        <option value="2">2</option>
      </select>
    </div>
  </div>
  <div class='col-2'>
    <button type="button" class="btn btn-primary"> 予 約 </button>
  </div>
  <div class='col-2'>
    <button type="button" class="btn btn-secondary">キャンセル</button>
  </div>
</div>



HTML

puts html

html_foot
