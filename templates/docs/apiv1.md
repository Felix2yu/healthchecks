# Management API v1

Version:
<select onchange="document.location = this.value">
    <option value="../apiv1/" selected>v1</option>
    <option value="../apiv2/">v2</option>
    <option value="../api/">v3</option>
</select>

通过管理 API，你可以以编程方式管理账户中的检查项和集成。

<div class="alert alert-info"><strong>API v1 已弃用</strong>。请改用 <a href="../api/">API v3</a>。</div>

## API Endpoints

<div id="api-toc"></div>

端点名称                                         | 端点地址
------------------------------------------------------|-------
**检查项**|
[列出已有检查项](#list-checks)                  | `GET SITE_ROOT/api/v1/checks/`
[获取单个检查项](#get-check)                      | `GET SITE_ROOT/api/v1/checks/<uuid>`<br>`GET SITE_ROOT/api/v1/checks/<unique_key>`
[创建新检查项](#create-check)                   | `POST SITE_ROOT/api/v1/checks/`
[更新已有检查项](#update-check)             | `POST SITE_ROOT/api/v1/checks/<uuid>`
[暂停检查项监控](#pause-check)           | `POST SITE_ROOT/api/v1/checks/<uuid>/pause`
[恢复检查项监控](#resume-check)         | `POST SITE_ROOT/api/v1/checks/<uuid>/resume`
[删除检查项](#delete-check)                         | `DELETE SITE_ROOT/api/v1/checks/<uuid>`
**Ping 记录**|
[列出检查项的 ping 记录](#list-pings)              | `GET SITE_ROOT/api/v1/checks/<uuid>/pings/`
[获取 ping 的请求体内容](#ping-body)                | `GET SITE_ROOT/api/v1/checks/<uuid>/pings/<n>/body`
**状态变更**|
[列出检查项的状态变更](#list-flips)   | `GET SITE_ROOT/api/v1/checks/<uuid>/flips/`<br>`GET SITE_ROOT/api/v1/checks/<unique_key>/flips/`
**集成**|
[列出已有集成](#list-channels) | `GET SITE_ROOT/api/v1/channels/`
**徽章**|
[列出项目的徽章](#list-badges)                  | `GET SITE_ROOT/api/v1/badges/`

## 身份验证

你对 SITE_NAME 管理 API 的请求必须使用 API 密钥进行身份验证。所有 API 密钥都是项目级别的，没有账户级别的 API 密钥。默认情况下，SITE_NAME 上的项目没有 API 密钥。你可以在**项目设置**页面上创建读写和只读 API 密钥。

读写密钥
:   对所有已记录的 API 端点具有完全访问权限。

只读密钥
:   仅适用于以下 API 端点：

    * [列出已有检查项](#list-checks)
    * [获取单个检查项](#get-check)
    * [列出检查项的状态变更](#list-flips)
    * [列出项目的徽章](#list-badges)

    在 API 响应中省略敏感信息。详情请参阅各个 API 端点的文档。

客户端可以通过在 HTTP 请求中包含 `X-Api-Key: <your-api-key>` 标头来进行身份验证。或者，对于带有 JSON 请求体的 POST 请求，客户端可以在 JSON 文档中放置 `api_key` 字段。请参阅[创建一个新检查项](#create-check)部分的示例。

## API 请求

对于 POST 请求，SITE_NAME API 期望请求体为 JSON 文档（*不是* `multipart/form-data` 编码的表单数据）。

## API 响应

SITE_NAME 尽可能使用 HTTP 状态码。通常，2xx 表示成功，4xx 表示客户端错误，5xx 表示服务器错误。

响应可能包含带有附加数据的 JSON 文档。

## 列出已有检查项 {: #list-checks .rule }

`GET SITE_ROOT/api/v1/checks/`

返回属于用户的检查项列表，可选择按一个或多个标签进行筛选。

### 查询参数

tag=&lt;值&gt;
:   筛选检查项，仅返回标有指定值的检查项。

    此参数可重复多次。

    示例：

    `SITE_ROOT/api/v1/checks/?tag=foo&tag=bar`

### 响应状态码

200 OK
:   请求成功。

401 Unauthorized
:   API 密钥缺失或无效。

### Example Request

```bash
curl --header "X-Api-Key: your-api-key" SITE_ROOT/api/v1/checks/
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
      "last_ping": "2020-03-24T14:02:03+00:00",
      "next_ping": "2020-03-24T15:02:03+00:00",
      "manual_resume": false,
      "methods": "",
      "start_kw": "START",
      "success_kw": "SUCCESS",
      "failure_kw": "ERROR",
      "filter_subject": true,
      "filter_body": false,
      "ping_url": "PING_ENDPOINT31365bce-8da9-4729-8ff3-aaa71d56b712",
      "update_url": "SITE_ROOT/api/v1/checks/31365bce-8da9-4729-8ff3-aaa71d56b712",
      "pause_url": "SITE_ROOT/api/v1/checks/31365bce-8da9-4729-8ff3-aaa71d56b712/pause",
      "resume_url": "SITE_ROOT/api/v1/checks/31365bce-8da9-4729-8ff3-aaa71d56b712/resume",
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
      "last_ping": "2020-03-23T10:19:32+00:00",
      "next_ping": null,
      "manual_resume": false,
      "methods": "",
      "start_kw": "",
      "success_kw": "",
      "failure_kw": "",
      "filter_subject": false,
      "filter_body": false,
      "ping_url": "PING_ENDPOINT803f680d-e89b-492b-82ef-2be7b774a92d",
      "update_url": "SITE_ROOT/api/v1/checks/803f680d-e89b-492b-82ef-2be7b774a92d",
      "pause_url": "SITE_ROOT/api/v1/checks/803f680d-e89b-492b-82ef-2be7b774a92d/pause",
      "resume_url": "SITE_ROOT/api/v1/checks/803f680d-e89b-492b-82ef-2be7b774a92d/resume",
      "channels": "1bdea468-03bf-47b8-ab27-29a9dd0e4b94,51c6eb2b-2ae1-456b-99fe-6f1e0a36cd3c",
      "schedule": "15 5 * * *",
      "tz": "UTC"
    }
  ]
}
```

`status` 字段的可能值为：`new`、`started`、`up`、`grace`、`down` 和 `paused`。

使用只读 API 密钥时，SITE_NAME 会在响应中省略以下字段：`ping_url`、`update_url`、`pause_url`、`resume_url`、`channels`。它会额外添加一个 `unique_key` 字段。`unique_key` 标识符在多次 API 调用中保持稳定，你可以在[获取单个检查项](#get-check)和[列出检查项的状态变更](#list-flips) API 调用中使用它。

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
      "last_ping": "2020-03-24T14:02:03+00:00",
      "next_ping": "2020-03-24T15:02:03+00:00",
      "manual_resume": false,
      "methods": "",
      "start_kw": "START",
      "success_kw": "SUCCESS",
      "failure_kw": "ERROR",
      "filter_subject": true,
      "filter_body": false,
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
      "last_ping": "2020-03-23T10:19:32+00:00",
      "next_ping": null,
      "manual_resume": false,
      "methods": "",
      "start_kw": "",
      "success_kw": "",
      "failure_kw": "",
      "filter_subject": false,
      "filter_body": false,
      "unique_key": "124f983e0e3dcaeba921cfcef46efd084576e783",
      "schedule": "15 5 * * *",
      "tz": "UTC"
    }
  ]
}
```

## 获取单个检查项 {: #get-check .rule }
`GET SITE_ROOT/api/v1/checks/<uuid>`<br>
`GET SITE_ROOT/api/v1/checks/<unique_key>`

返回单个检查项的 JSON 表示。接受检查项的 UUID 或 `unique_key`（从 UUID 派生并在使用只读 API 密钥时由 API 响应返回的字段）作为标识符。

### 响应状态码

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
curl --header "X-Api-Key: your-api-key" SITE_ROOT/api/v1/checks/<uuid>
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
  "last_ping": "2020-03-23T10:19:32+00:00",
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "start_kw": "START",
  "success_kw": "SUCCESS",
  "failure_kw": "ERROR",
  "filter_subject": true,
  "filter_body": false,
  "ping_url": "PING_ENDPOINT803f680d-e89b-492b-82ef-2be7b774a92d",
  "update_url": "SITE_ROOT/api/v1/checks/803f680d-e89b-492b-82ef-2be7b774a92d",
  "pause_url": "SITE_ROOT/api/v1/checks/803f680d-e89b-492b-82ef-2be7b774a92d/pause",
  "resume_url": "SITE_ROOT/api/v1/checks/803f680d-e89b-492b-82ef-2be7b774a92d/resume",
  "channels": "1bdea468-03bf-47b8-ab27-29a9dd0e4b94,51c6eb2b-2ae1-456b-99fe-6f1e0a36cd3c",
  "schedule": "15 5 * * *",
  "tz": "UTC"
}
```

`status` 字段的可能值为：`new`、`started`、`up`、`grace`、`down` 和 `paused`。

### 示例只读响应

使用只读 API 密钥时，SITE_NAME 会在响应中省略以下字段：`ping_url`、`update_url`、`pause_url`、`resume_url`、`channels`。它会额外添加一个 `unique_key` 字段。此标识符在多次 API 调用中保持稳定。

注意：虽然 API 在只读响应中省略了 `*_url` 字段，但如果客户端知道检查项的唯一 UUID，它们可以轻松自行构造这些 URL。

```json
{
  "name": "Database Backup",
  "slug": "database-backup",
  "tags": "production db",
  "desc": "Runs ~/db-backup.sh",
  "grace": 1200,
  "n_pings": 7,
  "status": "down",
  "last_ping": "2020-03-23T10:19:32+00:00",
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "start_kw": "START",
  "success_kw": "SUCCESS",
  "failure_kw": "ERROR",
  "filter_subject": true,
  "filter_body": false,
  "unique_key": "124f983e0e3dcaeba921cfcef46efd084576e783",
  "schedule": "15 5 * * *",
  "tz": "UTC"
}
```


## 创建检查项 {: #create-check .rule }
`POST SITE_ROOT/api/v1/checks/`

创建一个新的检查项并返回其 ping URL。所有请求参数均为可选项，省略时将使用默认值。

通过此 API 调用，你可以创建简单检查项和 Cron 检查项：

* 要创建简单检查项，请指定 `timeout` 参数。
* 要创建 Cron 检查项，请指定 `schedule` 和 `tz` 参数。

### 请求参数

name
:   字符串，可选，默认值：""

    新检查项的名称。

tags
:   字符串，可选，默认值：""

    新检查项的标签列表，以空格分隔。
    示例：

    <pre>{"tags": "reports staging"}</pre>

desc
:   字符串，可选。

    检查项的说明。

timeout
:   数字，可选，默认值：{{ default_timeout }}。

    检查项的预期周期（秒）。

    最小值：60（一分钟），最大值：31536000（365 天）。

    5 分钟超时示例：

    <pre>{"timeout": 300}</pre>

grace
:   数字，可选，默认值：{{ default_grace }}。

    检查项的宽限期（秒）。

    最小值：60（一分钟），最大值：31536000（365 天）。

schedule
:   字符串，可选，默认值："`* * * * *`"。

    定义检查项时间表的 cron 表达式。

    如果同时指定了 `timeout` 和 `schedule` 参数，SITE_NAME 将创建 Cron 检查项并忽略 `timeout` 值。

    每半小时运行一次的检查项示例：

    <pre>{"schedule": "0,30 * * * *"}</pre>

tz
:   字符串，可选，默认值："UTC"。

    服务器的时区。此设置仅在与 `schedule` 参数结合使用时才生效。

    示例：

    <pre>{"tz": "Europe/Riga"}</pre>

manual_resume
:   布尔值，可选，默认值：false。

    控制暂停的检查项在收到 ping 时是否自动恢复（默认行为）。如果设为 false，暂停的检查项在收到 ping 时将离开暂停状态。如果设为 true，暂停的检查项将忽略 ping 并保持暂停状态，直到你通过 Web 仪表盘手动恢复。

methods
:   字符串，可选，默认值：""。

    指定进行 ping 请求时允许的 HTTP 方法。必须是以下两个值之一：""（空字符串）或 "POST"。

    将此字段设为 ""（空字符串）以允许 HEAD、GET 和 POST 请求。

    将此字段设为 "POST" 以仅允许 POST 请求。

    示例：

    <pre>{"methods": "POST"}</pre>

channels
:   字符串，可选。

    默认情况下，此 API 调用不会为新创建的检查项分配任何集成。

    将此字段设为特殊值 "*" 以自动分配所有现有集成。示例：

    <pre>{"channels": "*"}</pre>

    要分配特定集成，请使用集成 UUID 的逗号分隔列表。你可以使用[列出已有集成](#list-channels) API 调用查找集成 UUID。

    示例：

    <pre>{"channels":
     "4ec5a071-2d08-4baa-898a-eb4eb3cd6941,746a083e-f542-4554-be1a-707ce16d3acc"}</pre>

    或者，如果你在 SITE_NAME 仪表盘中为集成命名了，也可以按名称指定集成。为此，你的集成需要有非空的唯一名称，且不能包含逗号。名称必须完全匹配，空格是显著的。

    示例：

    <pre>{"channels": "Email to Alice,SMS to Alice"}</pre>

unique
:   字符串值数组，可选，默认值：[]。

    启用"upsert"功能。在创建检查项之前，SITE_NAME 会根据 `unique` 中列出的字段查找已有检查项。

    如果 SITE_NAME 未找到匹配的检查项，则创建新检查项并返回 HTTP 状态码 201。

    如果 SITE_NAME 找到匹配的检查项，则更新现有检查项并返回 HTTP 状态码 200。

    `unique` 字段可接受的值为 `name`、`tags`、`timeout` 和 `grace`。

    示例：

    <pre>{"name": "Backups", unique: ["name"]}</pre>

    在此示例中，如果已存在名为 "Backups" 的检查项，将返回该检查项。否则，将创建并返回一个新的检查项。

start_kw
:   字符串，可选，默认值：""。

    指定将入站电子邮件分类为"开始"信号的关键词。多个关键词之间用逗号分隔。

    将此字段与 `filter_subject` 和 `filter_body` 字段结合使用。将 `filter_subject` 设为 `true` 可启用邮件主题行过滤，`filter_body` 可过滤整个邮件正文。SITE_NAME 同时支持纯文本和 HTML 邮件。

    示例：

    <pre>{"filter_subject": true, "start_kw": "STARTED"}</pre>

    在此示例中，如果主题行包含单词 "STARTED"，SITE_NAME 将该邮件分类为开始信号。

success_kw
:   字符串，可选，默认值：""。

    指定将入站电子邮件分类为"成功"信号的关键词。多个关键词之间用逗号分隔。

    将此字段与 `filter_subject` 和 `filter_body` 字段结合使用。将 `filter_subject` 设为 `true` 可启用邮件主题行过滤，`filter_body` 可过滤整个邮件正文。SITE_NAME 同时支持纯文本和 HTML 邮件。

    示例：

    <pre>{"filter_subject": true, "success_kw": "SUCCESS,COMPLETED"}</pre>

    在此示例中，如果主题行包含 "SUCCESS" 或 "COMPLETED"，该邮件视为成功。

failure_kw
:   字符串，可选，默认值：""。

    指定将入站电子邮件分类为"失败"信号的关键词。多个关键词之间用逗号分隔。

    将此字段与 `filter_subject` 和 `filter_body` 字段结合使用。将 `filter_subject` 设为 `true` 可启用邮件主题行过滤，`filter_body` 可过滤整个邮件正文。SITE_NAME 同时支持纯文本和 HTML 邮件。

    示例：

    <pre>{"filter_subject": true, "failure_kw": "FAILED, ERROR"}</pre>

    在此示例中，如果主题行包含 "FAILED" 或 "ERROR"，该邮件视为失败。

filter_subject
:   布尔值，可选，默认值：false。

    启用在邮件主题行中查找关键词来过滤入站邮件。另请参阅 `success_kw` 和 `failure_kw` 字段。

filter_body
:   布尔值，可选，默认值：false。

    启用在邮件正文中查找关键词来过滤入站邮件。另请参阅 `success_kw` 和 `failure_kw` 字段。

subject
:   字符串，可选，默认值：""。

    **已弃用**。改用 `success_kw`、`filter_subject` 和 `filter_body` 字段。

    指定将入站电子邮件分类为"成功"信号的关键词。多个关键词之间用逗号分隔。如果在邮件的主题行中找到任何关键词，该邮件将被视为"成功"。

    将此字段设为 ""（空字符串）可将所有入站邮件视为"成功"（除非它们匹配 `subject_fail` 中列出的任何关键词，从而被分类为"失败"）。

    示例：

    <pre>SUCCESS,COMPLETED</pre>

    在此示例中，如果主题行包含 "SUCCESS" 或 "COMPLETED"，该邮件视为成功。

subject_fail
:   字符串，可选，默认值：""。

    **已弃用**。改用 `failure_kw`、`filter_subject` 和 `filter_body` 字段。

    指定将入站电子邮件分类为"失败"信号的关键词。多个关键词之间用逗号分隔。如果在邮件的主题行中找到任何关键词，该邮件将被视为"失败"。

    将此字段设为 ""（空字符串）以不执行"失败"分类。

    示例：

    <pre>FAILED,ERROR</pre>

    在此示例中，如果主题行包含 "FAILED" 或 "ERROR"，该邮件视为失败。

### 响应状态码

201 Created
:   新检查项创建成功。

200 OK
:   找到并更新了已有检查项。

400 Bad Request
:   请求格式不正确、违反模式或使用了无效字段值。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   账户已达到检查项数量限制。对于免费账户，限制为每个账户 20 个检查项。

### Example Request

```bash
curl SITE_ROOT/api/v1/checks/ \
    --header "X-Api-Key: your-api-key" \
    --data '{"name": "Backups", "tags": "prod www", "timeout": 3600, "grace": 60}'
```

或者，另一种方式：

```bash
curl SITE_ROOT/api/v1/checks/ \
    --data '{"api_key": "your-api-key", "name": "Backups", "tags": "prod www", "timeout": 3600, "grace": 60}'
```

### Example Response

```json
{
  "channels": "",
  "desc": "",
  "grace": 60,
  "last_ping": null,
  "n_pings": 0,
  "name": "Backups",
  "slug": "backups",
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "pause_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/pause",
  "resume_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/resume",
  "ping_url": "PING_ENDPOINTf618072a-7bde-4eee-af63-71a77c5723bc",
  "status": "new",
  "tags": "prod www",
  "timeout": 3600,
  "update_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc",
}
```

## 更新已有检查项 {: #update-check .rule }

`POST SITE_ROOT/api/v1/checks/<uuid>`

更新一个已有的检查项。所有请求参数均为可选项。如果省略任何参数，SITE_NAME 将保持其值不变。

### 请求参数

name
:   字符串，可选。

    检查项的名称。

tags
:   字符串，可选。

    检查项的标签列表，以空格分隔。

    示例：

    <pre>{"tags": "reports staging"}</pre>

desc
:   字符串，可选。

    检查项的说明。

timeout
:   数字，可选。

    检查项的预期周期（秒）。

    最小值：60（一分钟），最大值：31536000（365 天）。

    5 分钟超时示例：

    <pre>{"timeout": 300}</pre>

grace
:   数字，可选。

    检查项的宽限期（秒）。

    最小值：60（一分钟），最大值：31536000（365 天）。

schedule
:   字符串，可选。

    定义检查项时间表的 cron 表达式。

    如果同时指定了 `timeout` 和 `schedule` 参数，SITE_NAME 将保存 `schedule` 参数并忽略 `timeout`。

    每半小时运行一次的检查项示例：

    <pre>{"schedule": "0,30 * * * *"}</pre>

tz
:   字符串，可选。

    服务器的时区。此设置仅在与"schedule"参数结合使用时才生效。

    示例：

    <pre>{"tz": "Europe/Riga"}</pre>

manual_resume
:   布尔值，可选，默认值：false。

    控制暂停的检查项在收到 ping 时是否自动恢复（默认行为），或者不自动恢复。如果设为 false，暂停的检查项在收到 ping 时将离开暂停状态。如果设为 true，暂停的检查项将忽略 ping 并保持暂停状态，直到你通过 Web 仪表盘手动恢复。

methods
:   字符串，可选，默认值：""。

    指定进行 ping 请求时允许的 HTTP 方法。必须是以下两个值之一：""（空字符串）或 "POST"。

    将此字段设为 ""（空字符串）以允许 HEAD、GET 和 POST 请求。

    将此字段设为 "POST" 以仅允许 POST 请求。

    示例：

    <pre>{"methods": "POST"}</pre>

channels
:   字符串，可选。

    将此字段设为特殊值 "*" 以自动分配所有现有集成。示例：

    <pre>{"channels": "*"}</pre>

    将此字段设为特殊值 ""（空字符串）以自动*取消分配*所有现有集成。示例：

    <pre>{"channels": ""}</pre>

    要分配特定集成，请使用集成 UUID 的逗号分隔列表。你可以使用[列出已有集成](#list-channels) API 调用查找集成 UUID。

    示例：

    <pre>{"channels":
     "4ec5a071-2d08-4baa-898a-eb4eb3cd6941,746a083e-f542-4554-be1a-707ce16d3acc"}</pre>

    或者，如果你在 SITE_NAME 仪表盘中为集成命名了，也可以按名称指定集成。为此，你的集成需要有非空且唯一的名称，且不能包含逗号。名称必须完全匹配，空格是显著的。

    示例：

    <pre>{"channels": "Email to Alice,SMS to Alice"}</pre>

start_kw
:   字符串，可选，默认值：""。

    指定将入站电子邮件分类为"开始"信号的关键词。多个关键词之间用逗号分隔。

    将此字段与 `filter_subject` 和 `filter_body` 字段结合使用。将 `filter_subject` 设为 `true` 可启用邮件主题行过滤，`filter_body` 可过滤整个邮件正文。SITE_NAME 同时支持纯文本和 HTML 邮件。

    示例：

    <pre>{"filter_subject": true, "start_kw": "STARTED"}</pre>

    在此示例中，如果主题行包含单词 "STARTED"，SITE_NAME 将该邮件分类为开始信号。

success_kw
:   字符串，可选，默认值：""。

    指定将入站电子邮件分类为"成功"信号的关键词。多个关键词之间用逗号分隔。

    将此字段与 `filter_subject` 和 `filter_body` 字段结合使用。将 `filter_subject` 设为 `true` 可启用邮件主题行过滤，`filter_body` 可过滤整个邮件正文。SITE_NAME 同时支持纯文本和 HTML 邮件。

    示例：

    <pre>{"filter_subject": true, "success_kw": "SUCCESS,COMPLETED"}</pre>

    在此示例中，如果主题行包含 "SUCCESS" 或 "COMPLETED"，该邮件视为成功。

failure_kw
:   字符串，可选，默认值：""。

    指定将入站电子邮件分类为"失败"信号的关键词。多个关键词之间用逗号分隔。

    将此字段与 `filter_subject` 和 `filter_body` 字段结合使用。将 `filter_subject` 设为 `true` 可启用邮件主题行过滤，`filter_body` 可过滤整个邮件正文。SITE_NAME 同时支持纯文本和 HTML 邮件。

    示例：

    <pre>{"filter_subject": true, "failure_kw": "FAILED, ERROR"}</pre>

    在此示例中，如果主题行包含 "FAILED" 或 "ERROR"，该邮件视为失败。

filter_subject
:   布尔值，可选，默认值：false。

    启用在邮件主题行中查找关键词来过滤入站邮件。另请参阅 `success_kw` 和 `failure_kw` 字段。

filter_body
:   布尔值，可选，默认值：false。

    启用在邮件正文中查找关键词来过滤入站邮件。另请参阅 `success_kw` 和 `failure_kw` 字段。

subject
:   字符串，可选，默认值：""。

    **已弃用**。改用 `success_kw`、`filter_subject` 和 `filter_body` 字段。

    指定将入站电子邮件分类为"成功"信号的关键词。多个关键词之间用逗号分隔。如果在邮件的主题行中找到任何关键词，该邮件将被视为"成功"。

    将此字段设为 ""（空字符串）可将所有入站邮件视为"成功"（除非它们匹配 `subject_fail` 中列出的任何关键词，从而被分类为"失败"）。

    示例：

    <pre>SUCCESS,COMPLETED</pre>

    在此示例中，如果主题行包含 "SUCCESS" 或 "COMPLETED"，该邮件视为成功。

subject_fail
:   字符串，可选，默认值：""。

    **已弃用**。改用 `failure_kw`、`filter_subject` 和 `filter_body` 字段。

    指定将入站电子邮件分类为"失败"信号的关键词。多个关键词之间用逗号分隔。如果在邮件的主题行中找到任何关键词，该邮件将被视为"失败"。

    将此字段设为 ""（空字符串）以不执行"失败"分类。

    示例：

    <pre>FAILED,ERROR</pre>

    在此示例中，如果主题行包含 "FAILED" 或 "ERROR"，该邮件视为失败。

### 响应状态码

200 OK
:   检查项更新成功。

400 Bad Request
:   请求格式不正确、违反模式或使用了无效字段值。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。


### Example Request

```bash
curl SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc \
    --header "X-Api-Key: your-api-key" \
    --data '{"name": "Backups", "tags": "prod www", "timeout": 3600, "grace": 60}'
```

Or, alternatively:

```bash
curl SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc \
    --data '{"api_key": "your-api-key", "name": "Backups", "tags": "prod www", "timeout": 3600, "grace": 60}'
```

### Example Response

```json
{
  "channels": "",
  "desc": "",
  "grace": 60,
  "last_ping": null,
  "n_pings": 0,
  "name": "Backups",
  "slug": "backups",
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "pause_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/pause",
  "resume_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/resume",
  "ping_url": "PING_ENDPOINTf618072a-7bde-4eee-af63-71a77c5723bc",
  "status": "new",
  "tags": "prod www",
  "timeout": 3600,
  "update_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc",
}
```

## 暂停检查项的监控 {: #pause-check .rule }

`POST SITE_ROOT/api/v1/checks/<uuid>/pause`

禁用对检查项的监控而不删除它。检查项将进入"暂停"状态。你可以通过发送 ping 或运行[恢复](#resume-check) API 调用来恢复监控（在检查项的 `manual_resume=True` 时有用）。

此 API 调用没有请求参数。

### 响应状态码

200 OK
:   检查项已成功暂停。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。

### Example Request

```bash
curl SITE_ROOT/api/v1/checks/0c8983c9-9d73-446f-adb5-0641fdacc9d4/pause \
    --request POST --header "X-Api-Key: your-api-key" --data ""
```

注意：`--data ""` 参数强制 curl 发送 `Content-Length` 请求标头，即使请求体为空。对于 HTTP POST 请求，某些网络代理和 Web 服务器有时要求包含 `Content-Length` 标头。

### Example Response

```json
{
  "channels": "",
  "desc": "",
  "grace": 60,
  "last_ping": null,
  "next_ping": null,
  "n_pings": 0,
  "name": "Backups",
  "slug": "backups",
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "pause_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/pause",
  "resume_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/resume",
  "ping_url": "PING_ENDPOINTf618072a-7bde-4eee-af63-71a77c5723bc",
  "status": "paused",
  "tags": "prod www",
  "timeout": 3600,
  "update_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc"
}
```

## 恢复检查项的监控 {: #resume-check .rule }

`POST SITE_ROOT/api/v1/checks/<uuid>/resume`

恢复一个检查项。检查项将进入"new"状态。使用此 API 调用来恢复处于暂停状态且 `manual_resume` 配置参数设为 `True` 的检查项的监控。

此 API 调用没有请求参数。

### 响应状态码

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
curl SITE_ROOT/api/v1/checks/0c8983c9-9d73-446f-adb5-0641fdacc9d4/resume \
    --request POST --header "X-Api-Key: your-api-key" --data ""
```

注意：`--data ""` 参数强制 curl 发送 `Content-Length` 请求标头，即使请求体为空。对于 HTTP POST 请求，某些网络代理和 Web 服务器有时要求包含 `Content-Length` 标头。

### Example Response

```json
{
  "channels": "",
  "desc": "",
  "grace": 60,
  "last_ping": null,
  "next_ping": null,
  "n_pings": 0,
  "name": "Backups",
  "slug": "backups",
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "pause_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/pause",
  "resume_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/resume",
  "ping_url": "PING_ENDPOINTf618072a-7bde-4eee-af63-71a77c5723bc",
  "status": "new",
  "tags": "prod www",
  "timeout": 3600,
  "update_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc"
}
```


## 删除检查项 {: #delete-check .rule }

`DELETE SITE_ROOT/api/v1/checks/<uuid>`

从用户账户中永久删除检查项。返回刚被删除的检查项的 JSON 表示。

此 API 调用没有请求参数。

### 响应状态码

200 OK
:   检查项已成功删除。

401 Unauthorized
:   API 密钥缺失或无效。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   指定的检查项不存在。

### Example Request

```bash
curl SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc \
    --request DELETE --header "X-Api-Key: your-api-key"
```

### Example Response

```json
{
  "channels": "",
  "desc": "",
  "grace": 60,
  "last_ping": null,
  "n_pings": 0,
  "name": "Backups",
  "slug": "backups",
  "next_ping": null,
  "manual_resume": false,
  "methods": "",
  "start_kw": "",
  "success_kw": "",
  "failure_kw": "",
  "filter_subject": false,
  "filter_body": false,
  "pause_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/pause",
  "resume_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/resume",
  "ping_url": "PING_ENDPOINTf618072a-7bde-4eee-af63-71a77c5723bc",
  "status": "new",
  "tags": "prod www",
  "timeout": 3600,
  "update_url": "SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc",
}
```

## 列出检查项的 ping 记录 {: #list-pings .rule }

`GET SITE_ROOT/api/v1/checks/<uuid>/pings/`

返回此检查项收到的 ping 列表。

此端点按倒序返回 ping（最新的在前），返回的 ping 总数取决于账户的计费方案：免费账户 100 条，付费账户 1000 条。

### 响应状态码

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
curl SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/pings/ \
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


## 获取 ping 的请求体内容 {: #ping-body .rule }

`GET SITE_ROOT/api/v1/checks/<uuid>/pings/<n>/body`

返回 ping 记录中保存的请求体内容。响应始终带有 `Content-Type: text/plain` 响应标头，并且请求体会按原样在响应正文中返回。

### 响应状态码

200 OK
:   请求成功且存在请求体内容。

403 Forbidden
:   访问被拒绝，API 密钥错误。

404 Not Found
:   检查项不存在、ping 不存在或 ping 没有请求体数据。

### Example Request

```bash
curl SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/pings/397/body \
    --header "X-Api-Key: your-api-key"
```

## 列出检查项的状态变更 {: #list-flips .rule }

`GET SITE_ROOT/api/v1/checks/<uuid>/flips/`<br>
`GET SITE_ROOT/api/v1/checks/<unique_key>/flips/`

返回此检查项经历过的"状态变更"列表。状态变更是状态的改变（从"down"到"up"，或从"up"到"down"）。

### 查询参数

seconds=&lt;值&gt;
:   返回过去 `value` 秒内的状态变更。

    示例：

    `SITE_ROOT/api/v1/checks/<uuid|unique_key>/flips/?seconds=3600`

start=&lt;值&gt;
:   返回早于指定 UNIX 时间戳的状态变更。

    示例：

    `SITE_ROOT/api/v1/checks/<uuid|unique_key>/flips/?start=1592214380`

end=&lt;值&gt;
:   返回晚于指定 UNIX 时间戳的状态变更。

    示例：

    `SITE_ROOT/api/v1/checks/<uuid|unique_key>/flips/?end=1592217980`

### 响应状态码

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
curl SITE_ROOT/api/v1/checks/f618072a-7bde-4eee-af63-71a77c5723bc/flips/ \
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

`GET SITE_ROOT/api/v1/channels/`

返回属于该项目的集成列表。

### 响应状态码

200 OK
:   请求成功。

401 Unauthorized
:   API 密钥缺失或无效。

### Example Request

```bash
curl --header "X-Api-Key: your-api-key" SITE_ROOT/api/v1/channels/
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

`GET SITE_ROOT/api/v1/badges/`

返回项目中所有标签的映射，包含每个标签的徽章 URL。SITE_NAME 提供几种不同格式的徽章：

* `svg`：以 SVG 文档形式返回徽章。
* `json`：返回 JSON 文档，你可以用它自行生成自定义徽章。
* `shields`：以 [Shields.io 兼容格式](https://shields.io/endpoint)返回 JSON。

此外，徽章还有 2 状态和 3 状态两种变体：

* `svg`、`json`、`shields`：报告两种状态："up"和"down"。它将宽限期内的任何检查项仍视为"up"。
* `svg3`、`json3`、`shields3`：报告三种状态："up"、"late"和"down"。

响应中包含一个特殊的 `*` 条目：这个伪标签报告项目中所有检查项的总体状态。

### 响应状态码

200 OK
:   请求成功。

401 Unauthorized
:   API 密钥缺失或无效。

### Example Request

```bash
curl --header "X-Api-Key: your-api-key" SITE_ROOT/api/v1/badges/
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

