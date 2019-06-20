/////////////////////////////////////////////////////////////////////////////////
// Unit exchange ////////////////////////////////////////////////////////////////////////

// Unit exchange init
var initUnitc_BWLF = function( com ){
	if( com == 'init' ){
		var code = '';
	} else{
		var code = document.getElementById( "food_no" ).value;
	}

	$.post( "gm-unitc.cgi", { command:com, code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Direct unit exchange button
var directUnitc_BWLF = function( code ){
	$.post( "gm-unitc.cgi", { command:'init', code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Update unit exchange button
var updateUintc_BWL1 = function(){
	var code = document.getElementById( "food_no" ).value;

	if( code != '' ){
		var uc2 = document.getElementById( "unitc2" ).value;
		var uc3 = document.getElementById( "unitc3" ).value;
		var uc4 = document.getElementById( "unitc4" ).value;
		var uc5 = document.getElementById( "unitc5" ).value;
		var uc6 = document.getElementById( "unitc6" ).value;
		var uc7 = document.getElementById( "unitc7" ).value;
		var uc8 = document.getElementById( "unitc8" ).value;
		var uc9 = document.getElementById( "unitc9" ).value;
		var uc10 = document.getElementById( "unitc10" ).value;
		var uc11 = document.getElementById( "unitc11" ).value;
		var uc12 = document.getElementById( "unitc12" ).value;
		var uc13 = document.getElementById( "unitc13" ).value;
		var uc14 = document.getElementById( "unitc14" ).value;
		var notice = document.getElementById( "notice" ).value;

		$.post( "gm-unitc.cgi", { command:'update', code:code, unitc2:uc2, unitc3:uc3, unitc4:uc4, unitc5:uc5, unitc6:uc6, unitc7:uc7, unitc8:uc8, unitc9:uc9, unitc10:uc10, unitc11:uc11, unitc12:uc12, unitc13:uc13, unitc14:uc14, notice:notice}, function( data ){ $( "#bw_levelF" ).html( data );});
		displayVideo( code + ' saved' );
	}
};


/////////////////////////////////////////////////////////////////////////////////
// Food color ////////////////////////////////////////////////////////////////////////

// Food color init
var initColor_BWLF = function( com ){
	if( com == 'init' ){
		var code = '';
	} else{
		var code = document.getElementById( "food_no" ).value;
	}

	$.post( "gm-color.cgi", { command:com, code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Direct food color button
var directColor_BWLF = function( code ){
	$.post( "gm-color.cgi", { command:'init', code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Update food color
var updateColor_BWL1 = function(){
	var code = document.getElementById( "food_no" ).value;
	if( code != '' ){
		var color1 = 0
		var color2 = 0
		var color1h = 0
		var color2h = 0

		if( document.getElementById( "color1_0" ).checked ){ color1 = 0; }
		if( document.getElementById( "color1_1" ).checked ){ color1 = 1; }
		if( document.getElementById( "color1_2" ).checked ){ color1 = 2; }
		if( document.getElementById( "color1_3" ).checked ){ color1 = 3; }
		if( document.getElementById( "color1_4" ).checked ){ color1 = 4; }
		if( document.getElementById( "color1_5" ).checked ){ color1 = 5; }
		if( document.getElementById( "color1_6" ).checked ){ color1 = 6; }
		if( document.getElementById( "color1_7" ).checked ){ color1 = 7; }
		if( document.getElementById( "color1_8" ).checked ){ color1 = 8; }
		if( document.getElementById( "color1_9" ).checked ){ color1 = 9; }
		if( document.getElementById( "color1_10" ).checked ){ color1 = 10; }
		if( document.getElementById( "color1_11" ).checked ){ color1 = 11; }

		if( document.getElementById( "color2_0" ).checked ){ color2 = 0; }
		if( document.getElementById( "color2_1" ).checked ){ color2 = 1; }
		if( document.getElementById( "color2_2" ).checked ){ color2 = 2; }
		if( document.getElementById( "color2_3" ).checked ){ color2 = 3; }
		if( document.getElementById( "color2_4" ).checked ){ color2 = 4; }
		if( document.getElementById( "color2_5" ).checked ){ color2 = 5; }
		if( document.getElementById( "color2_6" ).checked ){ color2 = 6; }
		if( document.getElementById( "color2_7" ).checked ){ color2 = 7; }
		if( document.getElementById( "color2_8" ).checked ){ color2 = 8; }
		if( document.getElementById( "color2_9" ).checked ){ color2 = 9; }
		if( document.getElementById( "color2_10" ).checked ){ color2 = 10; }
		if( document.getElementById( "color2_11" ).checked ){ color2 = 11; }

		if( document.getElementById( "color1h_0" ).checked ){ color1h = 0; }
		if( document.getElementById( "color1h_1" ).checked ){ color1h = 1; }
		if( document.getElementById( "color1h_2" ).checked ){ color1h = 2; }
		if( document.getElementById( "color1h_3" ).checked ){ color1h = 3; }
		if( document.getElementById( "color1h_4" ).checked ){ color1h = 4; }
		if( document.getElementById( "color1h_5" ).checked ){ color1h = 5; }
		if( document.getElementById( "color1h_6" ).checked ){ color1h = 6; }
		if( document.getElementById( "color1h_7" ).checked ){ color1h = 7; }
		if( document.getElementById( "color1h_8" ).checked ){ color1h = 8; }
		if( document.getElementById( "color1h_9" ).checked ){ color1h = 9; }
		if( document.getElementById( "color1h_10" ).checked ){ color1h = 10; }
		if( document.getElementById( "color1h_11" ).checked ){ color1h = 11; }

		if( document.getElementById( "color2h_0" ).checked ){ color2h = 0; }
		if( document.getElementById( "color2h_1" ).checked ){ color2h = 1; }
		if( document.getElementById( "color2h_2" ).checked ){ color2h = 2; }
		if( document.getElementById( "color2h_3" ).checked ){ color2h = 3; }
		if( document.getElementById( "color2h_4" ).checked ){ color2h = 4; }
		if( document.getElementById( "color2h_5" ).checked ){ color2h = 5; }
		if( document.getElementById( "color2h_6" ).checked ){ color2h = 6; }
		if( document.getElementById( "color2h_7" ).checked ){ color2h = 7; }
		if( document.getElementById( "color2h_8" ).checked ){ color2h = 8; }
		if( document.getElementById( "color2h_9" ).checked ){ color2h = 9; }
		if( document.getElementById( "color2h_10" ).checked ){ color2h = 10; }
		if( document.getElementById( "color2h_11" ).checked ){ color2h = 11; }

		$.post( "gm-color.cgi", { command:'update', code:code, color1:color1, color2:color2, color1h:color1h, color2h:color2h }, function( data ){ $( "#bw_levelF" ).html( data );});
		displayVideo( code + ' saved' );
	}
};


/////////////////////////////////////////////////////////////////////////////////
// Food name dictionary ////////////////////////////////////////////////////////////////////////

// Food name dictionary init
var initDic_BWL1 = function( com ){
	closeBroseWindows( 1 );
	$.post( "gm-dic.cgi", { command:com }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
};

// Direct food name dictionary button
var saveDic_BWL1 = function( org_name, tn ){
	displayVideo( tn );
	var aliases = document.getElementById( 'tn' + tn ).value;
	$.post( "gm-dic.cgi", { command:'save', org_name:org_name, tn:tn, aliases:aliases }, function( data ){});
	displayVideo( org_name + ' modified' );
};


/////////////////////////////////////////////////////////////////////////////////
// Allergen ////////////////////////////////////////////////////////////////////////

// Allergen init
var initAllergen_BWLF = function( com ){
	$.post( "gm-allergen.cgi", { command:com }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Direct allergen button
var directAllergen_BWLF = function( code ){
	$.post( "gm-allergen.cgi", { command:'init', code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Allergen ON
var onAllergen_BWL1 = function(){
	var code = document.getElementById( 'code' ).value;
	var allergen = 0
	if(document.getElementById( 'ag_class1' ).checked == true ){ allergen = '1' }
	if(document.getElementById( 'ag_class2' ).checked == true ){ allergen = '2' }
	if(document.getElementById( 'ag_class3' ).checked == true ){ allergen = '3' }
	$.post( "gm-allergen.cgi", { command:'on', code:code, allergen:allergen }, function( data ){ $( "#bw_levelF" ).html( data );});
	displayVideo( code + ':allergen ON' );
};

// Allergen OFF
var offAllergen_BWL1 = function( code ){
	$.post( "gm-allergen.cgi", { command:'off', code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	displayVideo( code + ':allergen OFF' );
};


/////////////////////////////////////////////////////////////////////////////////
// Green yellow color vegetable ////////////////////////////////////////////////////////////////////////

// GYCV init
var initGYCV_BWLF = function( com ){
	$.post( "gm-gycv.cgi", { command:com }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// GYCV ON
var onGYCV_BWL1 = function(){
	var food_no = document.getElementById( 'food_no' ).value;
	$.post( "gm-gycv.cgi", { command:'on', food_no:food_no }, function( data ){ $( "#bw_levelF" ).html( data );});
	displayVideo( food_no + ':GYCV ON' );
};

// GYCV OFF
var offGYCV_BWL1 = function( food_no ){
	$.post( "gm-gycv.cgi", { command:'off', food_no:food_no }, function( data ){ $( "#bw_levelF" ).html( data );});
	displayVideo( food_no + ':GYCV OFF' );
};

/////////////////////////////////////////////////////////////////////////////////
// Shun ////////////////////////////////////////////////////////////////////////

// Shun init
var initShun_BWLF = function( com ){
	$.post( "gm-shun.cgi", { command:com }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Direct shun button
var directShun_BWLF = function( code ){
	$.post( "gm-shun.cgi", { command:'init', code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Shun ON
var onShun_BWL1 = function(){
	var code = document.getElementById( 'code' ).value;
	var shun1s = document.getElementById( 'shun1s' ).value;
	var shun1e = document.getElementById( 'shun1e' ).value;
	var shun2s = document.getElementById( 'shun2s' ).value;
	var shun2e = document.getElementById( 'shun2e' ).value;
	$.post( "gm-shun.cgi", { command:'on', code:code, shun1s:shun1s, shun1e:shun1e, shun2s:shun2s, shun2e:shun2e }, function( data ){ $( "#bw_levelF" ).html( data );});
	displayVideo( code + ':Shun ON' );
};

// Shun OFF
var offShun_BWL1 = function( code ){
	$.post( "gm-shun.cgi", { command:'off', code:code }, function( data ){ $( "#bw_levelF" ).html( data );});
	displayVideo( code + ':Shun OFF' );
};


/////////////////////////////////////////////////////////////////////////////////
// Food search log ////////////////////////////////////////////////////////////////////////

// Food search log init
var initSlogf_BWL1 = function( com ){
	closeBroseWindows( 1 );
	$.post( "gm-slogf.cgi", { command:com }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Account ////////////////////////////////////////////////////////////////////////

// Account init
var initAccount_BWL1 = function( com ){
	closeBroseWindows( 1 );
	$.post( "gm-account.cgi", { command:com }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
};

// Edit account
var editAccount_BWL2 = function( target_uid ){
	$.post( "gm-account.cgi", { command:'edit', target_uid:target_uid }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'none';
	document.getElementById( "bw_level2" ).style.display = 'block';
};

// Update account
var saveAccount_BWL1 = function( target_uid ){
	var target_pass = document.getElementById( 'target_pass' ).value;
	var target_mail = document.getElementById( 'target_mail' ).value;
	var target_aliasu = document.getElementById( 'target_aliasu' ).value;
	var target_status = document.getElementById( 'target_status' ).value;
	var target_language = document.getElementById( 'target_language' ).value;
	$.post( "gm-account.cgi", { command:'save', target_uid:target_uid, target_pass:target_pass, target_mail:target_mail, target_aliasu:target_aliasu, target_status:target_status, target_language:target_language }, function( data ){ $( "#bw_level1" ).html( data );});
	displayVideo( target_uid + ' saved' );
	document.getElementById( "bw_level2" ).style.display = 'none';
	document.getElementById( "bw_level1" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Memory ////////////////////////////////////////////////////////////////////////

// Memory init
var initMemory_BWLF = function(){
	closeBroseWindows( 0 );
	$.post( "gm-memory.cgi", { command:'init' }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// New memory
var newMemory_BWLF = function(){
	$.post( "gm-memory.cgi", { command:'new' }, function( data ){ $( "#bw_levelF" ).html( data );});
};

// New pointer
var newPMemory_BWLF = function( category, pointer, post_process ){
	$.post( "gm-memory.cgi", { command:'new_pointer', category:category, pointer:pointer, post_process:post_process }, function( data ){ $( "#bw_levelF" ).html( data );});
	document.getElementById( "bw_levelF" ).style.display = 'block';
};

// Save memory
var saveMemory_BWLF = function( mode ){
	var memory = document.getElementById( 'memory' ).value;
	$.post( "gm-memory.cgi", { command:'save', memory:memory, mode:mode }, function( data ){ $( "#bw_levelF" ).html( data );});
	displayVideo( 'Saved' );
};

// Save pointer
var savePMemory_BWLF = function( category, post_process ){
	var pointer = document.getElementById( 'pointer' ).value;
	var memory = document.getElementById( 'memory' ).value;
	var rank = document.getElementById( 'rank' ).value;
	if( post_process == 'front'){
		$.post( "gm-memory.cgi", { command:'save_pointer', memory:memory, category:category, pointer:pointer, rank:rank }, function( data ){ $( "#bw_levelF" ).html( data );});
	}else{
		$.post( "gm-memory.cgi", { command:'save_pointer', memory:memory, category:category, pointer:pointer, rank:rank }, function( data ){});
		document.getElementById( "bw_levelF" ).style.display = 'none';
	}
	displayVideo( 'Saved' );
}

//
var editMemory_BWLF = function( category ){
	$.post( "gm-memory.cgi", { command:'edit', category:category }, function( data ){ $( "#bw_levelF" ).html( data );});
};

var newCategory_BWLF = function(){
	$.post( "gm-memory.cgi", { command:'new_category' }, function( data ){ $( "#bw_levelF" ).html( data );});
};

var saveCategory_BWLF = function(){
	var category = document.getElementById( 'category' ).value;
	$.post( "gm-memory.cgi", { command:'save_category', category:category }, function( data ){ $( "#bw_levelF" ).html( data );});
};

var deleteMemory_BWLF = function( category, delete_check_no ){
	if( document.getElementById( delete_check_no ).checked ){
		$.post( "gm-memory.cgi", { command:'delete', category:category }, function( data ){ $( "#bw_levelF" ).html( data );});
	}else{
		displayVideo( 'Check!' );
	}
};

var deletePMemory_BWLF = function( category, pointer, delete_check_no ){
	if( document.getElementById( delete_check_no ).checked ){
		$.post( "gm-memory.cgi", { command:'delete_pointer', category:category, pointer:pointer }, function( data ){ $( "#bw_levelF" ).html( data );});
	}else{
		displayVideo( 'Check!' );
	}
};
