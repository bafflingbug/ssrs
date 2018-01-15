<?php
if (!$ssr) {
    $ssr_s = trim(file_get_contents('./data/ssr.json'));
    if ($ssr_s !== '') {
        $ssr = json_decode($ssr_s, true);
    } else {
        echo '';
        exit();
    }
}
if (empty($ssr)){
    echo '';
    exit();
}
$urls = '';
foreach ($ssr as $host => $value) {
    foreach ($value as $remarks =>$url) {
        $urls .= $url;
    }
}
echo base64_encode($urls);