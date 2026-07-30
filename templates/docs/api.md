# 管理 API v3

版本:
<select onchange="document.location = this.value">
    <option value="../apiv1/">v1</option>
    <option value="../apiv2/">v2</option>
    <option value="../api/" selected>v3</option>
</select>

通过管理 API，您可以在账户中以编程方式管理检查项和集成。

## API 端点

<div id="api-toc"></div>

端点名称                                               | 端点地址
-------------------------------------------------------|-----------------
**检查项**                                              |
[列出已有检查项](#list-checks)                          | `GET SITE_ROOT/api/v3/checks/`
[获取单个检查项](#get-check)                            | `GET SITE_ROOT/api/v3/checks/<uuid>`<br>`GET SITE_ROOT/api/v3/checks/<unique_key>`
[创建新检查项](#create-check)                           | `POST SITE_ROOT/api/v3/checks/`
[更新已有检查项](#update-check)                         | `POST SITE_ROOT/api/v3/checks/<uuid>`
[暂停监控检查项](#pause-check)                          | `POST SITE_ROOT/api/v3/checks/<uuid>/pause`
[恢复监控检查项](#resume-check)                         | `POST SITE_ROOT/api/v3/checks/<uuid>/resume`
[删除检查项](#delete-check)                             | `DELETE SITE_ROOT/api/v3/checks/<uuid>`
**Ping**                                                |
[列出检查项的已记录 ping](#list-pings)                  | `GET SITE_ROOT/api/v3/checks/<uuid>/pings/`
[获取 ping 的请求体](#ping-body)                        | `GET SITE_ROOT/api/v3/checks/<uuid>/pings/<n>/body`
**状态变更**                                            |
[列出检查项的状态变更](#list-flips)                     | `GET SITE_ROOT/api/v3/checks/<uuid>/flips/`<br>`GET SITE_ROOT/api/v3/checks/<unique_key>/flips/`
**集成**                                                |
[列出已有集成](#list-channels)                          | `GET SITE_ROOT/api/v3/channels/`
**徽章**                                                |
[列出项目的徽章](#list-badges)                          | `GET SITE_ROOT/api/v3/badges/`
**服务状态**                                            |
[检查数据库连接](#status)                               | `GET SITE_ROOT/api/v3/status/`

## 与 v2 的区别

管理 API v3 增加了指定自定义检查项 slug 的功能，取代了从检查项名称自动生成 slug 的方式。[创建新检查项](#create-check)和[更新已有检查项](#update-check)接口现在接受一个新的 `slug` 参数，并使用它而非从检查项名称生成 slug。

## 认证

您向 SITE_NAME 管理 API 发出的请求必须使用 API 密钥进行认证。所有 API 密钥都是项目级别的，没有账户级别的 API 密钥。默认情况下，SITE_NAME 上的项目没有 API 密钥。您可以在**项目设置**页面上创建读写和只读 API 密钥。

读写密钥
:   对所有文档化的 API 端点具有完全访问权限。

只读密钥
:   仅适用于以下 API 端点：

    * [列出已有检查项](#list-checks)
    * [获取单个检查项](#get-check)
    * [列出检查项的状态变更](#list-flips)
    * [列出项目的徽章](#list-badges)

    在 API 响应中省略敏感信息。详情请参阅各 API 端点的文档。

客户端可以通过在 HTTP 请求中包含 `X-Api-Key: <your-api-key>` 头进行认证。或者，对于带有 JSON 请求体的 POST 请求，客户端可以在 JSON 文档中放入 `api_key` 字段。请参阅[创建新检查项](#create-check)部分的示例。

## API 请求

对于 POST 请求，SITE_NAME API 期望请求体为 JSON 文档（*不是* `multipart/form-data` 编码的表单数据）。

## API 响应

SITE_NAME 尽可能使用 HTTP 状态码。通常，2xx 表示成功，4xx 表示客户端错误，5xx 表示服务器错误。

响应可能包含带有额外数据的 JSON 文档。

## 速率限制

每分钟不要超过 100 次 API 请求。如果超过此限制，您最终会看到 HTTP 429 错误。

## 列出已有检查项 {: #list-checks .rule }

`GET SITE_ROOT/api/v3/checks/`

返回用户所属的检查项列表，可选择按一个或多个标签进行过滤。

### 查询参数

slug=&lt;value&gt;
:   过滤检查项，仅返回具有指定 slug 的检查项。如果没有匹配的检查项，则返回空列表。如果有多个匹配的检查项，则返回所有匹配项。

    示例：

    `SITE_ROOT/api/v3/checks/?slug=backups`

tag=&lt;value&gt;
:   过滤检查项，仅返回标记了指定值的检查项。

    此参数可以重复多次。

    示例：

    `SITE_ROOT/api/v3/checks/?tag=foo&tag=bar`

### 响应码

200 OK
:   请求成功。

401 Unauthorized
:   API 密钥缺失或无效。

### Example Request

```bash
curl --header "X-Api-Key: your-api-key" SITE_ROOT/api/v3/checks/
```

### Example Response

```json
{
  "checks": [
    {
      "name": "Filesystem Backup",
      "slug": "filesystem-backup",
      "tags": "backup fs",
      "desc": "Runs incremental backup every hour",
      "grace": 600,
      "n_pings": 1,
      "status": "up",
      "started": false,
      "last_ping": "2020-03-24T14:02:03+00:00",
      "next_ping": "2020-03-24T15:02:03+00:00",
      "manual_resume": false,
      "methods": "",
      "start_kw": "START",
      "success_kw": "SUCCESS",
      "failure_kw": "ERROR",
      "filter_subject": true,
      "filter_body": false,
      "filter_http_body": false,
      "filter_default_fail": false,
      "badge_url": "SITE_ROOT/b/2/1b9d0386-d07e-44b0-8995-4a9a372de43c.svg",
      "uuid": "31365bce-8da9-4729-8ff3-aaa71d56b712",
      "ping_url": "PING_ENDPOINT31365bce-8da9-4729-8ff3-aaa71d56b712",
      "update_url": "SITE_ROOT/api/v3/checks/31365bce-8da9-4729-8ff3-aaa71d56b712",
      "pause_url": "SITE_ROOT/api/v3/checks/31365bce-8da9-4729-8ff3-aaa71d56b712/pause",
      "resume_url": "SITE_ROOT/api/v3/checks/31365bce-8da9-4729-8ff3-aaa71d56b712/resume",
      "channels": "1bdea468-03bf-47b8-ab27-29a9dd0e4b94,51c6eb2b-2ae1-456b-99fe-6f1e0a36cd3c",
      "timeout": 3600
    },
    {
      "name": "Database Backup",
      "slug": "database-backup",
      "tags": "production db",
      "desc": "Runs ~/db-backup.sh",
      "grace": 1200,
      "n_pings": 7,
      "status": "down",
      "started": false,
      "last_ping": "2020-03-23T10:19:32+00:00",
      "next_ping": null,
      "manual_resume": false,
      "methods": "",
      "start_kw": "",
      "success_kw": "",
      "failure_kw": "",
      "filter_subject": false,
      "filter_body": false,
      "filter_http_body": false,
      "filter_default_fail": false,
      "badge_url": "SITE_ROOT/b/2/7d3ab93d-836e-4505-bbda-fcbd5e07adf9.svg",
      "uuid": "803f680d-e89b-492b-82ef-2be7b774a92d",
      "ping_url": "PING_ENDPOINT803f680d-e89b-492b-82ef-2be7b774a92d",
      "update_url": "SITE_ROOT/api/v3/checks/803f680d-e89b-492b-82ef-2be7b774a92d",
      "pause_url": "SITE_ROOT/api/v3/checks/803f680d-e89b-492b-82ef-2be7b774a92d/pause",
      "resume_url": "SITE_ROOT/api/v3/checks/803f680d-e89b-492b-82ef-2be7b774a92d/resume",
      "channels": "1bdea468-03bf-47b8-ab27-29a9dd0e4b94,51c6eb2b-2ae1-456b-99fe-6f1e0a36cd3c",
      "schedule": "15 5 * * *",
      "tz": "UTC"
    }
  ]
}
```

`status` 字段的可能值为：`new`、`up`、`grace`、`down` 和 `paused`。

当使用只读 API 密钥时，SITE_NAME 会从响应中省略以下字段：`uuid`、`ping_url`、`update_url`、`pause_url`、`resume_url`、`channels`。它会额外添加一个 `unique_key` 字段。`unique_key` 标识符在 API 调用之间是稳定的，您可以在[获取单个检查项](#get-check)和[列出检查项的状态变更](#list-flips) API 调用中使用它。

Example:

```json
{
  "checks": [
    {
      "name": "Filesystem Backup",
      "slug": "filesystem-backup",
      "tags": "backup fs",
      "desc": "Runs incremental backup every hour",
      "grace": 600,
      "n_pings": 1,
      "status": "up",
      "started": false,
      "last_ping": "2020-03-24T14:02:03+00:00",
      "next_ping": "2020-03-24T15:02:03+00:00",
      "manual_resume": false,
      "methods": "",
      "start_kw": "START",
      "success_kw": "SUCCESS",
      "failure_kw": "ERROR",
      "filter_subject": true,
      "filter_body": false,
      "filter_http_body": false,
      "filter_default_fail": false,
      "badge_url": "SITE_ROOT/b/2/1b9d0386-d07e-44b0-8995-4a9a372de43c.svg",
      "unique_key": "a6c7b0a8a66bed0df66abfdab3c77736861703ee",
      "timeout": 3600
    },
    {
      "name": "Database Backup",
      "slug": "database-backup",
      "tags": "production db",
      "desc": "Runs ~/db-backup.sh",
      "grace": 1200,
      "n_pings": 7,
      "status": "down",
      "started": false,
      "last_ping": "2020-03-23T10:19:32+00:00",
      "next_ping": null,
      "manual_resume": false,
      "methods": "",
      "start_kw": "",
      "success_kw": "",
      "failure_kw": "",
      "filter_subject": false,
      "filter_body": false,
      "filter_http_body": false,
      "filter_default_fail": false,
      "badge_url": "SITE_ROOT/b/2/7d3ab93d-836e-4505-bbda-fcbd5e07adf9.svg",
      "unique_key": "124f983e0e3dcaeba921cfcef46efd084576e783",
      "schedule": "15 5 * * *",
      "tz": "UTC"
    }
  ]
}
```

## 获取单个检查项 {: #get-check .rule }
`GET SITE_ROOT/api/v3/checks/<uuid>`<br>
`GET SITE_ROOT/api/v3/checks/<unique_key>`

返回单个检查项的 JSON 表示。接受检查项的 UUID 或 `unique_key`（从 UUID 派生并在使用只读 API 密钥时由 API 响应返回的字段）作为标识符。

### 响应码

200 OK
:   请求成功。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。


### 示例请求

```bash
curl --header "X-Api-Key: your-api-key" SITE_ROOT/api/v3/checks/<uuid>
```

### Example Response

```json
{
  "name": "Database Backup",
  "slug": "database-backup",
  "tags": "production db",
  "desc": "Runs ~/db-backup.sh",
  "grace": 1200,
  "n_pings": 7,
  "status": "down",
  "started": false,
  "last_ping": "2020-03-23T10:19:32+00:00",
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "start_kw": "START",
  "success_kw": "SUCCESS",
  "failure_kw": "ERROR",
  "filter_subject": true,
  "filter_body": false,
  "filter_http_body": false,
  "filter_default_fail": false,
  "badge_url": "SITE_ROOT/b/2/7d3ab93d-836e-4505-bbda-fcbd5e07adf9.svg",
  "uuid": "803f680d-e89b-492b-82ef-2be7b774a92d",
  "ping_url": "PING_ENDPOINT803f680d-e89b-492b-82ef-2be7b774a92d",
  "update_url": "SITE_ROOT/api/v3/checks/803f680d-e89b-492b-82ef-2be7b774a92d",
  "pause_url": "SITE_ROOT/api/v3/checks/803f680d-e89b-492b-82ef-2be7b774a92d/pause",
  "resume_url": "SITE_ROOT/api/v3/checks/803f680d-e89b-492b-82ef-2be7b774a92d/resume",
  "channels": "1bdea468-03bf-47b8-ab27-29a9dd0e4b94,51c6eb2b-2ae1-456b-99fe-6f1e0a36cd3c",
  "schedule": "15 5 * * *",
  "tz": "UTC"
}
```

`status` 字段的可能值为：`new`、`up`、`grace`、`down` 和 `paused`。

### 示例只读响应

当使用只读 API 密钥时，SITE_NAME 会从响应中省略以下字段：`uuid`、`ping_url`、`update_url`、`pause_url`、`resume_url`、`channels`。它会额外添加一个 `unique_key` 字段。此标识符在 API 调用之间是稳定的。

注意：尽管 API 在只读响应中省略了 `*_url` 字段，但客户端如果知道检查项的唯一 UUID，可以轻松自行构造这些 URL。

```json
{
  "name": "Database Backup",
  "slug": "database-backup",
  "tags": "production db",
  "desc": "Runs ~/db-backup.sh",
  "grace": 1200,
  "n_pings": 7,
  "status": "down",
  "started": false,
  "last_ping": "2020-03-23T10:19:32+00:00",
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "start_kw": "START",
  "success_kw": "SUCCESS",
  "failure_kw": "ERROR",
  "filter_subject": true,
  "filter_body": false,
  "filter_http_body": false,
  "filter_default_fail": false,
  "badge_url": "SITE_ROOT/b/2/7d3ab93d-836e-4505-bbda-fcbd5e07adf9.svg",
  "unique_key": "124f983e0e3dcaeba921cfcef46efd084576e783",
  "schedule": "15 5 * * *",
  "tz": "UTC"
}
```


## 创建检查项 {: #create-check .rule }
`POST SITE_ROOT/api/v3/checks/`

创建一个新的检查项并返回其 ping URL。
所有请求参数都是可选的，如果省略将使用默认值。

通过此 API 调用，您可以创建简单检查项和 Cron 检查项：

* 要创建简单检查项，请指定 `timeout` 参数。
* 要创建 Cron 检查项，请指定 `schedule` 和 `tz` 参数。

### 请求参数

name
:   字符串，可选，默认值：""

    新检查项的名称。

    API v3 中的变更：检查项的 slug 不再从名称自动生成。客户端可以通过 `slug` 字段显式指定 slug。

slug
:   字符串，可选，默认值：""

    新检查项的 slug。slug 只能包含以下字符：`a-z`、`0-9`、连字符、下划线。示例：

    <pre>{"slug": "my-custom-slug"}</pre>

tags
:   字符串，可选，默认值：""

    新检查项的以空格分隔的标签列表。示例：

    <pre>{"tags": "reports staging"}</pre>

desc
:   字符串，可选。

    检查项的描述。

timeout
:   数字，可选，默认值：{{ default_timeout }}。

    检查项的期望周期（秒）。

    最小值：60（一分钟），最大值：31536000（365 天）。

    5 分钟超时的示例：

    <pre>{"timeout": 300}</pre>

grace
:   数字，可选，默认值：{{ default_grace }}。

    检查项的宽限期（秒）。

    最小值：60（一分钟），最大值：31536000（365 天）。

schedule
:   字符串，可选。

    定义检查项调度周期的 cron 或 systemd OnCalendar 表达式。SITE_NAME 会自动检测表达式类型（cron 或 OnCalendar）。

    `schedule` 参数优先于 `timeout` 字段：如果同时指定了 `timeout` 和 `schedule` 参数，SITE_NAME 将保存 `schedule` 并忽略 `timeout`。

    使用 cron 表达式的示例（"每半小时运行一次"）：

    <pre>{"schedule": "0,30 * * * *"}</pre>

    使用 OnCalendar 表达式的示例（"每月最后一天 12:00 运行"）：

    <pre>{"schedule": "\*-\*~1 12:00"}</pre>

tz
:   字符串，可选，默认值："UTC"。

    服务器的时区。此设置仅在结合 `schedule` 参数时生效。

    示例：

    <pre>{"tz": "Europe/Riga"}</pre>

manual_resume
:   布尔值，可选，默认值：false。

    控制暂停的检查项在收到 ping 时是否自动恢复（默认行为），或者不自动恢复。如果设置为 false，暂停的检查项在收到 ping 时将退出暂停状态。如果设置为 true，暂停的检查项将忽略 ping 并保持暂停状态，直到您从 Web 仪表盘手动恢复它。

methods
:   字符串，可选，默认值：""。

    指定允许用于发送 ping 请求的 HTTP 方法。必须是以下两个值之一：""（空字符串）或 "POST"。

    将此字段设置为 ""（空字符串）以允许 HEAD、GET 和 POST 请求。

    将此字段设置为 "POST" 以仅允许 POST 请求。

    示例：

    <pre>{"methods": "POST"}</pre>

channels
:   字符串，可选。

    默认情况下，此 API 调用不会为新创建的检查项分配任何集成。

    将此字段设置为特殊值 "*" 以自动分配所有已有集成。示例：

    <pre>{"channels": "*"}</pre>

    要分配特定的集成，请使用逗号分隔的集成 UUID 列表。您可以使用[列出已有集成](#list-channels) API 调用来查找集成 UUID。

    示例：

    <pre>{"channels":
     "4ec5a071-2d08-4baa-898a-eb4eb3cd6941,746a083e-f542-4554-be1a-707ce16d3acc"}</pre>

    或者，如果您在 SITE_NAME 仪表盘中为集成命名了名称，则可以通过名称指定集成。为此，您的集成需要有非空的唯一名称，且不能包含逗号。名称必须完全匹配，空格有效。

    示例：

    <pre>{"channels": "Email to Alice,SMS to Alice"}</pre>

unique
:   字符串数组，可选，默认值：[]。

    启用"upsert"功能。在创建检查项之前，SITE_NAME 会查找已有的检查项，按 `unique` 中列出的字段进行过滤。

    如果 SITE_NAME 没有找到匹配的检查项，它会创建一个新的检查项并以 HTTP 状态码 201 返回。

    如果 SITE_NAME 找到匹配的检查项，它会更新已有的检查项并以 HTTP 状态码 200 返回。

    `unique` 字段可接受的值有 `name`、`slug`、`tags`、`timeout` 和 `grace`。

    示例：

    <pre>{"name": "Backups", unique: ["name"]}</pre>

    在此示例中，如果名为"Backups"的检查项已存在，则返回该检查项。否则，将创建并返回一个新的检查项。

start_kw
:   字符串，可选，默认值：""。

    指定用于将入站电子邮件和 HTTP ping 分类为 start 信号的关键词。多个关键词用逗号分隔。关键词区分大小写。

    将此字段与 `filter_subject`、`filter_body` 和 `filter_http_body` 字段结合使用。

    示例：

    <pre>{"filter_subject": true, "start_kw": "STARTED"}</pre>

    在此示例中，如果主题行包含单词"STARTED"，SITE_NAME 将入站电子邮件分类为 start 信号。

success_kw
:   字符串，可选，默认值：""。

    指定用于将入站电子邮件和 HTTP ping 分类为 success 信号的关键词。多个关键词用逗号分隔。关键词区分大小写。

    将此字段与 `filter_subject`、`filter_body` 和 `filter_http_body` 字段结合使用。

    示例：

    <pre>{"filter_subject": true, "success_kw": "SUCCESS,COMPLETED"}</pre>

    在此示例中，如果主题行包含"SUCCESS"或"COMPLETED"中的任一单词，则入站电子邮件计为 success。

failure_kw
:   字符串，可选，默认值：""。

    指定用于将入站电子邮件和 HTTP ping 分类为 failure 信号的关键词。多个关键词用逗号分隔。关键词区分大小写。

    将此字段与 `filter_subject`、`filter_body` 和 `filter_http_body` 字段结合使用。

    示例：

    <pre>{"filter_subject": true, "failure_kw": "FAILED,ERROR"}</pre>

    在此示例中，如果主题行包含"FAILED"或"ERROR"中的任一单词，则入站电子邮件计为 failure。

filter_subject
:   布尔值，可选，默认值：false。

    启用在入站电子邮件的主题行中查找关键词的过滤功能。另请参阅 `start_kw`、`success_kw` 和 `failure_kw` 字段。

filter_body
:   布尔值，可选，默认值：false。

    启用在入站电子邮件的正文中查找关键词的过滤功能。另请参阅 `start_kw`、`success_kw` 和 `failure_kw` 字段。

    SITE_NAME 支持纯文本和 HTML 格式的电子邮件，并在纯文本和 HTML 邮件内容中查找关键词。

filter_http_body
:   布尔值，可选，默认值：false。

    启用在 HTTP 请求体的前 PING_BODY_LIMIT_FORMATTED 字节中查找关键词的 HTTP ping 过滤功能。另请参阅 `start_kw`、`success_kw` 和 `failure_kw` 字段。

filter_default_fail
:   布尔值，可选，默认值：false。

    确定在启用关键词过滤但没有关键词匹配时如何处理电子邮件和 HTTP ping。

    如果 `filter_subject` 或 `filter_body`（或两者）设置为 `true`，则入站电子邮件启用关键词过滤。如果 `filter_http_body` 设置为 `true`，则 HTTP ping 启用关键词过滤。

    如果 `filter_default_fail=false`，且没有关键词匹配，则 ping 将被忽略。

    如果 `filter_default_fail=true`，且没有关键词匹配，则 ping 将被分类为 failure 信号。

    示例：

    <pre>{
        "filter_http_body": true,
        "filter_default_fail": true,
        "success_kw": "Backup successful"
    }</pre>

    在此示例中，HTTP ping 只有在且仅在请求体包含字符串"Backup successful"时才被分类为 success 信号。在所有其他情况下，包括带有空请求体的 HTTP GET 请求，ping 将被分类为 failure 信号。

### 响应码

201 Created
:   新检查项成功创建。

200 OK
:   找到了已有的检查项并已更新。

400 Bad Request
:   请求格式不正确、违反模式或使用了无效的字段值。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   账户已达到检查项数量限制。对于免费账户，限制为每个账户 20 个检查项。

### Example Request

```bash
curl SITE_ROOT/api/v3/checks/ \
    --header "X-Api-Key: your-api-key" \
    --data '{"name": "Backups", "tags": "prod www", "timeout": 3600, "grace": 60}'
```

Or, alternatively:

```bash
curl SITE_ROOT/api/v3/checks/ \
    --data '{"api_key": "your-api-key", "name": "Backups", "tags": "prod www", "timeout": 3600, "grace": 60}'
```

### Example Response

```json
{
  "name": "Backups",
  "slug": "",
  "tags": "prod www",
  "desc": "",
  "grace": 60,
  "n_pings": 0,
  "status": "new",
  "started": false,
  "last_ping": null,
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "subject": "",
  "subject_fail": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "filter_http_body": false,
  "filter_default_fail": false,
  "badge_url": "SITE_ROOT/b/2/d43c84db-1502-4d86-a89d-181a33e25896.svg",
  "uuid": "7918b17b-a745-4db1-8575-9d2e07c97f79",
  "ping_url": "PING_ENDPOINT7918b17b-a745-4db1-8575-9d2e07c97f79",
  "update_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79",
  "pause_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/pause",
  "resume_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/resume",
  "channels": "",
  "timeout": 3600
}
```

## 更新已有检查项 {: #update-check .rule }

`POST SITE_ROOT/api/v3/checks/<uuid>`

更新已有的检查项。所有请求参数都是可选的。如果省略任何参数，SITE_NAME 将保持其值不变。

### 请求参数

name
:   字符串，可选。

    检查项的名称。

    API v3 中的变更：检查项的 slug 不再从名称自动生成。客户端可以通过 `slug` 字段显式指定 slug。

slug
:   字符串，可选。

    检查项的 slug。slug 只能包含以下字符：`a-z`、`0-9`、连字符、下划线。示例：

    <pre>{"slug": "my-custom-slug"}</pre>

tags
:   字符串，可选。

    检查项的以空格分隔的标签列表。示例：

    <pre>{"tags": "reports staging"}</pre>

desc
:   字符串，可选。

    检查项的描述。

timeout
:   数字，可选。

    检查项的期望周期（秒）。

    最小值：60（一分钟），最大值：31536000（365 天）。

    5 分钟超时的示例：

    <pre>{"timeout": 300}</pre>

grace
:   数字，可选。

    检查项的宽限期（秒）。

    最小值：60（一分钟），最大值：31536000（365 天）。

schedule
:   字符串，可选。

    定义检查项调度周期的 cron 或 systemd OnCalendar 表达式。SITE_NAME 会自动检测表达式类型（cron 或 OnCalendar）。

    `schedule` 参数优先于 `timeout` 字段：如果同时指定了 `timeout` 和 `schedule` 参数，SITE_NAME 将保存 `schedule` 并忽略 `timeout`。

    使用 cron 表达式的示例（"每半小时运行一次"）：

    <pre>{"schedule": "0,30 * * * *"}</pre>

    使用 OnCalendar 表达式的示例（"每月最后一天 12:00 运行"）：

    <pre>{"schedule": "\*-\*~1 12:00"}</pre>

 tz
:   字符串，可选。

    服务器的时区。此设置仅在结合"schedule"参数时生效。

    示例：

    <pre>{"tz": "Europe/Riga"}</pre>

manual_resume
:   布尔值，可选，默认值：false。

    控制暂停的检查项在收到 ping 时是否自动恢复（默认行为），或者不自动恢复。如果设置为 false，暂停的检查项在收到 ping 时将退出暂停状态。如果设置为 true，暂停的检查项将忽略 ping 并保持暂停状态，直到您从 Web 仪表盘手动恢复它。

methods
:   字符串，可选，默认值：""。

    指定允许用于发送 ping 请求的 HTTP 方法。必须是以下两个值之一：""（空字符串）或 "POST"。

    将此字段设置为 ""（空字符串）以允许 HEAD、GET 和 POST 请求。

    将此字段设置为 "POST" 以仅允许 POST 请求。

    示例：

    <pre>{"methods": "POST"}</pre>

channels
:   字符串，可选。

    将此字段设置为特殊值 "*" 以自动分配所有已有集成。示例：

    <pre>{"channels": "*"}</pre>

    将此字段设置为特殊值 ""（空字符串）以自动*取消分配*所有已有集成。示例：

    <pre>{"channels": ""}</pre>

    要分配特定的集成，请使用逗号分隔的集成 UUID 列表。您可以使用[列出已有集成](#list-channels) API 调用来查找集成 UUID。

    示例：

    <pre>{"channels":
     "4ec5a071-2d08-4baa-898a-eb4eb3cd6941,746a083e-f542-4554-be1a-707ce16d3acc"}</pre>

    或者，如果您在 SITE_NAME 仪表盘中为集成命名了名称，则可以通过名称指定集成。为此，您的集成需要有非空的唯一名称，且不能包含逗号。名称必须完全匹配，空格有效。

    示例：

    <pre>{"channels": "Email to Alice,SMS to Alice"}</pre>

start_kw
:   字符串，可选，默认值：""。

    指定用于将入站电子邮件和 HTTP ping 分类为 start 信号的关键词。多个关键词用逗号分隔。关键词区分大小写。

    将此字段与 `filter_subject`、`filter_body` 和 `filter_http_body` 字段结合使用。

    示例：

    <pre>{"filter_subject": true, "start_kw": "STARTED"}</pre>

    在此示例中，如果主题行包含单词"STARTED"，SITE_NAME 将入站电子邮件分类为 start 信号。

success_kw
:   字符串，可选，默认值：""。

    指定用于将入站电子邮件和 HTTP ping 分类为 success 信号的关键词。多个关键词用逗号分隔。关键词区分大小写。

    将此字段与 `filter_subject`、`filter_body` 和 `filter_http_body` 字段结合使用。

    示例：

    <pre>{"filter_subject": true, "success_kw": "SUCCESS,COMPLETED"}</pre>

    在此示例中，如果主题行包含"SUCCESS"或"COMPLETED"中的任一单词，则入站电子邮件计为 success。

failure_kw
:   字符串，可选，默认值：""。

    指定用于将入站电子邮件和 HTTP ping 分类为 failure 信号的关键词。多个关键词用逗号分隔。关键词区分大小写。

    将此字段与 `filter_subject`、`filter_body` 和 `filter_http_body` 字段结合使用。

    示例：

    <pre>{"filter_subject": true, "failure_kw": "FAILED,ERROR"}</pre>

    在此示例中，如果主题行包含"FAILED"或"ERROR"中的任一单词，则入站电子邮件计为 failure。

filter_subject
:   布尔值，可选，默认值：false。

    启用在入站电子邮件的主题行中查找关键词的过滤功能。另请参阅 `start_kw`、`success_kw` 和 `failure_kw` 字段。

filter_body
:   布尔值，可选，默认值：false。

    启用在入站电子邮件的正文中查找关键词的过滤功能。另请参阅 `start_kw`、`success_kw` 和 `failure_kw` 字段。

    SITE_NAME 支持纯文本和 HTML 格式的电子邮件，并在纯文本和 HTML 邮件内容中查找关键词。

filter_http_body
:   布尔值，可选，默认值：false。

    启用在 HTTP 请求体的前 PING_BODY_LIMIT_FORMATTED 字节中查找关键词的 HTTP ping 过滤功能。另请参阅 `start_kw`、`success_kw` 和 `failure_kw` 字段。

filter_default_fail
:   布尔值，可选，默认值：false。

    确定在启用关键词过滤但没有关键词匹配时如何处理电子邮件和 HTTP ping。

    如果 `filter_subject` 或 `filter_body`（或两者）设置为 `true`，则入站电子邮件启用关键词过滤。如果 `filter_http_body` 设置为 `true`，则 HTTP ping 启用关键词过滤。

    如果 `filter_default_fail=false`，且没有关键词匹配，则 ping 将被忽略。

    如果 `filter_default_fail=true`，且没有关键词匹配，则 ping 将被分类为 failure 信号。

    示例：

    <pre>{
        "filter_http_body": true,
        "filter_default_fail": true,
        "success_kw": "Backup successful"
    }</pre>

    在此示例中，HTTP ping 只有在且仅在请求体包含字符串"Backup successful"时才被分类为 success 信号。在所有其他情况下，包括带有空请求体的 HTTP GET 请求，ping 将被分类为 failure 信号。

### 响应码

200 OK
:   检查项成功更新。

400 Bad Request
:   请求格式不正确、违反模式或使用了无效的字段值。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。


### Example Request

```bash
curl SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79 \
    --header "X-Api-Key: your-api-key" \
    --data '{"name": "Backups", "tags": "prod www", "timeout": 3600, "grace": 60}'
```

Or, alternatively:

```bash
curl SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79 \
    --data '{"api_key": "your-api-key", "name": "Backups", "tags": "prod www", "timeout": 3600, "grace": 60}'
```

### Example Response

```json
{
  "name": "Backups",
  "slug": "",
  "tags": "prod www",
  "desc": "",
  "grace": 60,
  "n_pings": 0,
  "status": "new",
  "started": false,
  "last_ping": null,
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "subject": "",
  "subject_fail": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "filter_http_body": false,
  "filter_default_fail": false,
  "badge_url": "SITE_ROOT/b/2/d43c84db-1502-4d86-a89d-181a33e25896.svg",
  "uuid": "7918b17b-a745-4db1-8575-9d2e07c97f79",
  "ping_url": "PING_ENDPOINT7918b17b-a745-4db1-8575-9d2e07c97f79",
  "update_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79",
  "pause_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/pause",
  "resume_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/resume",
  "channels": "",
  "timeout": 3600
}
```

## 暂停监控检查项 {: #pause-check .rule }

`POST SITE_ROOT/api/v3/checks/<uuid>/pause`

禁用检查项的监控而不删除它。检查项进入"paused"状态。您可以通过发送 ping 来恢复检查项的监控，或者运行[恢复](#resume-check) API 调用（当检查项的 `manual_resume=True` 时有用）。

此 API 调用没有请求参数。

### 响应码

200 OK
:   检查项成功暂停。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。

### Example Request

```bash
curl SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/pause \
    --request POST --header "X-Api-Key: your-api-key" --data ""
```

注意：`--data ""` 参数强制 curl 发送 `Content-Length` 请求头，即使请求体为空。对于 HTTP POST 请求，某些网络代理和 Web 服务器有时需要 `Content-Length` 头。

### Example Response

```json
{
  "name": "Backups",
  "slug": "",
  "tags": "prod www",
  "desc": "",
  "grace": 60,
  "n_pings": 0,
  "status": "paused",
  "started": false,
  "last_ping": null,
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "subject": "",
  "subject_fail": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "filter_http_body": false,
  "filter_default_fail": false,
  "badge_url": "SITE_ROOT/b/2/d43c84db-1502-4d86-a89d-181a33e25896.svg",
  "uuid": "7918b17b-a745-4db1-8575-9d2e07c97f79",
  "ping_url": "PING_ENDPOINT7918b17b-a745-4db1-8575-9d2e07c97f79",
  "update_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79",
  "pause_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/pause",
  "resume_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/resume",
  "channels": "",
  "timeout": 3600
}
```

## 恢复监控检查项 {: #resume-check .rule }

`POST SITE_ROOT/api/v3/checks/<uuid>/resume`

恢复检查项。检查项进入"new"状态。使用此 API 调用来恢复处于暂停状态且 `manual_resume` 配置参数设置为 `True` 的检查项的监控。

此 API 调用没有请求参数。

### 响应码

200 OK
:   操作成功。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。

409 Conflict
:   指定的检查项当前不处于暂停状态。

### Example Request

```bash
curl SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/resume \
    --request POST --header "X-Api-Key: your-api-key" --data ""
```

注意：`--data ""` 参数强制 curl 发送 `Content-Length` 请求头，即使请求体为空。对于 HTTP POST 请求，某些网络代理和 Web 服务器有时需要 `Content-Length` 头。

### Example Response

```json
{
  "name": "Backups",
  "slug": "",
  "tags": "prod www",
  "desc": "",
  "grace": 60,
  "n_pings": 0,
  "status": "new",
  "started": false,
  "last_ping": null,
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "subject": "",
  "subject_fail": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "filter_http_body": false,
  "filter_default_fail": false,
  "badge_url": "SITE_ROOT/b/2/d43c84db-1502-4d86-a89d-181a33e25896.svg",
  "uuid": "7918b17b-a745-4db1-8575-9d2e07c97f79",
  "ping_url": "PING_ENDPOINT7918b17b-a745-4db1-8575-9d2e07c97f79",
  "update_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79",
  "pause_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/pause",
  "resume_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/resume",
  "channels": "",
  "timeout": 3600
}
```


## 删除检查项 {: #delete-check .rule }

`DELETE SITE_ROOT/api/v3/checks/<uuid>`

从用户账户中永久删除检查项。返回刚刚被删除的检查项的 JSON 表示。

此 API 调用没有请求参数。

### 响应码

200 OK
:   检查项成功删除。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。

### Example Request

```bash
curl SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79 \
    --request DELETE --header "X-Api-Key: your-api-key"
```

### Example Response

```json
{
  "name": "Backups",
  "slug": "",
  "tags": "prod www",
  "desc": "",
  "grace": 60,
  "n_pings": 0,
  "status": "new",
  "started": false,
  "last_ping": null,
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "subject": "",
  "subject_fail": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "filter_http_body": false,
  "filter_default_fail": false,
  "badge_url": "SITE_ROOT/b/2/d43c84db-1502-4d86-a89d-181a33e25896.svg",
  "uuid": "7918b17b-a745-4db1-8575-9d2e07c97f79",
  "ping_url": "PING_ENDPOINT7918b17b-a745-4db1-8575-9d2e07c97f79",
  "update_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79",
  "pause_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/pause",
  "resume_url": "SITE_ROOT/api/v3/checks/7918b17b-a745-4db1-8575-9d2e07c97f79/resume",
  "channels": "",
  "timeout": 3600
}
```

## 列出检查项的已记录 ping {: #list-pings .rule }

`GET SITE_ROOT/api/v3/checks/<uuid>/pings/`

返回此检查项已接收到的 ping 列表。

此端点按倒序返回 ping（最新的在前），返回的 ping 总数取决于账户的计费方案：免费账户 100 条，付费账户 1000 条。

### 响应码

200 OK
:   请求成功。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。

### Example Request

```bash
curl SITE_ROOT/api/v3/checks/f618072a-7bde-4eee-af63-71a77c5723bc/pings/ \
    --header "X-Api-Key: your-api-key"
```

### Example Response

```json
{
  "pings": [
    {
      "type": "success",
      "date": "2020-06-09T14:51:06.113073+00:00",
      "n": 4,
      "scheme": "http",
      "remote_addr": "192.0.2.0",
      "method": "GET",
      "ua": "curl/7.68.0",
      "rid": "123e4567-e89b-12d3-a456-426614174000",
      "duration": 2.896736,
      "body_url": null
    },
    {
      "type": "start",
      "date": "2020-06-09T14:51:03.216337+00:00",
      "n": 3,
      "scheme": "http",
      "remote_addr": "192.0.2.0",
      "method": "GET",
      "ua": "curl/7.68.0",
      "rid": "123e4567-e89b-12d3-a456-426614174000",
      "body_url": null
    },
    {
      "type": "success",
      "date": "2020-06-09T14:50:59.633577+00:00",
      "n": 2,
      "scheme": "http",
      "remote_addr": "192.0.2.0",
      "method": "GET",
      "ua": "curl/7.68.0",
      "rid": null,
      "duration": 2.997976,
      "body_url": null
    },
    {
      "type": "start",
      "date": "2020-06-09T14:50:56.635601+00:00",
      "n": 1,
      "scheme": "http",
      "remote_addr": "192.0.2.0",
      "method": "GET",
      "ua": "curl/7.68.0",
      "rid": null,
      "body_url": null
    }
  ]
}
```


## 获取 ping 的请求体 {: #ping-body .rule }

`GET SITE_ROOT/api/v3/checks/<uuid>/pings/<n>/body`

返回 ping 的已记录请求体。响应的 `Content-Type` 始终为 `text/plain`，ping 的请求体会逐字返回到响应体中。

### 响应码

200 OK
:   请求成功且存在请求体。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   检查项不存在、ping 不存在或 ping 没有请求体数据。

503 Service Unavailable
:   外部对象存储服务不可用，请稍后重试。


### Example Request

```bash
curl SITE_ROOT/api/v3/checks/f618072a-7bde-4eee-af63-71a77c5723bc/pings/397/body \
    --header "X-Api-Key: your-api-key"
```

## 列出检查项的状态变更 {: #list-flips .rule }

`GET SITE_ROOT/api/v3/checks/<uuid>/flips/`<br>
`GET SITE_ROOT/api/v3/checks/<unique_key>/flips/`

返回此检查项经历的状态变更列表。状态变更是指状态的变化（从"down"到"up"，或从"up"到"down"）。

此 API 端点支持通过 `seconds`、`start` 和 `end` 查询参数进行时间过滤。如果未指定时间过滤器，API 将返回指定检查项的所有已存储状态变更。

关于状态变更保留的说明：SITE_NAME 保留当前月份以及当前月份之前两个整月的历史状态变更。SITE_NAME 会定期清理更早的状态变更。在任何时候，数据库中可能有少量已到期但尚未被删除的状态变更。此 API 调用也会返回这些状态变更。

### 查询参数

seconds=&lt;value&gt;
:   返回最近 `value` 秒内的状态变更

    示例：

    `SITE_ROOT/api/v3/checks/<uuid|unique_key>/flips/?seconds=3600`

start=&lt;value&gt;
:   返回早于指定 UNIX 时间戳的状态变更。

    示例：

    `SITE_ROOT/api/v3/checks/<uuid|unique_key>/flips/?start=1592214380`

end=&lt;value&gt;
:   返回晚于指定 UNIX 时间戳的状态变更。

    示例：

    `SITE_ROOT/api/v3/checks/<uuid|unique_key>/flips/?end=1592217980`


### 响应码

200 OK
:   请求成功。

400 Bad Request
:   无效的查询参数。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。

### Example Request

```bash
curl SITE_ROOT/api/v3/checks/f618072a-7bde-4eee-af63-71a77c5723bc/flips/ \
    --header "X-Api-Key: your-api-key"
```

### Example Response

```json
[
    {
      "timestamp": "2020-03-23T10:18:23+00:00",
      "up": 1
    },
    {
      "timestamp": "2020-03-23T10:17:15+00:00",
      "up": 0
    },
    {
      "timestamp": "2020-03-23T10:16:18+00:00",
      "up": 1
    }
]
```

## 列出已有集成 {: #list-channels .rule }

`GET SITE_ROOT/api/v3/channels/`

返回属于该项目的集成列表。

### 响应码

200 OK
:   请求成功。

401 Unauthorized
:   API 密钥缺失或无效。

### Example Request

```bash
curl --header "X-Api-Key: your-api-key" SITE_ROOT/api/v3/channels/
```

### Example Response

```json
{
  "channels": [
    {
      "id": "4ec5a071-2d08-4baa-898a-eb4eb3cd6941",
      "name": "My Work Email",
      "kind": "email"
    },
    {
      "id": "746a083e-f542-4554-be1a-707ce16d3acc",
      "name": "My Phone",
      "kind": "sms"
    }
  ]
}
```

## 列出项目的徽章 {: #list-badges .rule }

`GET SITE_ROOT/api/v3/badges/`

返回项目中所有标签的映射，以及每个标签的徽章 URL。SITE_NAME 提供几种不同格式的徽章：

* `svg`：以 SVG 文档形式返回徽章。
* `json`：返回一个 JSON 文档，您可以用来自行生成自定义徽章。
* `shields`：以 [Shields.io 兼容格式](https://shields.io/endpoint)返回 JSON。

此外，徽章有 2 状态和 3 状态的变体：

* `svg`、`json`、`shields`：报告两种状态："up"和"down"。它将宽限期内的任何检查项仍视为"up"。
* `svg3`、`json3`、`shields3`：报告三种状态："up"、"late"和"down"。

响应中包含一个特殊的 `*` 条目：此伪标签报告项目中所有检查项的总体状态。

### 响应码

200 OK
:   请求成功。

401 Unauthorized
:   API 密钥缺失或无效。

### Example Request

```bash
curl --header "X-Api-Key: your-api-key" SITE_ROOT/api/v3/badges/
```

### Example Response

```json
{
  "badges": {
    "backup": {
      "svg": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/LOegDs5M-2/backup.svg",
      "svg3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/LOegDs5M/backup.svg",
      "json": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/LOegDs5M-2/backup.json",
      "json3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/LOegDs5M/backup.json",
      "shields": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/LOegDs5M-2/backup.shields",
      "shields3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/LOegDs5M/backup.shields"
    },
    "db": {
      "svg": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/99MuQaKm-2/db.svg",
      "svg3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/99MuQaKm/db.svg",
      "json": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/99MuQaKm-2/db.json",
      "json3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/99MuQaKm/db.json",
      "shields": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/99MuQaKm-2/db.shields",
      "shields3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/99MuQaKm/db.shields"
    },
    "prod": {
      "svg": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/1TEhqie8-2/prod.svg",
      "svg3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/1TEhqie8/prod.svg",
      "json": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/1TEhqie8-2/prod.json",
      "json3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/1TEhqie8/prod.json",
      "shields": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/1TEhqie8-2/prod.shields",
      "shields3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/1TEhqie8/prod.shields"
    },
    "*": {
      "svg": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/9X7kcZoe-2.svg",
      "svg3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/9X7kcZoe.svg",
      "json": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/9X7kcZoe-2.json",
      "json3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/9X7kcZoe.json",
      "shields": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/9X7kcZoe-2.shields",
      "shields3": "SITE_ROOT/badge/67541b37-8b9c-4d17-b952-690eae/9X7kcZoe.shields"
    }
  }
}
```

## 检查数据库连接 {: #status .rule }

`GET SITE_ROOT/api/v3/status/`

运行一个测试查询，如果查询成功完成，则返回 HTTP 200。使用此端点通过外部正常运行时间监控系统来监控您的 Healthchecks 实例的运行状态。

### 响应码

200 OK
:   请求成功。

500 Internal Server Error
:   测试数据库查询未成功。
