# 附加日志

SITE_NAME ping 端点接受 HTTP HEAD、GET 和 POST 请求方法。

使用 HTTP POST 时，**您可以在请求体中包含任意载荷**。
SITE_NAME 将记录请求体的前 PING_BODY_LIMIT_FORMATTED（PING_BODY_LIMIT 字节），
以便您稍后检查。

## 记录命令输出

在此示例中，我们运行 `certbot renew`，捕获其输出（stdout
和 stderr 流），并将捕获的输出提交到 SITE_NAME：

```bash
#!/bin/sh

m=$(/usr/bin/certbot renew 2>&1)
curl -fsS -m 10 --retry 5 --data-raw "$m" PING_URL
```

我们可以扩展前面的示例，根据退出代码发送 success 或 failure
信号：

```bash
#!/bin/sh

m=$(/usr/bin/certbot renew 2>&1)
curl -fsS -m 10 --retry 5 --data-raw "$m" PING_URL/$?
```

如果命令产生大量输出，您可能会遇到以下错误：

```
/usr/bin/curl: Argument list too long
```

在这种情况下，一种解决方法是保存输出到临时文件，
然后告诉 curl 将文件作为请求体发送：

```bash
#!/bin/sh

/usr/bin/certbot renew > /tmp/certbot-renew.log 2>&1
curl -fsS -m 10 --retry 5 --data-binary @/tmp/certbot-renew.log PING_URL/$?
```

## 使用 Runitor

[Runitor](https://github.com/bdd/runitor) 是一个第三方工具，用于运行
提供的命令，捕获其输出并报告给 SITE_NAME。
它还测量执行时间并在临时错误时重试 HTTP 请求。
最棒的是，语法简单明了：

```bash
runitor -uuid your-uuid-here -- /usr/bin/certbot renew
```

## 发送日志而不发送 Success 或 Failure 信号

您有时可能希望记录诊断信息而不改变检查项的
当前状态。SITE_NAME 为此提供了 [/log 端点](../http_api#log-uuid)。
当您向此端点发送 HTTP POST 请求时，SITE_NAME 将记录该事件
并在检查项的"Events"部分显示，但保持检查项的状态不变。

## 处理超过 PING_BODY_LIMIT_FORMATTED 的日志

虽然 SITE_NAME 可以在紧急情况下存储少量日志，但它并非专门
为此而设计。如果您遇到日志被截断的问题，请考虑
以下选项：

* 查看是否可以让日志不那么冗长。例如，如果您有一个批处理任务
  每处理一个项目就输出一行文本，也许它可以输出一个包含总计的摘要。
* 如果重要内容通常在末尾，则提交**最后 PING_BODY_LIMIT_FORMATTED**
  而不是开头。以下示例提交 `dmesg` 输出的最后 PING_BODY_LIMIT_FORMATTED：

```bash
#!/bin/sh

m=$(dmesg | tail --bytes=PING_BODY_LIMIT)
curl -fsS -m 10 --retry 5 --data-raw "$m" PING_URL
```

* 最后，如果捕获完整日志输出至关重要，
  请考虑使用专门的日志聚合服务来捕获日志。

## 在哪里查看捕获的日志

在检查项的详情页面中，Events 部分，点击单个事件以查看
完整的事件详情，包括捕获的日志信息。

![Events 部分](IMG_URL/events.png)

在打开的对话框中，使用"Download Original"链接下载请求
体数据，完全按照提交到 SITE_NAME 的原始内容：

![Ping 详情对话框](IMG_URL/ping_details.png)
