# Ping API

通过 Ping API，你可以从你的系统发送 **success（成功）**、**start（开始）**、**failure（失败）**
和 **log（日志）** 信号。

## 通用说明

所有 ping 端点支持：

* HTTP 和 HTTPS
* HTTP 1.0、HTTP 1.1 和 HTTP 2
* IPv4 和 IPv6
* HEAD、GET 和 POST 请求方法。对于 HTTP POST 请求，客户端可以选择性地在请求体中包含诊断信息。
如果请求体看起来是有效的 UTF-8 字符串，SITE_NAME 会存储请求体（每个接收到的 ping
限制为前 PING_BODY_LIMIT_FORMATTED）。

成功的响应将包含 "200 OK" HTTP 响应状态码，并在响应体中包含简短的 "OK" 字符串。

## UUID 和标识

每个 Ping API 请求需要唯一标识一个检查项。
SITE_NAME 支持两种标识检查项的方式：通过检查项的 UUID
或通过项目的 Ping Key 和检查项的标识的组合。

**检查项的 UUID** 在创建检查项时自动分配。它是
不可变的。你不能用手动选择的 UUID 替换自动分配的 UUID。
当你删除一个检查项时，你会失去其 UUID 且无法找回。

你可以通过 Web UI 或 [Management API](../api/) 调用查看检查项的 UUID。

**检查项的标识**可以由用户选择。标识只能包含以下
字符：`a-z`、`0-9`、连字符和下划线。通常的做法是
从检查项的名称派生标识（例如，名为"Database Backup"的检查项
可能具有标识"database-backup"），但用户可以自由选择任意标识值。

检查项的标识**可以更改**，通过 Web 界面或使用
[Management API](../api/) 调用。

检查项的标识**不保证唯一**。如果你使用非唯一的标识发起 Ping API 请求，
SITE_NAME 将返回"409 Conflict" HTTP 状态码并忽略该请求。

标识 URL 可选地支持**自动配置**：如果你向一个没有对应检查项的标识
发起 Ping API 请求，SITE_NAME 将自动创建检查项。
自动配置默认关闭。要启用它，请在 ping URL 中添加 `create=1` 查询参数。

## 频率限制

请善待我们的服务器。不要过于频繁地 ping 检查项。
如果你每分钟 ping 检查项超过 5 次，某些请求可能会被限速
且不会记录到数据库。在极端情况下，我们会屏蔽客户端的
IP 地址。

## 端点

