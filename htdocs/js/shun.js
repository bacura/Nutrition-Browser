/////////////////////////////////////////////////////////////////////////////////
// Koyomi //////////////////////////////////////////////////////////////

// Koyomi
var initKoyomi = function(){
	closeBroseWindows( 1 );
	$.post( "koyomi.cgi", { command:"menu" }, function( data ){ $( "#bw_level1" ).html( data );});
	$.post( "koyomi.cgi", { command:"init" }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
	document.getElementById( "bw_level2" ).style.display = 'block';
};

// Koyomi change
var changeKoyomi_BW1 = function(){
	var yyyy = document.getElementById( "yyyy" ).value;
	var mm = document.getElementById( "mm" ).value;
	$.post( "koyomi.cgi", { command:"init", yyyy:yyyy, mm:mm }, function( data ){ $( "#bw_level2" ).html( data );});
};

// Koyomi return from EX
var returnKoyomi_BW1 = function( yyyy, mm ){
	$.post( "koyomi.cgi", { command:"init", yyyy:yyyy, mm:mm }, function( data ){ $( "#bw_level2" ).html( data );});
};

// Koyomi freeze
var freezeKoyomi = function( yyyy, mm, dd ){
	var freeze_check = document.getElementById( "freeze_check" + dd ).checked ;
	$.post( "koyomi.cgi", { command:'freeze', yyyy:yyyy, mm:mm, dd, freeze_check:freeze_check }, function( data ){ $( "#bw_level2" ).html( data );});
};

// Koyomi freeze all
var freezeKoyomiAll = function( yyyy, mm ){
	var freeze_check_all = document.getElementById( "freeze_check_all" ).checked ;
	$.post( "koyomi.cgi", { command:'freeze_all', yyyy:yyyy, mm:mm,  freeze_check_all:freeze_check_all }, function( data ){ $( "#bw_level2" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi Edit//////////////////////////////////////////////////////////////

// Koyomi edit
var editKoyomi_BW2 = function( com, dd ){
	var yyyy = document.getElementById( "yyyy" ).value;
	var mm = document.getElementById( "mm" ).value;
	$.post( "koyomi-edit.cgi", { command:com, yyyy:yyyy, mm:mm, dd:dd }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'none';
	document.getElementById( "bw_level3" ).style.display = 'block';
};

// Koyomi delete
var deleteKoyomi_BW2 = function( yyyy, mm, dd, tdiv, code, order ){
	$.post( "koyomi-edit.cgi", { command:'delete', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, code:code, order:order }, function( data ){ $( "#bw_level3" ).html( data );});
};

// Koyomi memo
var memoKoyomi = function( yyyy, mm, dd ){
	var memo = document.getElementById( "memo" ).value;
	$.post( "koyomi-edit.cgi", { command:'memo', yyyy:yyyy, mm:mm, dd:dd, memo:memo }, function( data ){ $( "#bw_level3" ).html( data );});
	displayVideo( 'memo saved');
};

// Koyomi Save Something
var koyomiSaveSome = function( yyyy, mm, dd, tdiv, id ){
	var some = document.getElementById( id ).value;
	$.post( "koyomi-edit.cgi", { command:'some', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:99, some:some }, function( data ){ $( "#bw_level3" ).html( data );});
	displayVideo( 'Something saved' );
};

// Koyomi edit return
var editKoyomiR_BW1 = function( yyyy, mm ){
	$.post( "koyomi.cgi", { command:"init", yyyy:yyyy, mm:mm }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
	document.getElementById( "bw_level3" ).style.display = 'none';
	document.getElementById( "bw_level4" ).style.display = 'none';
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi calc //////////////////////////////////////////////////////////////

// Koyomi calc
var calcKoyomi = function( yyyy, mm, dd, palette ){
	if( palette ){
		var palette = document.getElementById( "palette" ).value;
	}

	document.getElementById( "bw_level2" ).style.display = 'none';
	$.post( "koyomi-calc.cgi", { command:"init", yyyy:yyyy, mm:mm, dd:dd, palette:palette }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};

// Koyomi calc return
var calcKoyomiR = function( yyyy, mm ){
	document.getElementById( "bw_level2" ).style.display = 'block';
	document.getElementById( "bw_level3" ).style.display = 'none';
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi Direct fix data //////////////////////////////////////////////////////////////

// Koyomi fix
var fixKoyomi = function( com, yyyy, mm, dd, tdiv ){
	$.post( "koyomi-fix.cgi", { command:com, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv }, function( data ){ $( "#bw_level4" ).html( data );});
	document.getElementById( "bw_level4" ).style.display = 'block';
};

// Koyomi fix
var paletteKoyomi = function( yyyy, mm, dd, tdiv, modifyf ){
	displayVideo( modifyf );
	var palette = document.getElementById( "palette" ).value;
	$.post( "koyomi-fix.cgi", { command:'palette', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, palette:palette, modifyf:modifyf }, function( data ){ $( "#bw_level4" ).html( data );});
};

// Koyomi fix 100g check
var koyomiG100check = function(){
	if(document.getElementById( "g100_check" ).checked){
		document.getElementById( "food_weight" ).disabled = false;
	}else{
		document.getElementById( "food_weight" ).disabled = true;
	}
};


// Koyomi fix save
var koyomiSaveFix = function( yyyy, mm, dd, tdiv, modifyf, order ){
	var food_name = document.getElementById( "food_name" ).value;
	var hh = document.getElementById( "hh" ).value;
	var food_number = document.getElementById( "food_number" ).value;

	if( food_name != '' ){
		if(document.getElementById( "g100_check" ).checked){
			var food_weight = document.getElementById( "food_weight" ).value;
		}else{
			var food_weight = 100;
		}
		var ENERC_KCAL = document.getElementById( "ENERC_KCAL" ).value;
		var ENERC = document.getElementById( "ENERC" ).value;
		var WATER = document.getElementById( "WATER" ).value;

		var PROT = document.getElementById( "PROT" ).value;
		var PROTCAA = document.getElementById( "PROTCAA" ).value;
		var FAT = document.getElementById( "FAT" ).value;
		var FATNLEA = document.getElementById( "FATNLEA" ).value;
		var FASAT = document.getElementById( "FASAT" ).value;
		var FAMS = document.getElementById( "FAMS" ).value;
		var FAPU = document.getElementById( "FAPU" ).value;
		var CHOLE = document.getElementById( "CHOLE" ).value;
		var CHO = document.getElementById( "CHO" ).value;
		var CHOAVLM = document.getElementById( "CHOAVLM" ).value;
		var FIBSOL = document.getElementById( "FIBSOL" ).value;
		var FIBINS = document.getElementById( "FIBINS" ).value;
		var FIBTG = document.getElementById( "FIBTG" ).value;

		var ASH = document.getElementById( "ASH" ).value;
		var NA = document.getElementById( "NA" ).value;
		var K = document.getElementById( "K" ).value;
		var CA = document.getElementById( "CA" ).value;
		var MG = document.getElementById( "MG" ).value;
		var P = document.getElementById( "P" ).value;
		var FE = document.getElementById( "FE" ).value;
		var ZN = document.getElementById( "ZN" ).value;
		var CU = document.getElementById( "CU" ).value;
		var MN = document.getElementById( "MN" ).value;
		var ID = document.getElementById( "ID" ).value;
		var SE = document.getElementById( "SE" ).value;
		var CR = document.getElementById( "CR" ).value;
		var MO = document.getElementById( "MO" ).value;

		var RETOL = document.getElementById( "RETOL" ).value;
		var CARTA = document.getElementById( "CARTA" ).value;
		var CARTB = document.getElementById( "CARTB" ).value;
		var CRYPXB = document.getElementById( "CRYPXB" ).value;
		var CARTBEQ = document.getElementById( "CARTBEQ" ).value;
		var VITA_RAE = document.getElementById( "VITA_RAE" ).value;
		var VITD = document.getElementById( "VITD" ).value;
		var TOCPHA = document.getElementById( "TOCPHA" ).value;
		var TOCPHB = document.getElementById( "TOCPHB" ).value;
		var TOCPHG = document.getElementById( "TOCPHG" ).value;
		var TOCPHD = document.getElementById( "TOCPHD" ).value;
		var VITK = document.getElementById( "VITK" ).value;

		var THIAHCL = document.getElementById( "THIAHCL" ).value;
		var RIBF = document.getElementById( "RIBF" ).value;
		var NIA = document.getElementById( "NIA" ).value;
		var VITB6A = document.getElementById( "VITB6A" ).value;
		var VITB12 = document.getElementById( "VITB12" ).value;
		var FOL = document.getElementById( "FOL" ).value;
		var PANTAC = document.getElementById( "PANTAC" ).value;
		var BIOT = document.getElementById( "BIOT" ).value;
		var VITC = document.getElementById( "VITC" ).value;

		var NACL_EQ = document.getElementById( "NACL_EQ" ).value;
		var ALC = document.getElementById( "ALC" ).value;
		var NITRA = document.getElementById( "NITRA" ).value;
		var THEBRN = document.getElementById( "THEBRN" ).value;
		var CAFFN = document.getElementById( "CAFFN" ).value;
		var TAN = document.getElementById( "TAN" ).value;
		var POLYPHENT = document.getElementById( "POLYPHENT" ).value;
		var ACEAC = document.getElementById( "ACEAC" ).value;
		var COIL = document.getElementById( "COIL" ).value;
		var OA = document.getElementById( "OA" ).value;

		$.post( "koyomi-fix.cgi", {
			command:'save', yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh,
			food_name:food_name, food_weight:food_weight, food_number:food_number, modifyf:modifyf, order:order,
			ENERC_KCAL:ENERC_KCAL, ENERC:ENERC, WATER:WATER,
			PROT:PROT, PROTCAA:PROTCAA, FAT:FAT, FATNLEA:FATNLEA, FASAT:FASAT, FAMS:FAMS, FAPU:FAPU, CHOLE:CHOLE, CHO:CHO, CHOAVLM:CHOAVLM, FIBSOL:FIBSOL, FIBINS:FIBINS, FIBTG:FIBTG,
			ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
			RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
			THIAHCL:THIAHCL, RIBF:RIBF, NIA:NIA, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
			NACL_EQ:NACL_EQ, ALC:ALC, NITRA:NITRA, THEBRN:THEBRN, CAFFN:CAFFN, TAN:TAN, POLYPHENT:POLYPHENT, ACEAC:ACEAC, COIL:COIL, OA:OA
		}, function( data ){ $( "#bw_level4" ).html( data );});

		displayVideo( food_name + ' saved' );

		var fx = function(){
			$.post( "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){ $( "#bw_level3" ).html( data );});
		};
		setTimeout( fx , 1000 );
	} else{
		displayVideo( 'Food name! (>_<)' );
	}
};


// Koyomi modify or copy panel fix
var modifyKoyomif = function( code, yyyy, mm, dd, tdiv, hh, order ){
	closeBroseWindows( 3 );
	$.post( "koyomi-fix.cgi", {command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, order:order }, function( data ){ $( "#bw_level4" ).html( data );});
	document.getElementById( "bw_level4" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi import panel//////////////////////////////////////////////////////////////

// Koyomi insert panel
var addKoyomi_BWF = function( code ){
	closeBroseWindows( 0 );
	$.post( "koyomi-add.cgi", { command:"init", code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Koyomi insert panel change
var changeKoyomi_BWF = function( code, origin ){
	var dd = document.getElementById( "dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh = document.getElementById( "hh" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	var yyyy = document.getElementById( "yyyy_add" ).value;
	var mm = document.getElementById( "mm_add" ).value;
	displayVideo( mm );
	$.post( "koyomi-add.cgi", { command:"init", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin }, function( data ){ $( "#bw_levelF" ).html( data );});
};

// Saving code into Koyomi
var saveKoyomi_BWF = function( code, origin ){
	var yyyy = document.getElementById( "yyyy_add" ).value;
	var mm = document.getElementById( "mm_add" ).value;
	var dd = document.getElementById( "dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh = document.getElementById( "hh" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	$.post( "koyomi-add.cgi", { command:"save", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin }, function( data ){ $( "#bw_levelF" ).html( data );});
};

// Saving code into Koyomi2
var saveKoyomi2_BWF = function( code, yyyy, mm, dd, tdiv, origin ){
	var hh = document.getElementById( "hh" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	$.post( "koyomi-add.cgi", { command:"save", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin }, function( data ){ $( "#bw_levelF" ).html( data );});
};

// Koyomi insert panel change
var modifychangeKoyomi = function( code, origin ){
	var dd = document.getElementById( "dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh = document.getElementById( "hh" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	var yyyy = document.getElementById( "yyyy_add" ).value;
	var mm = document.getElementById( "mm_add" ).value;
	displayVideo( mm );
	$.post( "koyomi-add.cgi", { command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin }, function( data ){ $( "#bw_levelF" ).html( data );});
};

// Koyomi modify or copy panel
var modifyKoyomi = function( code, yyyy, mm, dd, tdiv, hh, ev, eu, order ){
	closeBroseWindows( 2 );
	$.post( "koyomi-add.cgi", {command:"modify", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, order:order }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};


// Modifying or copying code in Koyomi
var modifysaveKoyomi = function( code, origin ){
	var yyyy = document.getElementById( "yyyy_add" ).value;
	var mm = document.getElementById( "mm_add" ).value;
	var dd = document.getElementById( "dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh = document.getElementById( "hh" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	var copy = 0;
	if( document.getElementById( "copy" ).checked ){ copy = 1; }
	$.post( "koyomi-add.cgi", { command:"move", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin, copy:copy }, function( data ){ $( "#bw_levelF" ).html( data );});
};

// Modifying or copying code in Koyomi
var modifysaveKoyomi2 = function( code, yyyy, mm, dd, tdiv, origin ){
	var hh = document.getElementById( "hh" ).value;
	var ev = document.getElementById( "ev" ).value;
	var eu = document.getElementById( "eu" ).value;
	var copy = 0;
	if( document.getElementById( "copy" ).checked ){ copy = 1; }
	$.post( "koyomi-add.cgi", { command:"move", code:code, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, ev:ev, eu:eu, origin:origin, copy:copy }, function( data ){ $( "#bw_levelF" ).html( data );});
};

// Return from Koyomi
var koyomiReturn = function(){
	document.getElementById( "bw_levelF" ).style.display = 'none';
	if( bw_level == 1 ){
		document.getElementById( "bw_level1" ).style.display = 'block';
	}
	if( bw_level == 5 ){
		document.getElementById( "bw_level5" ).style.display = 'block';
	}
};

// Return from Koyomi to Koyomi edit
var koyomiReturn2KE = function( yyyy, mm, dd ){
	document.getElementById( "bw_levelF" ).style.display = 'none';
	document.getElementById( "bw_level3" ).style.display = 'block';
	$.post( "koyomi-edit.cgi", { command:'init', yyyy:yyyy, mm:mm, dd:dd }, function( data ){ $( "#bw_level3" ).html( data );});

};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi menu copy / move //////////////////////////////////////////////////////////////

var cmmKoyomi = function( cm_mode, yyyy, mm, dd, tdiv ){
	closeBroseWindows( 0 );
	$.post( "koyomi-cmm.cgi", { command:"init", cm_mode:cm_mode, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:99 }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

var cmmSaveKoyomi = function( cm_mode, yyyy, mm, dd, tdiv, origin ){
	var hh = document.getElementById( "hh" ).value;
	$.post( "koyomi-cmm.cgi", { command:"save", cm_mode:cm_mode, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, origin:origin }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

var cmmSaveKoyomi2 = function( cm_mode, origin ){
	var yyyy = document.getElementById( "yyyy" ).value;
	var mm = document.getElementById( "mm" ).value;
	var dd = document.getElementById( "dd" ).value;
	var tdiv = document.getElementById( "tdiv" ).value;
	var hh = document.getElementById( "hh" ).value;
	$.post( "koyomi-cmm.cgi", { command:"save", cm_mode:cm_mode, yyyy:yyyy, mm:mm, dd:dd, tdiv:tdiv, hh:hh, origin:origin }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Koyomi EX //////////////////////////////////////////////////////////////

// Koyomi EX init
var initKoyomiex_BW1 = function( yyyy, mm ){
	closeBroseWindows( 2 );
	$.post( "koyomiex.cgi", { command:"init", yyyy:yyyy, mm:mm }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
};

// Koyomiex change
var changeKoyomiex_BW1 = function(){
	var yyyy = document.getElementById( "yyyy" ).value;
	var mm = document.getElementById( "mm" ).value;
	$.post( "koyomiex.cgi", { command:"init", yyyy:yyyy, mm:mm }, function( data ){ $( "#bw_level2" ).html( data );});
};

// Updating Koyomiex cell
var updateKoyomiex = function( dd, item_no, cell_id ){
	var yyyy = document.getElementById( "yyyy" ).value;
	var mm = document.getElementById( "mm" ).value;
	var cell = document.getElementById( cell_id ).value;
//	$.post( "koyomiex.cgi", { command:"update", yyyy:yyyy, mm:mm, dd:dd, item_no:item_no, cell:cell }, function( data ){ $( "#bw_level2" ).html( data );});
	$.post( "koyomiex.cgi", { command:"update", yyyy:yyyy, mm:mm, dd:dd, item_no:item_no, cell:cell }, function( data ){});
};


/////////////////////////////////////////////////////////////////////////////////
// Ginmi //////////////////////////////////////////////////////////////

// Ginmi init
var initGinmi = function(){
	closeBroseWindows( 1 );
	$.post( "ginmi.cgi", { mod:'' }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
};

var ginmiForm = function( mod ){
	$.post( "ginmi.cgi", { mod:mod, command:'form' }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
};
