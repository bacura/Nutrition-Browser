# Ginmi module for METs 0.00
#encoding: utf-8


def ginmi_module( cgi, user )
	module_js()
	command = cgi['command']
	weight = cgi['weight']
	heading = cgi['heading']
	sub_heading = cgi['sub_heading']
	active = cgi['active']
	history = cgi['history']
	hh = cgi['hh'].to_i
	mm = cgi['mm'].to_i
	active = history if history != '0' &&  history != ''

	html = ''
	case command
	when 'form', 'koyomiex'
		#importing from config

		r = mdb( "SELECT weight, koyomiex FROM #{$MYSQL_TB_CFG} WHERE user='#{user.name}';", false, false )
		weight = 0.0
		weight = r.first['weight'] if r.first

		# inporting from koyomiex
		if command == 'koyomiex' && r.first['koyomiex']
			a = r.first['koyomiex'].split( ':' )
			a.size.times do |c|
				aa = a[c].split( "\t" )
				if aa[0] == '3'
					rr = mdb( "SELECT item#{aa[0]} FROM #{$MYSQL_TB_KOYOMIEX} WHERE user='#{user.name}' AND item#{aa[0]}!='' ORDER BY date DESC LIMIT 1;", false, true )
					if rr.first
						weight = rr.first["item#{aa[0]}"].to_f
					end
				end
			end
		end
	when 'result', 'display'
		mets_mm = hh * 60 + mm
		mets = ''
		r = mdb( "SELECT * FROM #{$MYSQL_TB_METS} WHERE user='#{user.name}' and name='default';", false, false )
		if r.first
			mets = r.first['mets']
			if command == 'result'
				mets = "#{mets}\t#{active}:#{mets_mm}"
				mdb( "UPDATE #{$MYSQL_TB_METS} SET mets='#{mets}' WHERE user='#{user.name}' and name='default';", false, false )
			end
		elsif command == 'result'
			mdb( "INSERT INTO #{$MYSQL_TB_METS} SET user='#{user.name}', name='default',mets='#{active}:#{mets_mm}';", false, false )
			mets << "#{active}:#{mets_mm}"
		end

		code_set = []
		mm_set = []
		total_mm = 0.0
		total_hm = ''
		total_energy = 0
		total_mets = BigDecimal( 0 )
		a = mets.split( "\t" )
		a.size.times do |c|
			aa = a[c].split( ':' )
			code_set << aa[0]
			mm_set << aa[1].to_i
		end

		mets_table_html = '<table class="table table-hover table-sm">'
		mets_table_html << '<thead>'
		mets_table_html << '<tr class="">'
		mets_table_html << '<td>Code</td>'
		mets_table_html << '<td>個別活動</td>'
		mets_table_html << '<td>METs</td>'
		mets_table_html << '<td>時間 [累積]</td>'
		mets_table_html << '<td>時間(h)</td>'
		mets_table_html << '<td>METs*h</td>'
		mets_table_html << '</tr>'
		mets_table_html << '</thead>'

		code_set.size.times do |c|
			r = mdb( "SELECT * FROM #{$MYSQL_TB_METST} WHERE code='#{code_set[c]}';", false, false )
			if r.first
				mets_table_html << '<tr>'
				mets = BigDecimal( r.first['mets'] )
				hh_ = sprintf( "%.3f", ( mm_set[c].to_f / 60 ).round(3).to_s )
				metsh = mets * mm_set[c].to_f / 60
				metsh_ = sprintf( "%.3f", metsh.round(3).to_s )
				total_mets += metsh
				total_energy += ( metsh * weight.to_f * 1.05 )
				total_mm += mm_set[c]

				h = mm_set[c].div( 60 )
				m = mm_set[c] % 60
				if m < 10
					m = "0#{m.to_i}"
				else
					m = m.to_i
				end
				hm = "#{h}:#{m}"

				th = total_mm.div( 60 )
				tm = total_mm % 60
				if tm < 10
					tm = "0#{tm.to_i}"
				else
					tm = tm.to_i
				end
				total_hm = "#{th}:#{tm}"

				mets_table_html << "<td>#{r.first['code']}</td><td>#{r.first['active']}</td><td>#{mets.to_f}</td><td>#{hm} [#{total_hm}]</td><td>#{hh_}</td><td>#{metsh_}</td>"
				mets_table_html << '</tr>'
			end
		end
		mets_table_html << '</table>'

		result_html = <<-"RESULT_HTML"
		<div class='row'>
			<div class='col-2'>合計METs*h</div>
			<div class='col-8'>#{total_mets.to_f.round( 3 )}</div>
			<div class='col-2'>
				<button class='btn btn-sm btn-outline-danger' onclick="ginmiEnergyMETsreset()">リセット</button>
			</div>
		</div>
		<div class='row'>
			<div class='col-2'>消費エネルギー</div>
			<div class='col-2'>#{total_energy.to_i} kcal</div>
			<div class='col-1'>計算式</div>
			<div class='col-5'>#{weight} * #{total_mets.to_f.round( 3 )} * 1.05</div>
		</div>
