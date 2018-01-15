<?php
require_once('./Spyc.php');
$config = spyc_load_file('../config.yaml');
echo array_key_exists("group", $config) ? $config["group"] : "PowerByBafflingBUG";