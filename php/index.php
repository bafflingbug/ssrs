<?php
    date_default_timezone_set('Asia/Shanghai');
    $json = file_get_contents('./config.json');
    $config = json_decode($json, true);
    if ($config["user-token"] !== md5(md5($_REQUEST["token"]))){
        echo "error:1";
    }else{
        $json = file_get_contents('./ssrURL.json');
        $url = json_decode($json, true);
        $ssr = "";
        foreach($url as $host => $value){
            if((strtotime(date("y-m-d H:i:s"))-strtotime($value["lasttime"]))/3600 < 3.0){
                $ssr .= $value["ssr"];
            }
        }
        echo base64_encode($ssr);
    }
?>