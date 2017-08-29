<?php

/*
日期: 2017/08/05
作者: Mikey
說明: 資料庫連線設定
用法: 
*/


$hostname ="140.138.152.207";
$database ="bd_captcha";
$username ="frank85";
$password ="ak800730";
try{
    $conn = new PDO('mysql:host='.$hostname.';dbname='.$database.';charset=utf8', $username, $password);
} catch(PDOException $ex) {
    echo $ex;
}

?>