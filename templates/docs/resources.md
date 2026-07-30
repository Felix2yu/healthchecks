# 第三方资源

与 SITE_NAME 集成的第三方软件项目集合。
请通过 [GitHub](https://github.com/healthchecks/healthchecks/issues) 提交补充和更正。

## 命令运行器、Shell 包装器

* [runitor](https://github.com/bdd/runitor) - 具有 Healthchecks.io 集成的命令运行器，让你的脚本和容器保持简单。
* [crontask.sh](https://github.com/pforret/crontask) – 用于 crontab 的 Bash 包装器。支持 ping。
* [task-mon](https://github.com/dimo414/task-mon) – 用于在命令运行时通知 Healthchecks.io 的小型二进制文件，用 Rust 编写。
* [hc-monitor](https://gist.github.com/odolbeau/bd6d8eb7910d1289e2687682c8db9275) – Bash 包装器，支持 ping。
* [pytocron](https://github.com/hartwork/pytocron) – 带有内置 Healthchecks 支持的 Python cron 实现。

## 自托管工具

* [linuxserver/docker-healthchecks](https://github.com/linuxserver/docker-healthchecks) – 替代 Docker 镜像
* [galexrt/docker-healthchecks](https://github.com/galexrt/docker-healthchecks) – 替代 Docker 镜像
* [Elestio](https://elest.io/open-source/healthchecks) – 具有 Healthchecks 支持的托管平台（使用 linuxserver 镜像）

## API 包装器

### Ansible

* [ansible-collections/community.healthchecksio](https://github.com/ansible-collections/community.healthchecksio) - 用于在 Healthchecks.io 上自动化任务的 Ansible 模块

### Go

* [kristofferahl/go-healthchecksio](https://github.com/kristofferahl/go-healthchecksio) – 支持列出、创建、更新、删除、暂停、ping。
* [gitlab.com/etke.cc/go/healthchecks](https://gitlab.com/etke.cc/go/healthchecks) – 支持 ping。

### PowerShell

* [davehope/HealthChecksIOStatusReport](https://github.com/davehope/HealthChecksIOStatusReport) – 支持 ping。
* [ptmorris1/healthchecks-pwsh](https://github.com/ptmorris1/healthchecks-pwsh) – 支持 ping 和所有 Management API 调用。

### Python

* [samarpan-rai/healthchecks_wrapper](https://github.com/samarpan-rai/healthchecks_wrapper) – Python 上下文管理器，支持 ping。
* [danidelvalle/healthchecks-decorator](https://github.com/danidelvalle/healthchecks-decorator) – Python 上下文管理器，支持 ping。
* [andrewthetechie/py-healthchecks.io](https://github.com/andrewthetechie/py-healthchecks.io) – 支持创建、ping。具有同步和异步实现。

### Rust

* [msfjarvis/healthchecks-rs](https://github.com/msfjarvis/healthchecks-rs) – 支持所有当前的 Ping API 和 Management API 调用。

### Terraform

* [terraform-provider-healthchecksio](https://github.com/kristofferahl/terraform-provider-healthchecksio) – Healthchecks.io 的 Terraform Provider。支持创建、更新、删除检查项。

## 备份软件集成

* [backrest](https://github.com/garethgeorge/backrest) – restic 的 Web UI 和编排器，包含 Healthchecks.io 支持。
* [binarybucks/restic-tools](https://github.com/binarybucks/restic-tools) – restic 备份的包装器，具有 Healthchecks.io 支持。
* [borgmatic](https://torsion.org/borgmatic/docs/how-to/monitor-your-backups/#healthchecks-hook) – Borg 的前端，包含 Healthchecks.io 支持。
* [emborg](https://emborg.readthedocs.io/en/latest/monitoring.html#healthchecks-io) – Borg 的前端，包含 Healthchecks.io 支持。

## 仪表盘

* [healthchecks/dashboard](https://github.com/healthchecks/dashboard) – 显示你账户中检查项状态的独立 HTML 页面。
* [nicoandrade/healthchecks-front](https://github.com/nicoandrade/healthchecks-front) – 漂亮且免费的 Web 仪表盘，在桌面和移动设备上都能很好地工作。
* [KumaBar](https://apps.apple.com/ca/app/kumabar/id6746335356?mt=12) – MacOS 菜单栏应用，支持 Uptime Kuma 和 Healthchecks.io。