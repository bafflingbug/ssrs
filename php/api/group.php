<?php
require_once('./Spyc.php');
$file = file_get_contents('./config.yaml');
$config = spyc_load_file($file);
echo array_key_exists("group", $config) ? $config["group"] : "PowerByBafflingBUG";
