<?php

/*
日期: 2017/08/05
作者: Mikey
說明: 資料庫連線設定
用法: 
*/


$hostname ="localhost";
$database ="bd_captcha";
$username ="mikey";
$password ="2gjixdjl3155";
try{
    $conn = new PDO('mysql:host='.$hostname.';dbname='.$database.';charset=utf8', $username, $password);
} catch(PDOException $ex) {
    echo $ex;
}

?>