# 服务器配置

Healthchecks 在 `hc/settings.py` 中准备其配置。它从环境变量中读取配置。
以下是它读取和使用的环境变量列表。

<ul class="self-hosted-configuration-toc">
<li><a href="#ADMINS">ADMINS</a></li>
<li><a href="#ALLOWED_HOSTS">ALLOWED_HOSTS</a></li>
<li><a href="#APPRISE_ENABLED">APPRISE_ENABLED</a></li>
<li><a href="#DB">DB</a></li>
<li><a href="#DB_CONN_MAX_AGE">DB_CONN_MAX_AGE</a></li>
<li><a href="#DB_HOST">DB_HOST</a></li>
<li><a href="#DB_NAME">DB_NAME</a></li>
<li><a href="#DB_PASSWORD">DB_PASSWORD</a></li>
<li><a href="#DB_PASSWORD_FILE">DB_PASSWORD_FILE</a></li>
<li><a href="#DB_PORT">DB_PORT</a></li>
<li><a href="#DB_SSLMODE">DB_SSLMODE</a></li>
<li><a href="#DB_TARGET_SESSION_ATTRS">DB_TARGET_SESSION_ATTRS</a></li>
<li><a href="#DB_USER">DB_USER</a></li>
<li><a href="#DEBUG">DEBUG</a></li>
<li><a href="#DEFAULT_FROM_EMAIL">DEFAULT_FROM_EMAIL</a></li>
<li><a href="#DISCORD_CLIENT_ID">DISCORD_CLIENT_ID</a></li>
<li><a href="#DISCORD_CLIENT_SECRET">DISCORD_CLIENT_SECRET</a></li>
<li><a href="#DISCORD_CLIENT_SECRET_FILE">DISCORD_CLIENT_SECRET_FILE</a></li>
<li><a href="#EMAIL_HOST">EMAIL_HOST</a></li>
<li><a href="#EMAIL_HOST_PASSWORD">EMAIL_HOST_PASSWORD</a></li>
<li><a href="#EMAIL_HOST_PASSWORD_FILE">EMAIL_HOST_PASSWORD_FILE</a></li>
<li><a href="#EMAIL_HOST_USER">EMAIL_HOST_USER</a></li>
<li><a href="#EMAIL_PORT">EMAIL_PORT</a></li>
<li><a href="#EMAIL_USE_TLS">EMAIL_USE_TLS</a></li>
<li><a href="#EMAIL_USE_SSL">EMAIL_USE_SSL</a></li>
<li><a href="#EMAIL_USE_VERIFICATION">EMAIL_USE_VERIFICATION</a></li>
<li><a href="#GITHUB_CLIENT_ID">GITHUB_CLIENT_ID</a></li>
<li><a href="#GITHUB_CLIENT_SECRET">GITHUB_CLIENT_SECRET</a></li>
<li><a href="#GITHUB_CLIENT_SECRET_FILE">GITHUB_CLIENT_SECRET_FILE</a></li>
<li><a href="#GITHUB_PRIVATE_KEY">GITHUB_PRIVATE_KEY</a></li>
<li><a href="#GITHUB_PRIVATE_KEY_FILE">GITHUB_PRIVATE_KEY_FILE</a></li>
<li><a href="#GITHUB_PUBLIC_LINK">GITHUB_PUBLIC_LINK</a></li>
<li><a href="#http_proxy">http_proxy and https_proxy</a></li>
<li><a href="#INTEGRATIONS_ALLOW_PRIVATE_IPS">INTEGRATIONS_ALLOW_PRIVATE_IPS</a></li>
<li><a href="#MASTER_BADGE_URL">MASTER_BADGE_LABEL</a></li>
<li><a href="#MATRIX_ACCESS_TOKEN">MATRIX_ACCESS_TOKEN</a></li>
<li><a href="#MATRIX_ACCESS_TOKEN_FILE">MATRIX_ACCESS_TOKEN_FILE</a></li>
<li><a href="#MATRIX_HOMESERVER">MATRIX_HOMESERVER</a></li>
<li><a href="#MATRIX_USER_ID">MATRIX_USER_ID</a></li>
<li><a href="#MATTERMOST_ENABLED">MATTERMOST_ENABLED</a></li>
<li><a href="#MSTEAMS_ENABLED">MSTEAMS_ENABLED</a></li>
<li><a href="#NTFY_SH_TOKEN">NTFY_SH_TOKEN</a></li>
<li><a href="#NTFY_SH_TOKEN_FILE">NTFY_SH_TOKEN_FILE</a></li>
<li><a href="#OPSGENIE_ENABLED">OPSGENIE_ENABLED</a></li>
<li><a href="#PAGERTREE_ENABLED">PAGERTREE_ENABLED</a></li>
<li><a href="#PD_APP_ID">PD_APP_ID</a></li>
<li><a href="#PD_ENABLED">PD_ENABLED</a></li>
<li><a href="#PING_BODY_LIMIT">PING_BODY_LIMIT</a></li>
<li><a href="#PING_EMAIL_DOMAIN">PING_EMAIL_DOMAIN</a></li>
<li><a href="#PING_ENDPOINT">PING_ENDPOINT</a></li>
<li><a href="#PROMETHEUS_ENABLED">PROMETHEUS_ENABLED</a></li>
<li><a href="#PUSHBULLET_CLIENT_ID">PUSHBULLET_CLIENT_ID</a></li>
<li><a href="#PUSHBULLET_CLIENT_SECRET">PUSHBULLET_CLIENT_SECRET</a></li>
<li><a href="#PUSHBULLET_CLIENT_SECRET_FILE">PUSHBULLET_CLIENT_SECRET_FILE</a></li>
<li><a href="#PUSHOVER_API_TOKEN">PUSHOVER_API_TOKEN</a></li>
<li><a href="#PUSHOVER_API_TOKEN_FILE">PUSHOVER_API_TOKEN_FILE</a></li>
<li><a href="#PUSHOVER_EMERGENCY_EXPIRATION">PUSHOVER_EMERGENCY_EXPIRATION</a></li>
<li><a href="#PUSHOVER_EMERGENCY_RETRY_DELAY">PUSHOVER_EMERGENCY_RETRY_DELAY</a></li>
<li><a href="#PUSHOVER_SUBSCRIPTION_URL">PUSHOVER_SUBSCRIPTION_URL</a></li>
<li><a href="#REGISTRATION_OPEN">REGISTRATION_OPEN</a></li>
<li><a href="#REMOTE_USER_HEADER">REMOTE_USER_HEADER</a></li>
<li><a href="#ROCKETCHAT_ENABLED">ROCKETCHAT_ENABLED</a></li>
<li><a href="#RP_ID">RP_ID</a></li>
<li><a href="#S3_ACCESS_KEY">S3_ACCESS_KEY</a></li>
<li><a href="#S3_BUCKET">S3_BUCKET</a></li>
<li><a href="#S3_ENDPOINT">S3_ENDPOINT</a></li>
<li><a href="#S3_REGION">S3_REGION</a></li>
<li><a href="#S3_SECRET_KEY">S3_SECRET_KEY</a></li>
<li><a href="#S3_SECRET_KEY_FILE">S3_SECRET_KEY_FILE</a></li>
<li><a href="#S3_TIMEOUT">S3_TIMEOUT</a></li>
<li><a href="#S3_SECURE">S3_SECURE</a></li>
<li><a href="#SECRET_KEY">SECRET_KEY</a></li>
<li><a href="#SECRET_KEY_FILE">SECRET_KEY_FILE</a></li>
<li><a href="#SECURE_PROXY_SSL_HEADER">SECURE_PROXY_SSL_HEADER</a></li>
<li><a href="#SHELL_ENABLED">SHELL_ENABLED</a></li>
<li><a href="#SIGNAL_CLI_SOCKET">SIGNAL_CLI_SOCKET</a></li>
<li><a href="#SITE_LOGO_URL">SITE_LOGO_URL</a></li>
<li><a href="#SITE_NAME">SITE_NAME</a></li>
<li><a href="#SITE_ROOT">SITE_ROOT</a></li>
<li><a href="#SLACK_CLIENT_ID">SLACK_CLIENT_ID</a></li>
<li><a href="#SLACK_CLIENT_SECRET">SLACK_CLIENT_SECRET</a></li>
<li><a href="#SLACK_CLIENT_SECRET_FILE">SLACK_CLIENT_SECRET_FILE</a></li>
<li><a href="#SLACK_ENABLED">SLACK_ENABLED</a></li>
<li><a href="#SPIKE_ENABLED">SPIKE_ENABLED</a></li>
<li><a href="#TELEGRAM_BOT_NAME">TELEGRAM_BOT_NAME</a></li>
<li><a href="#TELEGRAM_TOKEN">TELEGRAM_TOKEN</a></li>
<li><a href="#TELEGRAM_TOKEN_FILE">TELEGRAM_TOKEN_FILE</a></li>
<li><a href="#TRELLO_APP_KEY">TRELLO_APP_KEY</a></li>
<li><a href="#TRELLO_APP_KEY_FILE">TRELLO_APP_KEY_FILE</a></li>
<li><a href="#TWILIO_ACCOUNT">TWILIO_ACCOUNT</a></li>
<li><a href="#TWILIO_AUTH">TWILIO_AUTH</a></li>
<li><a href="#TWILIO_AUTH_FILE">TWILIO_AUTH_FILE</a></li>
<li><a href="#TWILIO_FROM">TWILIO_FROM</a></li>
<li><a href="#TWILIO_MESSAGING_SERVICE_SID">TWILIO_MESSAGING_SERVICE_SID</a></li>
<li><a href="#TWILIO_USE_WHATSAPP">TWILIO_USE_WHATSAPP</a></li>
<li><a href="#USE_PAYMENTS">USE_PAYMENTS</a></li>
<li><a href="#VICTOROPS_ENABLED">VICTOROPS_ENABLED</a></li>
<li><a href="#WEBHOOKS_ENABLED">WEBHOOKS_ENABLED</a></li>
<li><a href="#WHATSAPP_DOWN_CONTENT_SID">WHATSAPP_DOWN_CONTENT_SID</a></li>
<li><a href="#WHATSAPP_UP_CONTENT_SID">WHATSAPP_UP_CONTENT_SID</a></li>
<li><a href="#ZULIP_ENABLED">ZULIP_ENABLED</a></li>
</ul>

