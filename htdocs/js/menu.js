/////////////////////////////////////////////////////////////////////////////////
// Set menu ////////////////////////////////////////////////////////////////////////

// 献立追加ボタンを押してmealにレシピを追加して、まな献立カウンタを増やす
var addingMeal = function( recipe_code ){
	$.post( "mealm.cgi", { recipe_code:recipe_code }, function( data ){ $( "#mb_num" ).html( data );});
	if( recipe_code != '' ){ displayVideo( recipe_code + 'を追加' ); }
};


// 献立ボタンを押してL1にリストを表示
var initMeal_BWL1 = function( com, code ){
	closeBroseWindows( 1 );
	$.post( "meal.cgi", { command:com, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';

	var fx = function(){
		addingMeal( '' );
	};
	setTimeout( fx, 1000 );

	bw_level1_status = 'block';
	bw_level2_status = 'none';
	bw_level3_status = 'none';
	bw_level4_status = 'none';
	bw_level5_status = 'none';
};

// 献立クリアボタンを押してL1にリストを更新、そしてまな献立カウンターの更新
var clear_meal = function( order, code ){
	if( order == 'all'){
		if( document.getElementById( 'meal_all_check' ).checked ){
			$.post( "meal.cgi", { command:'clear', order:'all', code:code }, function( data ){ $( "#bw_level1" ).html( data );});
			displayVideo( '献立を初期化' );
			closeBroseWindows( 1 );
		} else{
			displayVideo( 'Check! (>_<)' );
		}
	} else{
		$.post( "meal.cgi", { command:'clear', order:order, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
	}
	var fx = function(){
		addingMeal( '' );
	};
	setTimeout( fx, 1000 );
};


// 献立上ボタンを押してL1に献立リストを更新
var upper_meal = function( order, code ){
	$.post( "meal.cgi", { command:'upper', order:order, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
};


// 献立下ボタンを押してL1に献立リストを更新
var lower_meal = function( order, code ){
	$.post( "meal.cgi", { command:'lower', order:order, code:code }, function( data ){ $( "#bw_level1" ).html( data );});
};

////////////////////////////////////////////////////////////////////////////////
// セットメニュー ////////////////////////////////////////////////////////////////////////

// 献立編集のレシピボタンを押してL2にレシピを表示
var menuEdit = function( com, code ){
	closeBroseWindows( 2 );
	$.post( "menu.cgi", { command:com, code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
	$.post( "menu-photo.cgi", { command:'form', code:code }, function( data ){ $( "#bw_level3" ).html( data );});
	document.getElementById( "bw_level3" ).style.display = 'block';
};


// メニュー編集の保存ボタンを押してレシピを保存、そしてL2にリストを再表示
var menuSave = function( code ){
	var menu_name = document.getElementById( "menu_name" ).value;
	if( menu_name == '' ){
		displayVideo( '献立名が必要' );
	}
	else{
		if( document.getElementById( "public" ).checked ){ var public = 1 }
		if( document.getElementById( "protect" ).checked ){ var protect = 1 }
		var label = document.getElementById( "label" ).value;
		var new_label = document.getElementById( "new_label" ).value;

		$.post( "menu.cgi", { command:'save', code:code, menu_name:menu_name, public:public, protect:protect, label:label, new_label:new_label }, function( data ){ $( "#bw_level2" ).html( data );});
		displayVideo( menu_name + 'を保存' );
		var fx = function(){
			$.post( "meal.cgi", { command:'init', code:code }, function( data ){ $( '#bw_level1' ).html( data );});
			$.post( "menu-photo.cgi", { command:'form', code:code }, function( data ){ $( "#bw_level3" ).html( data );});
		};
		setTimeout( fx , 1000 );
	}
};


// メニュー編集の写真をアップロードして保存、そしてL2にリストを再表示
var menu_photoSave = function( code ){
	$form = $( '#photo_form' );
	form_data = new FormData( $form[0] );
	form_data.append( 'command', 'upload' );
	form_data.append( 'code', code );
	form_data.append( 'slot', 'photo' );

//	document.getElementById( "bw_level3" ).style.display = 'block';

	$.ajax( "menu-photo.cgi",
		{
			type: 'post',
			processData: false,
			contentType: false,
			data: form_data,
			dataype: 'html',
			success: function( data ){ displayVideo( '写真を保存' ); }
//			success: function( data ){ $( '#bw_level3' ).html( data );}
		}
	);
	//		document.getElementById( "bw_level3" ).style.display = 'block';

	$.post( 'menu-photo.cgi', { command:'form', code:code }, function( data ){ $( '#bw_level3' ).html( data );});
};


// Deleting photo of set menu
var menu_photoDel = function( code ){
	$.post( "menu-photo.cgi", { command:'delete', code:code, slot:'photo' }, function( data ){ displayVideo( 'Deleted' );});
	var fx = function(){
		$.post( 'menu-photo.cgi', { command:'view', code:code }, function( data ){ $( '#bw_level2' ).html( data );});
	};
	setTimeout( fx, 1000 );
};


////////////////////////////////////////////////////////////////////////////////////
// Set menu list ////////////////////////////////////////////////////////////////////////

// まな板のレシピ読み込みボタンを押してL1に献立リストを表示
var menuList = function( page ){
	closeBroseWindows( 1 );
	$.post( "menul.cgi", { command:'view', page:page }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';

	bw_level1_status = 'block';
	bw_level2_status = 'none';
};


// まな板のレシピ読み込みボタンを押してL1に献立リストを表示
var menuList2 = function( page ){
	var range = document.getElementById( "range" ).value;
	var label = document.getElementById( "label" ).value;

	$.post( "menul.cgi", { command:'view2', page:page, range:range, label:label }, function( data ){ $( "#bw_level1" ).html( data );});
};


// まな板の削除ボタンを押してレシピを削除し、L1にリストを再表示
var menuDelete = function( code, menu_name ){
	if( document.getElementById( code ).checked ){
		$.post( "menul.cgi", { command:'delete', code:code }, function( data ){ $( "#bw_level1" ).html( data );});
		displayVideo( menu_name + 'deleted' );
	} else{
		displayVideo( 'Check! (>_<)' );
	}
};


// まな板のインポートボタンを押してレシピをインポートし、L1にリストを再表示
var menuImport = function( code ){
	$.post( "menul.cgi", { command:'import', code:code }, function( data ){ $( "#bw_level1" ).html( data );});
	displayVideo( code + 'imported' );
};


///////////////////////////////////////////////////////////////////////////////////
// 献立の成分計算 ////////////////////////////////////////////////////////////////////////

// 献立の成分計算表ボタンを押してL2にリストを表示
var menuCalcView = function( code ){
	closeBroseWindows( 2 );
	$.post( "menu-calc.cgi", { command:'view', code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	bw_level2_status = 'block';
};

// 献立の成分計算表の再計算ボタンを押してL2にリストを表示
var menuRecalcView = function( code ){
	var palette = document.getElementById( "palette" ).value;
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( "menu-calc.cgi", { command:'view', code:code, palette:palette, frct_mode:frct_mode, frct_accu:frct_accu, ew_mode:ew_mode }, function( data ){ $( "#bw_level2" ).html( data );});
	displayVideo( '再計算' );
};


// 献立の成分計算表の拡張ページボタンを押してメッセージを表示
var menuCalcExpand_NW = function( uname, code ){
	var palette = document.getElementById( "palette" ).value;
	var fraction = document.getElementById( "fraction" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 0; }else{ var frct_accu = 1; }
	url = 'menu-calcex.cgi?uname=' + uname + '&code=' + code + '&frct_mode=' + fraction + '&frct_accu=' + frct_accu + '&palette=' + palette;
	window.open( url, 'calc-ex' );
	displayVideo( '拡張ページ' );
};

///////////////////////////////////////////////////////////////////////////////////
// Analysis of menu ////////////////////////////////////////////////////////////////////////

// Analysis of menu
var menuAnalysis = function( code ){
	closeBroseWindows( 2 );
	$.post( "menu-analysis.cgi", { command:'', code:code }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';

	bw_level2_status = 'block';
};

// Reanalysis of menu
var menuReAnalysis = function( code ){
	var frct_mode = document.getElementById( "frct_mode" ).value;
	if( document.getElementById( "frct_accu" ).checked ){ var frct_accu = 1; }else{ var frct_accu = 0; }
	if( document.getElementById( "ew_mode" ).checked ){ var ew_mode = 1; }else{ var ew_mode = 0; }
	$.post( "menu-analysis.cgi", { command:'', code:code, frct_mode:frct_mode, frct_accu:frct_accu, ew_mode:ew_mode }, function( data ){ $( "#bw_level2" ).html( data );});
	displayVideo( 'Reanalysis' );
};
