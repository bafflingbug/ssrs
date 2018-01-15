<?php
set_time_limit(0);
date_default_timezone_set('Asia/Shanghai');
$last_time = strtotime(trim(file_get_contents('./data/last.date')));
require_once('./Spyc.php');
$config = spyc_load_file('../config.yaml');
if ($_REQUEST['pw'] == null) {
    echo '301: no password';
} elseif (md5(md5($_REQUEST['pw'])) == $config['password']) {
    if ((strtotime(date("y-m-d H:i:s")) - $last_time) / 60 < 20.0) {
        require('./ssrurl.php');
    } else {
        require('./all.php');
        require('./ssrurl.php');
    }
} else {
    echo '401: error password';
}