# PowerShell

你可以使用 [PowerShell](https://docs.microsoft.com/en-us/powershell/scripting/overview?view=powershell-7.2)
和 Windows 任务计划程序在 Windows 系统上自动化各种任务。
在 PowerShell 脚本中也可以轻松地 ping SITE_NAME。

这是一个简单的 PowerShell 脚本，用于 ping SITE_NAME。当通过
任务计划程序调度运行时，它会定期发送"我还活着"的消息。
当然，你可以扩展它来做更多事情。

```powershell
# 将其保存为 .ps1 扩展名的文件，例如 C:\Scripts\healthchecks.ps1
# 运行它的命令：
#     powershell.exe -ExecutionPolicy bypass -File C:\Scripts\healthchecks.ps1
#
Invoke-RestMethod PING_URL
```

你可以在 HTTP POST 请求中发送额外的诊断信息：

```powershell
Invoke-RestMethod -Uri PING_URL -Method Post -Body "temperature=-7"
```

关于 `Invoke-RestMethod` cmdlet 中可用的其他参数，
请参阅官方 [Invoke-RestMethod 文档](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-7.2)。

除了将脚本放在 .ps1 文件中，你也可以使用 "-Command" 参数
直接将其传递给 PowerShell：

```bat
# 直接传递命令给 PowerShell：
powershell.exe -Command "&{Invoke-RestMethod PING_URL}"
```

