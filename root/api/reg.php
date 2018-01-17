<?php
set_time_limit(0);
date_default_timezone_set('Asia/Shanghai');
include_once './Spyc.php';
$config = spyc_load_file('../config.yaml');
$reg_s = trim(file_get_contents('./data/reg.json', true));
if ($reg_s !== '') {
    $reg = json_decode($reg_s, true);
} else {
    $reg = array();
}
if ($_POST['token'] === null) {
    echo '301';
} elseif ($_POST['token'] === $config['token']) {
    try {
        $reg[$_POST['host']] = $_POST['port'];
        $reg_s = json_encode($reg);
        file_put_contents('./data/reg.json', $reg_s);
        echo '601';
        $isReg = true;
        include "./all.php";
    } catch (Exception $e) {
        echo '602:' . $e;
    }
} else {
    echo '401';
}