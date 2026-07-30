# GitHub Actions

你可以增强你的 GitHub Actions 工作流，向 SITE_NAME 报告成功和失败：

```yaml
name: Hourly Housekeeping
on:
  schedule:
    - cron: '15 * * * *'
jobs:
  Main-Job:
    runs-on: ubuntu-latest
    steps:
      - run: echo "正在执行维护任务..."
  Ping-Success:
    runs-on: ubuntu-latest
    needs: [Main-Job]
    steps:
      - run: curl -m 10 --retry 5 ${{ secrets.ping_url }}
  Ping-Failure:
    runs-on: ubuntu-latest
    if: ${{ failure() }}
    needs: [Main-Job]
    steps:
      - run: curl -m 10 --retry 5 ${{ secrets.ping_url }}/fail
```

注意 `Ping-Success` 和 `Ping-Failure` 作业将 `Main-Job` 定义为其依赖项。
`Ping-Success` 仅在 `Main-Job` 成功完成时运行，
而 `Ping-Failure` 在 `Main-Job` 失败时运行。

为避免暴露 ping URL，建议将其定义为
[密钥](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
并通过 `secrets` 上下文访问。

## 使用 `workflow_run` 触发器

或者，你可以将 ping 逻辑放在单独的工作流中，
并配置它在每次主工作流完成时触发。主工作流：

```yaml
name: Hourly Housekeeping
on:
  schedule:
    - cron: '15 * * * *'
jobs:
  Main-Job:
    runs-on: ubuntu-latest
    steps:
      - run: echo "正在执行维护任务..."
```

以及监控工作流：

```yaml
name: Ping SITE_NAME
on:
  workflow_run:
    workflows: ['Hourly Housekeeping']
    types: [completed]
jobs:
  Ping-Success:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - run: curl -m 10 --retry 5 ${{ secrets.ping_url }}
  Ping-Failure:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
      - run: curl -m 10 --retry 5 ${{ secrets.ping_url }}/fail
```