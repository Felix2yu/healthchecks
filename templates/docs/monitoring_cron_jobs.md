# 如何使用 SITE_NAME 监控 Cron 任务

SITE_NAME 可以监控你的 cron 任务，并在它们未按预期时间运行时通知你。
假设 `curl` 或 `wget` 可用，你不需要在服务器上安装任何新软件。

工作原理很简单：你的 cron 任务每次完成时向
SITE_NAME 发送一个 HTTP 请求（"ping"）。当 SITE_NAME 在预期时间
未收到 HTTP 请求时，它会通知你。这种监控技术有时被称为
"心跳监控"，是一种[死机开关](https://en.wikipedia.org/wiki/Dead_man%27s_switch)。
它可以检测各种故障模式：

* 整个机器宕机（断电、硬件故障、有人绊到线缆等）。
* cron 守护进程未运行或配置无效。
* Cron 确实启动了你的任务，但任务以非零退出码退出。
* cron 任务运行时间异常长。

## 设置

让我们看一个 cron 任务示例：

```bash
# 每天早上 06:08 运行 backup.sh
8 6 * * * /home/me/backup.sh
```

要监控它，首先在你的 SITE_NAME 账户中创建一个新的检查项：

!["添加检查项" 对话框](IMG_URL/add_check.png)

创建检查项后，复制生成的 **ping URL**，并更新任务的
定义：

```bash
# 运行 backup.sh，然后向 SITE_NAME 发送成功信号
8 6 * * * /home/me/backup.sh && curl -fsS -m 10 --retry 5 -o /dev/null PING_URL
```

额外的 curl 调用让 SITE_NAME 知道 cron 任务已成功运行。
SITE_NAME 会跟踪接收到的 ping，并在 ping 未按时到达时立即通知你。

注意：你也可以将额外的 `curl` 调用作为最后一行添加到
`/home/me/backup.sh` 脚本内部，以保持 cron 任务的定义简洁。
你可以使用 curl 以外的 HTTP 客户端来发送 HTTP 请求。

## Curl 选项

上例中的额外选项告诉 curl 重试失败的 HTTP 请求、
限制最大执行时间，并在无错误时静默输出。
请根据你的需要自由调整 curl 选项。

**&amp;&amp;**
:   仅在 `/home/me/backup.sh` 以退出码 0 退出时才运行 curl。

**-f, --fail**
:   使 curl 将非 200 的响应视为错误。

**-s, --silent**
:   静默或安静模式。隐藏进度条，但也会隐藏错误消息。

**-S, --show-error**
:   在使用 -s 时重新启用错误消息。

**-m &lt;seconds&gt;**
:   允许整个操作花费的最长时间（秒）。

**--retry &lt;num&gt;**
:   如果 curl 尝试传输时返回瞬时错误，
    它将在放弃前重试这么多次。
    设置为 0 表示不重试（这是默认值）。
    瞬时错误是超时或 HTTP 5xx 响应码。

**-o /dev/null**
:   将 curl 的 stdout 重定向到 /dev/null（错误消息仍发送到 stderr）。


## 宽限期

宽限期是指当 cron 任务运行延迟时，在将其宣告为宕机之前等待的额外时间。
将宽限期设置为高于 cron 任务的预期持续时间。

例如，假设 cron 任务每天 14:00 开始，需要 15 到 25 分钟完成。
宽限期设置为 30 分钟。在这种情况下，SITE_NAME 将期望在 14:00 收到 ping，
但不会立即发送警报。如果在 14:30 之前没有 ping，它将宣告任务失败并
发送警报。

## 通知

SITE_NAME 具有通过不同渠道发送通知的集成方式：电子邮件、
Webhook、短信、聊天消息、事件管理系统等。你可以且应该
设置多种方式来获取任务失败的通知：

* **冗余：**如果一个通知渠道失败（例如，电子邮件被投递到
  垃圾箱），你仍会通过其他渠道收到通知。
* **根据任务优先级使用不同的通知方法**。你可以将低优先级任务的
  通知仅设置为电子邮件，而高优先级任务的通知
  设置为电子邮件、短信和团队聊天。

此外，为确保没有任何问题"被遗漏"，在
[账户设置 › 电子邮件报告](../../accounts/profile/notifications/) 页面
中，你可以配置 SITE_NAME 在有任何任务宕机的情况下，
每小时或每天发送重复的电子邮件通知：

![电子邮件提醒选项](IMG_URL/email_reports.png)

## 高级技巧

* 如果你的 cron 任务遇到错误，你可以[主动向 SITE_NAME 发送信号](../signaling_failures/)。
* 你可以在 cron 任务开始时发送"start"信号，以[跟踪其运行时间](../measuring_script_run_time/)。
* 你可以在 HTTP POST 体中[发送 stdout 和 stderr 输出](../attaching_logs/)。

## 那 MAILTO 呢？

传统的 cron 实现有一个内置的通知 cron 任务失败的方法，即 MAILTO 变量：

```bash
MAILTO=email@example.org
8 6 * * * /home/me/backup.sh
```

那为什么不直接使用它呢？有几个缺点：

* MAILTO 要工作，服务器需要已配置 MTA。
* 如果整个机器断电或失去网络连接，你将不会收到通知。
* 如果你的 cron 任务产生任何 stdout 输出，你将在每次任务运行时收到
  一封电子邮件。这可能导致警报疲劳，并且你可能
  无法在诊断消息之间注意到错误。

## 查看机器的时区

如果你的 cron 任务始终提前或推迟一小时 ping SITE_NAME，
很可能是时区不匹配：你的机器可能使用了与你在 SITE_NAME 上配置的
不同的时区。

在 modern GNU/Linux 系统上，你可以使用 `timedatectl status` 命令
查看时区，在输出中查找"Time zone"：

```text hl_lines="6"
$ timedatectl status

               Local time: C  2020-01-23 12:35:50 EET
           Universal time: C  2020-01-23 10:35:50 UTC
                 RTC time: C  2020-01-23 10:35:50
                Time zone: Europe/Riga (EET, +0200)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```


## 使用 `journalctl` 查看 Cron 日志

在基于 systemd 的系统上，你可以使用 `journalctl` 工具查看系统日志，
包括 cron 守护进程的日志。

查看实时日志：

```bash
journalctl -f
```

查看例如过去一小时且仅来自 cron 守护进程的日志：

```bash
journalctl --since "1 hour ago" -t CRON
```
