/////////////////////////////////////////////////////////////////////////////////
// アカウント情報の変更 //////////////////////////////////////////////////////////////

// アカウント情報ボタンを押したときにL2閲覧ウインドウの内容を書き換える
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
// 成分パレットの設定 //////////////////////////////////////////////////////////////

// 成分パレットボタンを押したときにL2閲覧ウインドウの内容を書き換える
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
			displayVideo( 'パレット名が必要' );
		}
	}

	// パレット編集
	if( step == 'edit_palette' ){
		$.post( "config.cgi", { command:"palette", step:step, palette_name:id }, function( data ){ $( "#bw_level3" ).html( data );});
		document.getElementById( "bw_level3" ).style.display = 'block';
	}

	// パレット削除
	if( step == 'delete_palette' ){
		if( document.getElementById( id ).checked ){
			$.post( "config.cgi", { command:"palette", step:step, palette_name:id }, function( data ){ $( "#bw_level2" ).html( data );});
			closeBroseWindows( 2 );
		} else{
			displayVideo( 'チェックが必要' );
		}
	}

};


/////////////////////////////////////////////////////////////////////////////////
// 履歴 /////////////////////////////////////////////////////////////////////

// 履歴初期化ボタンを押したときにL2閲覧ウインドウの内容を書き換える
var history_cfg = function( step ){
	closeBroseWindows( 2 );
	$.post( "config.cgi", { command:"history", step:step }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	if( step == 'clear' ){
		displayVideo( '履歴を初期化' );
	}
};

/////////////////////////////////////////////////////////////////////////////////
// まな板 /////////////////////////////////////////////////////////////////////

// まな板初期化ボタンを押したときにまな板を初期化する
var sum_cfg = function( step ){
	closeBroseWindows( 2 );
	$.post( "config.cgi", { command:"sum", step:step }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	if( step == 'clear' ){
		displayVideo( 'まな板を初期化' );
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