RESULT_HTML

		puts result_html
		puts mets_table_html

		if command == 'result'
			r = mdb( "SELECT * FROM #{$MYSQL_TB_METS} WHERE user='#{user.name}' AND name='history';", false, false)
			if r.first
				a = r.first['mets'].split( "\t" )
				a.unshift( active ).uniq!
				limit = 19
				limit = a.size - 1 if a.size < 19
				if a.size == 1
					new_history = active
				else
					new_history = a[0..limit].join( "\t" )
				end
				mdb( "UPDATE #{$MYSQL_TB_METS} SET mets='#{new_history}' WHERE user='#{user.name}' AND name='history';", false, false )
			else
				mdb( "INSERT INTO #{$MYSQL_TB_METS} SET user='#{user.name}', name='history', mets='#{active}';", false, false )
			end
		end
		exit()
	when 'reset'
			mdb( "delete from #{$MYSQL_TB_METS} WHERE user='#{user.name}' and name='default';", false, false )
			exit()
	end


	####
	heading_select = ''
	r = mdb( "SELECT DISTINCT heading FROM #{$MYSQL_TB_METST};", false, false )
	heading = r.first['heading'] if heading == ''
	r.each do |e|
		if e['heading'] == heading
			heading_select << "<option value='#{e['heading']}' SELECTED>#{e['heading']}</option>"
		else
			heading_select << "<option value='#{e['heading']}'>#{e['heading']}</option>"
		end
	end

	####
	sub_heading_select = ''
	r = mdb( "SELECT DISTINCT sub_heading FROM #{$MYSQL_TB_METST} WHERE heading='#{heading}';", false, false )
	sub_heading = r.first['sub_heading'] if sub_heading == ''
	r.each do |e|
		if e['sub_heading'] == sub_heading
			sub_heading_select << "<option value='#{e['sub_heading']}' SELECTED>#{e['sub_heading']}</option>"
		else
			sub_heading_select << "<option value='#{e['sub_heading']}'>#{e['sub_heading']}</option>"
		end
	end

	####
	active_select = ''
	mets_value = '0.0'
	r = mdb( "SELECT * FROM #{$MYSQL_TB_METST} WHERE sub_heading='#{sub_heading}';", false, false )
	mets_value = r.first['mets']
	r.each do |e|
		if e['code'] == active
			active_select << "<option value='#{e['code']}' SELECTED>#{e['active']}</option>"
			mets_value = e['mets']
		else
			active_select << "<option value='#{e['code']}'>#{e['active']}</option>"
		end
	end


	####
	history_select = "<option value='0'>↓↓</option>"
	r = mdb( "SELECT mets FROM #{$MYSQL_TB_METS} WHERE user='#{user.name}' AND name='history';", false, false )
	if r.first
		a = r.first['mets'].split( "\t" )
		a.each do |e|
			rr = mdb( "SELECT * FROM #{$MYSQL_TB_METST} WHERE code='#{e}';", false, false )
			history_select << "<option value='#{e}'>[#{e}] #{rr.first['active']}</option>"
		end
	end


	html = <<-"HTML"
	<div class='row'>
	<h5>METs 計算フォーム</h5>
	</div>
	<br>

	<div class='row'>
		<div class='col-4'>
			<div class='input-group input-group-sm'>
				<span class='input-group-text'>体重(kg)</span>
				<input type='text' class='form-control' id='weight' maxlength='6' value='#{weight}'>
			</div>
		</div>
		<div class='col-2'>
			<button class='btn btn-sm btn-outline-primary' onclick="ginmiEnergyMETskex()">拡張こよみ適用</button>
		</div>
	</div>
	<br>

	<div class='row'>
		<div class='col-6'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="heading">　大項目</label>
				<select class="form-select form-select-sm" id="heading" onchange="ginmiEnergyMETs( 'heading' )">
					#{heading_select}
				</select>
			</div>
		</div>
	</div>
	<div class='row'>
		<div class='col-6'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="sub_heading">　副項目</label>
				<select class="form-select form-select-sm" id="sub_heading" onchange="ginmiEnergyMETs( 'sub_heading' )">
					#{sub_heading_select}
				</select>
			</div>
		</div>
	</div>
	<div class='row'>
		<div class='col-6'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="active">個別活動</label>
				<select class="form-select form-select-sm" id="active" onchange="ginmiEnergyMETs( 'active' )">
					#{active_select}
				</select>
			</div>
		</div>
	</div>
	<br>

	<div class='row'>
		<div class='col-6'>
			<div class="input-group input-group-sm">
				<label class="input-group-text" for="inputGroupSelect01">履　　歴</label>
				<select class="form-select form-select-sm" id="history">
				#{history_select}
			</select>
		</div>
	<div>
	<br>

	<div class='row'>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<input type='number' class='form-control' value="#{mets_value}" DISABLED>
				<span class='input-group-text'>METs</span>
			</div>
		</div>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<input type='number' min='0' max='24' class='form-control' id='hh' maxlength='2' value='0'>
				<span class='input-group-text'>時間</span>
			</div>
		</div>
		<div class='col-3'>
			<div class='input-group input-group-sm'>
				<input type='number' min='0' max='59' step='5' class='form-control' id='mm' maxlength='2' value='0'>
				<span class='input-group-text'>分間</span>
			</div>
		</div>
		<div class='col-3'>
			<button class='btn btn-sm btn-outline-primary' onclick="ginmiEnergyMETsres()">追加</button>
		</div>
	</div>
