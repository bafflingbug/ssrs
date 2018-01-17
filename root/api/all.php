<?php
function logdata($str)
{
    file_put_contents('./err.log', '[' . date('y-m-d H:i:s') . ']' . $str . "\n", FILE_APPEND);
}

define("isShell", !isset($_SERVER["HTTP_USER_AGENT"]));
if (!$config) {
    include_once './Spyc.php';
    $config = spyc_load_file('../config.yaml');
}
if (!isShell && ($_REQUEST['pw'] === null || md5(md5($_REQUEST['pw'])) !== $config['password']) && $isReg === null) {
    echo '500: Illegal access';
    exit(500);
}
set_time_limit(0);
date_default_timezone_set('Asia/Shanghai');
$reg_s = trim(file_get_contents('./data/reg.json'));
if ($reg_s !== '') {
    $reg = json_decode($reg_s, true);
} else {
    logdata('404: 没有已注册的代理服务器');
    exit(404);
}
$sockets = array();
$command = 101;
if (!$ssr) {
    $ssr_s = trim(file_get_contents('./data/ssr.json'));
    if ($ssr_s !== '') {
        $ssr = json_decode($ssr_s, true);
    } else {
        $ssr = array();
    }
}
$ns = array();
foreach ($reg as $host => $port) {
    $socket = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
    if ($socket !== false) {
        if ($result = @socket_connect($socket, $host, (int)$port) !== false) {
            $data = json_encode(array('command' => $command, 'token' => $config['token']));
            @socket_write($socket, $data, strlen($data));
            array_push($sockets, $socket);
            $ns[$host] = '';
        } else {
            logdata("socket_connect() failed.\nReason: ($result) " . socket_strerror(socket_last_error($socket)));
        }
    } else {
        logdata("socket_create() failed: reason: " . socket_strerror(socket_last_error()));
    }
}
$reg = array_intersect_key($reg, $ns);
file_put_contents('./data/reg.json', json_encode($reg));
$ssr = array_intersect_key($ssr, $ns);
while (!empty($sockets)) {
    $read_sock = $sockets;
    $sock_num = @socket_select($read_sock, $write_sock = null, $except_sock = null, 0);
    if ($sock_num === false) {
        echo "socket_select() failed, reason: " . socket_strerror(socket_last_error()) . "\n";
        break;
    } else if ($sock_num > 0) {
        foreach ($read_sock as $s) {
            $str = trim(@socket_read($s, 1024));
            if ($str !== '') {
                $data = json_decode($str, true);
                if ($data['status'] === 201) {
                    foreach ($data['data'] as $host => $value) {
                        if (!empty($value)) {
                            $ssr[$host] = $value;
                        } else {
                            $ssr = array_diff_key($ssr, $ns = array($host => ''));
                        }
                    }
                } elseif ($data['status'] >= 300 && $data['status'] < 400) {
                    logdata($data['status']);
                } elseif ($data['status'] >= 400) {
                    logdata($data['status'] . ":" . $data['err']);
                }
            }
            socket_close($s);
        }
    }
    $sockets = array_diff($sockets, $read_sock);
}
file_put_contents('./data/ssr.json', json_encode($ssr));
file_put_contents('./data/last.date', date("y-m-d H:i:s"));