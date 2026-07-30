# 配置检查项

在 SITE_NAME 中，**检查项**代表您要监控的单个服务。
例如，在监控 cron 作业时，您需要为每个要监控的 cron 作业创建一个单独的检查项。
SITE_NAME 的定价计划主要围绕
您的帐户中可以拥有多少检查项来设计。您可以在
SITE_NAME Web 界面或通过[管理 API](../api/)创建检查项。

## 名称、标签、描述

使用可选的名称、标识、标签和描述字段来描述每个检查项。

![编辑名称、标签和描述](IMG_URL/edit_name.png)

* **名称**：名称是可选的，但设置它们是个好主意。
  良好的命名在您向帐户添加更多检查项时变得尤为重要。
  SITE_NAME 将在 Web 界面、电子邮件报告
  和通知中显示检查项名称。
* **标识**：用于[基于标识的 ping URL](../http_api/#success-slug) 的 URL 友好标识符
  （默认基于 UUID 的 ping URL 的替代方案）。标识应仅包含
  以下字符：`a-z`、`0-9`、连字符和下划线。如果您不打算使用
  基于标识的 ping URL，可以将标识字段留空。
* **标签**：可选标签的空格分隔列表。使用标签来组织和分组
  项目内的检查项。您可以按环境
  （`prod`、`staging`、`dev` 等）、按角色（`www`、`db`、`worker` 等）或使用
  任何其他系统来标记检查项。
* **描述**：一个自由格式的文本字段，用于为您的团队
  或您自己保存相关信息。描述 cron 作业的角色、谁设置的、
  失败时该怎么做，以及到哪里查找更多信息。

## 简单计划

SITE_NAME 支持三种类型的计划：**Simple**、**Cron** 和 **OnCalendar**。
使用 Simple 计划来监控您期望以相对规律的间隔运行的进程：
每小时一次、每天一次、每周一次等。

![编辑周期和宽限期](IMG_URL/edit_simple_schedule.png)

对于简单计划，您可以配置两个参数：周期和宽限期。

* **周期**是 ping 之间的预期时间。
* **宽限期**是在检查项延迟时发送警报前额外等待的时间。
  使用此参数来考虑任务执行时间中微小、预期的偏差。

注意：如果您使用"start"信号来[测量任务运行时间](../measuring_script_run_time/)，
则宽限期还指定了"start"和"success"信号之间允许的最大时间间隔。
每当 SITE_NAME 收到"start"信号时，它期望在宽限期内收到后续的
"success"信号。如果 success 信号未在配置的宽限期内到达，
SITE_NAME 将把检查项标记为失败并发出警报。

## Cron 计划

使用"Cron"来监控 cron 作业和其他具有更复杂计划的进程。
此监控模式确保作业**在正确的时间**运行，而不仅仅是
在正确的时间间隔运行。

有关 cron 表达式语法示例，请参阅 [Cron 语法速查表](../cron/)。
有关完整的 cron 语法参考，请参阅 [crontab(5) man page](https://www.man7.org/linux/man-pages/man5/crontab.5.html)。

![编辑 cron 计划](IMG_URL/edit_cron_schedule.png)

您需要指定 cron 表达式、服务器的时区和宽限期。

* **Cron 表达式**是您在 crontab 中指定的 cron 表达式。
* **服务器的时区**是您的服务器所在的时区。cron 守护进程通常使用
  系统的本地时间。如果机器不使用 UTC 时区，请在此处指定其
  时区。
* **宽限期**，与简单计划相同，是在发送延迟检查项
  警报前等待的时间。

## OnCalendar 计划

使用"OnCalendar"计划来监控使用 `OnCalendar=` 计划的 systemd 定时器。
与 systemd 定时器一样，您可以指定多个 `OnCalendar` 表达式
（用换行符分隔，每行一个计划），SITE_NAME 将在
任何计划匹配时预期收到 ping。

有关完整的 OnCalendar 语法参考，请参阅 [systemd.time(7) man page](https://www.man7.org/linux/man-pages/man7/systemd.time.7.html#CALENDAR_EVENTS)。

![编辑 cron 计划](IMG_URL/edit_oncalendar_schedule.png)

## 过滤规则 {: #filtering-rules }

在"Filtering Rules"对话框中，您可以控制 SITE_NAME 如何处理
特定检查项的传入 ping 的几个高级方面。

![设置过滤规则](IMG_URL/filtering_rules.png)

* **允许的 HTTP 请求方法**。您可以要求 ping
  请求使用 HTTP POST。如果您在通过电子邮件发送或发布到聊天时遇到
  预览机器人点击 ping URL 的问题，请使用"Only POST"选项。
* **内容过滤**。您可以指示 SITE_NAME 在电子邮件 ping 的
  主题行或消息正文中，以及在 HTTP ping 的 HTTP 请求体中
  查找特定关键字。
* **Ping 已暂停的检查项**。通常，当您 ping 已暂停的检查项时，它会离开
  暂停状态并进入"up"状态（或在
  [failure 信号](../signaling_failures/)的情况下进入"down"状态）。
  您可以通过选择"Ignore the ping, stay in
  the paused state"选项来更改此行为。选择此选项后，暂停状态变为"粘性"：
  SITE_NAME 将忽略所有传入的 ping，直到您显式*恢复*检查项。

### 内容过滤

如果选中了 **HTTP 请求的请求体** 选项，SITE_NAME 将通过
在请求体的前 PING_BODY_LIMIT_FORMATTED 中查找关键字来将
HTTP ping 分类为 start、success 或 failure 信号。

如果选中了**电子邮件的主题行**或**电子邮件的消息正文**
选项，SITE_NAME 将通过查找主题行和/或消息正文中的关键字来将
电子邮件 ping 分类为 start、success 或 failure 信号。
SITE_NAME 支持 HTML 电子邮件：在消息正文中查找关键字时，它会检查
电子邮件的纯文本和 HTML 版本。

您可以在 **Start Keywords**、**Success Keywords** 和 **Failure Keywords** 字段中
通过逗号分隔指定多个关键字。关键字匹配区分大小写
（例如，"error"和"ERROR"是不同的关键字）。

SITE_NAME 按特定顺序查找关键字：

* 它首先查找 **failure 关键字**。如果找到任何关键字，则将 ping
  分类为 failure 信号，不再继续查找。
* 然后查找 **success 关键字**。如果找到任何关键字，则将 ping
  分类为 success 信号，不再继续查找。
* 然后查找 **start 关键字**。如果找到任何关键字，则将 ping
  分类为 start 信号。
* 最后，如果没有找到匹配的关键字，SITE_NAME 将忽略 ping 或
  将其分类为 failure 信号，具体取决于 **If no keywords match**
  配置选项。被忽略的 ping 在事件日志中显示为"Ignored"标签，
  但它们不会影响检查项的状态，因为它们既不是"success"也不是"failure"
  更不是"start"信号。

示例用例：考虑一个每次完成时发送 HTTP POST 请求的备份 cron 作业。
如果作业成功完成，HTTP 请求将包含
文本"Backup successful"。如果作业失败，请求体将包含
错误消息。错误消息可能各不相同，并且无法预知所有可能错误消息的
完整列表。要处理此场景，您可以如下使用内容过滤：

* 启用 **HTTP 请求的请求体**——启用 HTTP ping 的内容过滤。
* 在 **Success keywords** 字段中输入"Backup successful"——如果在
  HTTP ping 的请求体中找到此字符串，SITE_NAME 将把 ping 分类为 success
  信号。
* 选择 **If no keywords match: Classify the ping as failure** 选项——SITE_NAME
  将把所有其他 HTTP 请求分类为 failure 信号。

使用这些设置，SITE_NAME 将把 HTTP ping 分类为 success 信号
当且仅当请求体包含文本"Backup successful"。如果请求
体不包含此字符串（或根本没有请求体），
它将把 ping 分类为 failure 信号。