HTML

	return html
end


def module_js()
	js = <<-"JS"
<script type='text/javascript'>

var ginmiEnergyMETskex = function(){
	$.post( "ginmi.cgi", { mod:"energy-mets", command:'koyomiex' }, function( data ){ $( "#bw_level2" ).html( data );});
};

var ginmiEnergyMETs = function( select ){
	var weight = document.getElementById( "weight" ).value;
	var heading = document.getElementById( "heading" ).value;
	if( select == 'sub_heading'){
		var sub_heading = document.getElementById( "sub_heading" ).value;
		$.post( "ginmi.cgi", { mod:"energy-mets", command:'', weight:weight, heading:heading, sub_heading:sub_heading }, function( data ){ $( "#bw_level2" ).html( data );});
	} else if( select == 'active'){
		var sub_heading = document.getElementById( "sub_heading" ).value;
		var active = document.getElementById( "active" ).value;
		displayVideo( active );
		$.post( "ginmi.cgi", { mod:"energy-mets", command:'', weight:weight, heading:heading, sub_heading:sub_heading, active:active }, function( data ){ $( "#bw_level2" ).html( data );});
	} else{
		$.post( "ginmi.cgi", { mod:"energy-mets", command:'', weight:weight, heading:heading }, function( data ){ $( "#bw_level2" ).html( data );});
	}
};

var ginmiEnergyMETsres = function(){
	var weight = document.getElementById( "weight" ).value;
	var active = document.getElementById( "active" ).value;
	var hh = document.getElementById( "hh" ).value;
	var mm = document.getElementById( "mm" ).value;
	var history = document.getElementById( "history" ).value;

	if( hh=='0' && mm=='0'){
		displayVideo( 'Time! (>_<)' );
		$.post( "ginmi.cgi", { mod:"energy-mets", command:'display', weight:weight, active:active, history:history, hh:hh, mm:mm }, function( data ){ $( "#bw_level3" ).html( data );});
	}else{
		$.post( "ginmi.cgi", { mod:"energy-mets", command:'result', weight:weight, active:active, history:history, hh:hh, mm:mm }, function( data ){ $( "#bw_level3" ).html( data );});
		setTimeout( ginmiEnergyMETs( 'active' ), 1000 );
	}
	document.getElementById( "bw_level3" ).style.display = 'block';
};

var ginmiEnergyMETsreset = function(){
	displayVideo( 'METs reset' );
	$.post( "ginmi.cgi", { mod:"energy-mets", command:'reset' }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'none';
};

</script>
JS
	puts js
end
