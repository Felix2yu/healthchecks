# Slug URL

SITE_NAME 提供两种不同的 URL 格式用于发送 ping HTTP 请求：
UUID URL 和 slug URL。

## UUID URL 快速回顾

基于 UUID 的 ping URL 是 SITE_NAME 中使用较早且默认的 ping URL 格式。
系统中的每个检查项都有自己唯一且不可变的 UUID。要发送 success 信号
（"ping"），客户端向 `PING_ENDPOINT` 发起请求，并在末尾添加检查项的 UUID。
示例：

<pre>
PING_ENDPOINT<b>d1665499-e827-441f-bf13-8f15e8f4c0b9</b>
</pre>

要发送 start、failure 或特定退出状态信号，以及记录诊断
消息，客户端可以在 UUID 后添加更多内容：

<pre>
PING_ENDPOINTd1665499-e827-441f-bf13-8f15e8f4c0b9<b>/start</b>
PING_ENDPOINTd1665499-e827-441f-bf13-8f15e8f4c0b9<b>/fail</b>
PING_ENDPOINTd1665499-e827-441f-bf13-8f15e8f4c0b9<b>/123</b>
PING_ENDPOINTd1665499-e827-441f-bf13-8f15e8f4c0b9<b>/log</b>
</pre>

这在概念上简单且运行良好。基于 UUID 的 ping URL 不需要额外的
认证——UUID 值本身就是认证，而 UUID 地址空间如此
巨大，没人能通过随机猜测找到有效的 ping URL。

基于 UUID 的 ping URL 有一些缺点：

* UUID 不太友好人类。除非您擅长记忆 UUID，
  否则仅通过查看很难将 ping URL 与检查项关联起来。而且
  在复制粘贴 UUID 时很容易出错。
* 每个 UUID 都是一个秘密。因此，如果您有很多东西要监控，您将需要
  管理许多秘密。

## Slug URL

Slug URL 是自 2021 年引入的一种可选的替代 URL 格式。在 slug URL 中，
我们使用两个可变组件，**ping key** 和 **标识**，而不是使用 UUID：

<pre>
PING_ENDPOINT<b>&lt;ping-key&gt;</b>/<b>&lt;slug&gt;</b>
</pre>

以下是一个具体示例：

<pre>
PING_ENDPOINT<b>fqOOd6-F4MMNuCEnzTU01w</b>/<b>db-backups</b>
</pre>

Slug URL 支持 start 和 failure 信号，方式与 UUID URL 相同：

<pre>
PING_ENDPOINTfqOOd6-F4MMNuCEnzTU01w/db-backups<b>/start</b>
PING_ENDPOINTfqOOd6-F4MMNuCEnzTU01w/db-backups<b>/fail</b>
PING_ENDPOINTfqOOd6-F4MMNuCEnzTU01w/db-backups<b>/123</b>
PING_ENDPOINTfqOOd6-F4MMNuCEnzTU01w/db-backups<b>/log</b>
</pre>

单个项目中的所有检查项共享相同的 ping key。Ping key 是您必须管理的
用于 ping 项目中任何检查项的唯一机密。您可以在项目设置的
"Settings"页面中，紧挨着项目 API 密钥的位置查找或创建
ping key：

![项目设置页面中的 Ping Key](IMG_URL/project_settings_ping_key.png)

URL 的标识部分（`db-backups`）由用户（您）选择。您可以选择
描述性、人类可读的值。与 UUID 不同，每个检查项的标识是可变的；
您可以在创建检查项后更新现有检查项的标识。

标识中允许的字符为小写 ASCII 字母（`a-z`）、
数字（`0-9`）、下划线（`_`）和连字符（`-`）。

Slug URL 的安全性依赖于 ping key。这意味着您可以将标识
值硬编码在脚本中、提交到版本控制，甚至公开分享，而无需
担心来自爬虫、内容扫描机器人和随机
好奇人员的意外 ping 请求。

与 UUID URL 相比：

* 您可以选择描述性、人类可读的标识值。您可以更改现有
  检查项的标识。
* 您可以使用单个秘密（ping key）监控多个进程。
* Slug URL 支持[检查项自动配置功能](../autoprovisioning/)。

## 重复标识值

SITE_NAME 不强制您选择唯一的标识值。如果多个检查项具有相同的
标识，它们将具有相同的基于标识的 ping URL。如果您向该 URL 发送 HTTP 请求，
您将收到 HTTP 409 响应，响应正文中包含文本"ambiguous slug"。
当然，这些检查项的基于 UUID 的 ping URL 仍然有效。

SITE_NAME 的 Web 界面也会警告您任何具有相同标识的检查项：

![检查项列表页面显示"重复标识"提示](IMG_URL/duplicate_slugs.png)

## UUID / Slug 选择器

SITE_NAME 在检查项列表中显示"UUID / Slug"选择器：

![检查项列表页面中的 uuid / slug 选择器](IMG_URL/checks_uuid_slug_selector.png)

并且在每个检查项的详情页面中也显示：

![检查项详情页面中的 uuid / slug 选择器](IMG_URL/details_uuid_slug_selector.png)

选择器让您选择在 Web 界面中显示的 URL 格式。
它仅控制显示值，不影响 ping API 的操作：
SITE_NAME 将接受使用任一格式的 ping 请求，无论
选择器的值如何。
