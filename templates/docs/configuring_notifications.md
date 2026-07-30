# 配置通知

您可以设置多种方式来接收帐户中检查项状态变化时的通知。
这样做有几个好处：

* **通知失败时的冗余。** 使用两个不同的通知渠道（例如，电子邮件和 Slack）设置通知。如果一个传输
  失败（例如，电子邮件进入垃圾邮件箱），您仍然可以通过
  其他渠道收到通知。
* **根据紧急程度使用不同的通知方法。** 例如，如果
  低优先级的日常维护脚本失败，在聊天中发布消息。如果重要服务失败，
  在聊天中发布消息、发送电子邮件并发送短信。
* 将通知路由到正确的人员。

每个通知方法（"集成"）属于一个项目：
如果您想在多个项目中使用同一个通知方法，您必须在每个项目中
单独设置。

Web 界面中的"Checks"页面显示了每个检查项启用了哪些警报
方法的视觉概览。您可以点击图标来开启和关闭它们：

<video autoplay loop muted playsinline>
  <source src="IMG_URL/checks_integrations.webm" type="video/webm">
</video>

您也可以通过点击每个检查项详情页面上的"ON"/"OFF"标签来切换
集成：

<video autoplay loop muted playsinline>
  <source src="IMG_URL/details_integrations.webm" type="video/webm">
</video>

## SMS、WhatsApp 和电话月度配额

SITE_NAME 对每个帐户每月可以发送的 SMS、WhatsApp 和电话
通知的最大数量设置了配额。具体限制取决于
帐户的计费计划。配额在每个月开始时自动重置。
上个月的"未使用"发送次数不会结转到下个月。

当帐户超过其月度限制时，SITE_NAME 将：

* 向帐户的主电子邮件地址发送警告邮件
* 在 **Integrations** 页面上显示警告消息

## 重复通知

如果您想在特定检查项宕机期间持续接收重复通知，
您有几种不同的选择：

* 如果您使用**事件管理系统**（PagerDuty、Splunk On-Call、Opsgenie、
  PagerTree），您可以在那里设置升级规则。
* 使用 **Pushover** 集成并选择"Emergency"优先级。Pushover 将
  每隔 5 分钟在您的手机上播放响亮的通知声音，直到通知
  得到确认。
* 如果任何项目中的任何检查项宕机，SITE_NAME 可以发送**每小时或每日的电子邮件提醒**。
  在[帐户设置 › 电子邮件报告](../../accounts/profile/notifications/)中设置它们：

![电子邮件提醒选项](IMG_URL/email_reports.png)

## 每周和每月报告

SITE_NAME 发送定期的电子邮件报告，要么在每月初（月度）
要么每周一（每周）。使用它们来确保所有检查项都处于预期状态，
没有"遗漏"任何问题。

报告列出您所有项目中的检查项，按项目分组。
对于每个检查项，它们显示：

* 检查项的当前状态
* 过去两个月的月度宕机次数
* 过去两个月的月度总宕机时长

![月度报告示例](IMG_URL/monthly_report.png)

您可以在[帐户设置 › 电子邮件报告](../../accounts/profile/notifications/)页面
或通过点击电子邮件报告页脚的"Unsubscribe"链接来选择不接收报告。
