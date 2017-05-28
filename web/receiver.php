<?php
	// 取得上傳圖片
	if($_FILES["file"]["error"] > 0){
		echo "Error: ".$_FILES["file"]["error"];
	}else{
		if(file_exists("upload/".$_FILES["file"]["name"])){
			echo "File Exists.";
		}else{
			move_uploaded_file($_FILES["file"]["tmp_name"],"upload/".$_FILES["file"]["name"]);
			echo("<meta http-equiv=refresh content=0;url=index.html>");
		}
	}
?>