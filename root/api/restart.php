<?php
function logdata($str)
{
    file_put_contents('./err.log', '[' . date('y-m-d H:i:s') . ']' . $str . "\n", FILE_APPEND);
}

set_time_limit(0);
date_default_timezone_set('Asia/Shanghai');
require_once('./Spyc.php');
$config = spyc_load_file('../config.yaml');
if ($_REQUEST['pw'] == null) {
    echo '301: no password';
} elseif (md5(md5($_REQUEST['pw'])) == $config['password']) {
    $host = $_REQUEST['host'];
    $remarks = $_REQUEST['remarks'];
    $reg_s = trim(file_get_contents('./data/reg.json'));
    if ($reg_s !== '') {
        $reg = json_decode($reg_s, true);
    } else {
        logdata('404: 没有已注册的代理服务器');
        echo '404: No registered proxy Server';
        exit(404);
    }
    if (!$ssr) {
        $ssr_s = trim(file_get_contents('./data/ssr.json'));
        if ($ssr_s !== '') {
            $ssr = json_decode($ssr_s, true);
        } else {
            logdata('404: ssr.json没有数据');
            echo '404: ssr.json No data';
            exit(404);
        }
    }
    if (!array_key_exists($remarks, $ssr[$host])) {
        logdata('404: ' . $host . '不存在名为' . $remarks . '的SS/SSR进程');
        echo '404: ' . $host . ' is no SS/SSR process named ' . $remarks;
        exit(404);
    }
    $command = 102;
    $socket = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socket !== false) {
        if ($result = @socket_connect($socket, $host, (int)$reg[$host]) !== false) {
            $data = json_encode(array('command' => $command, 'remarks' => $remarks, 'token' => $config['token']));
            @socket_write($socket, $data, strlen($data));
            $str = trim(@socket_read($s, 1024));
            if ($str !== '') {
                $data = json_decode($str, true);
                if ($data['status'] === 202) {
                    foreach ($data['data'] as $host => $value) {
                        if (!empty($value)) {
                            $ssr[$host][$remarks] = $value[$remarks];
                            echo '200: OK';
                        } else {
                            $ssr = array_diff_key($ssr[$host], $ns = array($remarks => ''));
                            echo '500: restart filed';
                        }
                    }
                } elseif ($data['status'] >= 300 && $data['status'] < 400) {
                    logdata($data['status']);
                    echo $data['status'];
                    exit($data['status']);
                } elseif ($data['status'] >= 400) {
                    logdata($data['status'] . ":" . $data['err']);
                    echo $data['status'];
                    exit($data['status']);
                }
            }
        } else {
            $ns = array($host => '');
            $reg = array_diff_key($reg, $ns);
            file_put_contents('./data/reg.json', json_encode($reg));
            $ssr = array_diff_key($ssr, $ns);
            file_put_contents('./data/ssr.json', json_encode($ssr));
            logdata("socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)));
            echo "socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket));
        }
    } else {
        logdata("socket_create() failed: reason: " . socket_strerror(socket_last_error()));
        echo "socket_create() failed: reason: " . socket_strerror(socket_last_error());
    }
} else {
    echo '401: error password';
}