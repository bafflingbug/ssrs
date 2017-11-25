# ShadowsocksR-support
一个在服务器端生成ShadowsockR服务器订阅的简单实现

### 设计目的
- 防止因为DNS解析导致SSR服务器ip被BAN
- 降低因服务器新增/迁移，SSR设置更新等的工作量

### 部署方式
- 主服务器的部署
    1. 拷贝php目录下文件到主服务器
    2. 修改`config.json`配置文件
    3. 配置Nginx/apache等Web服务器
- SSR服务器的部署
    1. 将python目录下的拷贝到部署SSR的服务器
    2. 修改`config.json`配置文件
    3. 添加开机启动(必须设置时间延迟，否则会导致网络错误)
        1. 打开`/etc/rc.d/rc.local`
        2. 添加
            ```
            (
                sleep 120
                nohup python /项目路径/python/main.py > /项目路径/python/log.out 2>&1 
            )&
            ```
    4. 添加定时任务
        1. 控制台输入`crontab -e`
        2. 添加
            ```
            0 * * * * python /项目路径/python/main.py &
            ```

### config.json配置文件
- 主服务器config.json
    ```
    {
        "group": "PowerByBafflingBUG",      //SSR GROUP
        "token": "password"                 //验证,用于确认权限(弱验证)
    }
    ```

- SSR服务器config.json
    ```
    {
        "ss-config-file": ["ss_config1","ss_config2"],      //SS服务器的配置文件路径
        "ssr-config-file": ["ssr_config1","ssr_config2"],   //SSR服务器的配置文件路径
        "main-server": "ssr.example.com",                   //主服务器的域名/IP
        "host": "0.0.0.0",                                  //当前服务器的外网IP
        "token": "password",                                //验证,需与主服务器一致  
        "ssl": false                                        //主服务器是否使用SSL(https)
    }
    ```

### SSR服务器订阅地址
**http(s)://[main-server]/?token=[token]**

示例：*http://example.com/?token=password*

### 运行流程
1. SSR服务器每小时检测本地各配置文件(包括SS配置文件，SSR配置文件，SSRS配置文件)是否被更新
2. - 若有更新 向主服务器推送新的SSR链接
   - 若无更新 向主服务器发送SSR服务器在线确认
   > - 若主服务器不存在当前服务器的记录 重新推送SSR链接到主服务器 
3. 主服务器记录各SSR服务器的推送/确认时间，且抛弃3小时未确认的服务器的SSR链接

### 写在最后
- 这个一个个人项目，没有做很多的兼容性判断。可能会在其他环境下无法运行
- python的运行环境是2.7
- 选择python和php的原因是我现在使用的两台服务器的运行环境