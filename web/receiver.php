<?php
 	// header('Access-Control-Allow-Origin: *');
	error_reporting(E_ALL || ~E_NOTICE);
	$datetime= date("YmdHis");
	$random = rand();
	$filepath = $datetime."_".$random;

	
	// 取得上傳圖片
	if($_FILES["file"]["error"] > 0){
		echo "Error: ".$_FILES["file"]["error"];
	}else{
		if(!is_file($_SERVER['HTTP_HOST']."/upload/".$filepath))
			mkdir("upload/".$filepath);
		move_uploaded_file($_FILES["file"]["tmp_name"],"upload/".$datetime."_".$random."/src.jpg");
		//echo("<meta http-equiv=refresh content=0;url=index.html>");
		echo $datetime."_".$random;
	}
	
	if($_FILES["1_bright"]["error"] > 0){
		echo "Error: ".$_FILES["1_bright"]["error"];
	}else{
		$path = $_POST['path'];
		if($path){
			move_uploaded_file($_FILES["1_bright"]["tmp_name"],"upload/".$path."/1_bright.jpg");
			//echo("<meta http-equiv=refresh content=0;url=index.html>");
			//echo $_SERVER['HTTP_HOST']."/upload/".$path."/1_bright.jpg";
		}
	}

	if($_FILES["1_black"]["error"] > 0){
		echo "Error: ".$_FILES["1_black"]["error"];
	}else{
		$path = $_POST['path'];
		if($path){
			move_uploaded_file($_FILES["1_black"]["tmp_name"],"upload/".$path."/1_black.jpg");
			//echo("<meta http-equiv=refresh content=0;url=index.html>");
			//echo $_SERVER['HTTP_HOST']."/upload/".$path."/1_black.jpg";
		}
	}

	if($_FILES["2_canny"]["error"] > 0){
		echo "Error: ".$_FILES["2_canny"]["error"];
	}else{
		$path = $_POST['path'];
		if($path){
			move_uploaded_file($_FILES["2_canny"]["tmp_name"],"upload/".$path."/2_canny.jpg");
			//echo("<meta http-equiv=refresh content=0;url=index.html>");
			//echo $_SERVER['HTTP_HOST']."/upload/".$path."/2_canny.jpg";
		}
	}
?>