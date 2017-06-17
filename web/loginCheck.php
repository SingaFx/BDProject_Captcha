<?php session_start(); ?>
<?php
	$userAcc = trim($_POST["account"]);
	$userPwd = trim($_POST["password"]);

	$database = mysql_connect( "140.138.152.207","blazing93", "meteor95188" );
	if ( !mysql_select_db( "house", $database ) )
	   die( "Could not open database!" );
	// 比對其帳號與密碼
	$sql = "SELECT * FROM db_captcha_user WHERE account = '".mysql_real_escape_string($userAcc)."' AND password = '".mysql_real_escape_string($userPwd)."' ";
	$result = mysql_query( $sql, $database );

	$row = mysql_fetch_row($result);

	// 依檢查結果分別導向主作業畫面與錯誤警告畫面
	if ($row != null && $userAcc != null && $userPwd != null) {
		$_SESSION["account"] = $userAcc;
		echo 'success';
		//header("location:index.php");
		exit;
	}
	else{
		echo 'fail';
	}
?>