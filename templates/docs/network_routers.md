# 网络路由器

某些网络路由器操作系统可以配置为直接从路由器向 SITE_NAME 发送定期 HTTP(S)
请求。这是监控它们的便捷方式：当
路由器失去 WAN 连接时，它将无法 ping SITE_NAME，SITE_NAME
会通知你中断情况。

## DD-WRT

[DD-WRT](https://dd-wrt.com/) 是一种基于 Linux 的路由器固件，可运行在多种
路由器型号上。DD-WRT 自带 cron 守护进程和 wget 工具。你可以
在 DD-WRT 控制面板中启用 cron 守护进程并编辑 crontab，
路径为 **Administration › Management › Cron**。

DD-WRT 上的 crontab 语法为：

    [cron 表达式] [用户名] [命令]

每分钟发送 ping 的示例：

    * * * * * root wget PING_URL

截图：

![DD-WRT 控制面板](IMG_URL/ddwrt.png)

## MikroTik RouterOS

[MikroTik RouterOS](https://mikrotik.com/software) 是一种路由器操作系统，主要用于
MikroTik 网络硬件。其众多功能包括脚本支持
和调度器。

首先，在 WebFig 中创建脚本，路径为 **System › Scripts › Add New**。使用以下
参数：

* Name: `ping`（示例，你可以使用其他名称）
* Policy: `read`, `test`
* Source: `/tool fetch url="PING_URL" output=none`

![DD-WRT 控制面板](IMG_URL/routeros1.png)

然后，在 WebFig 中创建调度，路径为 **System › Scheduler › Add New**。使用参数：

* Interval: `00:01:00`（一分钟）
* Policy: `read`, `test`
* On Event: `ping`（上一步中脚本的名称）

![DD-WRT 控制面板](IMG_URL/routeros2.png)

注意：

* `output=none` 参数告诉系统丢弃响应体。如果没有
  此参数，系统会将响应体保存到文件，这还额外需要 `write` 策略。
* "tool fetch" 工具支持 HTTPS URL，但默认情况下不验证 TLS 证书。
  你可以添加 `check-certificate=yes` 参数以要求有效 TLS
  证书。请注意，RouterOS 不附带根 CA 证书，因此你还需要
  加载这些证书。
* [这里是 "tool fetch" 支持的完整选项列表](https://wiki.mikrotik.com/wiki/Manual:Tools/Fetch)。



