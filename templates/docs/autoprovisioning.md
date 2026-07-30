# 自动配置

你可以指示 SITE_NAME 在首次收到 ping 时自动创建缺失的检查项。
要启用自动配置，请使用基于标识的 ping 端点，并在末尾附加 `?create=1`：

```bash
# 做一些工作
sleep 5
# 向 SITE_NAME 发送成功信号
curl -m 10 --retry 5 PING_ENDPOINTmy-ping-key/srv01?create=1
```

在此示例中，SITE_NAME 将查找具有 Ping Key `my-ping-key` 的项目，
并检查其中是否存在标识为 `srv01` 的检查项。

* 如果检查项尚不存在，SITE_NAME 将创建它，ping 它，并返回 HTTP 201 响应。
* 如果检查项已存在，SITE_NAME 将 ping 它并返回 HTTP 200 响应。

自动配置适用于所有基于标识的 ping 端点：

* [成功](../http_api/#success-slug)
* [开始](../http_api/#start-slug)
* [失败](../http_api/#fail-slug)
* [日志](../http_api/#log-slug)
* [退出状态](../http_api/#exitcode-slug)

自动配置在处理动态基础设施时非常方便：如果你将 Ping Key 分发给
你的监控客户端，每个客户端可以选择自己的标识（例如，从服务器的主机名派生），
构造一个 ping URL，并在发送其第一个 ping 时"即时"向 SITE_NAME 注册。

## 自动配置的检查项使用默认配置

通过自动配置创建的检查项将使用默认参数：

* 周期：1 天。
* 宽限期：1 小时。
* 所有集成已启用。

目前无法通过 ping URL 指定自定义周期、宽限期或其他参数。
如果你需要更改任何参数，你需要通过 Web 仪表盘或
[Management API](../api/) 来进行。

## 自动配置与账户限制

每个 SITE_NAME 账户都有允许创建的检查项数量的特定限制：
免费账户 20 个检查项；付费账户 100 或 1000 个检查项。为了减少
摩擦和静默失败的风险，自动配置功能**允许临时超出账户检查项
限制最多两倍**。也就是说，如果你的账户已经达到上限，自动配置
仍然能够创建新的检查项，直到达到限制的两倍。