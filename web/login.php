<?php session_start(); ?>
<!DOCTYPE HTML>
<html>
	<head>
		<title>Captcha Analysis</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="assets_login/css/index.css" />
		<!-- Scripts -->
		<script src="assets_login/js/main.js"></script>
		<script type="text/javascript" src="assets_login/js/jquery-1.8.2.min.js"></script>
	</head>
	<body>
		<script>
	
	    /* login submit */
	    function submitForm()
	    {  
			var data = $("#login-form").serialize();

			$.ajax({

				type : 'POST',
				url  : 'loginCheck.php',
				data : data,
				success : function(response)
				{      
					if(response == "success"){
						alert("Login succeed!");
						location.href = 'index.php';
					}
					else if(response == "fail")
						alert("Login failed!");
				},

				error : function(xhr, ajaxOptions, thrownError){ 
                    alert(xhr.status); 
                    alert(thrownError); 
                }
	   		});
	    	return false;
	  	}
	    /* login submit */
		</script>
		<!-- Header -->
		<header id="header" style="font-family:微軟正黑體;">
			<h1>Captcha Analysis - API</h1>
			<p>登入</p>
		</header>

		<!-- Login Form -->
		<form id="login-form" method="post">
            <input type="text" class="text" placeholder="帳號" name="account"/><br/>
			<input type="password" placeholder="密碼" name="password"/>
			<input type="button" value="LOGIN" onClick="submitForm()"/>
			<input type="button" value="SIGN UP" onclick="location.href='signUp.html'">
			<a href="#">Forgot Password ?</a>
		</form>

		
	</body>
</html>