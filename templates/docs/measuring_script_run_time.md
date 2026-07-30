# 测量脚本运行时间

在 ping URL 后追加 `/start`，并在任务开始时使用它发送信号。
收到 start 信号后，SITE_NAME 将显示检查项为"Started"。
它将存储"start"事件并显示任务执行时间。SITE_NAME
将任务执行时间计算为相邻"start"和"success"事件之间的时间间隔。

注意：如果在客户端向 ping URL 追加 `/start` 不可行，您也可以
配置 SITE_NAME 通过[在 HTTP 请求体中查找特定关键字](../configuring_checks/#filtering-rules)
来将 HTTP ping 分类为 start、success 或 failure 信号。

## 警报逻辑

SITE_NAME 对使用 `/start` 信号的任务应用额外的警报规则。

如果任务发送了"start"信号但未在其配置的宽限期内发送"success"
信号，SITE_NAME 将假定该任务
已失败。它将把该任务标记为"down"并发出发警报。

## 使用示例

以下是 Python 代码示例：

```python
import requests
URL = "PING_URL"


# "/start" 启动计时器：如果任务执行时间超过
# 配置的宽限期，SITE_NAME 将将其标记为"down"
try:
    requests.get(URL + "/start", timeout=5)
except requests.exceptions.RequestException:
    # 如果网络请求因任何原因失败，我们不希望
    # 它阻止主任务的运行
    pass


# TODO: 在此处运行任务
fib = lambda n: n if n < 2 else fib(n - 1) + fib(n - 2)
print("F(42) = %d" % fib(42))

# 发送 success 信号：
requests.get(URL)
```

## 查看测量的运行时间

当 SITE_NAME 收到"start"信号后跟常规 ping 或"fail"
信号，且两个事件相隔不到 72 小时时，
您将在检查项列表中看到显示的执行时间。如果两个事件
相隔超过 72 小时，则假定它们不相关，并且不显示
执行时间。

![带有执行时间的检查项列表](IMG_URL/checks_durations.png)

您还可以在查看单个检查项时看到先前运行的执行时间：

![带有执行时间的收到 ping 日志](IMG_URL/details_durations.png)

## 指定运行 ID

当同一任务的多个实例可以同时运行时，计算出的运行时间
可能出错，因为 SITE_NAME 无法可靠地确定哪个 success 事件
对应于哪个 start 事件。为解决此问题，客户端可以
在任何 ping URL 的 `rid` 查询参数中可选地指定运行 ID。当
success 事件指定了 `rid` 参数时，SITE_NAME 将在计算执行时间时查找
具有匹配 `rid` 值的 start 事件。

运行 ID 必须是特定格式：它们必须是规范文本表示形式的 UUID 值
（示例：`728b3763-ea80-4113-9fc0-f49b3adf226a`，注意没有
花括号）。UUID 中的字母可以是小写或
大写。

客户端可以自由地随机选择运行 ID 值，或使用确定性过程
来生成它们。唯一重要的是，单个任务执行的 start 和 success
ping 使用相同的运行 ID 值。

以下是使用 `uuidgen` 生成运行 ID 并使用 curl 发起 HTTP 请求的
示例 shell 脚本：

```bash
#!/bin/sh

RID=`uuidgen`

# 发送 start ping，指定 rid 参数：
curl -fsS -m 10 --retry 5 PING_URL/start?rid=$RID

# ... FIXME: 在此处运行任务 ...

# 发送 success ping，使用相同的 rid 参数：
curl -fsS -m 10 --retry 5 PING_URL?rid=$RID
```

如果客户端指定了运行 ID，SITE_NAME 将在"Events"
部分中以缩写形式显示它们：

![带有运行 ID 和执行时间的收到 ping 日志](IMG_URL/run_ids.png)

另外，请注意两个"success"事件都有执行时间。如果
在此示例中未使用运行 ID，事件 #4 将不显示执行时间，
因为它前面没有"start"事件。

## 使用运行 ID 时的警报逻辑

如果任务发送了"start"信号但未在其配置的宽限期内发送"success"
信号，SITE_NAME 将假定该任务
已失败并通知您。但是，使用运行 ID 时，有一个重要的
注意事项：SITE_NAME **不会监控所有并发任务运行的
执行时间**。它只会监控最近启动的运行
的执行时间。

为了说明，假设宽限期为 1 分钟，再次查看上面的示例。
事件 #4 运行了 6 分 39 秒，超出了 1 分钟的时间预算。
但 SITE_NAME 没有产生警报，因为**最近启动的
运行在时限内完成了**（耗时 37 秒，不到 1 分钟）。
