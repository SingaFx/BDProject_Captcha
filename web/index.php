<?php session_start(); ?>
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
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.min.js"></script>
		<link rel="stylesheet" href="assets/css/main.css" />
        <link rel=stylesheet type="text/css" href="assets/css/BDProject.css">
		<script src="https://code.highcharts.com/highcharts.js"></script>
		<script src="https://code.highcharts.com/modules/data.js"></script>
		<script src="https://code.highcharts.com/modules/drilldown.js"></script>
	</head>
    <style>
    </style>
	<body>
	<!-- Header -->
		<header id="header">
            <div class="logo">
                <a href="index.php">Big Data Project</a>
            </div>
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

	<!-- Banner -->
	<!--
		Note: To show a background image, set the "data-bg" attribute below
		to the full filename of your image. This is used in each section to set
		the background image.
	-->
		<section id="banner" class="bg-img" data-bg="banner.jpg">
			<div class="inner">
				<header>
					<h1>This is an Analysis for Captcha</h1>
				</header>
			</div>
			<a href="#one" class="more">Learn More</a>
		</section>
        <!--Upload Image-->
        <section id="one" class="wrapper post bg-img" data-bg="banner6.jpg">
            <div class="inner">
                <article class="box">
                    <header>
                        <h4>Please Upload Your Captcha</h4>
                    </header>
                    <!--
                    <form method="post" enctype="multipart/form-data" action="receiver.php">
                       
                        <br>
                        <img id="previewFile" height="100" width="200"/>
                        </br>
                        <a href="javascript:;" class="file">選擇檔案
                            <input type="file" name="file" id="file" accept="image/*" onchange="loadFile(event)">
                        </a>
                        <a href="javascript:;" class="file">上傳
                            <input type="submit" name="upload" id="">
                        </a>
                     
                    </form>
                    -->
                    
                    <nav role="navigation" class="tabs">
                        <a href="#tab1" style="color:#82CAFA;" class="active animBtn themeD">文字驗證碼</a>
                        <a href="#tab2" style="color:#82CAFA;" class="animBtn themeD">reCAPTCHA</a>
                    </nav>
                    <div class="filecontainer" role="main">
                        <div id="tab1" style="display: block;">
                            <form class="filebox" id="captcha" method="post" action="receiver.php" enctype="multipart/form-data" novalidate class="filebox has-advanced-upload">
                                <br><img id="previewFile" height="100" width="200"/></br>
                                <div class="filebox__input">
                                    <input type="file" name="file" id="file" class="file" data-multiple-caption="{count} files selected" multiple accept="image/*">
                                    <label for="file"><strong>Choose a image</strong><span class=""> or drag it here</span>.</label>
                                    <!--<button class="" type="submit">Upload</button>-->
                                </div>
                                <div id="imageContainer"></div>
                                <div id="resultContainer"></div>
                                <div class="filebox__uploading">Uploading&hellip;</div>
                                <div class="filebox__processing">Processing&hellip;</div>
                                <div class="filebox__success">Done!</div>
                                <div class="filebox__error">Error! <span></span>.</div>
                                <input type="hidden" name="ajax" value="1"></form>
                            </form>
                        </div>

                        <div id="tab2" style="display: none;">

                            <form class="filebox" id="reCaptcha" method="post" action="receiver.php" enctype="multipart/form-data" novalidate class="filebox has-advanced-upload">
                            <div style="margin: 0px auto;">
                                <input class="effect-1" id="keyword" type="text" placeholder="Please input keyword">
                                <span class="focus-border"></span>
                            </div>
                            <br><img id="previewFile2" height="300" width="300"/></br>
                            <div class="filebox__input">
                                <input type="file" name="file" id="file2" class="file" data-multiple-caption="{count} files selected" multiple accept="image/*">
                                <label for="file"><strong>Choose a reCAPTCHA image</strong><span class=""> or drag it here</span>.</label>
                                <!--<button class="" type="submit">Upload</button>-->
                            </div>
                            <div id="imageContainer2"></div>
                            <div id="resultContainer2"></div>
                            <p></p>
                            <p></p>
                            <div class="filebox__uploading">Uploading&hellip;</div>
                            <div class="filebox__processing">Processing&hellip;</div>
                            <div class="filebox__success">Done!</div>
                            <div class="filebox__error">Error! <span></span>.</div>
                            <input type="hidden" name="ajax" value="1"></form>
                            </form>
                        </div>
                    </div>
                   
                </article>
            </div>
        </section>
		<!-- One -->
			<section id="one" class="wrapper post bg-img" data-bg="banner2.jpg">
				<div class="inner">
					<article class="box">
                        <header>
                            <h2>方法一</h2>
                        </header>
						<div class="content">
                            <div id="container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
							<script type="text/javascript">
							Highcharts.chart('container', {
								    chart: {
								        type: 'column'
								    },
								    title: {
								        text: '測試結果(20次)'
								    },
								    xAxis: {
								        categories: [
								            '9乘9購物網',
								            '清大南大校區登入系統',
								            '交大選課系統',
								            '大氣水文資料庫',
								            'OB嚴選',
								            '元智選課系統'
								        ],
								        crosshair: true
								    },
								    yAxis: {
								        min: 0,
								        title: {
								            text: '成功率(%)'
								        }
								    },
								    tooltip: {
								        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
								        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
								            '<td style="padding:0"><a>{point.y} %</a></td></tr>',
								        footerFormat: '</table>',
								        shared: true,
								        useHTML: true
								    },
								    plotOptions: {
								        column: {
								            pointPadding: 0,
								            borderWidth: 0
								        }
								    },
								    series: [{
								        name: 'Tesseract',
								        data: [0, 95, 10, 10, 55, 0]

								    }, {
								        name: 'Vision',
								        data: [0, 90, 30, 65, 100, 75]
								    }]
								});
							</script>
						</div>
					</article>
				</div>
				<a href="#two" class="more">Learn More</a>
			</section>

		<!-- Two -->
			<section id="two" class="wrapper post bg-img" data-bg="banner5.jpg">
				<div class="inner">
					<article class="box">
                        <header>
                            <h2>方法二</h2>
                        </header>
						<div class="content">
							<div id="container2" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
							<script type="text/javascript">
							Highcharts.chart('container2', {
								    chart: {
								        type: 'column'
								    },
								    title: {
								        text: '測試結果(20次)'
								    },
                                    colors: ['#2f7ed8', '#0d233a', '#8bbc21', '#910000', '#1aadce', 
   '#492970', '#f28f43', '#77a1e5', '#c42525', '#a6c96a'],
								    xAxis: {
								        categories: [
								            '9乘9購物網',
								            '清大南大校區登入系統',
								            '交大選課系統',
								            '大氣水文資料庫',
								            'OB嚴選',
								            '元智選課系統'
								        ],
								        crosshair: true
								    },
								    yAxis: {
								        min: 0,
								        title: {
								            text: '成功率(%)'
								        }
								    },
								    tooltip: {
								        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
								        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
								            '<td style="padding:0;"><a>{point.y} %</a></td></tr>',
								        footerFormat: '</table>',
								        shared: true,
								        useHTML: true
								    },
								    plotOptions: {
								        column: {
								            pointPadding: 0,
								            borderWidth: 0
								        }
								    },
								    series: [{
								        name: 'Tesseract',
								        data: [0, 0, 5, 45, 75, 30]

								    }, {
								        name: 'Vision',
								        data: [20, 0, 10, 60, 100, 70]
								    }]
								});
								</script>
						</div>
					</article>
				</div>
				<a href="#three" class="more">Learn More</a>
			</section>

		<!-- Three -->
			<section id="three" class="wrapper post bg-img" data-bg="banner4.jpg">
				<div class="inner">
					<article class="box">
						<header>
							<h2>方法三</h2>
						</header>
						<div class="content">
							<div id="container3" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
							<script type="text/javascript">
							Highcharts.chart('container3', {
								    chart: {
								        type: 'column'
								    },
								    title: {
								        text: '測試結果(20次)'
								    },
								    xAxis: {
								        categories: [
								            '9乘9購物網',
								            '清大南大校區登入系統',
								            '交大選課系統',
								            '大氣水文資料庫',
								            'OB嚴選',
								            '元智選課系統'
								        ],
								        crosshair: true
								    },
								    yAxis: {
								        min: 0,
								        title: {
								            text: '成功率(%)'
								        }
								    },
								    tooltip: {
								        headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
								        pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
								            '<td style="padding:0"><a>{point.y} %</a></td></tr>',
								        footerFormat: '</table>',
								        shared: true,
								        useHTML: true
								    },
								    plotOptions: {
								        column: {
								            pointPadding: 0,
								            borderWidth: 0
								        }
								    },
								    series: [{
								        name: 'Tesseract',
								        data: [5, 0, 0, 0, 0, 0]

								    }, {
								        name: 'Vision',
								        data: [5, 35, 0, 0, 0, 0]
								    }]
								});
							</script>
						</div>
					</article>
				</div>
				<a href="#four" class="more">Learn More</a>
			</section>

		<!-- Four -->
			<section id="four" class="wrapper post bg-img" data-bg="banner3.jpg">
				<div class="inner">
					<article class="box">
						<header>
							<h2>reCAPTCHA</h2>
						</header>
						<div class="content">
							<div id="container4" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
							<script type="text/javascript">
							// Create the chart
								Highcharts.chart('container4', {
								  chart: {
								    type: 'column'
								  },
								  title: {
								    text: '測試結果(20次)'
								  },
								  xAxis: {
								    type: 'category'
								  },
								  yAxis: {
								    title: {
								      text: '成功率(%)'
								    }

								  },
								  legend: {
								    enabled: false
								  },
								  plotOptions: {
								    series: {
								      borderWidth: 0,
								      dataLabels: {
								        enabled: true,
								      }
								    }
								  },

								  tooltip: {
								    headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
								    pointFormat: '<span style="color:{point.color}"></span><a>{point.y}</a>%<br/>'
								  },

								  series: [{
								    name: '成功率',
								    colorByPoint: true,
								    data: [{
								      name: 'Google Vision',
								      y: 0,
								    }, {
								      name: 'Clarifai',
								      y: 25,
								    }]
								}]
							});
							</script>
						</div>
					</article>
				</div>
			</section>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.scrolly.min.js"></script>
			<script src="assets/js/jquery.scrollex.min.js"></script>
			<script src="assets/js/skel.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>
