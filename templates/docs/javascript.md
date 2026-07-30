# Javascript

以下是从 Node.js 向 SITE_NAME 发起 HTTP 请求的最小示例。

```js
var https = require('https');
https.get('PING_URL').on('error', (err) => {
    console.log('Ping failed: ' + err)
});
```

注意："https" 库会异步执行请求。如果你同时发送 "start" 和 "success" 信号，
可能会遇到 "success" 信号在 "start" 信号之前到达的竞态条件。
通过使用回调、promise 或 async/await 特性可以避免竞态条件。以下是使用 async/await 和
[axios](https://axios-http.com/) 库的示例：

```js
const axios = require("axios");

async function ping(url) {
    try {
        await axios.get(url, {timeout: 5000});
    } catch(error) {
        // 记录错误并继续。ping 失败不应
        // 阻止任务运行。
        console.error("Ping failed: " + error);
    }
}

async function runJob() {
    var pingUrl = "PING_URL";

    await ping(pingUrl + "/start");
    try {
        console.log("TODO: 在此运行任务");

        await ping(pingUrl); // 成功
    } catch(error) {
        await ping(pingUrl + "/fail");
    }
}

runJob();
```

## 浏览器

你也可以从浏览器环境发送 ping。SITE_NAME 设置了
`Access-Control-Allow-Origin:*` CORS 头，因此跨域 AJAX 请求可以正常工作。

```js
var xhr = new XMLHttpRequest();
xhr.open('GET', 'PING_URL', true);
xhr.send(null);
```
