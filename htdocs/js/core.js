///////////////////////////////////////////////////////////////////////////////////
// Global ////////////////////////////////////////////////////////////////////
bw_level = 0;
menu_status = 0;
general_ = '';

/////////////////////////////////////////////////////////////////////////////////
// Paging /////////////////////////////////////////////////////////////////////////

// initialization
window.onload = function(){
	if( !!document.getElementById( "bw_level1" )){
		document.getElementById( "bw_level1" ).innerHTML = "";
		document.getElementById( "bw_level2" ).innerHTML = "";
		document.getElementById( "bw_level3" ).innerHTML = "";
		document.getElementById( "bw_level4" ).innerHTML = "";
		document.getElementById( "bw_level5" ).innerHTML = "";
		document.getElementById( "bw_levelF" ).innerHTML = "";

		bookOpen( 'books/information.html', 1 );
	}
};


// Closing browse windows
var closeBroseWindows = function( num ){
	switch( Number( num )){
	case 0:
		document.getElementById( "bw_level1" ).style.display = 'none';
	case 1:
		document.getElementById( "bw_level2" ).style.display = 'none';
	case 2:
		document.getElementById( "bw_level3" ).style.display = 'none';
	case 3:
		document.getElementById( "bw_level4" ).style.display = 'none';
	case 4:
		document.getElementById( "bw_level5" ).style.display = 'none';
	case 5:
		document.getElementById( "bw_levelF" ).style.display = 'none';
 	}
};


// Displaying message on VIDEO
var displayVideo = function( msg ){
	document.getElementById( "video" ).innerHTML = msg;
	document.getElementById( "video" ).style.display = 'block';
	var fx = function(){
		document.getElementById( "video" ).innerHTML = "";
		document.getElementById( "video" ).style.display = 'none';
	};
	setTimeout( fx, 2000 );
};


// Saving code into FC memory
var memoryFC = function( code ){
	fn_mem = code;
	displayVideo( code + ' saved');
};


// Exchanging menu sets
var changeMenu = function(){
	if( menu_status == 0 ){
		document.getElementById( "normal_menu" ).style.display = 'none';
		document.getElementById( "guild_menu" ).style.display = 'inline';
		displayVideo( 'Guild menu');
		menu_status = 1;
	}else{
		document.getElementById( "guild_menu" ).style.display = 'none';
		document.getElementById( "normal_menu" ).style.display = 'inline';
		displayVideo( 'Standard menu' );
		menu_status = 0;
	}
}


/////////////////////////////////////////////////////////////////////////////////
// Browsing nutritional Information /////////////////////////////////////////////////////////////////////