<script>
    var loadFile = function(file, form) {
        if( form.classList.contains( 'is-uploading' ) || form.classList.contains( 'is-processing' ))
        {
            alert("處理中，請勿重複上傳！");
            return false;
        }
        if(form.id == 'captcha')
        {
            id = 'previewFile'
        }
        else if(form.id == 'reCaptcha')
        {
            if($('#keyword').val() == "")
            {
                alert("請輸入reCAPTCHA關鍵字！");
                return false;
            }
            id = 'previewFile2'
        }
        var output = document.getElementById(id);
        output.src = URL.createObjectURL(file);
        return true;
    };
      
</script>
<script>
    'use strict';

    $(window).load(function(){
      $(".col-3 input").val("");
      $(".input-effect input").focusout(function(){
        if($(this).val() != ""){
          $(this).addClass("has-content");
        }else{
        $(this).removeClass("has-content");
        }
      });
    });   

    $(function(){
        // 預設顯示第一個 Tab
        var _showTab = 0;
        var $defaultLi = $('nav.tabs a').eq(_showTab).addClass('active');
        $($defaultLi.find('a').attr('href')).siblings().hide();
        
        // 當 li 頁籤被點擊時...
        // 若要改成滑鼠移到 li 頁籤就切換時, 把 click 改成 mouseover
        $('nav.tabs a').click(function() {
            // 找出 li 中的超連結 href(#id)
            var $this = $(this),
                _clickTab = $this.attr('href');
            // 把目前點擊到的 li 頁籤加上 .active
            // 並把兄弟元素中有 .active 的都移除 class
            $this.addClass('active').siblings('.active').removeClass('active');
            // 淡入相對應的內容並隱藏兄弟元素
            $(_clickTab).stop(false, true).fadeIn().siblings().hide();

            return false;
        }).find('a').focus(function(){
            this.blur();
        });
    });


    ;( function ( document, window, index )
    {
        // feature detection for drag&drop upload
        var isAdvancedUpload = function()
            {
                var div = document.createElement( 'div' );
                return ( ( 'draggable' in div ) || ( 'ondragstart' in div && 'ondrop' in div ) ) && 'FormData' in window && 'FileReader' in window;
            }();


        // applying the effect for every form
        var forms = document.querySelectorAll( '.filebox' );
        Array.prototype.forEach.call( forms, function( form )
        {
            var input        = form.querySelector( 'input[type="file"]' ),
                label        = form.querySelector( 'label' ),
                errorMsg     = form.querySelector( '.filebox__error span' ),
                restart      = form.querySelectorAll( '.filebox__restart' ),
                droppedFiles = false,
                showFiles    = function( files )
                {
                    var isLoad = loadFile(files[0], form);
                    if(isLoad){
                        label.textContent = files.length > 1 ? ( input.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', files.length ) : files[ 0 ].name;
                        return true;
                    }
                    else
                        return false;
                },
                triggerFormSubmit = function()
                {
                    var event = document.createEvent( 'HTMLEvents' );
                    event.initEvent( 'submit', true, false );
                    form.dispatchEvent( event );
                };

            // letting the server side to know we are going to make an Ajax request
            var ajaxFlag = document.createElement( 'input' );
            ajaxFlag.setAttribute( 'type', 'hidden' );
            ajaxFlag.setAttribute( 'name', 'ajax' );
            ajaxFlag.setAttribute( 'value', 1 );
            form.appendChild( ajaxFlag );

            // automatically submit the form on file select
            input.addEventListener( 'change', function( e )
            {
                if(showFiles( e.target.files ))
                    triggerFormSubmit();
            });

            // drag&drop files if the feature is available
            if( isAdvancedUpload )
            {
                form.classList.add( 'has-advanced-upload' ); // letting the CSS part to know drag&drop is supported by the browser

                [ 'drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop' ].forEach( function( event )
                {
                    form.addEventListener( event, function( e )
                    {
                        // preventing the unwanted behaviours
                        e.preventDefault();
                        e.stopPropagation();
                    });
                });
                [ 'dragover', 'dragenter' ].forEach( function( event )
                {
                    form.addEventListener( event, function()
                    {
                        form.classList.add( 'is-dragover' );
                    });
                });
                [ 'dragleave', 'dragend', 'drop' ].forEach( function( event )
                {
                    form.addEventListener( event, function()
                    {
                        form.classList.remove( 'is-dragover' );
                    });
                });
                form.addEventListener( 'drop', function( e ){
                    droppedFiles = e.dataTransfer.files; // the files that were dropped
                    if(showFiles( droppedFiles ))
                        triggerFormSubmit();
                });
            }

            
            // if the form was submitted
            form.addEventListener( 'submit', function( e )
            {
                // preventing the duplicate submissions if the current one is in progress
                if( form.classList.contains( 'is-uploading' ) || form.classList.contains( 'is-processing' )) return false;
                if(form.id == 'captcha')
                {
                    $('#imageContainer').empty();
                    $('#resultContainer').empty();
                }
                else if(form.id == 'reCaptcha')
                {
                    $('#imageContainer2').empty();
                    $('#resultContainer2').empty();
                }

                
                form.classList.add( 'is-uploading' );
                form.classList.remove( 'is-error' );

                if( isAdvancedUpload ) // ajax file upload for modern browsers
                {
                    e.preventDefault();

                    // gathering the form data
                    var ajaxData = new FormData( form );
                    if( droppedFiles )
                    {
                        Array.prototype.forEach.call( droppedFiles, function( file )
                        {
                            ajaxData.append( input.getAttribute( 'name' ), file );
                        });
                    }

                    // ajax request
                    var ajax = new XMLHttpRequest();
                    ajax.open( form.getAttribute( 'method' ), form.getAttribute( 'action' ), true );
                    var xhr = new XMLHttpRequest();

                    if(form.id == 'captcha')
                    {
                        xhr.onload = function()
                        {
                            if( xhr.status >= 200 && xhr.status < 400 )
                            {
                                form.classList.remove( 'is-processing' );
                                var data = JSON.parse(xhr.responseText);
                                var webHost = 'http://140.138.152.207/'
                                // alert()
                                //alert(xhr.responseText)
                                $('#imageContainer').empty();
                                $('#resultContainer').empty();
                                $('#imageContainer').append("<img src="+webHost+'BDProject/upload/' + data['method1']['path'] + ' height="100" width="200"' + " />");
                                $('#imageContainer').append("<img src="+webHost+'BDProject/upload/' + data['method2']['path'] + ' height="100" width="200"' + " />");
                                $('#imageContainer').append("<img src="+webHost+'BDProject/upload/' + data['method3']['path'] + ' height="100" width="200"' + " />");
                                $('#resultContainer').append("<div><span style='color:#737CA1;'>Tesseract result:</span><div>");
                                $('#resultContainer').append("<span style='color:#737CA1; width: 200px; display: inline-block;'> " + data['method1']['tesseract_result'] + " </span>");
                                $('#resultContainer').append("<span style='color:#737CA1; width: 200px; display: inline-block;'> " + data['method2']['tesseract_result'] + " </span>");
                                $('#resultContainer').append("<span style='color:#737CA1; width: 200px; display: inline-block;'> " + data['method3']['tesseract_result'] + " </span>");
                                $('#resultContainer').append("<div><span style='color:#737CA1;'>GoogleVision result:</span><div>");
                                $('#resultContainer').append("<span style='color:#737CA1; width: 200px; display: inline-block;'> " + data['method1']['googleVision_result'] + " </span>");
                                $('#resultContainer').append("<span style='color:#737CA1; width: 200px; display: inline-block;'> " + data['method2']['googleVision_result'] + " </span>");
                                $('#resultContainer').append("<span style='color:#737CA1; width: 200px; display: inline-block;'> " + data['method3']['googleVision_result'] + " </span>");
                            }
                        };
                        
                        xhr.onerror = function()
                        {
                            form.classList.remove( 'is-uploading' );
                            alert( 'Error. Please, try again!' );
                        };
                    }
                    else if(form.id == 'reCaptcha')
                    {
                        xhr.onload = function()
                        {
                            if( xhr.status >= 200 && xhr.status < 400 )
                            {
                                form.classList.remove( 'is-processing' );
                                var data = JSON.parse(xhr.responseText);
                                // alert()
                                //alert(xhr.responseText)
                                $('#imageContainer2').empty();
                                $('#resultContainer2').empty();
                                $('#resultContainer2').append("<div><span style='color:#737CA1;'>GoogleVision result:</span><div>");
                                $('#resultContainer2').append("<span style='color:#737CA1; width: 200px; display: inline-block;'> " + data['method1']['result'] + " </span>");
                                $('#resultContainer2').append("<div><span style='color:#737CA1;'>Clarifai result:</span><div>");
                                $('#resultContainer2').append("<span style='color:#737CA1; width: 200px; display: inline-block;'> " + data['method2']['result'] + " </span>");
                            }
                        };
                        
                        xhr.onerror = function()
                        {
                            form.classList.remove( 'is-uploading' );
                            alert( 'Error. Please, try again!' );
                        };
                    }
                    
                    /*
                    xhr.onreadystatechange = function() {
                        var status;
                        var data;
                        // https://xhr.spec.whatwg.org/#dom-xmlhttprequest-readystate
                        if (xhr.readyState == 4) { // `DONE`
                            form.classList.remove( 'is-processing' );
                            status = xhr.status;
                            if (status == 200) {
                                data = JSON.parse(xhr.responseText);
                                alert(data['methods'][0]['description']);
                            } else {
                                alert('http error ' + status);
                            }
                        }
                    };
                    */
                    ajax.onload = function()
                    {
                        var host = "http://140.138.152.199"
                        form.classList.remove( 'is-uploading' );
                        if( ajax.status >= 200 && ajax.status < 400 )
                        {
                            form.classList.add( ajax.responseText != "" ? 'is-processing' : 'is-error' );
                            if( ajax.responseText == "" )
                                errorMsg.textContent = data.error;
                            else{
                                if(form.id == 'captcha')
                                    xhr.open("GET", host + ":8080/BD_Project/api/v1.0/methods/runAll?path=" + ajax.responseText, true);
                                else if(form.id == 'reCaptcha')
                                    xhr.open("GET", host + ":8080/BD_Project/api/v1.0/methods/reCaptcha?path=" + ajax.responseText + "&keyword=" + $('#keyword').val(), true);
                                // xhr.open("GET", "http://140.138.225.10:8080/BD_Project/api/v1.0/methods/runAll?path=" + ajax.responseText, true);
                                // xhr.setRequestHeader("Authorization", "Basic " + btoa("username:password"));
                                xhr.send();
                            }
                                
                        }
                        else alert( 'Error. Please, contact the webmaster!' );
                    };

                    ajax.onerror = function()
                    {
                        form.classList.remove( 'is-uploading' );
                        alert( 'Error. Please, try again!' );
                    };


                    ajax.send( ajaxData );
                }
                else // fallback Ajax solution upload for older browsers
                {
                    var iframeName  = 'uploadiframe' + new Date().getTime(),
                        iframe      = document.createElement( 'iframe' );

                        $iframe     = $( '<iframe name="' + iframeName + '" style="display: none;"></iframe>' );

                    iframe.setAttribute( 'name', iframeName );
                    iframe.style.display = 'none';

                    document.body.appendChild( iframe );
                    form.setAttribute( 'target', iframeName );

                    iframe.addEventListener( 'load', function()
                    {
                        var data = JSON.parse( iframe.contentDocument.body.innerHTML );
                        form.classList.remove( 'is-uploading' )
                        form.classList.add( data.success == true ? 'is-success' : 'is-error' )
                        form.removeAttribute( 'target' );
                        if( !data.success ) errorMsg.textContent = data.error;
                        iframe.parentNode.removeChild( iframe );
                    });
                }
            });
            
            
            // restart the form if has a state of error/success
            Array.prototype.forEach.call( restart, function( entry )
            {
                entry.addEventListener( 'click', function( e )
                {
                    e.preventDefault();
                    form.classList.remove( 'is-error', 'is-success' );
                    input.click();
                });
            });

            // Firefox focus bug fix for file input
            input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
            input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });

        });
    }( document, window, 0 ));


</script>
	</body>
</html>