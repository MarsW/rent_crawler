<?php
	$id = $_POST['id'];
	$value = $_POST['value'];
	//$fp1 = fopen("./test.txt", 'w');
	//fwrite($fp1, print_r($id, TRUE));
	//fclose($fp1);

	//將$_POST['id']用explode函式拆解為$field和$id兩個變數
	list($field, $id) = explode('-', $id);

	//mysql query
	$username="";
	$password="";
	$database="";
	$ip="";

	$connection=mysql_connect ($ip, $username, $password) or die("Not connected : " . mysql_error());
	$db_selected = mysql_select_db($database, $connection) or die("Can\'t use db : " . mysql_error());
	mysql_query("SET NAMES utf8");
	mysql_query("UPDATE `rent` SET $field='$value' WHERE sn='$id'");
	
	//將值傳回前端
	echo $value;

?>