# PHP

以下是从 PHP 向 SITE_NAME 发起 HTTP 请求的示例。

```php
file_get_contents('PING_URL');
```

如果你想要设置超时和重试选项（如[可靠性提示](../reliability_tips/)中所述），有一个
[curl 包](https://www.phpcurlclass.com/)可以轻松实现：

```php
use Curl\Curl;

$curl = new Curl();
$curl->setRetry(20);
$curl->setTimeout(5);
$curl->get('PING_URL');
```

注意：此代码不会抛出任何异常。
