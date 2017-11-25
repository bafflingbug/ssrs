<?php
    $json = file_get_contents('./config.json');
    $config = json_decode($json, true);
    echo array_key_exists("group", $config)?$config["group"]:"PowerByBafflingBUG";
?>