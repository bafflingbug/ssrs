<?php
    date_default_timezone_set('Asia/Shanghai');
    $json = file_get_contents('./config.json');
    $config = json_decode($json, true);
    if ($config["token"] !== $_POST["token"]){
        echo "error:1";
    }else{
        $json = file_get_contents('./ssrURL.json');
        $url = json_decode($json, true);
        echo "1";
        $url[$_POST["host"]] = array(
            "ssr" => $_POST["ssr"],
            "lasttime" => date("y-m-d H:i:s")
        );
        $json = json_encode($url);
        file_put_contents('./ssrURL.json', $json);
    }
?>