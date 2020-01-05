# SSRS
一个在服务器端生成ShadowsockR或v2ray服务器订阅以及维护进程存活的简单实现

## 下载
[release](https://github.com/bafflingbug/ssrs/releases)

### 设计目的
- 防止因为DNS解析导致SSR服务器ip被BAN
- 防止SSR进程因意外被终止
- 降低因服务器新增/迁移，SSR设置更新等的工作量

### 插件
1. ssrs
    - 用于读取ssr/ss配置文件,生成ssr://链接
2. ssrs_server
    - 用于汇总多个ssrs插件生成的链接,并提供适用于SSR客户端的服务器订阅
3. v2s
    - 用于读取v2ray配置文件,生成vmess://链接
4. v2s_server
    - 用于汇总多个v2s插件生成的链接,并提供适用于v2ray客户端的服务器订阅

> 关于插件
> 1. ssrs与ssrs_server需要配合使用
> 2. ssrs可以与ssrs_server在不同服务器上(设计如此),也可在同一台服务器上
> 3. 允许添加新的插件,参见 [自定义插件](#自定义插件)
> 4. v2s和v2s_server同上

### 部署方式
1. 拷贝代码到服务器
2. 执行`pip install -r requirements.txt`安装依赖
3. 到`src/service/plugins`启用/禁用插件（禁用方式为删除或在文件夹前加入两个下划线`__`）
4. 使用gunicorn或其他wsgi来启动服务器（一条建议的命令`gunicorn -c /data/ssrs/src/gun.conf main:app --chdir /data/ssrs/src -D`其中`/data/ssrs`为项目路径）

- 一条用于重新加载SSRS配置/重启SSRS的命令：`cat /tmp/gunicorn.pid |xargs kill -HUP`


### config.yaml配置文件
- config.yaml在相应的插件目录下

- ssrs_server插件的config.yaml
    ```
    group: PowerByBafflingBUG                         # SSR GROUP
    token: password                                   # 服务器间token，必须和代理服务器相同字段保持一致(弱验证)
    password: 696d29e0940a4957748fe3fc9efd22a3        # 客户连接中介服务器使用的password，此处填写值为原始密钥经过[两次]md5加密以后的值(32位/小写/强验证)
    ```

- ssrs插件的config.yaml
    ```
    host: 0.0.0.0                                     # 本机公网
    server: http://127.0.0.1:80                       # 本机web服务器地址,用于ssrs_server访问ssrs(如果部署在同一台机器上可以使用环回地址)
    reg_server: http://example.com/ssrs_server/       # ssrs的地址(用于注册一个代理服务器,由于插件名的可变性请带上插件名）
    token: password                                   # 服务器间token，必须和中介服务器相同字段保持一致(弱验证)
    ssr:                                              # 兼容SS
        - config: /etc/shadowsocksR/config.json  # SSR进程的配置文件路径(完整路径)
          remarks: ssr                                # SSR进程的备注名(请勿使用中文，空格，特殊符号等)
          restart: /etc/init.d/shadowsocksR restart   # SSR进程的重启命令
        # 第二个SSR进程(可选)
        - config:
          remarks:
          restart:
    ```

- v2s_server插件的config.yaml

   参见`ssrs_server插件的config.yaml`

- v2s插件的config.yaml

    ```
    host: 0.0.0.0                                     # 本机公网(可以用域名)
    server: http://127.0.0.1:80                       # 本机web服务器地址,用于v2s_server访问v2s(如果部署在同一台机器上可以使用环回地址)
    reg_server: http://example.com/ssrs_server/       # v2s的地址(用于注册一个代理服务器,由于插件名的可变性请带上插件名）
    token: password                                   # 服务器间token，必须和中介服务器相同字段保持一致(弱验证)
    v2ray:
        - config: /etc/v2ray/config.json              # v2ray进程的配置文件路径(完整路径)
          remarks: v2ray                              # v2ray进程的备注名(请勿使用中文，空格，特殊符号等)
          restart: service v2ray restart              # v2ray进程的重启命令
          tips:                                       # 选填，用来覆盖v2ray服务器配置文件不包含的配置项
            - origin_port:                            # 必填
              # 下列选项均为选填，生成的配置链接会用下述配置覆盖config中的配置
              ps:
              add:
              port:
              host:
              path:
              tls:
            - origin_port:
              tls:
        # 第二个v2ray进程(可选)
        # 如果不需要配置tips可以像下面一样直接省略
        - config:
          remarks:
          restart:
    ```
    - 关于tips字段的说明参见[wiki](https://github.com/bafflingbug/ssrs/wiki/v2s-tips-%E5%AD%97%E6%AE%B5%E8%AF%B4%E6%98%8E)
### SSR服务器订阅地址
`http(s)://[main-server]/<ssrs plugins name>/?pw=[password]`

此处user-token为未加密的明文

示例：*http://example.com/ssrs_server/?pw=password*

### 自定义插件
1. 插件的工作方式
    - 使用flask的Blueprint实现
    - 访问插件的url为`host[:port]/<plugins name>/<path>`
    - 插件文件存放于`src/service/plugins/<plugins name>`下
2. 插件名
    - 插件名即其plugins下的文件夹名,更改文件夹名会使得插件url产生相同改动
3. 如何编写插件
    1. 建立插件的目录
    2. 在插件目录下建立`__init__py`
    3. `__init__.py`里需要有一个类型为`flask.Blueprint`的`blueprint`变量
    4. 使用flask编写代码


### 写在最后
- 这个一个个人项目，没有做很多的兼容性判断。可能会在其他环境下无法运行
- python的运行环境是python3+
- 如果难以看懂教程尝试切换分支到以前的版本(我也觉得如此)
