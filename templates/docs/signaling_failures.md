# 发送故障信号

您可以通过略微更改 ping URL 来向 SITE_NAME 主动发送故障信号：
在正常的 ping URL 后追加 `/fail` 或 `/{exit-status}`。
退出状态应为 0-255 的整数。SITE_NAME 将
退出状态 0 解释为成功，所有非零值为失败。

示例：

```bash

# 通过追加 /fail 后缀报告失败：
curl --retry 3 PING_URL/fail

# 通过追加非零退出状态报告失败：
curl --retry 3 PING_URL/1
```

通过主动向 SITE_NAME 发送故障信号，您可以最大程度地缩短从
被监控服务遇到问题到您收到通知之间的延迟。

或者，如果为 success 和 failure 信号使用不同的 URL
不可行，您可以配置 SITE_NAME 通过
[在 HTTP 请求体中查找特定关键字](../configuring_checks/#filtering-rules)
来将 HTTP ping 分类为 success 或 failure 信号。

## Shell 脚本

下面的 shell 脚本将 `$?`（一个包含最后执行命令
退出状态的特殊变量）追加到 ping URL：

```bash
#!/bin/sh

/usr/bin/certbot renew
curl --retry 3 PING_URL/$?

```

## Python

下面是一个 Python 骨架代码示例，当 work 函数返回意外值或抛出异常时
发出故障信号：

```python
import requests
URL = "PING_URL"

def do_work():
    # 在此处进行您的数字运算、备份转储、新闻通讯发送等工作。
    # 成功时返回真值。
    # 失败时返回假值或抛出异常。
    return True

success = False
try:
    success = do_work()
finally:
    # 成功时，请求 PING_URL
    # 失败时，请求 PING_URL/fail
    requests.get(URL if success else URL + "/fail")
```
