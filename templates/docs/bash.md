# Shell 脚本

你可以轻松地为 shell 脚本添加 SITE_NAME 监控。只需在脚本中的适当位置发起 HTTP 请求即可。
[curl](https://curl.haxx.se/docs/manpage.html) 和
[wget](https://www.gnu.org/software/wget/manual/wget.html)
是两种常用的命令行 HTTP 客户端。

```bash
# 使用 curl 发送 HTTP GET 请求：
curl -m 10 --retry 5 PING_URL

# 静默版本（除非 curl 遇到错误，否则不输出 stdout/stderr）：
curl -fsS -m 10 --retry 5 -o /dev/null PING_URL

```

以下是每个 curl 参数的作用：

**-m &lt;seconds&gt;**
:   允许 HTTP 请求花费的最长时间（秒）。
    如果使用了 `--retry` 参数，则每次重试开始时计时器会重置。

**--retry &lt;num&gt;**
:   对于瞬时错误，最多重试这么多次。默认情况下，curl
    会在每次重试之间使用递增的延迟（1s、2s、4s、8s...）。
    另请参阅 [--retry-delay](https://curl.haxx.se/docs/manpage.html#--retry-delay)。
    瞬时错误包括：超时、HTTP 状态码 408、429、500、502、503、504。

**-f, --fail**
:   使 curl 将非 200 的响应视为错误，并
    [返回错误码 22](https://curl.se/docs/manpage.html#-f)。

**-s, --silent**
:   静默或安静模式。隐藏进度条，但也会
    隐藏错误消息。

**-S, --show-error**
:   在使用 -s 时重新启用错误消息。

**-o /dev/null**
:   将 curl 的 stdout 重定向到 /dev/null（错误消息仍会发送到 stderr）。

## 从 Shell 脚本发送故障信号

你可以将 `/fail` 或 `/{exit-status}` 附加到任何 ping URL，并使用生成的 URL
主动发送故障信号。退出状态应为 0-255 的整数。
SITE_NAME 将退出状态 0 解释为成功，所有非零值解释为失败。

以下示例运行 `/usr/bin/certbot renew`，并使用 `$?` 变量来
获取其退出状态：

```bash
#!/bin/sh

# 此处为实际任务：
/usr/bin/certbot renew
# Ping SITE_NAME
curl -m 10 --retry 5 PING_URL/$?
```

关于 Bash 脚本中管道（`command1 | command2 | command3`）的说明：默认情况下，管道的
退出状态是管道中最右侧命令的退出状态。
如果你需要管道在*任何*部分失败时返回非零退出状态，请使用 `set -o pipefail`：

```bash
#!/bin/sh

set -o pipefail
pg_dump somedb | gpg --encrypt --recipient alice@example.org --output somedb.sql.gpg
# 如果没有 pipefail，如果 pg_dump 命令失败但 gpg 成功，$? 将为 0，
# 脚本将报告成功。
# 使用 pipefail 后，如果 pg_dump 失败，脚本将报告 pg_dump 返回的退出码。
curl -m 10 --retry 5 PING_URL/$?
```

## 记录命令输出

使用 HTTP POST 进行 ping 时，可以在请求体中放入额外的诊断信息。
如果请求体看起来是有效的 UTF-8 字符串，SITE_NAME
将接受并存储请求体的前 PING_BODY_LIMIT_FORMATTED。

在下面的示例中，certbot 的输出被捕获并通过 HTTP POST 提交：

```bash
#!/bin/sh

m=$(/usr/bin/certbot renew 2>&1)
curl -fsS -m 10 --retry 5 --data-raw "$m" PING_URL
```

## 自动配置新检查项

此示例使用 SITE_NAME 的[自动配置功能](../autoprovisioning/)来
在检查项尚不存在时"即时"创建。使用此技术，你可以
编写在首次运行时自动向 SITE_NAME 注册的服务。

```bash
#!/bin/bash

PING_KEY=fixme-your-ping-key-here

# 使用系统的主机名作为检查项的标识
SLUG=$(hostname)

# 构造 ping URL 并在末尾追加 "?create=1"：
URL=PING_ENDPOINT$PING_KEY/$SLUG?create=1

# 发送 ping：
curl -m 10 --retry 5 $URL
```
