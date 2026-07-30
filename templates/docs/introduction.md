# SITE_NAME 文档

SITE_NAME 是一个用于监控 cron 作业（[查看指南](monitoring_cron_jobs/)）
和类似定期流程的服务：

* SITE_NAME **监听来自 cron 作业和计划任务的 HTTP 请求（"ping"）**。
* 只要 ping 按时到达，它**保持沉默**。
* 一旦 ping 未按时到达，它**发出警报**。

SITE_NAME 作为需要持续运行或按定期、已知计划运行的流程的
[死 man 开关](https://en.wikipedia.org/wiki/Dead_man%27s_switch)。一些适合使用
SITE_NAME 监控的任务示例：

* 文件系统备份、数据库备份
* 任务队列
* 数据库复制监控脚本
* 报告生成脚本
* 定期数据导入和同步任务
* 定期防病毒扫描
* DDNS 更新脚本
* SSL 续期脚本

SITE_NAME *不*适合用于：

* 通过 HTTP 请求探测网站来监控其在线状态
* 收集应用程序性能指标
* 日志聚合

## 概念

**检查项**代表您要监控的单个服务。例如，在
[监控 cron 作业](monitoring_cron_jobs/)时，您将为每个要监控的 cron 作业创建一个单独的检查项。
每个检查项都有唯一的 ping URL、计划
和关联的集成。有关可用配置选项，请参阅
[配置检查项](configuring_checks/)。

每个检查项始终处于以下状态之一，由状态图标表示：

<span class="status ic-new"></span>
:   **新建**。尚未收到任何 ping 的新创建的检查项。您创建的每个
    新检查项都将以该状态开始。

<span class="status ic-up"></span>
:   **正常**。一切正常。最近的"success"信号已按时到达。

<span class="status ic-grace"></span>
:   **延迟**。"success"信号应到达但尚未到达。
    仍未超过检查项配置的**宽限期**。

<span class="status ic-down"></span>
:   **宕机**。"success"信号尚未到达，且宽限期已过。
    当检查项转换到"Down"状态时，SITE_NAME 会通过
    已配置的集成发送警报消息。

<span class="status ic-paused"></span>
:   **暂停**。您可以手动暂停特定检查项的监控。例如，
    如果某个频繁运行的 cron 作业存在已知问题，修复工作正在进行中
    但尚未就绪，您可以临时暂停对相应检查项的监控，以
    避免就已知问题收到不必要的警报。

<span class="status ic-up"></span><div class="spinner started"></div>
:   此外，如果最近收到的信号是"start"信号，
    这将在检查项的状态图标下通过三个动画点表示。

---

**Ping URL**。每个检查项都有唯一的 **Ping URL**。客户端（cron 作业、后台
工作者、批处理脚本、计划任务、Web 服务）向 ping URL 发送 HTTP 请求
以表示执行开始、成功或失败。

SITE_NAME 支持两种 ping URL 格式：

* `PING_ENDPOINT<uuid>`<br>
  检查项由其 UUID 标识。检查项 UUID 由 SITE_NAME 自动分配，
  且保证唯一。
* `PING_ENDPOINT<project-ping-key>/<name-slug>`<br>
  检查项由项目的 **Ping key** 和检查项的
  **标识**（用户选择的、URL 友好的标识符）标识。可选地支持自动配置：
  如果您 ping 一个没有对应检查项的标识值，SITE_NAME 可以
  自动创建该检查项。

您可以向基本 ping URL 追加 `/start`、`/fail` 或 `/<exitcode>` 来发送
"start"和"failure"信号。"start"和"failure"信号是可选的。
您不一定非要用它们，但如果使用它们，您将获得额外的监控洞察。
详情请参阅[测量脚本运行时间](measuring_script_run_time/)和
[发送故障信号](signaling_failures/)。

您应将检查项 UUID 和项目 Ping key 视为机密。如果您将它们公开，
任何人都可以向您的检查项发送遥测信号并干扰您的监控。

在[Ping API](http_api/)中阅读更多关于 Ping URL 的信息。

---

**宽限期**是您可以为每个检查项设置的配置参数之一。
它是在检查项延迟时发送警报前额外等待的时间。
使用此参数来考虑任务执行时间中微小、预期的偏差。

检查项何时被视为*延迟*取决于检查项使用的是简单
计划还是 cron 计划，以及您是否使用"start"事件
[跟踪任务持续时间](measuring_script_run_time/)。

对于**简单计划**，当检查项的配置周期已过时，该检查项即为延迟。
例如，考虑一个应每小时运行一次的定期任务，运行间隔
不应超过 5 分钟（周期 = 1 小时，宽限期 = 5 分钟）。
假设最后一次成功的 ping 在 12:00 到达。

* 在 13:00，检查项将被声明为延迟（因为距离上次 ping
  已过去 1 小时）。
* 在 13:05，检查项将被声明为宕机并发出警报（因为
  距离上次 ping 已过去 1 小时 + 5 分钟）。

对于 **cron 和 OnCalendar 计划**，检查项在当前的挂钟时间与计划匹配的
确切时刻进入延迟状态。考虑一个计划为 `10 * * * *`（每小时的第 10 分钟）且宽限期为
5 分钟的 cron 作业。假设最后一次成功的 ping 在 12:30 到达。

* 在 13:10，检查项将被声明为延迟（因为 13:10 是根据 cron 计划
  cron 作业应发送 ping 的下一个计划时间）。
* 在 13:15，检查项将被声明为宕机并发出警报（因为自
  cron 作业应签到的时间起已过去 5 分钟）。

如果您使用"start"信号来[测量任务执行时间](measuring_script_run_time/)，
宽限期还设置了"start"和"success"信号之间允许的最大时间间隔。
如果任务发送了"start"信号但未在宽限期内发送"success"信号，
SITE_NAME 将假定为失败并发出警报。

---

**集成**是在检查项状态发生变化时发送监控警报的特定方法。
SITE_NAME 支持多种类型的集成：电子邮件、
Webhook、短信、Slack、PagerDuty 等。您可以设置多个集成。
对于每个检查项，您可以指定应使用哪些集成。

有关集成的更多信息，请参阅
[配置通知](configuring_notifications/)。

---

**项目**。为了保持井然有序，您可以将检查项和集成分组到**项目**中。
您的帐户从单个默认项目开始，但您可以根据需要创建
其他项目。您可以在项目之间转移现有检查项，
同时保留其配置和 ping URL。

每个项目都有可配置的名称、单独的 API 密钥集以及单独的
项目团队。项目的团队是您授予了项目只读或
读写权限的人员集合。

有关项目的更多信息，请参阅[项目和团队](projects_teams/)。
