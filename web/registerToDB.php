<?php
	$hash = md5(rand(0,1000));
	$database = mysql_connect( "140.138.152.207","blazing93", "meteor95188" );
	if ( !mysql_select_db( "house", $database ) )
	   die( "Could not open database!" );

	$userAcc = trim($_POST["Username"]);
	$userPwd = trim($_POST["Password"]);
	$Email = trim($_POST["Email"]);

	mysql_query("INSERT INTO db_captcha_user (account, password, email, hash) VALUES(
				'". mysql_escape_string($userAcc) ."',
				'". mysql_escape_string($userPwd) ."',
				'". mysql_escape_string($Email) ."',
				'". mysql_escape_string($hash) ."') ") or die(mysql_error());
	header('Location: index.php');
?>