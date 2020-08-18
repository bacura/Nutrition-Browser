
// Chopping boad ////////////////////////////////////////////////////////////////////////

// Add food into sum, and reload CB counter
var addingCB = function( fn, weight_id ){
	if( weight_id != '' ){
		var weight = document.getElementById( weight_id ).value;
	}
	$.post( "cboardm.cgi", { food_no:fn, food_weight:weight, mode:'add' }, function( data ){ $( "#cb_num" ).html( data );});
	if( fn != '' ){ displayVideo( '+' + fn ); }

	var fxRI = function(){
		$.post( "cboardm.cgi", { mode:'refresh' }, function( data ){ $( "#cb_num" ).html( data );});
	};
	setTimeout( fxRI, 1000 );
};


// Only reload CB counter
var refreshCB = function(){
	$.post( "cboardm.cgi", { mode:'refresh' }, function( data ){ $( "#cb_num" ).html( data );});
};


// 変更ボタンを押してsumの食品を変更する
var changingCB = function( fn, base_fn ){
	var weight = document.getElementById( "weight" ).value;

	$.post( "cboardm.cgi", { food_no:fn, food_weight:weight, base_fn:base_fn, mode:'change' }, function( data ){ $( "#cb_num" ).html( data );});
	if( fn != '' ){ displayVideo( fn + 'has modified' ); }
	$.post( "cboard.cgi", { command:'refresh', code:'' }, function( data ){ $( "#bw_level1" ).html( data );});
	closeBroseWindows( 1 );
};


