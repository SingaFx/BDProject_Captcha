<?php session_start(); ?>
<?php

    function crypto_rand_secure($min, $max)
    {
        $range = $max - $min;
        if ($range < 1) return $min; // not so random...
        $log = ceil(log($range, 2));
        $bytes = (int) ($log / 8) + 1; // length in bytes
        $bits = (int) $log + 1; // length in bits
        $filter = (int) (1 << $bits) - 1; // set all lower bits to 1
        do {
            $rnd = hexdec(bin2hex(openssl_random_pseudo_bytes($bytes)));
            $rnd = $rnd & $filter; // discard irrelevant bits
        } while ($rnd > $range);
        return $min + $rnd;
    }

    function getToken($length)
    {
        $token = "";
        $codeAlphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
        $codeAlphabet.= "abcdefghijklmnopqrstuvwxyz";
        $codeAlphabet.= "0123456789";
        $max = strlen($codeAlphabet); // edited

        for ($i=0; $i < $length; $i++) {
            $token .= $codeAlphabet[crypto_rand_secure(0, $max-1)];
        }

        return $token;
    }

    $account = $_SESSION["account"];
    $token = getToken(40);
    $database = mysql_connect( "140.138.152.207","blazing93", "meteor95188" );
    if ( !mysql_select_db( "house", $database ) )
        die( "Could not open database!" );

    // 更新資料庫
    $sql = "UPDATE db_captcha_user SET api_key = '".$token."' WHERE account = '".mysql_real_escape_string($account)."'";
    $result = mysql_query( $sql, $database );
    echo $token;
?>