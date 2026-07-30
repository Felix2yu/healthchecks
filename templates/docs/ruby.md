# Ruby

以下是从 Ruby 向 SITE_NAME 发起 HTTP 请求的示例。

```ruby
require 'net/http'
require 'uri'

Net::HTTP.get(URI.parse('PING_URL'))
```