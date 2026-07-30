# 克隆检查项

你可以从"检查项详情"页面克隆单个检查项：

!["创建副本"按钮](IMG_URL/create_copy.png)

"创建副本..."功能会在同一项目中创建一个新的检查项，并复制以下内容：

* 名称、标签、描述
* 时间表
* 过滤规则
* 已分配的通知方式

新创建的检查项具有不同的 ping URL 和空的日志历史。

## 将所有检查项克隆到新项目

有时克隆整个项目会很有用。例如，在新区域重建已有部署时。SITE_NAME Web 界面没有克隆整个项目的功能，但你可以使用[管理 API](../api/) 调用来相对容易地克隆项目中的所有检查项。以下是使用 Python 和 [requests](https://requests.readthedocs.io/en/master/) 库的示例：

```python
import requests

API_URL = "SITE_ROOT/api/v3/checks/"
SOURCE_PROJECT_READONLY_KEY = "..."
TARGET_PROJECT_KEY = "..."

r = requests.get(API_URL, headers={"X-Api-Key": SOURCE_PROJECT_READONLY_KEY})
for check in r.json()["checks"]:
    print("Cloning %s" % check["name"])
    requests.post(API_URL, json=check, headers={"X-Api-Key": TARGET_PROJECT_KEY})
```
