/////////////////////////////////////////////////////////////////////////////////
// カレンダーの変更 //////////////////////////////////////////////////////////////

// こよみボタンを押したときにL1閲覧ウインドウの内容を書き換える
var initKoyomi = function(){
	closeBroseWindows( 1 );
	$.post( "koyomi.cgi", { command:"init" }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
};