## `ADMINS` {: #ADMINS }

默认值：`""`（空字符串）

用于发送代码错误通知的电子邮件地址列表，以逗号分隔。当 `DEBUG=False` 时，Healthchecks 会将请求/响应周期中引发的异常详情发送到列出的地址。示例：

```ini
ADMINS=alice@example.org,bob@example.org
```

注意：要使错误通知生效，请确保你还在 `EMAIL_...` 环境变量中指定了有效的 SMTP 凭据。

## `ALLOWED_HOSTS` {: #ALLOWED_HOSTS }

默认值：`SITE_ROOT` 的域名部分

此站点可以服务的主机/域名。Healthchecks 会自动用 [SITE_ROOT](#SITE_ROOT) 的域名部分填充此设置。除非你在多个域名上提供 Healthchecks 服务，否则无需设置。

如果确实在多个域名上提供同一 Healthchecks 实例的服务，请在 `ALLOWED_HOSTS` 中指定它们，以逗号分隔：

```ini
ALLOWED_HOSTS=first.example.org,second.example.org
```

除了逗号分隔语法之外，这是一个标准的 Django 设置。在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts)中了解更多。

## `APPRISE_ENABLED` {: #APPRISE_ENABLED }

默认值：`False`

一个布尔值，用于开启/关闭 [Apprise](https://github.com/caronc/apprise) 集成。

在启用 Apprise 集成之前，请确保已安装 `apprise` 包：

```bash
pip install apprise
```

## `DB` {: #DB }

默认值：`sqlite`

要使用的数据库引擎。可能的值：`sqlite`、`postgres`、`mysql`。

## `DB_CONN_MAX_AGE` {: #DB_CONN_MAX_AGE }

默认值：`0`

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#conn-max-age)中了解更多。

## `DB_HOST` {: #DB_HOST }

默认值：`""`（空字符串）

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#host)中了解更多。

## `DB_NAME` {: #DB_NAME }

默认值：`hc`（PostgreSQL、MySQL）或 `/path/to/projectdir/hc.sqlite`（SQLite）

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#name)中了解更多。

## `DB_PASSWORD` {: #DB_PASSWORD }

默认值：`""`（空字符串）

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#password)中了解更多。

## `DB_PASSWORD_FILE` {: #DB_PASSWORD_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [DB_PASSWORD](#DB_PASSWORD) 设置。如果同时设置了 `DB_PASSWORD` 和 `DB_PASSWORD_FILE`，则 `DB_PASSWORD_FILE` 优先。

## `DB_PORT` {: #DB_PORT }

默认值：`""`（空字符串）

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#port)中了解更多。

## `DB_SSLMODE` {: #DB_SSLMODE }

默认值：`prefer`

PostgreSQL 专用，[详情](https://www.postgresql.org/docs/10/libpq-connect.html#LIBPQ-CONNECT-SSLMODE)

## `DB_TARGET_SESSION_ATTRS` {: #DB_TARGET_SESSION_ATTRS }

默认值：`read-write`

PostgreSQL 专用，[详情](https://www.postgresql.org/docs/10/libpq-connect.html#LIBPQ-CONNECT-TARGET-SESSION-ATTRS)

## `DB_USER` {: #DB_USER }

默认值：`postgres`（PostgreSQL）或 `root`（MySQL）

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#user)中了解更多。

## `DEBUG` {: #DEBUG }

默认值：`True`

一个布尔值，用于开启/关闭调试模式。

_切勿在生产环境中以调试模式运行 Healthchecks 实例！_

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#debug)中了解更多。

## `DEFAULT_FROM_EMAIL` {: #DEFAULT_FROM_EMAIL }

默认值：`healthchecks@example.org`

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#default-from-email)中了解更多。

## `DISCORD_CLIENT_ID` {: #DISCORD_CLIENT_ID }

默认值：`None`

Discord 客户端 ID，Discord 集成所需。

设置 Discord 集成：

* 在 [https://discordapp.com/developers/applications/me](https://discordapp.com/developers/applications/me) 注册一个新应用
* 为你的 Discord 应用添加重定向 URI。URI 格式为 `SITE_ROOT/integrations/add_discord/`。例如，如果你的 `SITE_ROOT` 是 `https://my-hc.example.org`，则重定向 URI 为 `https://my-hc.example.org/integrations/add_discord/`
* 查找你的 Discord 应用的_客户端 ID_ 和_客户端密钥_。将它们放入 `DISCORD_CLIENT_ID` 和 `DISCORD_CLIENT_SECRET` 环境变量中。

## `DISCORD_CLIENT_SECRET` {: #DISCORD_CLIENT_SECRET }

默认值：`None`

Discord 客户端密钥，Discord 集成所需。在 [https://discordapp.com/developers/applications/me](https://discordapp.com/developers/applications/me) 查找。

## `DISCORD_CLIENT_SECRET_FILE` {: #DISCORD_CLIENT_SECRET_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [DISCORD_CLIENT_SECRET](#DISCORD_CLIENT_SECRET) 设置。如果同时设置了 `DISCORD_CLIENT_SECRET` 和 `DISCORD_CLIENT_SECRET_FILE`，则 `DISCORD_CLIENT_SECRET_FILE` 优先。

## `EMAIL_HOST` {: #EMAIL_HOST }

默认值：`""`（空字符串）

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#email-host)中了解更多。

## `EMAIL_HOST_PASSWORD` {: #EMAIL_HOST_PASSWORD }

默认值：`""`（空字符串）

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#email-host-password)中了解更多。

## `EMAIL_HOST_PASSWORD_FILE` {: #EMAIL_HOST_PASSWORD_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [EMAIL_HOST_PASSWORD](#EMAIL_HOST_PASSWORD) 设置。如果同时设置了 `EMAIL_HOST_PASSWORD` 和 `EMAIL_HOST_PASSWORD_FILE`，则 `EMAIL_HOST_PASSWORD_FILE` 优先。

## `EMAIL_HOST_USER` {: #EMAIL_HOST_USER }

默认值：`""`（空字符串）

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#email-host-user)中了解更多。

## `EMAIL_PORT` {: #EMAIL_PORT }

默认值：`587`

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#email-port)中了解更多。

## `EMAIL_USE_TLS` {: #EMAIL_USE_TLS }

默认值：`True`

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#email-use-tls)中了解更多。

## `EMAIL_USE_SSL` {: #EMAIL_USE_SSL}

默认值：`False`

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#email-use-ssl)中了解更多。

## `EMAIL_USE_VERIFICATION` {: #EMAIL_USE_VERIFICATION }

默认值：`True`

一个布尔值，用于开启/关闭添加电子邮件集成时的验证步骤。

如果启用，每当用户添加电子邮件集成时，Healthchecks 会向新地址发送一封验证链接邮件。新的集成只有在用户单击验证链接后才会激活。

如果你在设置一个受信任的私有 Healthchecks 实例，你可以选择禁用验证步骤。在这种情况下，将 `EMAIL_USE_VERIFICATION` 设置为 `False`。

## `GITHUB_CLIENT_ID` {: #GITHUB_CLIENT_ID }

默认值：`None`

GitHub 客户端 ID，GitHub Issues 集成所需。

设置 GitHub Issues 集成：

* [注册一个新的 GitHub App](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app)（不是 OAuth 应用）。
* 在 GitHub App 设置中，在 **General › About** 下查找**客户端 ID** 和**公共链接**值，分别放入 Healthchecks 的 `GITHUB_CLIENT_ID` 和 `GITHUB_PUBLIC_LINK` 环境变量。
* 在 **General › Client secrets** 下生成客户端密钥，放入 Healthchecks 的 `GITHUB_CLIENT_SECRET` 环境变量。
* 在 **General › Identifying and authorizing users** 下设置**回调 URL**。URL 格式为 `SITE_ROOT/integrations/add_github/`。例如，如果你的 `SITE_ROOT` 是 `https://my-hc.example.org`，则回调 URL 为 `https://my-hc.example.org/integrations/add_github/`。
* 在 **General › Post installation** 下，将**设置 URL** 设置为相同的值。
* 在 **General › Private keys** 下生成私钥，放入 Healthchecks 的 `GITHUB_PRIVATE_KEY` 环境变量。
* 在 **Permissions & events › Repository permissions** 下，将"Issues"权限设置为"Read and write"。

## `GITHUB_CLIENT_SECRET` {: #GITHUB_CLIENT_SECRET }

默认值：`None`

GitHub App 的客户端密钥，GitHub Issues 集成所需。

## `GITHUB_CLIENT_SECRET_FILE` {: #GITHUB_CLIENT_SECRET_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [GITHUB_CLIENT_SECRET](#GITHUB_CLIENT_SECRET) 设置。如果同时设置了 `GITHUB_CLIENT_SECRET` 和 `GITHUB_CLIENT_SECRET_FILE`，则 `GITHUB_CLIENT_SECRET_FILE` 优先。

## `GITHUB_PRIVATE_KEY` {: #GITHUB_PRIVATE_KEY }

默认值：`None`

GitHub App 的私钥，GitHub Issues 集成所需。

## `GITHUB_PRIVATE_KEY_FILE` {: #GITHUB_PRIVATE_KEY_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [GITHUB_PRIVATE_KEY](#GITHUB_PRIVATE_KEY) 设置。如果同时设置了 `GITHUB_PRIVATE_KEY` 和 `GITHUB_PRIVATE_KEY_FILE`，则 `GITHUB_PRIVATE_KEY_FILE` 优先。

## `GITHUB_PUBLIC_LINK` {: #GITHUB_PUBLIC_LINK }

默认值：`None`

指向 GitHub App 在 GitHub 网站上的公共页面的 URL，GitHub Issues 集成所需。

## `http_proxy` and `https_proxy` {: #http_proxy}

默认值：`""`（空字符串）

指定用于出站 HTTP 和 HTTPS 请求的代理服务器。支持不同的代理服务器类型。示例：

```ini
https_proxy=http://example.org:1234
https_proxy=https://example.org:1234
https_proxy=socks4://example.org:1234
https_proxy=socks5://example.org:1234
```

Healthchecks 使用 libcurl 作为 HTTP 客户端库来发出 HTTP(S) 请求。有关代理功能的更多信息，请参阅 [libcurl 文档](https://curl.se/libcurl/c/CURLOPT_PROXY.html)。

注意：如果你的代理服务器具有私有 IP 地址，你还需要将 `INTEGRATIONS_ALLOW_PRIVATE_IPS` 设置为 `True` 才能使用它。

## `INTEGRATIONS_ALLOW_PRIVATE_IPS` {: #INTEGRATIONS_ALLOW_PRIVATE_IPS }

默认值：`False`

一个布尔值，控制集成是否允许向私有 IP 地址（127.0.0.1、192.168.x.x 等）发出 HTTP(S) 请求。默认情况下此设置为 `False`，因为允许用户定义探测内部地址的 Webhook 存在安全风险。

只有在受信任的环境中运行 Healthchecks 实例，并且需要与内部网络中的服务集成时，才启用此设置。

此设置影响除 Apprise 之外的所有集成类型，而不仅仅是 Webhook。例如，如果你在 `localhost` 上运行 Gotify 实例，你需要启用 `INTEGRATIONS_ALLOW_PRIVATE_IPS` 才能通过 Gotify 集成使用它。

此设置影响所有出站 HTTP 请求，包括在设置新集成时发出的请求（例如在 OAuth2 授权流程期间）。

此设置也影响在设置 `http_proxy` 或 `https_proxy` 环境变量时与代理服务器的连接。如果你的代理服务器具有私有 IP 地址，你需要启用 `INTEGRATIONS_ALLOW_PRIVATE_IPS` 才能使用它。

此设置*不*影响 Apprise 集成，因为 Apprise 库使用自己的 HTTP 客户端。无论此设置如何，Apprise 都可以向私有 IP 发出请求。

## `MASTER_BADGE_LABEL` {: #MASTER_BADGE_URL }

默认值：与 `SITE_NAME` 相同

"总体状态"状态徽章的标签。

## `MATRIX_ACCESS_TOKEN` {: #MATRIX_ACCESS_TOKEN }

默认值：`None`

[Matrix](https://matrix.org/) 机器人用户的访问令牌，Matrix 集成所需。

设置 Matrix 集成：

* 在你首选的 Matrix 主服务器上注册一个机器人用户（用于发布通知）。
* 使用[登录 API 调用](https://www.matrix.org/docs/guides/client-server-api#login)检索机器人用户的访问令牌。你可以按照文档中的说明，使用 curl 在命令 shell 中运行它。
* 设置 `MATRIX_` 环境变量。示例：

```ini
MATRIX_ACCESS_TOKEN=[登录调用返回的一长串字符]
MATRIX_HOMESERVER=https://matrix.org
MATRIX_USER_ID=@mychecks:matrix.org
```

## `MATRIX_ACCESS_TOKEN_FILE` {: #MATRIX_ACCESS_TOKEN_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [MATRIX_ACCESS_TOKEN](#MATRIX_ACCESS_TOKEN) 设置。如果同时设置了 `MATRIX_ACCESS_TOKEN` 和 `MATRIX_ACCESS_TOKEN_FILE`，则 `MATRIX_ACCESS_TOKEN_FILE` 优先。

## `MATRIX_HOMESERVER` {: #MATRIX_HOMESERVER }

默认值：`None`

Matrix 机器人的主服务器地址，Matrix 集成所需。

## `MATRIX_USER_ID` {: #MATRIX_USER_ID }

默认值：`None`

Matrix 机器人的用户标识符，Matrix 集成所需。

## `MATTERMOST_ENABLED` {: #MATTERMOST_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 Mattermost 集成。默认启用。

## `MSTEAMS_ENABLED` {: #MSTEAMS_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 MS Teams 集成。默认启用。

## `NTFY_SH_TOKEN` {: #NTFY_SH_TOKEN }

默认值：`None`

向托管的 ntfy.sh 服务器发送 ntfy 通知时使用的默认访问令牌。此令牌仅在发送到 `https://ntfy.sh` 的 ntfy 服务器且用户在设置 ntfy 集成时未指定自己的访问令牌时使用。

如果你的 Healthchecks 实例达到了 ntfy.sh 免费计划的[每日发送限制](https://docs.ntfy.sh/publish/#limitations)，并且你希望确保未自带访问令牌的 ntfy 集成能够可靠地投递通知，请使用此设置。

## `NTFY_SH_TOKEN_FILE` {: #NTFY_SH_TOKEN_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [NTFY_SH_TOKEN](#NTFY_SH_TOKEN) 设置。如果同时设置了 `NTFY_SH_TOKEN` 和 `NTFY_SH_TOKEN_FILE`，则 `NTFY_SH_TOKEN_FILE` 优先。

## `OPSGENIE_ENABLED` {: #OPSGENIE_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 Opsgenie 集成。默认启用。

## `PAGERTREE_ENABLED` {: #PAGERTREE_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 PagerTree 集成。默认启用。

## `PD_APP_ID` {: #PD_APP_ID }

默认值：`None`

PagerDuty 应用 ID。如果设置，启用 PagerDuty [简单安装流程](https://developer.pagerduty.com/docs/app-integration-development/events-integration/)。如果为 `None`，Healthchecks 将回退到更简单的流程，用户手动从 PagerDuty 复制集成密钥并粘贴到 Healthchecks 中。

设置步骤：

* 在 [PagerDuty](https://pagerduty.com/) › 开发者模式 › 我的应用 中注册一个 PagerDuty 应用
* 在新创建的应用中，添加"Events Integration"功能
* 指定重定向 URL：`https://your-domain.com/integrations/add_pagerduty/`
* 复制显示的 app_id 值（PXXXXX）并放入 `PD_APP_ID` 环境变量

## `PD_ENABLED` {: #PD_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 PagerDuty 集成。默认启用。

## `PING_BODY_LIMIT` {: #PING_BODY_LIMIT }

默认值：`10000`

记录的 ping 请求体的最大字节数限制。默认值为 10000（10 KB）。你可以调整限制，或者通过将此值设置为 `None` 来完全移除限制。

## `PING_EMAIL_DOMAIN` {: #PING_EMAIL_DOMAIN }

Default: `localhost`

用于生成 ping 电子邮件地址的域名。示例：

```ini
PING_EMAIL_DOMAIN=hc.example.org
```

在此示例中，Healthchecks 将生成类似于
`3f1a7317-8e96-437c-a17d-b0d550b51e86@hc.example.org` 的 ping 电子邮件地址。

此设置仅控制 ping 电子邮件地址的构建方式，
其本身不会启用通过发送电子邮件进行 ping 的功能。要接收
电子邮件，您还需要：

* 一条将 `hc.example.org` 指向您的 Healthchecks 实例 IP 地址的 DNS 记录。
* `manage.py smtpd`（Healthchecks 的 SMTP 监听服务）正在运行，监听
  端口 25，并且可从外部世界访问。如果您使用的是
  [官方 Docker 镜像](https://hub.docker.com/r/healthchecks/healthchecks)，
  请参阅[此处的说明](../self_hosted_docker/#SMTPD_PORT)以了解如何启用 SMTP
  监听服务。

## `PING_ENDPOINT` {: #PING_ENDPOINT }

Default: `SITE_ROOT` + `/ping/`

用于构建显示用 ping URL 的基础 URL。Healthchecks 通过将 UUID 值或 `<ping-key>/<slug>` 值追加到 `PING_ENDPOINT` 来构建 ping URL。

注意：

* 确保 `PING_ENDPOINT` 值以尾部斜杠结尾。如果缺少尾部斜杠，
  Healthchecks *不会*隐式添加它。
* Healthchecks 使用 `PING_ENDPOINT` 来格式化用于显示的 ping URL。
  `PING_ENDPOINT` 值不影响传入 HTTP 请求的路由。
  如果您更改 `PING_ENDPOINT` 值，您可能还需要在反向代理配置中添加匹配的
  URL 重写规则。

Example:

```ini
PING_ENDPOINT=https://ping.my-hc.example.org/
```

使用此设置，Healthchecks 将生成类似于以下的 ping URL：

```
https://ping.my-hc.example.org/3f1a7317-8e96-437c-a17d-b0d550b51e86
https://ping.my-hc.example.org/1fj9XWM6Ns8vLGTmnPGk9g/dummy-slug
```

## `PROMETHEUS_ENABLED` {: #PROMETHEUS_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 Prometheus 集成。默认启用。

## `PUSHBULLET_CLIENT_ID` {: #PUSHBULLET_CLIENT_ID }

默认值：`None`

Pushbullet 客户端 ID，Pushbullet 集成所需。

设置 Pushbullet 集成：

* 在 [https://www.pushbullet.com/#settings/clients](https://www.pushbullet.com/#settings/clients) 添加新的 OAuth 客户端
* 为你的 OAuth 客户端添加 `redirect_uri`。URI 格式为 `SITE_ROOT/integrations/add_pushbullet/`。例如，如果你的 `SITE_ROOT` 是 `https://my-hc.example.org`，则 `redirect_uri` 为 `https://my-hc.example.org/integrations/add_pushbullet/`
* 查找你的 OAuth 客户端的 `client_id` 和 `client_secret` 值。将它们放入 `PUSHBULLET_CLIENT_ID` 和 `PUSHBULLET_CLIENT_SECRET` 环境变量。

在 [Pushbullet OAuth2 指南](https://docs.pushbullet.com/#oauth2)中阅读有关设置 Pushbullet OAuth 客户端的更多信息。

## `PUSHBULLET_CLIENT_SECRET` {: #PUSHBULLET_CLIENT_SECRET }

默认值：`None`

Pushbullet 客户端密钥，Pushbullet 集成所需。在 [https://www.pushbullet.com/#settings/clients](https://www.pushbullet.com/#settings/clients) 查找。

## `PUSHBULLET_CLIENT_SECRET_FILE` {: #PUSHBULLET_CLIENT_SECRET_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [PUSHBULLET_CLIENT_SECRET](#PUSHBULLET_CLIENT_SECRET) 设置。如果同时设置了 `PUSHBULLET_CLIENT_SECRET` 和 `PUSHBULLET_CLIENT_SECRET_FILE`，则 `PUSHBULLET_CLIENT_SECRET_FILE` 优先。

## `PUSHOVER_API_TOKEN` {: #PUSHOVER_API_TOKEN }

默认值：`None`

[Pushover](https://pushover.net/) API 令牌，Pushover 集成所需。

启用 Pushover 集成：

* 在 [https://pushover.net/apps/build](https://pushover.net/apps/build) 注册一个新的 Pushover 应用。
* 在 Pushover 应用配置中，启用订阅。确保订阅类型设置为"URL"。同时确保重定向 URL 配置为指向 Healthchecks 实例的根路径（例如 `https://my-hc.example.org/`）。
* 将 Pushover 应用的_API 令牌_和_订阅 URL_ 放入 `PUSHOVER_API_TOKEN` 和 `PUSHOVER_SUBSCRIPTION_URL` 环境变量。Pushover 订阅 URL 应类似于 `https://pushover.net/subscribe/yourAppName-randomAlphaNumericData`。

## `PUSHOVER_API_TOKEN_FILE` {: #PUSHOVER_API_TOKEN_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [PUSHOVER_API_TOKEN](#PUSHOVER_API_TOKEN) 设置。如果同时设置了 `PUSHOVER_API_TOKEN` 和 `PUSHOVER_API_TOKEN_FILE`，则 `PUSHOVER_API_TOKEN_FILE` 优先。

## `PUSHOVER_EMERGENCY_EXPIRATION` {: #PUSHOVER_EMERGENCY_EXPIRATION }

默认值：`86400`（24 小时）

指定紧急 Pushover 通知将持续重试的秒数。

更多信息请参阅 [Pushover API 文档](https://pushover.net/api#priority)。

## `PUSHOVER_EMERGENCY_RETRY_DELAY` {: #PUSHOVER_EMERGENCY_RETRY_DELAY }

默认值：`300`（5 分钟）

指定 Pushover 服务器向用户发送相同通知的频率（秒）。

更多信息请参阅 [Pushover API 文档](https://pushover.net/api#priority)。

## `PUSHOVER_SUBSCRIPTION_URL` {: #PUSHOVER_SUBSCRIPTION_URL }

默认值：`None`

Pushover 订阅 URL，Pushover 集成所需。

## `REGISTRATION_OPEN` {: #REGISTRATION_OPEN }

默认值：`True`

一个布尔值，控制站点访问者是否可以创建新帐户。如果你在设置一个私有 Healthchecks 实例，但它需要公开访问（例如，你的云服务需要向其发送 ping），请将其设置为 `False`。

如果你关闭了新用户注册，你仍然可以有选择地邀请用户加入你的团队帐户。

## `REMOTE_USER_HEADER` {: #REMOTE_USER_HEADER }

默认值：`None`

指定用于外部身份验证的请求标头。如果你使用处理用户身份验证的反向代理，并且反向代理可以在 HTTP 请求标头中传递已验证用户的电子邮件地址，你可以使用此设置将 Healthchecks 与之集成。

设置了 `REMOTE_USER_HEADER` 后，Healthchecks 将：

- 在需要身份验证的视图中，查找 `REMOTE_USER_HEADER` 中指定的请求标头
- 假定该标头包含用户的电子邮件地址
- 自动登录具有匹配电子邮件地址的用户
- 如果用户帐户不存在，则自动创建
- 禁用默认的身份验证方法（登录链接到电子邮件、密码）

`REMOTE_USER_HEADER` 中的标头名称必须使用大写指定，将所有短横线替换为下划线，并加上 `HTTP_` 前缀。例如，如果你的身份验证代理设置了 `X-Authenticated-User` 请求标头，则应将 `REMOTE_USER_HEADER` 设置为 `HTTP_X_AUTHENTICATED_USER`。

**重要：** 启用此选项后，**Healthchecks 将隐式信任该标头的值**，因此**非常重要的是**确保攻击者无法自行设置该值（从而冒充任何用户）。如何做到这一点因你选择的代理而异，但通常涉及将其配置为剥离与所选身份标头归一化后同名的标头。

**关于使用 `local_settings.py`：**
当 Healthchecks 从环境变量读取设置并遇到 `REMOTE_USER_HEADER` 环境变量时，它会设置*两个*设置：`REMOTE_USER_HEADER` 和 `AUTHENTICATION_BACKENDS`。在 Healthchecks 读取 `local_settings.py` 时，此逻辑已运行完毕。因此，如果你使用 `local_settings.py` 文件而不是环境变量来配置 Healthchecks，并在其中指定 `REMOTE_USER_HEADER`，你还需要一行设置另一个设置 `AUTHENTICATION_BACKENDS`：

```
REMOTE_USER_HEADER = "HTTP_X_AUTHENTICATED_USER"
AUTHENTICATION_BACKENDS = ["hc.accounts.backends.CustomHeaderBackend"]
```

## `ROCKETCHAT_ENABLED` {: #ROCKETCHAT_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 Rocket.Chat 集成。默认启用。

## `RP_ID` {: #RP_ID }

默认值：`None`

[依赖方标识符](https://www.w3.org/TR/webauthn-2/#relying-party-identifier)，WebAuthn 双因素身份验证功能所需。

Healthchecks 可选地支持使用 WebAuthn 标准的双因素身份验证。要启用 WebAuthn 支持，请将 `RP_ID` 设置为非空值。将其值设置为站点的域名，不包含协议和端口。例如，如果你的站点运行在 `https://my-hc.example.org`，将 `RP_ID` 设置为 `my-hc.example.org`。

请注意 WebAuthn 需要 HTTPS，即使在 localhost 上运行也是如此。要在本地使用自签名证书测试 WebAuthn，你可以使用 `django-sslserver` 包中的 `runsslserver` 命令。

## `S3_ACCESS_KEY` {: #S3_ACCESS_KEY }

默认值：`None`

S3 服务中账户的访问密钥。

Healthchecks 可以选择将 ping 请求体数据上传到兼容 S3 的对象存储，而不是存储在数据库中。要使用此功能，请通过设置以下环境变量向兼容 S3 的服务提供有效凭据：

* `S3_ACCESS_KEY`（示例：`AKIAFIXMEFIXME`）
* `S3_BUCKET`（示例：`my-bucket`）
* `S3_ENDPOINT`（示例：`s3.eu-central-1.amazonaws.com`）
* `S3_REGION`（示例：`eu-central-1`）
* `S3_SECRET_KEY`

## `S3_BUCKET` {: #S3_BUCKET }

默认值：`None`

S3 服务中用于存储 ping 请求体数据的存储桶名称。

## `S3_ENDPOINT` {: #S3_ENDPOINT }

默认值：`None`

兼容 S3 的服务的 URL。

## `S3_REGION` {: #S3_REGION }

默认值：`None`

S3 服务中存储桶的区域名称。

## `S3_SECRET_KEY` {: #S3_SECRET_KEY }

默认值：`None`

S3 服务中账户的密钥。

## `S3_SECRET_KEY_FILE` {: #S3_SECRET_KEY_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [S3_SECRET_KEY](#S3_SECRET_KEY) 设置。如果同时设置了 `S3_SECRET_KEY` 和 `S3_SECRET_KEY_FILE`，则 `S3_SECRET_KEY_FILE` 优先。

## `S3_TIMEOUT` {: #S3_TIMEOUT }

默认值：`60`

单个 S3 操作的超时时间（秒）。

## `S3_SECURE` {: #S3_SECURE }

默认值：`True`

是否使用安全（TLS）连接到 S3。要使用未加密的 HTTP 请求，请将此值设置为 `False`。

## `SECRET_KEY` {: #SECRET_KEY }

默认值：`---`

用于加密签名的密钥。应设置为唯一且不可预测的值。

这是一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#secret-key)中了解更多。

## `SECRET_KEY_FILE` {: #SECRET_KEY_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [SECRET_KEY](#SECRET_KEY) 设置。如果同时设置了 `SECRET_KEY` 和 `SECRET_KEY_FILE`，则 `SECRET_KEY_FILE` 优先。

## `SECURE_PROXY_SSL_HEADER` {: #SECURE_PROXY_SSL_HEADER }

默认值：`None`

以逗号分隔的 HTTP 标头名称和值，用于标识请求是安全的（通过 https:// 发出）。此信息对于 CSRF 保护很重要。

如果 Healthchecks 在代理后面运行，代理可能会"吞掉"原始请求是否使用 HTTPS 的信息。在这种情况下，你可能会在提交表单时看到 HTTP 403 错误（例如，尝试登录时）。

如果设置，该值应包含要查找的标头名称和所需值，以逗号分隔。标头名称必须使用大写指定，将所有短横线替换为下划线，并加上 `HTTP_` 前缀。示例：

```ini
# environment variable
SECURE_PROXY_SSL_HEADER=HTTP_X_FORWARDED_PROTO,https
```

你*仅*应在控制代理或有其他保证它能正确设置/剥离此标头时才设置此环境变量。

**关于使用 `local_settings.py` 的说明：**
当 Healthchecks 从环境变量读取设置时，它期望 `SECURE_PROXY_SSL_HEADER` 包含标头名称和值，以逗号分隔。如果你在 `local_settings.py` 中设置 `SECURE_PROXY_SSL_HEADER`，它应该是一个包含两个元素的元组：

```ini
# in local_settings.py
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

此环境变量映射到一个标准的 Django 设置，在 [Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#secure-proxy-ssl-header)中了解更多。

## `SHELL_ENABLED` {: #SHELL_ENABLED }

默认值：`False`

一个布尔值，用于开启/关闭"Shell Commands"集成。

"Shell Commands"集成在检查项的状态变为 up 或 down 时运行用户定义的本地 shell 命令。此集成默认禁用，可以通过将 `SHELL_ENABLED` 环境变量设置为 `True` 来启用。

注意：使用"Shell Commands"集成时要小心，只有在完全信任 Healthchecks 实例的用户时才启用它。这些命令将由 `manage.py sendalerts` 进程执行，并使用其系统权限运行。

## `SIGNAL_CLI_SOCKET` {: #SIGNAL_CLI_SOCKET }

默认值：`None`

signal-cli UNIX 套接字的路径，或 signal-cli TCP 套接字的主机名:端口。

示例（UNIX 套接字）：

```ini
SIGNAL_CLI_SOCKET=/tmp/signal-cli.socket
```

示例（TCP 套接字）：

```ini
SIGNAL_CLI_SOCKET=example.org:7583
```

Healthchecks 使用 [signal-cli](https://github.com/AsamK/signal-cli) 发送 Signal 通知。Healthchecks 通过 UNIX 或 TCP 套接字与 signal-cli 交互（需要 signal-cli 0.10.0 或更高版本）。

启用 Signal 集成：

* 设置并配置 signal-cli 以在 UNIX 或 TCP 套接字上暴露 JSON RPC（[说明](https://github.com/AsamK/signal-cli/wiki/JSON-RPC-service)）。示例：`signal-cli -a +xxxxxx daemon --socket /tmp/signal-cli-socket`
* 将套接字的位置放入 `SIGNAL_CLI_SOCKET` 环境变量。

## `SITE_LOGO_URL` {: #SITE_LOGO_URL }

默认值：`None`

指向要用作站点徽标的图像的 URL。如果未设置，Healthchecks 将使用备用图像：`/static/img/logo.png`。

你可以将自定义徽标放在 `/static/img/` 中，运行 `manage.py collectstatic`，然后像这样指向 `SITE_LOGO_URL`：

```ini
SITE_LOGO_URL=/static/img/my-custom-logo.png
```

或者你可以从另一台服务器提供徽标，并使用绝对 URL 指向它：

```ini
SITE_LOGO_URL=https://example.org/cdn/my-custom-logo.png
```

无论哪种方式，Healthchecks 都会在 HTML 页面中按原样使用提供的 `SITE_LOGO_URL` 值，你应该使用**最终用户的浏览器可以直接访问的** URL。徽标图像可以使用浏览器支持的任何图像格式（PNG、SVG、JPG 都可以）。

**Docker 说明。** 你可以构建一个带有"内置"徽标的自定义 Docker 镜像。为此，请使用包含以下内容的 Dockerfile，并将你的 logo.png 放在其旁边：

```docker
FROM healthchecks/healthchecks
COPY logo.png /opt/healthchecks/static-collected/img/
```

这会覆盖默认的占位符徽标，因此在这种情况下，您无需
指定 `SITE_LOGO_URL`。请注意，徽标必须放置在 `static-collected` 中，而不是
`static` 中。这是因为 `manage.py collectstatic` 已在基础镜像构建时运行，
并且 Web 服务器不会识别放置在 `static` 目录中的任何新文件。

请不要在自托管实例上使用 Healthchecks.io 徽标（带有深绿色背景的那个）。
此徽标不属于 Healthchecks 开源项目。

## `SITE_NAME` {: #SITE_NAME }

Default: `Mychecks`

此 Healthchecks 实例的显示名称。Healthchecks 在其整个 Web UI 和文档中使用它。

## `SITE_ROOT` {: #SITE_ROOT }

默认值：`http://localhost:8000`

此 Healthchecks 实例的基础 URL。每当 Healthchecks 需要构建绝对 URL 时，
它都会使用 `SITE_ROOT`。Healthchecks 还使用 `SITE_ROOT` 来设置
其他几个设置，详情如下。

如果未设置 [ALLOWED_HOSTS](#ALLOWED_HOSTS)，Healthchecks
会自动用 `SITE_ROOT` 的域名部分填充它。在典型场景下，
你可以使用自动填充的值，无需自行设置 `ALLOWED_HOSTS`。

如果 SITE_ROOT 包含路径（例如 <code>http://localhost:8000<b>/prefix</b></code>），
则 Healthchecks 会自动设置以下额外的 Django 设置：

* <code>LOGIN_URL=<b>/prefix</b>/accounts/login/</code>。当未认证用户请求需要认证的页面时，
需要此设置以正确重定向到登录页面。`LOGIN_URL` 是一个标准的 Django 设置，在
[Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#login-url)中了解更多。
* <code>STATIC_URL=<b>/prefix</b>/static/</code>。需要此设置以正确生成静态文件（JS、CSS、图像）的 URL。
`STATIC_URL` 是一个标准的 Django 设置，在
[Django 文档](https://docs.djangoproject.com/en/5.1/ref/settings/#static-url)中了解更多。

**关于使用 `local_settings.py`：** 仅当你通过环境变量指定 `SITE_ROOT` 时，Healthchecks 才会设置上述额外设置。如果你在 `local_settings.py` 中指定它，你还需要在其中设置 `ALLOWED_HOSTS`、`LOGIN_URL` 和 `STATIC_URL`。

## `SLACK_CLIENT_ID` {: #SLACK_CLIENT_ID }

默认值：`None`

Slack 客户端 ID，由 Healthchecks 的 Slack 集成使用。

该集成可以在设置或不设置 Slack 客户端 ID 的情况下工作。如果未设置 Slack 客户端 ID，在"集成 - 添加 Slack"页面中，Healthchecks 将要求用户提供用于发布通知的 Webhook URL。

如果设置了 Slack 客户端 ID，Healthchecks 将使用 OAuth2 流程从 Slack 获取 Webhook URL。OAuth2 流程更加用户友好。要设置它，请访问 [https://api.slack.com/apps/](https://api.slack.com/apps/) 并创建一个 _Slack 应用_。在设置 Slack 应用时，请确保：

* 将 [incoming-webhook](https://api.slack.com/scopes/incoming-webhook) 范围添加到 Bot Token Scopes。
* 添加格式为 `SITE_ROOT/integrations/add_slack_btn/` 的_重定向 URL_。例如，如果你的 `SITE_ROOT` 是 `https://my-hc.example.org`，则重定向 URL 为 `https://my-hc.example.org/integrations/add_slack_btn/`。

## `SLACK_CLIENT_SECRET` {: #SLACK_CLIENT_SECRET }

默认值：`None`

Slack 客户端密钥。如果设置了 `SLACK_CLIENT_ID`，则此为必需。在 [https://api.slack.com/apps/](https://api.slack.com/apps/) 查找。

## `SLACK_CLIENT_SECRET_FILE` {: #SLACK_CLIENT_SECRET_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [SLACK_CLIENT_SECRET](#SLACK_CLIENT_SECRET) 设置。如果同时设置了 `SLACK_CLIENT_SECRET` 和 `SLACK_CLIENT_SECRET_FILE`，则 `SLACK_CLIENT_SECRET_FILE` 优先。

## `SLACK_ENABLED` {: #SLACK_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 Healthchecks 的 Slack 集成。默认启用。

## `SPIKE_ENABLED` {: #SPIKE_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 Spike.sh 集成。默认启用。

## `TELEGRAM_BOT_NAME` {: #TELEGRAM_BOT_NAME }

默认值：`ExampleBot`

[Telegram](https://telegram.org/) 机器人名称，Telegram 集成所需。

设置 Telegram 集成：

* 通过与 [BotFather](https://core.telegram.org/bots#6-botfather) 对话创建 Telegram 机器人。设置机器人名称、描述、用户头像，并添加 "/start" 命令。
* 创建机器人后，你将获得机器人的名称和令牌。将它们放入 `TELEGRAM_BOT_NAME` 和 `TELEGRAM_TOKEN` 环境变量。
* 运行 `settelegramwebhook` 管理命令。此命令通过调用 Telegram 的 [setWebhook](https://core.telegram.org/bots/api#setwebhook) API 告诉 Telegram 将频道消息转发到何处：

```bash
$ ./manage.py settelegramwebhook
Done, Telegram's webhook set to: https://my-monitoring-project.com/integrations/telegram/bot/
```

为此，你的 `SITE_ROOT` 必须可公开访问并使用 "https://" 协议。

## `TELEGRAM_TOKEN` {: #TELEGRAM_TOKEN }

默认值：`None`

Telegram 机器人用户的身份验证令牌，Telegram 集成所需。

## `TELEGRAM_TOKEN_FILE` {: #TELEGRAM_TOKEN_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [TELEGRAM_TOKEN](#TELEGRAM_TOKEN) 设置。如果同时设置了 `TELEGRAM_TOKEN` 和 `TELEGRAM_TOKEN_FILE`，则 `TELEGRAM_TOKEN_FILE` 优先。

## `TRELLO_APP_KEY` {: #TRELLO_APP_KEY }

默认值：`None`

[Trello](https://trello.com/) 应用密钥，Trello 集成所需。

要设置 Trello 集成，请从 [https://trello.com/app-key](https://trello.com/app-key) 获取开发者 API 密钥，并将其放入 `TRELLO_APP_KEY` 环境变量。

## `TRELLO_APP_KEY_FILE` {: #TRELLO_APP_KEY_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [TRELLO_APP_KEY](#TRELLO_APP_KEY) 设置。如果同时设置了 `TRELLO_APP_KEY` 和 `TRELLO_APP_KEY_FILE`，则 `TRELLO_APP_KEY_FILE` 优先。

## `TWILIO_ACCOUNT` {: #TWILIO_ACCOUNT }

默认值：`None`

Twilio 账户 SID，SMS、电话和 WhatsApp 集成所需。

## `TWILIO_AUTH` {: #TWILIO_AUTH }

默认值：`None`

Twilio 身份验证令牌，SMS、电话和 WhatsApp 集成所需。

## `TWILIO_AUTH_FILE` {: #TWILIO_AUTH_FILE }

默认值：`None`

如果设置，必须包含指向可读文件的文件系统路径。Healthchecks 会将文件内容读入 [TWILIO_AUTH](#TWILIO_AUTH) 设置。如果同时设置了 `TWILIO_AUTH` 和 `TWILIO_AUTH_FILE`，则 `TWILIO_AUTH_FILE` 优先。

## `TWILIO_FROM` {: #TWILIO_FROM }

默认值：`None`

用作 SMS 和 WhatsApp 通知发送方以及电话集成的呼叫方的 Twilio 电话号码。

示例：

```ini
TWILIO_FROM=+15017122661
```

## `TWILIO_MESSAGING_SERVICE_SID` {: #TWILIO_MESSAGING_SERVICE_SID }

默认值：`None`

用于发送 SMS 和 WhatsApp 通知的 Twilio Messaging Service SID。

发送 WhatsApp 通知**需要** `TWILIO_MESSAGING_SERVICE_SID`。

发送 SMS 通知时 `TWILIO_MESSAGING_SERVICE_SID` 是**可选**的。如果指定，Healthchecks 会将其作为"MessagingServiceSid"字段传递给 Twilio API。这将导致 Twilio 使用 Messaging Service 而不是普通发送方号码来投递 SMS 消息。如果未指定，Healthchecks 将回退到使用 [TWILIO_FROM](#TWILIO_FROM) 中配置的"From"字段。

示例：

```ini
TWILIO_MESSAGING_SERVICE_SID=MGe56e622d540e6badc52ae0ac4af028c6
```

## `TWILIO_USE_WHATSAPP` {: #TWILIO_USE_WHATSAPP }

默认值：`False`

一个布尔值，用于开启/关闭 WhatsApp 集成。要使 WhatsApp 集成正常工作，你还需要指定：

* [TWILIO_ACCOUNT](#TWILIO_ACCOUNT)
* [TWILIO_AUTH](#TWILIO_AUTH)
* [TWILIO_FROM](#TWILIO_FROM)
* [TWILIO_MESSAGING_SERVICE_SID](#TWILIO_MESSAGING_SERVICE_SID)
* [WHATSAPP_DOWN_CONTENT_SID](#WHATSAPP_DOWN_CONTENT_SID)
* [WHATSAPP_UP_CONTENT_SID](#WHATSAPP_UP_CONTENT_SID)。

## `USE_PAYMENTS` {: #USE_PAYMENTS }

默认值：`False`

一个布尔值，用于开启/关闭计费功能。

## `VICTOROPS_ENABLED` {: #VICTOROPS_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 Splunk On-Call (VictorOps) 集成。默认启用。

## `WEBHOOKS_ENABLED` {: #WEBHOOKS_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 Webhooks 集成。默认启用。

## `WHATSAPP_DOWN_CONTENT_SID` {: #WHATSAPP_DOWN_CONTENT_SID }

默认值：`None`

用于 WhatsApp "down"通知的 Twilio 内容模板标识符。WhatsApp 集成所需。

Meta 要求 WhatsApp 消息模板需要预先注册和批准。在你的 Twilio 账户中创建具有以下内容的内容模板：

````
The check “{{1}}” is DOWN.
````

你可以根据需要调整消息内容，但请确保它有一个类似于上述示例的单个占位符。

## `WHATSAPP_UP_CONTENT_SID` {: #WHATSAPP_UP_CONTENT_SID }

默认值：`None`

用于 WhatsApp "up"通知的 Twilio 内容模板标识符。WhatsApp 集成所需。

Meta 要求 WhatsApp 消息模板需要预先注册和批准。在你的 Twilio 账户中创建具有以下内容的内容模板：

````
The check “{{1}}” is now UP.
````

你可以根据需要调整消息内容，但请确保它有一个类似于上述示例的单个占位符。

## `ZULIP_ENABLED` {: #ZULIP_ENABLED }

默认值：`True`

一个布尔值，用于开启/关闭 Zulip 集成。默认启用。
