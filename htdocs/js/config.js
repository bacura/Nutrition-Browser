/////////////////////////////////////////////////////////////////////////////////
// Account //////////////////////////////////////////////////////////////

// Updating account information
var account_cfg = function( step ){
	var new_mail = '';
	var new_aliasu = '';
	var old_password = '';
	var new_password1 = '';
	var new_password2 = '';

	if( step == 'change' ){
		var new_mail = document.getElementById( "new_mail" ).value;
		var new_aliasu = document.getElementById( "new_aliasu" ).value;
		var old_password = document.getElementById( "old_password" ).value;
		var new_password1 = document.getElementById( "new_password1" ).value;
		var new_password2 = document.getElementById( "new_password2" ).value;
	}
	closeBroseWindows( 1 );

	$.post( "config.cgi", { command:"account", step:step, new_mail:new_mail, new_aliasu:new_aliasu, old_password:old_password, new_password1:new_password1, new_password2:new_password2 }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Bio information //////////////////////////////////////////////////////////////

// Updating bio information
var bio_cfg = function( step ){
	var sex = '';
	var age = '';
	var height = '';
	var weight = '';

	if( step == 'change' ){
		if( document.getElementById( "male" ).checked ){
			sex = 0;
		}else{
			sex = 1;
		}
		var age = document.getElementById( "age" ).value;
		var height = document.getElementById( "height" ).value;
		var weight = document.getElementById( "weight" ).value;
	}
	closeBroseWindows( 1 );

	$.post( "config.cgi", { command:"bio", step:step, sex:sex, age:age, height:height, weight:weight }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Display config //////////////////////////////////////////////////////////////

// Updating bio information
var display_cfg = function( step ){
	var icache = '';

	closeBroseWindows( 1 );

	$.post( "config.cgi", { command:"display", step:step, icache:icache }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Food constituent paltte //////////////////////////////////////////////////////////////

// Sending FC palette
var palette_cfg = function( step, id ){
	if( step == 'list' ){
		closeBroseWindows( 2 );
		$.post( "config.cgi", { command:"palette", step:step }, function( data ){ $( "#bw_level2" ).html( data );});
		document.getElementById( "bw_level2" ).style.display = 'block';
	}

	if( step == 'new_palette' ){
		$.post( "config.cgi", { command:"palette", step:step }, function( data ){ $( "#bw_level3" ).html( data );});
		document.getElementById( "bw_level3" ).style.display = 'block';
	}


	switch( step ){
	case 'reset_palette':
		$.post( "config.cgi", { command:"palette", step:step }, function( data ){ $( "#bw_level2" ).html( data );});
		document.getElementById( "bw_level2" ).style.display = 'block';
		displayVideo( 'Palette reset' );
		break;
	}

	if( step == 'regist' ){
		var palette_name = document.getElementById( "palette_name" ).value;

		if( palette_name != '' ){
			if( document.getElementById( "REFUSE" ).checked ){ var REFUSE = 1 }
			if( document.getElementById( "ENERC_KCAL" ).checked ){ var ENERC_KCAL = 1 }
			if( document.getElementById( "ENERC" ).checked ){ var ENERC = 1 }
			if( document.getElementById( "WATER" ).checked ){ var WATER = 1 }

			if( document.getElementById( "PROT" ).checked ){ var PROT = 1 }
			if( document.getElementById( "PROTCAA" ).checked ){ var PROTCAA = 1 }
			if( document.getElementById( "FAT" ).checked ){ var FAT = 1 }
			if( document.getElementById( "FATNLEA" ).checked ){ var FATNLEA = 1 }
			if( document.getElementById( "FASAT" ).checked ){ var FASAT = 1 }
			if( document.getElementById( "FAMS" ).checked ){ var FAMS = 1 }
			if( document.getElementById( "FAPU" ).checked ){ var FAPU = 1 }
			if( document.getElementById( "CHOLE" ).checked ){ var CHOLE = 1 }
			if( document.getElementById( "CHO" ).checked ){ var CHO = 1 }
			if( document.getElementById( "CHOAVLM" ).checked ){ var CHOAVLM = 1 }
			if( document.getElementById( "FIBSOL" ).checked ){ var FIBSOL = 1 }
			if( document.getElementById( "FIBINS" ).checked ){ var FIBINS = 1 }
			if( document.getElementById( "FIBTG" ).checked ){ var FIBTG = 1 }

			if( document.getElementById( "ASH" ).checked ){ var ASH = 1 }
			if( document.getElementById( "NA" ).checked ){ var NA = 1 }
			if( document.getElementById( "K" ).checked ){ var K = 1 }
			if( document.getElementById( "CA" ).checked ){ var CA = 1 }
			if( document.getElementById( "MG" ).checked ){ var MG = 1 }
			if( document.getElementById( "P" ).checked ){ var P = 1 }
			if( document.getElementById( "FE" ).checked ){ var FE = 1 }
			if( document.getElementById( "ZN" ).checked ){ var ZN = 1 }
			if( document.getElementById( "CU" ).checked ){ var CU = 1 }
			if( document.getElementById( "MN" ).checked ){ var MN = 1 }
			if( document.getElementById( "ID" ).checked ){ var ID = 1 }
			if( document.getElementById( "SE" ).checked ){ var SE = 1 }
			if( document.getElementById( "CR" ).checked ){ var CR = 1 }
			if( document.getElementById( "MO" ).checked ){ var MO = 1 }

			if( document.getElementById( "RETOL" ).checked ){ var RETOL = 1 }
			if( document.getElementById( "CARTA" ).checked ){ var CARTA = 1 }
			if( document.getElementById( "CARTB" ).checked ){ var CARTB = 1 }
			if( document.getElementById( "CRYPXB" ).checked ){ var CRYPXB = 1 }
			if( document.getElementById( "CARTBEQ" ).checked ){ var CARTBEQ = 1 }
			if( document.getElementById( "VITA_RAE" ).checked ){ var VITA_RAE = 1 }
			if( document.getElementById( "VITD" ).checked ){ var VITD = 1 }
			if( document.getElementById( "TOCPHA" ).checked ){ var TOCPHA = 1 }
			if( document.getElementById( "TOCPHB" ).checked ){ var TOCPHB = 1 }
			if( document.getElementById( "TOCPHG" ).checked ){ var TOCPHG = 1 }
			if( document.getElementById( "TOCPHD" ).checked ){ var TOCPHD = 1 }
			if( document.getElementById( "VITK" ).checked ){ var VITK = 1 }

			if( document.getElementById( "THIAHCL" ).checked ){ var THIAHCL = 1 }
			if( document.getElementById( "RIBF" ).checked ){ var RIBF = 1 }
			if( document.getElementById( "NIA" ).checked ){ var NIA = 1 }
			if( document.getElementById( "VITB6A" ).checked ){ var VITB6A = 1 }
			if( document.getElementById( "VITB12" ).checked ){ var VITB12 = 1 }
			if( document.getElementById( "FOL" ).checked ){ var FOL = 1 }
			if( document.getElementById( "PANTAC" ).checked ){ var PANTAC = 1 }
			if( document.getElementById( "BIOT" ).checked ){ var BIOT = 1 }
			if( document.getElementById( "VITC" ).checked ){ var VITC = 1 }

			if( document.getElementById( "NACL_EQ" ).checked ){ var NACL_EQ = 1 }
			if( document.getElementById( "ALC" ).checked ){ var ALC = 1 }
			if( document.getElementById( "NITRA" ).checked ){ var NITRA = 1 }
			if( document.getElementById( "THEBRN" ).checked ){ var THEBRN = 1 }
			if( document.getElementById( "CAFFN" ).checked ){ var CAFFN = 1 }
			if( document.getElementById( "TAN" ).checked ){ var TAN = 1 }
			if( document.getElementById( "POLYPHENT" ).checked ){ var POLYPHENT = 1 }
			if( document.getElementById( "ACEAC" ).checked ){ var ACEAC = 1 }
			if( document.getElementById( "COIL" ).checked ){ var COIL = 1 }
			if( document.getElementById( "OA" ).checked ){ var OA = 1 }
			if( document.getElementById( "WCR" ).checked ){ var WCR = 1 }

			if( document.getElementById( "Notice" ).checked ){ var Notice = 1 }

			$.post( "config.cgi", {
				command:'palette', step:step, palette_name:palette_name,
				REFUSE:REFUSE, ENERC_KCAL:ENERC_KCAL, ENERC:ENERC, WATER:WATER,
				PROT:PROT, PROTCAA:PROTCAA, FAT:FAT, FATNLEA:FATNLEA, FASAT:FASAT, FAMS:FAMS, FAPU:FAPU, CHOLE:CHOLE, CHO:CHO, CHOAVLM:CHOAVLM, FIBSOL:FIBSOL, FIBINS:FIBINS, FIBTG:FIBTG,
				ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
				RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
				THIAHCL:THIAHCL, RIBF:RIBF, NIA:NIA, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
				NACL_EQ:NACL_EQ, ALC:ALC, NITRA:NITRA, THEBRN:THEBRN, CAFFN:CAFFN, TAN:TAN, POLYPHENT:POLYPHENT, ACEAC:ACEAC, COIL:COIL, OA:OA, WCR:WCR,
				Notice:Notice
			}, function( data ){ $( "#bw_level2" ).html( data );});
			displayVideo( palette_name + 'を登録' );

//			$.post( "config.cgi", { command:"palette", step:'list' }, function( data ){ $( "#bw_level2" ).html( data );});
			closeBroseWindows( 2 );
		} else{
			displayVideo( 'Palette name!(>_<)' );
		}
	}

	// Edit FC palette
	if( step == 'edit_palette' ){
		$.post( "config.cgi", { command:"palette", step:step, palette_name:id }, function( data ){ $( "#bw_level3" ).html( data );});
		document.getElementById( "bw_level3" ).style.display = 'block';
	}

	// Deleting FC palette
	if( step == 'delete_palette' ){
		if( document.getElementById( id ).checked ){
			$.post( "config.cgi", { command:"palette", step:step, palette_name:id }, function( data ){ $( "#bw_level2" ).html( data );});
			closeBroseWindows( 2 );
		} else{
			displayVideo( 'Check!(>_<)' );
		}
	}

};


/////////////////////////////////////////////////////////////////////////////////
// History /////////////////////////////////////////////////////////////////////

// History initialisation
var history_cfg = function( step, his_max ){
	closeBroseWindows( 2 );
	$.post( "config.cgi", { command:"history", step:step, his_max:his_max }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	if( step == 'clear' ){
		displayVideo( 'Initialized' );
	}
	if( step == 'max' ){
		displayVideo( 'History max -> '+ his_max );
	}
};

/////////////////////////////////////////////////////////////////////////////////
// Chopping board /////////////////////////////////////////////////////////////////////

// Chopping board initialisation
var sum_cfg = function( step ){
	closeBroseWindows( 2 );
	$.post( "config.cgi", { command:"sum", step:step }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	if( step == 'clear' ){
		displayVideo( 'Initialized' );
	}

	var fx = function(){
		refreshCB();
	};
	setTimeout( fx, 1000 );
};


/////////////////////////////////////////////////////////////////////////////////
// 登録解除 /////////////////////////////////////////////////////////////////////

// パスワードボタンを押したときにL2閲覧ウインドウの内容を書き換える
var release_cfg = function( step ){
	var password = ''
	closeBroseWindows( 2 );

	$.post( "config.cgi", { command:"release", step:step, password:password }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
	if( step == 'clear' ){
		displayVideo( 'パスワードを変更' );
	}
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi EX /////////////////////////////////////////////////////////////////////

//
var koyomiex_cfg = function( step, del_id, del_no ){
	closeBroseWindows( 2 );

	if( step == 'update' ){
		var koyomiy = document.getElementById( "koyomiy" ).value;

		var breakfast_st = document.getElementById( "breakfast_st" ).value;
		var lunch_st = document.getElementById( "lunch_st" ).value;
		var dinner_st = document.getElementById( "dinner_st" ).value;

		var kex_select0 = document.getElementById( "kex_select0" ).value;
		var kex_select1 = document.getElementById( "kex_select1" ).value;
		var kex_select2 = document.getElementById( "kex_select2" ).value;
		var kex_select3 = document.getElementById( "kex_select3" ).value;
		var kex_select4 = document.getElementById( "kex_select4" ).value;
		var kex_select5 = document.getElementById( "kex_select5" ).value;
		var kex_select6 = document.getElementById( "kex_select6" ).value;
		var kex_select7 = document.getElementById( "kex_select7" ).value;
		var kex_select8 = document.getElementById( "kex_select8" ).value;
		var kex_select9 = document.getElementById( "kex_select9" ).value;

		var item0 = document.getElementById( "item0" ).value;
		var item1 = document.getElementById( "item1" ).value;
		var item2 = document.getElementById( "item2" ).value;
		var item3 = document.getElementById( "item3" ).value;
		var item4 = document.getElementById( "item4" ).value;
		var item5 = document.getElementById( "item5" ).value;
		var item6 = document.getElementById( "item6" ).value;
		var item7 = document.getElementById( "item7" ).value;
		var item8 = document.getElementById( "item8" ).value;
		var item9 = document.getElementById( "item9" ).value;

		var unit0 = document.getElementById( "unit0" ).value;
		var unit1 = document.getElementById( "unit1" ).value;
		var unit2 = document.getElementById( "unit2" ).value;
		var unit3 = document.getElementById( "unit3" ).value;
		var unit4 = document.getElementById( "unit4" ).value;
		var unit5 = document.getElementById( "unit5" ).value;
		var unit6 = document.getElementById( "unit6" ).value;
		var unit7 = document.getElementById( "unit7" ).value;
		var unit8 = document.getElementById( "unit8" ).value;
		var unit9 = document.getElementById( "unit9" ).value;

		$.post( "config.cgi", {
			command:"koyomiex", step:step, koyomiy:koyomiy, breakfast_st:breakfast_st, lunch_st:lunch_st, dinner_st:dinner_st,
			kex_select0:kex_select0, kex_select1:kex_select1, kex_select2:kex_select2, kex_select3:kex_select3, kex_select4:kex_select4, kex_select5:kex_select5, kex_select6:kex_select6, kex_select7:kex_select7, kex_select8:kex_select8, kex_select9:kex_select9,
			item0:item0, item1:item1, item2:item2, item3:item3, item4:item4, item5:item5, item6:item6, item7:item7, item8:item8, item9:item9,
			unit0:unit0, unit1:unit1, unit2:unit2, unit3:unit3, unit4:unit4, unit5:unit5, unit6:unit6, unit7:unit7, unit8:unit8, unit9:unit9,
		}, function( data ){ $( "#bw_level2" ).html( data );});
		displayVideo( 'Saved' );
	}else if( step == 'delete' ){
		if( document.getElementById( del_id ).checked ){
			$.post( "config.cgi", { command:"koyomiex", step:step, del_no:del_no }, function( data ){ $( "#bw_level2" ).html( data );});
			displayVideo( 'Deleted' );
		}else{
			displayVideo( 'Check!(>_<)' );
		}
	}else{
		$.post( "config.cgi", { command:"koyomiex", step:step,  }, function( data ){ $( "#bw_level2" ).html( data );});
	}
	document.getElementById( "bw_level2" ).style.display = 'block';
};

var kexChangeselect = function( no ){
	var select_id = 'kex_select' + no;
	displayVideo( document.getElementById( select_id ).value );

	if( document.getElementById( select_id ).value == 1 ){

		document.getElementById('item' + no ).disabled = false;
		document.getElementById('unit' + no ).disabled = false;
	}else{
		document.getElementById('item' + no ).disabled = true;
		document.getElementById('unit' + no ).disabled = true;
	}
};
