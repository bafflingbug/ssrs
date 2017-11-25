<?php
    date_default_timezone_set('Asia/Shanghai');
    $json = file_get_contents('./config.json');
    $config = json_decode($json, true);
    if ($config["token"] !== $_POST["token"]){
        echo "error:1";
    }else{
        $json = file_get_contents('./ssrURL.json');
        $url = json_decode($json, true);
        if(array_key_exists("lasttime", $url[$_POST["host"]])){
            $url[$_POST["host"]]["lasttime"] = date("y-m-d H:i:s");
            $json = json_encode($url);
            file_put_contents('./ssrURL.json', $json);
        }else{
            echo "error:2";
        }
    }
?>