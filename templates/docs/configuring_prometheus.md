# 配置 Prometheus

SITE_NAME 支持将指标和检查项状态导出到
[Prometheus](https://prometheus.io/)，以配合 [Grafana](https://grafana.com/) 使用。

## 创建只读 API 密钥

在 **Project Settings › API Access** 中创建一个只读 API 密钥。

确保使用**只读** API 密钥。Prometheus 不需要
读写 API 访问权限。

![项目的 API 密钥](IMG_URL/prometheus_api_keys.png)

## 更新 prometheus.yml

将以下抓取配置添加到 Prometheus：

```yaml
  - job_name: "healthchecks"
    scrape_interval: 60s
    scheme: SITE_SCHEME
    metrics_path: /projects/{your-project-uuid}/metrics/{your-readonly-api-key}
    static_configs:
      - targets: ["SITE_HOSTNAME"]
```

"{your-project-uuid}" 是您在浏览器地址栏中查看特定项目
的检查项列表时看到的 UUID。

重新加载 Prometheus，您的更改应该会生效，指标将以 `hc_` 前缀呈现。

## 可用指标

Prometheus 指标端点导出以下指标：

hc_check_up
:   对于每个检查项，指示该检查项当前是否正常
    （1 表示是，0 表示否）。

    标签：

    * `name` – 检查项的名称
    * `tags` – 检查项的标签，以文本字符串表示；多个标签以空格分隔
    * `unique_key` – 检查项的稳定唯一标识符（从检查项的代码派生）

hc_check_started
:   对于每个检查项，指示该检查项当前是否正在运行
    （1 表示是，0 表示否）。

    标签：

    * `name` – 检查项的名称
    * `tags` – 检查项的标签，以文本字符串表示；多个标签以空格分隔
    * `unique_key` – 检查项的稳定唯一标识符（从检查项的代码派生）

hc_check_grace
:   对于每个检查项，指示该检查项当前是否处于宽限期
    （1 表示是，0 表示否）。

    标签：

    * `name` – 检查项的名称
    * `tags` – 检查项的标签，以文本字符串表示；多个标签以空格分隔
    * `unique_key` – 检查项的稳定唯一标识符（从检查项的代码派生）

hc_check_paused
:   对于每个检查项，指示该检查项当前是否已暂停
    （1 表示是，0 表示否）。

    标签：

    * `name` – 检查项的名称
    * `tags` – 检查项的标签，以文本字符串表示；多个标签以空格分隔
    * `unique_key` – 检查项的稳定唯一标识符（从检查项的代码派生）

hc_tag_up
:   对于每个标签，指示具有此标签的所有检查项是否都正常
    （1 表示是，0 表示否）。

    标签：

    * `tag` – 标签名称

hc_checks_total
:   检查项的总数。

hc_checks_down_total
:   <br>当前宕机的检查项数量。

## 构建指向检查项详情页面的 URL

您可以使用 `unique_key` 标签来构建指向 SITE_NAME 中检查项
详情页面的 URL。像这样构建 URL：

```
SITE_ROOT/cloaked/{unique_key}/
```

## 使用 Grafana Cloud

Grafana Cloud 要求使用 HTTP "Basic"或"Bearer"认证方案对指标端点进行
认证。它拒绝抓取公共端点。
为满足此要求，SITE_NAME 提供了一个需要"Bearer"认证的
备用指标端点。将以下设置用于 Grafana Cloud：

* Scrape Job URL: `SITE_ROOT/projects/{your-project-uuid}/metrics/`
* Authentication type: Bearer
* Bearer token: 只读 API 密钥