// Display CB sum in L1
var initCB_BWL1 = function( com, code ){
	closeBroseWindows( 1 );
	$.post( "cboard.cgi", { command:com, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
	setTimeout( refreshCB(), 1000 );
	bw_level = 1;
};


// Clear foods, and reload CB counter
var clear_BWL1 = function( order, code ){
	if( order == 'all'){
		if( document.getElementById( 'all_check' ).checked ){
			$.post( "cboard.cgi", { command:'clear', option1:'all', code:code }, function( data ){ $( "#bw_level1" ).html( data );});

			document.getElementById( "bw_level2" ).style.display = 'none';
			document.getElementById( "bw_level3" ).style.display = 'none';

			displayVideo( 'CB has cleared' );
		} else{
			displayVideo( '(>_<)cheack!' );
		}
	} else{
		$.post( "cboard.cgi", { command:'clear', order:order, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
	}
	setTimeout( refreshCB(), 1000 );
};


// 食品上ボタンを押してなま板リストを更新してL1に表示
var upper_BWL1 = function( order, code ){
	$.post( "cboard.cgi", { command:'upper', order:order, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
};


// まな板の食品下ボタンを押してL1にリストを更新
var lower_BWL1 = function( order, code ){
	$.post( "cboard.cgi", { command:'lower', order:order, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
};


// Changing dish number
var dishCB = function( code ){
	var dish_num = document.getElementById( "dish_num" ).value;
	$.post( "cboard.cgi", { command:'dish', code:code, dish_num:dish_num }, function( data ){ $( "#bw_level1" ).html( data );});
};


// Adjusting total food weight
var weightAdj = function( code ){
	var weight_adj = document.getElementById( "weight_adj" ).value;
	$.post( "cboard.cgi", { command:'wadj', code:code, weight_adj:weight_adj }, function( data ){ $( "#bw_level1" ).html( data );});
	displayVideo( 'Adjusted by weight' );
};


// Adjusting total food energy
var energyAdj = function( code ){
	var energy_adj = document.getElementById( "energy_adj" ).value;
	$.post( "cboard.cgi", { command:'eadj', code:code, energy_adj:energy_adj }, function( data ){ $( "#bw_level1" ).html( data );});
		displayVideo( 'Adjusted by energy' );
};


// Adjusting feeding rate by food loss
var lossAdj = function( code ){
	var loss_adj = document.getElementById( "loss_adj" ).value;
	$.post( "cboard.cgi", { command:'ladj', code:code, loss_adj:loss_adj }, function( data ){ $( "#bw_level1" ).html( data );});
		displayVideo( 'Adjusted by loss' );
};


// まな板の食品番号追加ボタンを押して食品を追加してL1にリストを表示。そしてカウンターも更新
var recipeAdd_BWL1 = function( code ){
	var fn = document.getElementById( "food_add" ).value;
	$.post( "cboard.cgi", { command:'add', option1:fn, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
	setTimeout( refreshCB(), 1000 );
};


// まな板の調味％ボタンを押してプリセット食品を追加してL1にリストを表示。そしてカウンターも更新
var seasoningAdd_BWL1 = function( code ){
	var seasoning = document.getElementById( "seasoning" ).value;
	$.post( "cboard.cgi", { command:'seasoning', seasoning:seasoning, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
	setTimeout( refreshCB(), 1000 );
};


// まな板の重量情報更新でL1にリストを更新
var weightCB_BWL1 = function( order, unitv_id, unit_id, food_init_id, food_rr_id, code ){
	var unitv = document.getElementById( unitv_id ).value;
	var unit = document.getElementById( unit_id ).value;
	var food_init = document.getElementById( food_init_id ).value;
	var food_rr = document.getElementById( food_rr_id ).value;

	$.post( "cboard.cgi", { command:'weight', order:order, option2:unitv, option3:unit, code:code, food_init:food_init, food_rr:food_rr }, function( data ){ $( "#bw_level1" ).html( data );});
};


// まな板の初期状態更新で裏で更新
var initCB_SS = function( order, unitv_id, unit_id, food_init_id, food_rr_id, code ){
	var unitv = document.getElementById( unitv_id ).value;
	var unit = document.getElementById( unit_id ).value;
	var food_init = document.getElementById( food_init_id ).value;
	var food_rr = document.getElementById( food_rr_id ).value;

	$.post( "cboard.cgi", { command:'weight', order:order, option2:unitv, option3:unit, code:code, food_init:food_init, food_rr:food_rr }, function( data ){});
};


// まな板の食品チェックボックスを押してL1にリストを更新
var checkCB = function( order, code, check_id ){
	if( document.getElementById( check_id ).checked ){
		var checked = 1;
	} else{
		var checked = 0;
	}
	$.post( "cboard.cgi", { command:'check_box', order:order, option2:checked, code:code }, function( data ){});
};


// Switching all check box
var allSwitch = function( code ){
	if( document.getElementById( 'switch_all' ).checked ){
		var allSwitch = 1;
	} else{
		var allSwitch = 0;
	}
	$.post( "cboard.cgi", { command:'allSwitch', code:code, allSwitch:allSwitch }, function( data ){ $( "#bw_level1" ).html( data );});
};


// Quick Save
var quickSave = function( code ){
	$.post( "cboard.cgi", { command:'quick_save', code:code }, function( data ){ $( "#bw_level1" ).html( data );});
	displayVideo( 'Saved' );
};


// GN Exchange
var gnExchange = function( code ){
	if( document.getElementById( 'gn_check' ).checked ){
		$.post( "cboard.cgi", { command:'gn_exchange', code:code }, function( data ){ $( "#bw_level1" ).html( data );});
		displayVideo( 'Adjusted' );
	} else{
		displayVideo( 'Check!!(>_<)' );
	}
};


// まな板からでL5閲覧ウインドウを表示する。
var cb_summonBWL5 = function( key, weight, base_fn ){
	closeBroseWindows( 1 );
	$.get( "square.cgi", { channel:"fctb_l5", food_key:key, frct_mode:0, food_weight:weight, base:'cb', base_fn:base_fn }, function( data ){ $( "#bw_level5" ).html( data );});
	document.getElementById( "bw_level5" ).style.display = 'block';
	bw_level = 5;
};



////////////////////////////////////////////////////////////////////////////////
// Recipe ////////////////////////////////////////////////////////////////////////

// レシピ編集のレシピボタンを押してL2にレシピを表示
var recipeEdit_BWL2 = function( com, code ){
	closeBroseWindows( 2 );
	$.post( "recipe.cgi", { command:com, code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
	$.post( "photo.cgi", { command:'form', code:code }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';

	bw_level = 2;
};


// レシピ編集の保存ボタンを押してレシピを保存、そしてL2にリストを再表示
var recipeSave_BWL2 = function( code ){
	var recipe_name = document.getElementById( "recipe_name" ).value;
	if( recipe_name == '' ){
		displayVideo( 'レシピ名が必要' );
	}
	else{
		var type = document.getElementById( "type" ).value;
		var role = document.getElementById( "role" ).value;
		var tech = document.getElementById( "tech" ).value;
		var time = document.getElementById( "time" ).value;
		var cost = document.getElementById( "cost" ).value;
		var protocol = document.getElementById( "protocol" ).value;

		if( document.getElementById( "public" ).checked ){ var public = 1 }
		if( document.getElementById( "protect" ).checked ){ var protect = 1 }
		if( document.getElementById( "draft" ).checked ){ var draft = 1 }

		$.post( "recipe.cgi", { command:'save', code:code, recipe_name:recipe_name, type:type, role:role, tech:tech, time:time, cost:cost, protocol:protocol, public:public, protect:protect, draft:draft }, function( data ){ $( "#bw_level2" ).html( data );});
		displayVideo( 'レシピを保存' );

		var fx = function(){
			$.post( "cboard.cgi", { command:'init', code:code }, function( data ){ $( '#bw_level1' ).html( data );});
			$.post( "photo.cgi", { command:'form', code:'' }, function( data ){ $( "#bw_level3" ).html( data );});
		};
		setTimeout( fx , 1000 );
	}
};


// レシピ編集の写真をアップロードして保存、そしてL3に写真を再表示
var photoSave_BWL3 = function( slot, code ){
	$form = $( '#photo_form' );
	form_data = new FormData( $form[0] );
	form_data.append( 'command', 'upload' );
	form_data.append( 'code', code );
	form_data.append( 'slot', slot );
	displayVideo( '写真を送信' );

	$.ajax( "photo.cgi",
		{
			type: 'post',
			processData: false,
			contentType: false,
			data: form_data,
			dataype: 'html',
			success: function( data ){ displayVideo( '写真を保存' ); }
//			success: function( data ){ $( '#bw_level4' ).html( data ); }
		}
	);
//		document.getElementById( "bw_level4" ).style.display = 'block';

	$.post( 'photo.cgi', { command:'form', code:code, slot:'photo0' }, function( data ){ $( '#bw_level3' ).html( data );});
};


// レシピ編集の公開ボタンを押して
var recipeBit_public = function(){
	if( document.getElementById( "public" ).checked ){
		document.getElementById( "protect" ).checked = true;
		document.getElementById( "draft" ).checked = false;
	}
};

// レシピ編集の保護ボタンを押して
var recipeBit_protect = function(){
	if( document.getElementById( "protect" ).checked ){
		document.getElementById( "draft" ).checked = false;
	}
};

// レシピ編集の仮組ボタンを押して
var recipeBit_draft = function(){
	if( document.getElementById( "draft" ).checked ){
		document.getElementById( "protect" ).checked = false;
		document.getElementById( "public" ).checked = false;
	}
};


// レシピ編集の写真を削除、そしてL3にリストを再表示
var photoDel_BWL2 = function( slot, code ){
	$.post( "photo.cgi", { command:'delete', code:code, slot:slot }, function( data ){ displayVideo( '写真を削除' );});
//	$.post( "photo.cgi", { command:'delete', code:code, slot:slot }, function( data ){ $( '#bw_level3' ).html( data );});
	var fx = function(){
		$.post( 'photo.cgi', { command:'form', code:code }, function( data ){ $( '#bw_level3' ).html( data );});
	};
	setTimeout( fx, 1000 );
};


////////////////////////////////////////////////////////////////////////////////////
// Recipe list ////////////////////////////////////////////////////////////////////////

// Dosplaying recipe list with reset
var recipeList = function( com ){
	closeBroseWindows( 1 );
	$.post( "recipel.cgi", { command:com }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
	bw_level1 = 1;
};


// Refreshing list
var fxRLR = function( range, type, role, tech, time, cost, page ){
	$.post( "recipel.cgi", { command:'limit', range:range, type:type, role:role, tech:tech, time:time, cost:cost, page:page }, function( data ){ $( "#bw_level1" ).html( data );});
};


// Dosplaying recipe list with narrow down
var recipeList2 = function( page ){
	var range = document.getElementById( "range" ).value;
	var type = document.getElementById( "type" ).value;
	var role = document.getElementById( "role" ).value;
	var tech = document.getElementById( "tech" ).value;
	var time = document.getElementById( "time" ).value;
	var cost = document.getElementById( "cost" ).value;
	fxRLR( range, type, role, tech, time, cost, page )
};


// Dosplaying recipe list after delete
var recipeDelete = function( code, page ){
	var range = document.getElementById( "range" ).value;
	var type = document.getElementById( "type" ).value;
	var role = document.getElementById( "role" ).value;
	var tech = document.getElementById( "tech" ).value;
	var time = document.getElementById( "time" ).value;
	var cost = document.getElementById( "cost" ).value;

	if( document.getElementById( code ).checked ){
		$.post( "recipel.cgi", { command:'delete', code:code }, function( data ){});
		displayVideo( 'Removed' );
		setTimeout( fxRLR( range, type, role, tech, time, cost, page ), 1000 );
	} else{
		displayVideo( '(>_<) Check!' );
	}
};


// Importing public recipe & Generationg subSpecies
var recipeImport = function( com, code, page ){
	var range = document.getElementById( "range" ).value;
	var type = document.getElementById( "type" ).value;
	var role = document.getElementById( "role" ).value;
	var tech = document.getElementById( "tech" ).value;
	var time = document.getElementById( "time" ).value;
	var cost = document.getElementById( "cost" ).value;

	$.post( "recipel.cgi", { command:com, code:code }, function( data ){});
	displayVideo( '+recipe' );
	setTimeout( fxRLR( range, type, role, tech, time, cost, page ), 1000 );
};


///////////////////////////////////////////////////////////////////////////////////
// 成分計算 ////////////////////////////////////////////////////////////////////////

// まな板の成分計算表ボタンを押してL2にリストを表示
var calcView_BWL2 = function( code ){
	closeBroseWindows( 2 );
	$.post( "calc.cgi", { command:'view', code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	bw_level1 = 2;
};

// 成分計算表の再計算ボタンを押してL2にリストを表示
var recalcView = function( code ){
	var palette = document.getElementById( "palette" ).value;
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( "calc.cgi", { command:'view', code:code, palette:palette, frct_mode:frct_mode, frct_accu:frct_accu, ew_mode:ew_mode }, function( data ){ $( "#bw_level2" ).html( data );});
	displayVideo( 'Recalc' );
};


///////////////////////////////////////////////////////////////////////////////////
// 原価計算 ////////////////////////////////////////////////////////////////////////

// まな板の原価計算表ボタンを押してL2にリストを表示
var priceView_BWL2 = function( code ){
	closeBroseWindows( 2 );
	$.post( "price.cgi", { command:'view', code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	bw_level1 = 2;
};

// 原価計算表の購入量変更でL2に原価表を更新
var changeFV_BWL2 = function( code, fvid, food_no ){
	var food_volume = document.getElementById( fvid ).value;
	$.post( "price.cgi", { command:'changeFV', code:code, food_volume:food_volume, food_no:food_no }, function( data ){ $( "#bw_level2" ).html( data );});
};

// 原価計算表の支払金額変更でL2に原価表を更新
var changeFP_BWL2 = function( code, fpid, food_no ){
	var food_price = document.getElementById( fpid ).value;
	$.post( "price.cgi", { command:'changeFP', code:code, food_price:food_price, food_no:food_no }, function( data ){ $( "#bw_level2" ).html( data );});
};

// 原価計算表のマスター価格を適用してL2に原価表を更新
var pricemAdpt_BWL2 = function( code ){
	$.post( "price.cgi", { command:'adpt_master', code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	displayVideo( 'マスター価格を適用' );
};

// 原価計算表のマスター価格登録（でL2に原価表を更新）
var pricemReg_BWL2 = function( code ){
//	$.post( "price.cgi", { command:'reg_master', code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	$.post( "price.cgi", { command:'reg_master', code:code }, function( data ){});
	displayVideo( 'マスター価格に登録' );
};

// 原価計算表の価格を元にレシピの価格区分を変更
var recipeRef_BWL2 = function( code ){
//	$.post( "price.cgi", { command:'ref_recipe', code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	$.post( "price.cgi", { command:'ref_recipe', code:code }, function( data ){});
	displayVideo( '価格区分へ反映' );
};

// 原価計算表の初期化ボタンでL2に原価表を更新
var clearCT_BWL2 = function( code ){
	if( document.getElementById( "clearCT_check" ).checked ){
		$.post( "price.cgi", { command:'clearCT', code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	}else{
		displayVideo( '(>_<) check!' );
	}
};

///////////////////////////////////////////////////////////////////////////////////
// Lucky star input ////////////////////////////////////////////////////////////////////////

// Lucky☆入力ボタンを押してL2に入力画面を表示、そしてL1を非表示にする
var luckyInput_BWL2 = function(){
	closeBroseWindows( 2 );
	$.post( "lucky.cgi", { command:'form' }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'none';
	document.getElementById( "bw_level2" ).style.display = 'block';

	bw_level1 = 2;
};

// Lucky☆転送ボタンを押してL2に確認画面を表示
var luckyAnalyze_BWL2 = function( mode ){
	var lucky_data = document.getElementById( 'lucky_data' ).value;
//	$.post( "lucky.cgi", { command:'analyze', mode:mode, lucky_data:lucky_data }, function( data ){});
	document.getElementById( "bw_level2" ).style.display = 'block';
	$.post( "lucky.cgi", { command:'analyze', mode:mode, lucky_data:lucky_data }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';

	var fx = function(){
		$.post( "cboard.cgi", { command:'init', code:'' }, function( data ){ $( '#bw_level1' ).html( data );});
		refreshCB();
	};
	setTimeout( fx , 1000 );
	displayVideo( 'Lucky?' );
};

///////////////////////////////////////////////////////////////////////////////////
// Foodize ////////////////////////////////////////////////////////////////////////

// 成分計算表の食品化ボタンを押してL3に擬似食品フォームを表示
var Pseudo_R2F_BWL3 = function( code ){
	closeBroseWindows( 3 );
	$.post( "pseudo_r2f.cgi", { command:'form', code:code }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
	bw_level1 = 3;
};

// 食品化フォームの保存ボタンを押して保存してL3を消す。
var Pseudo_R2F_BWLX = function( code ){
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

		$.post( "pseudo_r2f.cgi", {
			command:'save', code:code, frct_mode:0, frct_accu:1, ew_mode:0,
			food_name:food_name, food_group:food_group, class1:class1, class2:class2, class3:class3, tag1:tag1,
			tag2:tag2, tag3:tag3, tag4:tag4, tag5:tag5
//		}, function( data ){});
		}, function( data ){$( "#bw_level3" ).html( data );});
		document.getElementById( "bw_level3" ).style.display = 'block';

		closeBroseWindows( 3 );
		bw_level1 = 3;
		displayVideo( 'Foodized' );
	}else{
		displayVideo( '(>_<) Food name!' );
	}
};

///////////////////////////////////////////////////////////////////////////////////
// 印刷用清書レシピ /////////////////////////////////////////////////////////////////

// レシピ帳の印刷ボタンを押してL2に印刷画面テンプレートを表示
var print_templateSelect = function( code ){
	$.post( "print.cgi", { command:'select', code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'none';
	document.getElementById( "bw_level2" ).style.display = 'block';
};

// 印刷テンプレート画面の戻るボタンを押してレシピ帳に復帰
var print_templateReturen_BWL2 = function(){
	document.getElementById( "bw_level1" ).style.display = 'block';
	document.getElementById( "bw_level2" ).style.display = 'none';
};

// 印刷テンプレート画面の印刷表示ボタンを押して新規タブに印刷画面を表示する。
var openPrint = function( uname, code, template ){
	var dish = document.getElementById( "dish" ).value;
	var palette = document.getElementById( "palette" ).value;
	var frct_mode = document.getElementById( "frct_mode" ).value;

	if(  document.getElementById( "frct_accu" ).checked ){
		var frct_accu = 1;
	}else{
		var frct_accu = 0;
	}

	if( document.getElementById( "ew_mode" ).checked ){
		var ew_mode = 1;
	}else{
		var ew_mode = 0;
	}

	if( document.getElementById( "hr_image" ).checked ){
		var hr_image = 1;
	}else{
		var hr_image = 0;
	}

	var url = 'printv.cgi?&c=' + code + '&t=' + template + '&d=' + dish + '&p=' + palette + '&fa=' + frct_accu + '&ew=' + ew_mode + '&fm=' + frct_mode + '&hr=' + hr_image;

	window.open( url, 'print' );
	displayVideo( 'Printing page' );
};
