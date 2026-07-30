# Go

以下是从 Go 向 SITE_NAME 发起 HTTP 请求的示例。

```go
package main

import "fmt"
import "net/http"
import "time"

func main() {
    var client = &http.Client{
        Timeout: 10 * time.Second,
    }

    _, err := client.Head("PING_URL")
    if err != nil {
        fmt.Printf("%s", err)
    }
}

```
