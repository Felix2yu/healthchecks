# Python

如果你已经在使用 [requests](https://requests.readthedocs.io/en/master/)
库，那么在这里也用它会很方便：

```python
import requests

try:
    requests.get("PING_URL", timeout=10)
except requests.RequestException as e:
    # 记录 ping 失败信息...
    print("Ping failed: %s" % e)
```

或者，你可以使用 Python 3 标准库中的 [urllib.request](https://docs.python.org/3/library/urllib.request.html)
模块：

```python
import socket
import urllib.request

try:
    urllib.request.urlopen("PING_URL", timeout=10)
except socket.error as e:
    # 记录 ping 失败信息...
    print("Ping failed: %s" % e)
```

你可以在请求体（POST 请求）中包含额外的诊断信息：

```python
# 在 POST 体中传递诊断信息：
import requests
requests.post("PING_URL", data="temperature=-7")
```
