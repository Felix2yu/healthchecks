# 自托管 Healthchecks

Healthchecks 是开源的，采用 BSD 3-clause 许可证。

除了使用位于 [https://healthchecks.io](https://healthchecks.io) 的托管服务外，
您还可以选择自行托管
Healthchecks 实例。

其构建模块包括：

* Python 3.12+
* Django 6.0
* PostgreSQL 或 MySQL

## 设置开发环境

您可以在本地系统的 Python
[虚拟环境](https://docs.python.org/3/tutorial/venv.html)中
设置开发环境，以开发新功能、编写新集成
或测试错误修复。

以下说明假设您使用基于 Debian 的操作系统。

* 安装依赖：

        $ sudo apt-get update
        $ sudo apt-get install -y gcc python3-dev python3-venv

* 准备项目代码和 virtualenv 的目录。请随意使用
  不同的位置：

        $ mkdir -p ~/webapps
        $ cd ~/webapps

* 准备虚拟环境
  （使用 virtualenv，您将获得 pip，我们很快就会用它来安装依赖）：

        $ python3 -m venv hc-venv
        $ source hc-venv/bin/activate

* 检出项目代码：

        $ git clone https://github.com/healthchecks/healthchecks.git

* 将依赖（Django 等）安装到 virtualenv 中：

        $ pip install wheel
        $ pip install -r healthchecks/requirements.txt

* 创建数据库表和超级用户帐户：

        $ cd ~/webapps/healthchecks
        $ ./manage.py migrate
        $ ./manage.py createsuperuser

    使用默认配置时，Healthchecks 将数据存储在项目目录下的 SQLite 文件
    `hc.sqlite` 中（`~/webapps/healthchecks/`）。

* 运行测试：

        $ ./manage.py test

* 运行开发服务器：

        $ ./manage.py runserver

* 在另一个 shell 中，运行负责发送通知的 `sendalerts` 管理命令：
        $ ./manage.py sendalerts

此时，站点应已在 `http://localhost:8000` 运行。

## 访问管理面板

Healthchecks 附带 Django 的管理面板，您可以在其中执行
管理任务：删除用户帐户、更改密码、提高特定用户的限制、
检查数据库表的内容。

要访问管理面板，如果您还没有创建超级用户帐户：

    $ ./manage.py createsuperuser

这将触发交互式提示。

您也可以通过参数提供凭据，绕过交互式提示：

    $ ./manage.py createsuperuser --email user@example.com --password changeme123

然后，使用超级用户凭据登录站点。登录后，
点击顶部导航中的"Account"下拉菜单，选择"Site Administration"。

## 发送电子邮件

Healthchecks 需要 SMTP 凭据才能发送电子邮件：
登录链接、监控通知、月度报告。

使用 `EMAIL_HOST`、`EMAIL_PORT`、`EMAIL_HOST_USER`、`EMAIL_HOST_PASSWORD`、`EMAIL_USE_SSL` 和 `EMAIL_USE_TLS` 环境变量指定 SMTP 凭据。
示例：

```ini
EMAIL_HOST=my-smtp-server-here.com
EMAIL_PORT=465
EMAIL_HOST_USER=my-username
EMAIL_HOST_PASSWORD=mypassword
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False
```

您可以在 Django 文档的 [Sending Email](https://docs.djangoproject.com/en/4.2/topics/email/)
部分阅读有关处理外发电子邮件的更多信息。

## 接收电子邮件

Healthchecks 附带一个 `smtpd` 管理命令，用于启动
SMTP 监听服务。运行该命令后，您可以通过发送电子邮件消息
来 ping 您的检查项。

在端口 2525 上启动 SMTP 监听器：

    $ ./manage.py smtpd --port 2525

发送测试邮件：

    $ curl --url 'smtp://127.0.0.1:2525' \
        --mail-from 'foo@example.org' \
        --mail-rcpt '11111111-1111-1111-1111-111111111111@my-hc.example.org' \
        -F '='

## 发送状态通知

`sendalerts` 管理命令持续轮询数据库以查找状态变化的检查项，
并根据需要发送通知。
当 `sendalerts` 未运行时，Healthchecks 实例将不发送任何
警报。

在激活的 virtualenv 中，按如下方式运行 `sendalerts` 命令：

    $ ./manage.py sendalerts

在生产设置中，确保 `sendalerts` 命令能够在
服务器重启后继续运行。

## 数据库清理 {: #database-cleanup }

Healthchecks 自动从 `api_ping`、`api_flip` 和 `api_notification`
表中删除旧条目。默认情况下，Healthchecks 为每个检查项保留最近的 100 条
ping。您可以设置更高的限制以保留更长的历史记录：
转到管理面板，查找用户的 **Profile** 并修改其
"Ping log limit"字段。

Healthchecks 提供了用于清理 `auth_user`（用户帐户）和 `api_tokenbucket`（速率限制记录）表的
管理命令，
以及用于从外部对象存储中删除过时对象的命令。

删除超过 1 个月且从未登录过的用户帐户：

```sh
$ ./manage.py pruneusers
```

从 `api_tokenbucket` 表中删除旧记录。TokenBucket
模型用于速率限制登录尝试和类似操作。
任何超过一天的记录都可以安全删除。

```sh
$ ./manage.py prunetokenbucket
```

从外部对象存储中删除旧对象。当用户删除
检查项、删除项目或关闭其帐户时，Healthchecks
不会立即从外部对象存储中删除关联的对象。
相反，您应该偶尔运行 `pruneobjects` 命令
（例如，每月一次）。此命令首先枚举
数据库中所有检查项，然后遍历对象存储桶中的顶级
键，并删除数据库中不存在的任何键。

```sh
$ ./manage.py pruneobjects
```

当您首次对数据运行这些命令时，最好先在
数据库副本上进行测试，而不是立即在实时数据库上操作。
在生产环境中，您需要定期运行这些命令，并
设置定期的自动数据库备份。

## 后续步骤

获取[源代码](https://github.com/healthchecks/healthchecks)。

查看[配置](../self_hosted_configuration/)以获取配置选项列表。
