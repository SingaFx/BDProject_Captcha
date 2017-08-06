<?php session_start(); ?>
<?php
    if (!$_SESSION) {
        header("location:login.php");
        exit;
    }
?>
<!DOCTYPE HTML>
<!--
    Road Trip by TEMPLATED
    templated.co @templatedco
    Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
-->
<html>
    <head>
        <title>Big Data Project</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" href="assets/css/main.css" />
    <!-- Scripts -->
        <script src="assets/js/jquery.min.js"></script>
        <script src="assets/js/jquery.scrolly.min.js"></script>
        <script src="assets/js/jquery.scrollex.min.js"></script>
        <script src="assets/js/skel.min.js"></script>
        <script src="assets/js/util.js"></script>
        <script src="assets/js/main.js"></script>
    </head>
    <body class="subpage">
        <script>
    
        /* generate api key */
        function generateKey()
        {  
            $.ajax({

                type : 'POST',
                url  : 'generateKey.php',
                success : function(response)
                {
                    if(response != ""){
                        $("#api_key").val(response);
                    }
                },

                error : function(xhr, ajaxOptions, thrownError){ 
                    alert(xhr.status); 
                    alert(thrownError); 
                }
            });
            return false;
        }
        /* generate api key */
        </script>

        <!-- Header -->
            <header id="header" class="alt">
                <div class="logo"><a href="index.php">Big Data Project</a></div>
                <a href="#menu"><span>Menu</span></a>
            </header>

        <!-- Nav -->
            <nav id="menu">
                <ul class="links">
                    <li><a href="index.php">首頁</a></li>
                    <li><a href="api.php">API</a></li>
                    <?php
                    if (!$_SESSION) {
                        echo '<li><a href="login.php">登入</a></li>';
                    }
                    else{
                        echo '<li><a href="logout.php">登出</a></li>';
                    }
                    ?>
                </ul>
            </nav>

        <!-- Main -->
            <div id="main" class="container">
                <h2>API Key</h2>
                <div class="row uniform">
                    <div class="9u 12u$(small)">
                        <?php
                        require 'db_connection.php';

                        $result = $conn->query("SELECT * FROM user WHERE account = '".$_SESSION["account"]."'");
                        $row = $result->fetch(PDO::FETCH_ASSOC);
                        $key = $row['api_key'];
                        if($key != '')
                            echo '<input type="text" name="api_key" id="api_key" value="'.$key.'" placeholder="API" readonly>';
                        else
                            echo '<input type="text" name="api_key" id="api_key" value="" placeholder="API" readonly>';
                        ?>
                        
                    </div>
                    <div class="3u$ 12u$(small)">
                        <input id="generate" type="button" value="Generate" class="fit" onclick="generateKey()">
                    </div>
                </div>
                <hr class="major" />
            <!-- Preformatted Code -->
                <h3>Example</h3>
                <pre><code>
                <?php
                require 'config.php';
                echo $api_url.'1?key='.$key.'&url='.$url.'upload/20170617122555_30997/src.png';
                ?>
                
                </code></pre>
                <hr class="major" />
                <h3>Result</h3>
                <pre><code>
                {
                    "method1": {
                        "googleVision_result": "AETV", 
                        "name": "Our first algorithm", 
                        "tesseract_result": "tETVi"
                    }
                }
                </code></pre>
            </div>
    </body>
</html>