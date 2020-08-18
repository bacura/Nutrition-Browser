/////////////////////////////////////////////////////////////////////////////////
// Cooking school //////////////////////////////////////////////////////////////

//
var initSchool = function(){
	closeBroseWindows( 1 );
	$.post( "school.cgi", { command:"menu" }, function( data ){ $( "#bw_level1" ).html( data );});
	$.post( "school.cgi", { command:"init" }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
	document.getElementById( "bw_level2" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Cooking school Yoyaku //////////////////////////////////////////////////////////////

// Yoyaku Office
var scsYoyakuNew = function( yyyy, mm, dd, ampm ){
	$.post( "yoyaku-office.cgi", { command:"new", yyyy:yyyy, mm:mm, dd:dd, ampm:ampm }, function( data ){ $( "#world_frame" ).html( data );});
};



/////////////////////////////////////////////////////////////////////////////////
// Cooking school menu //////////////////////////////////////////////////////////////

// menu
var initSchoolMenu = function(){
	closeBroseWindows( 1 );
	$.post( "school-menu.cgi", { command:"init" }, function( data ){ $( "#bw_level2" ).html( data );});
	document.getElementById( "bw_level2" ).style.display = 'block';
};


/////////////////////////////////////////////////////////////////////////////////
// Management of account M //////////////////////////////////////////////////////////////

// Account list
var initAccountM = function(){
	closeBroseWindows( 1 );
	$.post( "account-mom.cgi", { command:"init" }, function( data ){ $( "#bw_level1" ).html( data );});
	document.getElementById( "bw_level1" ).style.display = 'block';
};


// New account form
var newAccountM = function(){
	$.post( "account-mom.cgi", { command:"new" }, function( data ){ $( "#bw_level1" ).html( data );});
};


// Save new account
var saveAccountM = function(){
	var uid_d = document.getElementById( 'uid_d' ).value;
	var mail_d = document.getElementById( 'mail_d' ).value;
	var pass_d = document.getElementById( 'pass_d' ).value;
	var aliasu_d = document.getElementById( 'aliasu_d' ).value;
	var language_d = document.getElementById( 'language_d' ).value;
	$.post( "account-mom.cgi", { command:"save", uid_d:uid_d, mail_d:mail_d, pass_d:pass_d, aliasu_d:aliasu_d, language_d:language_d }, function( data ){ $( "#bw_level1" ).html( data );});
};


// Update account
var updateAccountM = function( uid_d ){
	var mail_d = document.getElementById( 'mail_d' ).value;
	var pass_d = document.getElementById( 'pass_d' ).value;
	var aliasu_d = document.getElementById( 'aliasu_d' ).value;
	var language_d = document.getElementById( 'language_d' ).value;
	$.post( "account-mom.cgi", { command:"update", uid_d:uid_d, mail_d:mail_d, pass_d:pass_d, aliasu_d:aliasu_d, language_d:language_d }, function( data ){ $( "#bw_level1" ).html( data );});
};


// Edit account
var editAccountM = function( uid_d ){
	$.post( "account-mom.cgi", { command:"edit", uid_d:uid_d }, function( data ){ $( "#bw_level1" ).html( data );});
};


// Delete account
var deleteAccountM = function( uid_d ){
	if(document.getElementById( "delete_checkM" ).checked){
		$.post( "account-mom.cgi", { command:"delete", uid_d:uid_d }, function( data ){ $( "#bw_level1" ).html( data );});
	}else{
		displayVideo( 'Check! (>_<)' );
	}
};


// Switch account
var switchAccountM = function( switch_id, uid_d ){
	if(document.getElementById( switch_id ).checked){ var switch_d = 1; }else{ var switch_d = 0; }
	$.post( "account-mom.cgi", { command:"switch", uid_d:uid_d, switch_d:switch_d }, function( data ){});
};