端点名称                                               | 端点地址
------------------------------------------------------------|-------
[成功 (UUID)](#success-uuid)       | `PING_ENDPOINT<uuid>`
[开始 (UUID)](#start-uuid)           | `PING_ENDPOINT<uuid>/start`
[失败 (UUID)](#fail-uuid)          | `PING_ENDPOINT<uuid>/fail`
[日志 (UUID)](#log-uuid)               | `PING_ENDPOINT<uuid>/log`
[报告脚本退出状态 (UUID)](#exitcode-uuid)           | `PING_ENDPOINT<uuid>/<exit-status>`
[成功 (标识)](#success-slug)       | `PING_ENDPOINT<ping-key>/<slug>`
[开始 (标识)](#start-slug)           | `PING_ENDPOINT<ping-key>/<slug>/start`
[失败 (标识)](#fail-slug)          | `PING_ENDPOINT<ping-key>/<slug>/fail`
[日志 (标识)](#log-slug)               | `PING_ENDPOINT<ping-key>/<slug>/log`
[报告脚本退出状态 (标识)](#exitcode-slug)           | `PING_ENDPOINT<ping-key>/<slug>/<exit-status>`

## 使用 UUID 发送"success"信号 {: #success-uuid .rule }

```text
HEAD|GET|POST PING_ENDPOINT<uuid>
```

向 SITE_NAME 发送信号，表示任务已成功完成（或者
持续运行的过程仍在运行且健康）。

SITE_NAME 通过 URL 中的 UUID 值来标识检查项。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。如果指定了运行 ID，
    SITE_NAME 使用它来匹配此 ping 对应的正确开始 ping 并
    计算准确的持续时间。值必须是客户端选择的 UUID，
    采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

404 not found
:   找不到具有指定 UUID 的检查项。

**示例**

```http
GET /5bf66975-d4c7-4bf5-bcc8-b8d8a82ea278 HTTP/1.0
Host: hc-ping.com
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

## 使用 UUID 发送"start"信号 {: #start-uuid .rule }

```text
HEAD|GET|POST PING_ENDPOINT<uuid>/start
```

向 SITE_NAME 发送"任务已开始！"消息。发送"start"信号是可选的，
但它启用了一些额外功能：

* SITE_NAME 将测量并显示任务执行时间
* SITE_NAME 将检测任务是否运行超过其配置的宽限期

SITE_NAME 通过 URL 中的 UUID 值来标识检查项。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。如果指定了运行 ID，
    SITE_NAME 使用它来匹配此 ping 对应的正确完成 ping
    并计算准确的持续时间。值必须是客户端选择的 UUID，
    采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

404 not found
:   找不到具有指定 UUID 的检查项。

**Example**

```http
GET /5bf66975-d4c7-4bf5-bcc8-b8d8a82ea278/start HTTP/1.0
Host: hc-ping.com
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

## 使用 UUID 发送"failure"信号 {: #fail-uuid .rule }

```text
HEAD|GET|POST PING_ENDPOINT<uuid>/fail
```

向 SITE_NAME 发送信号，表示任务已失败。主动发送故障信号
最大程度地缩短从被监控服务失败到收到警报的延迟。

SITE_NAME 通过 URL 中的 UUID 值来标识检查项。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。如果指定了运行 ID，
    SITE_NAME 使用它来匹配此 ping 对应的正确开始 ping 并
    计算准确的持续时间。值必须是客户端选择的 UUID，
    采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

404 not found
:   找不到具有指定 UUID 的检查项。

**Example**

```http
GET /5bf66975-d4c7-4bf5-bcc8-b8d8a82ea278/fail HTTP/1.0
Host: hc-ping.com
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

## 使用 UUID 发送"log"信号 {: #log-uuid .rule }

```text
HEAD|GET|POST PING_ENDPOINT<uuid>/log
```

向 SITE_NAME 发送日志信息，而不发送 success 或 failure 信号。
SITE_NAME 将记录该事件并在检查项的"Events"部分以"Log"标签显示。
检查项的状态将保持不变。

SITE_NAME 通过 URL 中的 UUID 值来标识检查项。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。值必须是客户端选择的
    UUID，采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

404 not found
:   找不到具有指定 UUID 的检查项。

**Example**

```http
POST /5bf66975-d4c7-4bf5-bcc8-b8d8a82ea278/log HTTP/1.1
Host: hc-ping.com
Content-Type: text/plain
Content-Length: 11

Hello World
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

## 报告脚本退出状态（使用 UUID）{: #exitcode-uuid .rule }

```text
HEAD|GET|POST PING_ENDPOINT<uuid>/<exit-status>
```

根据 URL 中包含的退出状态发送 success 或 failure 信号。
退出状态是 0-255 的整数。SITE_NAME
将 0 解释为成功，所有其他值解释为失败。

SITE_NAME 通过 URL 中的 UUID 值来标识检查项。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。如果指定了运行 ID，
    SITE_NAME 使用它来匹配此 ping 对应的正确开始 ping 并
    计算准确的持续时间。值必须是客户端选择的 UUID，
    采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

400 invalid url format
:   URL 不符合预期格式。

404 not found
:   找不到具有指定 UUID 的检查项。

**示例**

```http
GET /5bf66975-d4c7-4bf5-bcc8-b8d8a82ea278/1 HTTP/1.0
Host: hc-ping.com
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

## 使用标识发送"success"信号 {: #success-slug .rule }

```text
HEAD|GET|POST PING_ENDPOINT<ping-key>/<slug>
```

向 SITE_NAME 发送信号，表示任务已成功完成（或者
持续运行的过程仍在运行且健康）。

SITE_NAME 通过 URL 中项目的 ping key 和检查项的标识
来标识检查项。标识应仅包含小写 ASCII 字母（`a-z`）、
数字（`0-9`）、下划线（`_`）和连字符（`-`）。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

create=0|1
:   可选，默认为"0"。如果设置为"1"，并且 URL 中的标识与
    项目中的任何现有检查项都不匹配，SITE_NAME 会自动创建一个新的检查项。

    示例：`create=1`

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。如果指定了运行 ID，
    SITE_NAME 使用它来匹配此 ping 对应的正确开始 ping，并
    计算准确的持续时间。值必须是客户端选择的 UUID，
    采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

201 Created
:   自动创建了新的检查项，请求成功。

400 invalid url format
:   URL 不符合预期格式。

404 not found
:   找不到具有指定 ping key 和标识组合的检查项。

409 ambiguous slug
:   标识不明确，匹配了多个检查项。

**Example**

```http
GET /fqOOd6-F4MMNuCEnzTU01w/database-backup HTTP/1.0
Host: hc-ping.com
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

## 使用标识发送"start"信号 {: #start-slug .rule }

```text
HEAD|GET|POST PING_ENDPOINT<ping-key>/<slug>/start
```

向 SITE_NAME 发送"任务已开始！"消息。发送"start"信号是
可选的，但它启用了一些额外功能：

* SITE_NAME 将测量并显示任务执行时间
* SITE_NAME 将检测任务是否运行超过其配置的宽限期

SITE_NAME 通过 URL 中项目的 ping key 和检查项的标识
来标识检查项。标识应仅包含小写 ASCII 字母（`a-z`）、
数字（`0-9`）、下划线（`_`）和连字符（`-`）。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

create=0|1
:   可选，默认为"0"。如果设置为"1"，并且 URL 中的标识与
    项目中的任何现有检查项都不匹配，SITE_NAME 会自动创建一个新的检查项。

    示例：`create=1`

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。如果指定了运行 ID，
    SITE_NAME 使用它来匹配此 ping 对应的正确完成 ping，
    并计算准确的持续时间。值必须是客户端选择的 UUID，
    采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

201 Created
:   自动创建了新的检查项，请求成功。

400 invalid url format
:   URL 不符合预期格式。

404 not found
:   找不到具有指定 ping key 和标识组合的检查项。

409 ambiguous slug
:   标识不明确，匹配了多个检查项。

**Example**

```http
GET /fqOOd6-F4MMNuCEnzTU01w/database-backup/start HTTP/1.0
Host: hc-ping.com
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

## 使用标识发送"failure"信号 {: #fail-slug .rule }

```text
HEAD|GET|POST PING_ENDPOINT<ping-key/<slug>/fail
```

向 SITE_NAME 发送信号，表示任务已失败。主动发送故障信号
最大程度地缩短从被监控服务失败到收到警报的延迟。

SITE_NAME 通过 URL 中项目的 ping key 和检查项的标识
来标识检查项。标识应仅包含小写 ASCII 字母（`a-z`）、
数字（`0-9`）、下划线（`_`）和连字符（`-`）。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

create=0|1
:   可选，默认为"0"。如果设置为"1"，并且 URL 中的标识与
    项目中的任何现有检查项都不匹配，SITE_NAME 会自动创建一个新的检查项。

    示例：`create=1`

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。如果指定了运行 ID，
    SITE_NAME 使用它来匹配此 ping 对应的正确开始 ping，并
    计算准确的持续时间。值必须是客户端选择的 UUID，
    采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

201 Created
:   自动创建了新的检查项，请求成功。

400 invalid url format
:   URL 不符合预期格式。

404 not found
:   找不到具有指定 ping key 和标识组合的检查项。

409 ambiguous slug
:   标识不明确，匹配了多个检查项。

**Example**

```http
GET /fqOOd6-F4MMNuCEnzTU01w/database-backup/fail HTTP/1.0
Host: hc-ping.com
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

## 使用标识发送"log"信号 {: #log-slug .rule }

```text
HEAD|GET|POST PING_ENDPOINT<ping-key/<slug>/log
```

向 SITE_NAME 发送日志信息，而不发送 success 或 failure 信号。
SITE_NAME 将记录该事件并在检查项的"Events"部分以"Log"标签显示。
检查项的状态将保持不变。

SITE_NAME 通过 URL 中项目的 ping key 和检查项的标识
来标识检查项。标识应仅包含小写 ASCII 字母（`a-z`）、
数字（`0-9`）、下划线（`_`）和连字符（`-`）。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

create=0|1
:   可选，默认为"0"。如果设置为"1"，并且 URL 中的标识与
    项目中的任何现有检查项都不匹配，SITE_NAME 会自动创建一个新的检查项。

    示例：`create=1`

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。值必须是客户端选择的 UUID，
    采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

201 Created
:   自动创建了新的检查项，请求成功。

404 not found
:   找不到具有指定 ping key 和标识组合的检查项。

409 ambiguous slug
:   标识不明确，匹配了多个检查项。

**Example**

```http
POST /fqOOd6-F4MMNuCEnzTU01w/database-backup/log HTTP/1.1
Host: hc-ping.com
Content-Type: text/plain
Content-Length: 11

Hello World
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

## 报告脚本退出状态（使用标识）{: #exitcode-slug .rule }

```text
HEAD|GET|POST PING_ENDPOINT<ping-key>/<slug>/<exit-status>
```

根据 URL 中包含的退出状态发送 success 或 failure 信号。
退出状态是 0-255 的整数。SITE_NAME
将 0 解释为成功，所有其他值解释为失败。

SITE_NAME 通过 URL 中项目的 ping key 和检查项的标识
来标识检查项。标识应仅包含小写 ASCII 字母（`a-z`）、
数字（`0-9`）、下划线（`_`）和连字符（`-`）。

响应可能可选地包含 `Ping-Body-Limit: <n>` 响应头。
如果存在此头，其值为整数，指定 SITE_NAME 每次请求
将存储请求体中的多少字节。例如，如果 n=100，
但客户端在请求体中发送了 123 字节，SITE_NAME 将存储前
100 字节并忽略剩余的 23 字节。客户端可以使用此头来决定
后续请求的请求体中发送多少数据。

### 查询参数

create=0|1
:   可选，默认为"0"。如果设置为"1"，并且 URL 中的标识与
    项目中的任何现有检查项都不匹配，SITE_NAME 会自动创建一个新的检查项。

    示例：`create=1`

rid=&lt;uuid&gt;
:   可选，指定此 ping 的运行 ID。如果指定了运行 ID，
    SITE_NAME 使用它来匹配此 ping 对应的正确开始 ping，并
    计算准确的持续时间。值必须是客户端选择的 UUID，
    采用规范的文本表示形式。

    示例：`rid=123e4567-e89b-12d3-a456-426614174000`。

### 响应码

200 OK
:   请求成功。

201 Created
:   自动创建了新的检查项，请求成功。

400 invalid url format
:   URL 不符合预期格式。

404 not found
:   找不到与指定 ping key 匹配的项目。

409 ambiguous slug
:   标识不明确，匹配了多个检查项。

**Example**

```http
GET /fqOOd6-F4MMNuCEnzTU01w/database-backup/1 HTTP/1.0
Host: hc-ping.com
```

```http
HTTP/1.1 200 OK
Server: nginx
Date: Wed, 29 Jan 2020 09:58:23 GMT
Content-Type: text/plain; charset=utf-8
Content-Length: 2
Connection: close
Access-Control-Allow-Origin: *
Ping-Body-Limit: PING_BODY_LIMIT

OK
```

