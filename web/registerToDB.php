<?php
	$hash = md5(rand(0,1000));
	require 'db_connection.php';

	$userAcc = trim($_POST["Username"]);
	$userPwd = trim($_POST["Password"]);
	$Email = trim($_POST["Email"]);

	$conn->query("INSERT INTO user (account, password, email, hash) VALUES(
				'". $userAcc ."',
				'". $userPwd ."',
				'". $Email ."',
				'". $hash ."') ");
	header('Location: index.php');
?>