// Display foods on BWL1
var summonBWL1 = function( num ){
	closeBroseWindows( 1 );
	$.get( "square.cgi", { channel:"fctb", category:num }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
	bw_level = 1;
};


// Display foods on BWL2
var summonBWL2 = function( key ){
	closeBroseWindows( 2 );
	$.get( "square.cgi", { channel:"fctb_l2", food_key:key }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
	bw_level = 2;
};


// Display foods on BWL3
var summonBWL3 = function( key, direct ){
	if( direct > 0 ){
		closeBroseWindows( direct );
	}
	$.get( "square.cgi", { channel:"fctb_l3", food_key:key }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
	bw_level = 3;
};


// Display foods on BWL4
var summonBWL4 = function( key, direct ){
	if( direct > 0 ){
		closeBroseWindows( direct );
	}
	$.get( "square.cgi", { channel:"fctb_l4", food_key:key }, function( data ){ $( "#bw_level4" ).html( data );});
	document.getElementById( "bw_level4" ).style.display = 'block';
	bw_level = 4;
};


// Display foods on BWL5
var summonBWL5 = function( key, direct ){
	if( direct > 0 ){
		closeBroseWindows( direct );
	}
	$.get( "square.cgi", { channel:"fctb_l5", food_key:key }, function( data ){ $( "#bw_level5" ).html( data );});
	document.getElementById( "bw_level5" ).style.display = 'block';
	bw_level = 5;
};


// Changing weight of food
var changeWeight = function( key, fn ){
	var fraction_mode = document.getElementById( "fraction" ).value;
	var weight = document.getElementById( "weight" ).value;
	$.get( "square.cgi", { channel:"fctb_l5", food_key:key, frct_mode:fraction_mode, food_weight:weight }, function( data ){ $( "#bw_level5" ).html( data );});
};


//////////////////////////////////////////////////////////////////////////////////
// Browsing nutritional Information (ditail) ///////////////////////////////////////////////////////////////////////

// Display ditail information on LF
var detailView = function( fn ){
	var fraction_mode = document.getElementById( "fraction" ).value;
	var weight = document.getElementById( "weight" ).value;
	$.get( "detail.cgi", { food_no:fn, frct_mode:fraction_mode, food_weight:weight }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_level5" ).style.display = 'none';
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Display ditail information on LF (history)
var detailView_his = function( fn ){
	var fraction_mode = document.getElementById( "fraction" ).value;
	var weight = document.getElementById( "weight" ).value;
	$.get( "detail.cgi", { food_no:fn, frct_mode:fraction_mode, food_weight:weight }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'none';
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// 詳細ボタンを押したらL1-L4の窓を閉じて、LF閲覧ウインドウに詳細を表示する２。
//var detailView2 = function( fn, weight ){
//	$.get( "detail.cgi", { food_no:fn, food_weight:weight }, function( data ){ $( "#bw_levelF" ).html( data );});
//	document.getElementById( "bw_levelF" ).style.display = 'block';
//};

// Changing weight of food (ditail)
var detailWeight = function( fn ){
	var fraction_mode = document.getElementById( "detail_fraction" ).value;
	var weight = document.getElementById( "detail_weight" ).value;
	$.get( "detail.cgi", { food_no:fn, frct_mode:fraction_mode, food_weight:weight }, function( data ){ $( "#bw_levelF" ).html( data );});
};


// 詳細画面のページボタンを押したらL5閲覧ウインドウの内容を書き換える。
var detailPage = function( dir, sid ){
	var fraction_mode = document.getElementById( "detail_fraction" ).value;
	var weight = document.getElementById( "detail_weight" ).value;
	$.get( "detail.cgi", { dir:dir, sid:sid, frct_mode:fraction_mode, food_weight:weight }, function( data ){ $( "#bw_levelF" ).html( data );});
};


// 詳細画面のページボタンを押したらL5閲覧ウインドウの内容を書き換える。
var detailReturn = function(){
	document.getElementById( "bw_levelF" ).style.display = 'none';
	if( bw_level == 1 ){
		document.getElementById( "bw_level1" ).style.display = 'block';
	}
	if( bw_level == 5 ){
		document.getElementById( "bw_level5" ).style.display = 'block';
	}
};


/////////////////////////////////////////////////////////////////////////////////
// Referencing /////////////////////////////////////////////////////////////////////////

// Disply results
var searchBWL1 = function(){
	var words = document.getElementById( "words" ).value;
	var qcate = document.getElementById( "qcate" ).value;
	if( words != '' ){
		closeBroseWindows( 1 );
		switch( qcate ){
		case '0':
			$.post( "search-food.cgi", { words:words }, function( data ){ $( "#bw_level1" ).html( data );});
			break;
		case '1':
			$.post( "recipel.cgi", { command:'refer', words:words }, function( data ){ $( "#bw_level1" ).html( data );});
			break;
		case '2':
			$.post( "memory.cgi", { command:'refer', pointer:words }, function( data ){ $( "#bw_level1" ).html( data );});
			break;
 		}
		document.getElementById( "bw_level1" ).style.display = 'block';
	}
};

// Sending alias request
var aliasRequest = function( food_no ){
	document.getElementById( "bw_levelF" ).style.display = 'block';
	var alias = document.getElementById( "alias" ).value;
	if( alias != '' && alias != general_ ){
		$.post( "alias-req.cgi", { food_no:food_no, alias:alias }, function( data ){});
		displayVideo( 'Request sent' );
	}else if( alias == general_ ){
		displayVideo( 'Request sent' );
	}else{
		displayVideo( 'Alias! (>_<)' );
	}
	general_ = alias;
};

/////////////////////////////////////////////////////////////////////////////////
// history /////////////////////////////////////////////////////////////////////////

// Display history
var historyBWL1 = function( order, weight, fraction_mode, sub_fg ){
	closeBroseWindows( 1 );
	$.post( "history.cgi", { order_mode:order, food_weight:weight, frct_mode:fraction_mode, sub_fg:sub_fg }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
	bw_level = 1;
};


// Changing food weight on history
var history_changeWeight = function( order, fn, sub_fg ){
	var fraction_mode = document.getElementById( "fraction" ).value;
	var weight = document.getElementById( "weight" ).value;
	$.post( "history.cgi", { order_mode:order, food_no:fn, food_weight:weight, frct_mode:fraction_mode, sub_fg:sub_fg }, function( data ){ $( "#bw_level1" ).html( data );});
};


/////////////////////////////////////////////////////////////////////////////////
// Puseudo food //////////////////////////////////////////////////////////////////////

// カテゴリーボタンを押したときに非同期通信でL1閲覧ウインドウの内容を書き換える
var pseudoAdd_BWLF = function( com, food_key, code ){
	closeBroseWindows( 5 );
	$.post( "pseudo.cgi", { command:com, food_key:food_key, code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';

	bw_levelF_status = 'block';
};


// 登録ボタンを押してLFにエディタを表示
var pseudoSave_BWLF = function( code ){
	var food_name = document.getElementById( "food_name" ).value;

	if( food_name != '' ){
		var food_group = document.getElementById( "food_group" ).value;
		var class1 = document.getElementById( "class1" ).value;
		var class2 = document.getElementById( "class2" ).value;
		var class3 = document.getElementById( "class3" ).value;
		var tag1 = document.getElementById( "tag1" ).value;
		var tag2 = document.getElementById( "tag2" ).value;
		var tag3 = document.getElementById( "tag3" ).value;
		var tag4 = document.getElementById( "tag4" ).value;
		var tag5 = document.getElementById( "tag5" ).value;
		var food_weight = document.getElementById( "food_weight" ).value;

		var REFUSE = document.getElementById( "REFUSE" ).value;
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
		var WCR = document.getElementById( "WCR" ).value;

		var Notice = document.getElementById( "Notice" ).value;

		$.post( "pseudo.cgi", {
			command:'save', code:code, food_name:food_name, food_group:food_group, food_weight:food_weight,
			class1:class1, class2:class2, class3:class3, tag1:tag1, tag2:tag2, tag3:tag3, tag4:tag4, tag5:tag5,
			REFUSE:REFUSE, ENERC_KCAL:ENERC_KCAL, ENERC:ENERC, WATER:WATER,
			PROT:PROT, PROTCAA:PROTCAA, FAT:FAT, FATNLEA:FATNLEA, FASAT:FASAT, FAMS:FAMS, FAPU:FAPU, CHOLE:CHOLE, CHO:CHO, CHOAVLM:CHOAVLM, FIBSOL:FIBSOL, FIBINS:FIBINS, FIBTG:FIBTG,
			ASH:ASH, NA:NA, K:K, CA:CA, MG:MG, P:P, FE:FE, ZN:ZN, CU:CU, MN:MN, ID:ID, SE:SE, CR:CR, MO:MO,
			RETOL:RETOL, CARTA:CARTA, CARTB:CARTB, CRYPXB:CRYPXB, CARTBEQ:CARTBEQ, VITA_RAE:VITA_RAE, VITD:VITD, TOCPHA:TOCPHA, TOCPHB:TOCPHB, TOCPHG:TOCPHG, TOCPHD:TOCPHD, VITK:VITK,
			THIAHCL:THIAHCL, RIBF:RIBF, NIA:NIA, VITB6A:VITB6A, VITB12:VITB12, FOL:FOL, PANTAC:PANTAC, BIOT:BIOT, VITC:VITC,
			NACL_EQ:NACL_EQ, ALC:ALC, NITRA:NITRA, THEBRN:THEBRN, CAFFN:CAFFN, TAN:TAN, POLYPHENT:POLYPHENT, ACEAC:ACEAC, COIL:COIL, OA:OA, WCR:WCR,
			Notice:Notice
		}, function( data ){ $( "#bw_levelF" ).html( data );});

		displayVideo( food_name + ' saved' );
	} else{
		displayVideo( 'Food name! (>_<)' );
	}
};

// 削除ボタンを押したときに非同期通信でLFの内容を書き換える
var pseudoDelete_BWLF = function( code ){
	$.post( "pseudo.cgi", { command:'delete', code:code }, function( data ){});
	displayVideo( code + ' deleted' );
	closeBroseWindows( 5 );
};


/////////////////////////////////////////////////////////////////////////////////
// Bookshelf /////////////////////////////////////////////////////////////////////////

// Display Bookshelf
var bookOpen = function( url, level ){

	closeBroseWindows( level );
	$.ajax({ url:url, type:'GET', dataType:'html', success:function( data ){ $( "#bw_level" + level ).html( data ); }});
	document.getElementById( "bw_level" + level ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Memory /////////////////////////////////////////////////////////////////////////

// Display memory
var memoryOpen = function( com, category, pointer, depth ){
	closeBroseWindows( depth );
	$.post( "memory.cgi", { command:com, category:category, pointer:pointer, depth:depth }, function( data ){ $( "#bw_level" + depth ).html( data );});
	document.getElementById( "bw_level" + depth ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Meta data //////////////////////////////////////////////////////////////////////////

// Display meta data
var metaDisplay = function( com ){
	closeBroseWindows( 2 );
	$.post( "meta.cgi", { command:com }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Proprty //////////////////////////////////////////////////////////////////////////

// Display config menu
var configInit = function(){
	closeBroseWindows( 2 );
	$.post( "config.cgi", { command:'init' }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
};
