> - v2.0已经不再维护（但可用）,v3.0使用go重构
> - 此分支为v2.0版本的预览版
> - 如果存在问题请切换到1.0分支(版本号为v1.x)

# ShadowsocksR-support
一个在服务器端生成ShadowsockR服务器订阅以及维护进程存活的简单实现

### 设计目的
- 防止因为DNS解析导致SSR服务器ip被BAN
- 防止SSR进程因意外被终止
- 降低因服务器新增/迁移，SSR设置更新等的工作量

### 部署方式
- 中介服务器的部署
    1. 拷贝root目录下文件到主服务器
    2. 修改`config.yaml`配置文件
    3. 添加计划任务(可选)
       1. 控制台输入`crontab -e`
       2. 输入
        ```
            0 * * * * cd /项目路径;php ./all.php &
        ```
    4. 执行`service crond restart`
    5. 配置Nginx/apache等Web服务器
- 代理服务器的部署
    1. 将proxy目录下的拷贝到部署SSR的服务器
    2. 修改`config.yaml`配置文件
    3. 添加开机启动(必须设置时间延迟，否则会导致网络错误)
        1. 打开`/etc/rc.d/rc.local`
        2. 添加
            ```
            (
                sleep 120
                cd /项目路径
                nohup python -m proxy.core > log.out 2>&1
            )&
            ```
- socket连接问题
    - 检查代理服务器的SSRS运行状态
    - 关闭防火墙
    - 配置安全组放行1025-65535端口的TCP

### config.yaml配置文件
- 中介服务器config.yaml
    ```
    group: PowerByBafflingBUG                         # SSR GROUP
    token: password                                   # 服务器间token，必须和代理服务器相同字段保持一致(弱验证)
    password: 696d29e0940a4957748fe3fc9efd22a3        # 客户连接中介服务器使用的password，此处填写值为原始密钥经过[两次]md5加密以后的值(32位/小写/强验证)
    ```

- 代理服务器config.json
    ```
    url: http://example.com/                          # 中介服务器的地址(用于注册一个代理服务器)
    token: password                                   # 服务器间token，必须和中介服务器相同字段保持一致(弱验证)
    server:
        host: 127.0.0.1                               # 服务器的公网ip，请勿填写0.0.0.0或者127.0.0.1
        port: 65535                                   # SSRS进程使用的端口(非SSR端口)
    ssr_list:
        - config_file: /etc/shadowsocksR/config.json  # SSR进程的配置文件路径(完整路径)
          remarks: ssr                                # SSR进程的备注名(请勿使用中文，空格，特殊符号等)
          restart: /etc/init.d/shadowsocksR restart   # SSR进程的重启命令
        # 第二个SSR进程
        - config_file:
          remarks:
          restart:
    # 如果同时存在SS进程在此配置
    ss_list:
        - config_file:
          remarks:
          restart:
    ```

### SSR服务器订阅地址
`http(s)://[main-server]/api/?pw=[password]`

此处user-token为未加密的明文

示例：*http://example.com/?token=password*

### 重启指定SSR服务器
`http(s)://[main-server]/api/restart.php?pw=[password]&host=[host]&remarks=[remarks]`

示例：*http://example.com/api/restart.php?pw=password&host=127.0.0.1&remarks=ssr*

### 运行流程
1. 代理服务器启动监听socket并向中介服务器POST注册信息
2. 中介服务器记录代理服务器上SSRS的端口，并通过socket请求代理服务器上SSR进程的信息
3. 代理服务器收到请求后查找本机上的SSR进程
   > SSR进程未启动则执行对应的重启命令
4. 中介服务器定期请求代理服务器上SSR进程的信息

### 写在最后
- 这个一个个人项目，没有做很多的兼容性判断。可能会在其他环境下无法运行
- ~~python的运行环境是2.7~~ 同时兼容python2.7及python3+
- 选择python和php的原因是我现在使用的两台服务器的运行环境
