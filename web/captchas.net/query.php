<?php

require 'CaptchasDotNet.php';

// Required Parameters
// Replace the values you receive upon registration at http://captchas.net.
//
//   client: 'demo'
//
//   secret: 'secret'
//
// Optional Parameters and defaults
//
//   repository_prefix: '/tmp/captchasnet-random-strings' path to repository
//   ATTENTION SAFE-MODE, YOU HAVE TO CHOOSE SOMETHING LIKE
//   '/writable/path/captchasnet-random-strings'
//
//   cleanup_time: '3600' (means max 1 hour between query and check)
//
//   alphabet: 'abcdefghijklmnopqrstuvwxyz' (Used characters in captcha)
//   We recommend alphabet without ijl: 'abcdefghkmnopqrstuvwxyz'
//
//   letters: '6' (Number of characters in captcha)
//
//   width: '240' (image width)
//
//   height: '80' (image height)
//
//   color: '000000' (image color in rgb)
//
//   language: 'en' (audio language, append &language=fr/de/it/nl to audio-url)
//
//   Usage
//   $captchas = new CaptchasDotNet (<client>, <secret>,
//                                   <repository_prefix>, <cleanup_time>,
//                                   <alphabet>,<letters>,
//                                   <height>,<width>,<color>);
//
// Don't forget same settings in check.php

require 'generateKey.php';

$randomKey = getToken(40);

echo $randomKey;
// Construct the captchas object.

$captchas = new CaptchasDotNet ('demo', 'secret',
                                'tmp/captchasnet-random-strings','3600',
                                'abcdefghijklmnopqrstuvwxyz','6',
                                '240','80','000000');
?>

<html>
  <head>
    <title>Sample PHP CAPTCHA Query</title>
  </head>
  <h1>Sample PHP CAPTCHA Query</h1>
  <form method="get" action="check.php">
    <table>
      <tr>
        <td>
          <input type="hidden" name="random" value="<?= $captchas->random () ?>" />
        </td>
        <td>
          <?= $captchas->image()?> 
          <a href="javascript:captchas_image_reload('captchas.net')">Reload Image</a>
        </td>
        <td>
          <a id="pwd"><?= $captchas->getPwd()?></a>
        </td>
      </tr>
    </table>
  </form>
</html>