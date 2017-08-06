<?php session_start(); ?>
<?php
	$userAcc = trim($_POST["account"]);
	$userPwd = trim($_POST["password"]);

	require 'db_connection.php';
	// 比對其帳號與密碼
	$sql = "SELECT * FROM user WHERE account = '".$userAcc."' AND password = '".$userPwd."' ";
	$result = $conn->query($sql);

	$row = $result->fetch(PDO::FETCH_ASSOC);

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