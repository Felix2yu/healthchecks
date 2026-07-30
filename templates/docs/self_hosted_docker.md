# 使用 Docker 运行

在 Healthchecks 源代码的 [/docker/ 目录](https://github.com/healthchecks/healthchecks/tree/master/docker)中，
您可以找到使用 [Docker](https://www.docker.com) 和 [Docker Compose](https://docs.docker.com/compose/)
运行项目的示例配置。

注意：为简单起见，示例配置启动单个数据库
节点和单个 Web 服务器节点，两者位于同一主机上。它不处理 TLS
终止。

## 入门指南

* 从 [GitHub 仓库](https://github.com/healthchecks/healthchecks)
  获取 Healthchecks 源代码。
* 将 `docker/.env.example` 复制到 `docker/.env` 并在其中添加您的配置。
  至少设置以下字段：
    * `ALLOWED_HOSTS` – 您的 Healthchecks 实例的域名。
    示例：`ALLOWED_HOSTS=hc.example.org`。
    * `DEFAULT_FROM_EMAIL` – 外发电子邮件的"From:"地址。
    * `EMAIL_HOST` – SMTP 服务器。
    * `EMAIL_HOST_PASSWORD` – SMTP 密码。
    * `EMAIL_HOST_USER` – SMTP 用户名。
    * `SECRET_KEY` – 保护 HTTP 会话，设置为随机值。
    * `SITE_ROOT` – 您的 Healthchecks 实例的公共基础 URL。示例：
    `SITE_ROOT=https://hc.example.org`。

* 创建并启动容器：

        $ cd docker
        $ docker compose up

* 创建超级用户：

        $ docker compose run web /opt/healthchecks/manage.py createsuperuser

    这将触发交互式提示。

    您也可以通过参数提供凭据，绕过交互式提示：

        $ docker compose run web /opt/healthchecks/manage.py createsuperuser --email user@example.com --password changeme123

* 在浏览器中打开 [http://localhost:8000](http://localhost:8000) 并使用
  上一步的凭据登录。

## uWSGI 配置

参考 Dockerfile 使用 [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/)
作为 WSGI 服务器。您可以通过在 `docker/.env` 中设置 `UWSGI_...` 环境
变量来配置 uWSGI。例如，要禁用 HTTP 请求日志，设置：

    UWSGI_DISABLE_LOGGING=1

要调整 uWSGI 进程数（例如，为节省内存），设置：

    UWSGI_PROCESSES=2

在 [uWSGI 文档](https://uwsgi-docs.readthedocs.io/en/latest/Configuration.html#environment-variables)
中阅读有关配置 uWSGI 的更多信息。

## 通过 `SMTPD_PORT` 配置 SMTP 监听器 {: #SMTPD_PORT }

Healthchecks 附带一个 `smtpd` 管理命令，用于运行 SMTP 监听
服务。运行该命令后，您可以通过发送电子邮件到
`your-uuid-here@hc.example.org` 电子邮件地址来 ping 您的检查项。

容器配置为根据 `SMTPD_PORT` 环境变量的值有条件地启动 SMTP 监听器：

* 如果未设置 `SMTPD_PORT` 环境变量，SMTP 监听器将不会运行。
* 如果设置了 `SMTPD_PORT`，监听器将运行并监听指定的端口。
  您可能还需要编辑 `docker-compose.yml` 以暴露监听端口
  （请参阅 `docker-compose.yml` 中"web"服务下的"ports"部分）。

条件逻辑存在于 uWSGI 配置文件中，
[uwsgi.ini](https://github.com/healthchecks/healthchecks/blob/master/docker/uwsgi.ini)。

另请参阅：[PING_EMAIL_DOMAIN](../self_hosted_configuration/#PING_EMAIL_DOMAIN)
环境变量，用于自定义电子邮件地址的域名部分。

## 反向代理、TLS 终止和 CSRF 保护 {: #tls-termination }

如果您计划将 Healthchecks 实例暴露到公共互联网，请确保在它前面
放置一个 TLS 终止反向代理或负载均衡器。

**重要：** 配置反向代理以设置 `X-Forwarded-For` 请求
头。Healthchecks 信任它来确定客户端的 IP 地址。如果代理
未设置 `X-Forwarded-For` 头，客户端可以传递自己的值并
绕过登录表单中基于 IP 的速率限制等功能。

**重要：** 此 Dockerfile 使用 uWSGI，它依赖 [X-Forwarded-Proto](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-Proto)
头来判断请求是否安全。没有此信息，您
在使用 Healthchecks 实例时可能会遇到 HTTP 403 "CSRF verification failed." 错误。
有关更多信息，请参见
[此 issue 评论](https://github.com/healthchecks/healthchecks/discussions/851#discussioncomment-6293396)。

确保您的 TLS 终止反向代理：

* 丢弃最终用户发送的 `X-Forwarded-Proto` 头。
* 将 `X-Forwarded-Proto` 头值设置为与原始请求的协议匹配
  （"http"或"https"）。

例如，在 NGINX 中，您可以像这样使用 `$scheme` 变量：

```text
proxy_set_header X-Forwarded-Proto $scheme;
```

如果您使用 haproxy，可以像这样实现相同效果：

```text
http-request set-header X-Forwarded-Proto https if { ssl_fc }
http-request set-header X-Forwarded-Proto http unless { ssl_fc }
```

## 让 Healthchecks 信任您的自签名 TLS 证书

如果您将 Healthchecks 配置为向使用自签名 TLS 证书的服务器
发送通知，您可能会在发送通知时看到
"TLS handshake failed"错误。

Healthchecks 使用 libcurl 发起出站 HTTP(S) 请求。curl 和 libcurl
会验证证书，如果无法验证证书则拒绝继续。
可以关闭证书验证，但这样做在
[curl 文档](https://curl.se/docs/sslcerts.html)中是被强烈不推荐的。

要让 curl 接受自托管证书，请将您的自签名证书添加到
Healthchecks 容器的信任存储中。

首先，将证书挂载到运行 healthchecks Web 应用程序的容器内部。
在 `docker-compose.yml` 的 `web:` 部分中添加以下内容：

```yaml
volumes:
    - /path/to/cert.pem:/usr/local/share/ca-certificates/my-selfsigned-cert.crt:ro
```

注意：`/path/to/cert.pem` 必须是主机系统中的**绝对路径**，指向
证书。

然后重新加载配置并在容器内以 root 用户身份运行
`update-ca-certificates`：

```sh
docker compose up
docker compose exec -u root web update-ca-certificates
```

## 升级数据库

当您在 `docker-compose.yml` 中升级数据库版本时（例如，
从 `postgres:12` 升级到 `postgres:16`），您还需要升级您的 postgres
数据目录。一种方法是使用
[pgautoupgrade](https://hub.docker.com/r/pgautoupgrade/pgautoupgrade) 容器。

步骤：

* 作为第一步，**对数据库进行完整备份**。
* 停止 `db` 和 `web` 容器：`docker compose stop`
* 使用 `docker volume ls` 查找 postgres 数据卷的名称
* 像这样运行 `pgautoupgrade`：

```
docker run --rm --name pgauto -it \
   --mount type=volume,source=<pg-volume-name-here>,target=/var/lib/postgresql/data \
   -e POSTGRES_PASSWORD=password \
   -e PGAUTO_ONESHOT=yes \
   pgautoupgrade/pgautoupgrade:16-bookworm
```

* 更新 `docker-compose.yml` 文件以使用 `postgres:16` 镜像
* 启动容器：`docker compose up`

## 预构建镜像

从 `/docker/` 目录中的 Dockerfile 构建的预构建 Docker 镜像，
可在 [Docker Hub](https://hub.docker.com/r/healthchecks/healthchecks) 上获取。
这些镜像会在每次新版本发布时自动构建。

Docker 镜像：

* 支持 amd64、arm/v7 和 arm64 架构。
* 使用 uWSGI 作为 Web 服务器。uWSGI 配置为在启动时执行数据库迁移，
  并在后台运行 `sendalerts`、`sendreports` 和 `smtpd`。
  您无需单独运行它们。
* 附带 PostgreSQL 和 MySQL 数据库驱动程序。
* 使用 whitenoise 库提供静态文件服务。
* 预装了 apprise 库。
* *不*处理 TLS 终止。在生产环境中，您需要将
  Healthchecks 容器放在处理 TLS 终止的反向代理或负载均衡器后面。

要在 `docker-compose.yml` 文件中使用 Healthchecks X.Y 版本的预构建镜像，
将"build"部分替换为：

```text
image: healthchecks/healthchecks:vX.Y
```
