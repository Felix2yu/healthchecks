# C\#

以下是从 C# 向 SITE_NAME 发起 HTTP 请求的示例。

```csharp
try
{
    using (var client = new System.Net.Http.HttpClient())
    {
        client.Timeout = System.TimeSpan.FromSeconds(10);
        client.GetAsync("PING_URL").Wait();
    }
}
catch (System.Exception ex)
{
    System.Console.WriteLine($"Ping failed: {ex.Message}");
}
```