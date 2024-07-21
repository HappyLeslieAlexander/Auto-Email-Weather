# 每日天气报告发送脚本
## 介绍

该 Python 脚本通过 OpenWeatherMap API 获取指定城市的天气信息，并通过 SMTP 服务器发送每日天气报告邮件。邮件内容包括简体中文的天气描述、当前温度、最高温度、最低温度、湿度、风速、风向、日出时间和日落时间。

## 功能

获取指定城市的天气信息（使用 OpenWeatherMap API）。

通过 SMTP 服务器发送天气报告邮件。

支持简体中文天气描述。

包含问候语和详细的天气信息。

## 用法

安装依赖

在运行脚本之前，确保已安装所需的 Python 包：

```
pip install requests
```

## 设置环境变量

为了脚本能够正常运行，需要设置以下环境变量：

SMTP_SERVER：SMTP 服务器地址（如 smtp.gmail.com）。

SMTP_PORT：SMTP 服务器端口（通常是 465 或 587）。

SMTP_USER：SMTP 服务器的用户名（通常是你的电子邮件地址）。

SMTP_PASSWORD：SMTP 服务器的密码或应用专用密码。

EMAIL_FROM：发送邮件的电子邮件地址。

EMAIL_TO：接收邮件的电子邮件地址。

WEATHER_API_KEY：OpenWeatherMap API 密钥。

WEATHER_CITY：需要获取天气信息的城市名称。

你可以在 .env 文件中设置这些变量，然后在脚本中使用 python-dotenv 来加载它们，或直接在运行脚本前导出这些环境变量。

## 运行脚本

确保所有环境变量都已正确设置，然后运行脚本：

``` 
python send_weather_email.py
```

## GitHub Actions 自动化

你可以使用 GitHub Actions 来每天定时运行该脚本并发送天气报告邮件。以下是一个 GitHub Actions 工作流配置示例：

```
name: Send Daily Weather Report

on:
  schedule:
    - cron: '0 22 * * *'  # 每天 UTC 时间 22:00 运行，相当于 UTC+8 的早上 6 点
  workflow_dispatch: # 允许手动触发工作流

jobs:
  send_email:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run the script
        env:
          SMTP_SERVER: ${{ secrets.SMTP_SERVER }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
          EMAIL_FROM: ${{ secrets.EMAIL_FROM }}
          EMAIL_TO: ${{ secrets.EMAIL_TO }}
          WEATHER_API_KEY: ${{ secrets.WEATHER_API_KEY }}
          WEATHER_CITY: ${{ secrets.WEATHER_CITY }}
        run: python send_weather_email.py
```

示例输出
收到的电子邮件将包含以下内容：

```
早上好！

这是今天的天气报告：

天气: 多云
温度: 25°C
最高温度: 28°C
最低温度: 22°C
湿度: 78%
风速: 5 m/s
风向: 东南 (135°)
日出时间: 05:45:00
日落时间: 18:30:00
```

## 备注

确保 OpenWeatherMap API 密钥有效，并且你已经在 OpenWeatherMap 中启用了 API 访问。

确保 SMTP 服务器设置正确，并且你的邮箱允许使用 SMTP 发送邮件。如果使用 Gmail，请确保启用了“允许不太安全的应用”或生成了应用专用密码。

通过以上设置和使用，你可以每天自动获取并发送详细的天气报告。

### 捐赠

加密货币

TRON

TY7n1xwiHCBqcQqGH1cxjTQqZTuTXbzB4S

Ethereum

0xed57e7237e88cec19d3fd12a0d26bacb1dcc247b

Polygon

0xed57e7237e88cec19d3fd12a0d26bacb1dcc247b

TON

UQC4r4gxAIbOTEEZGG-C1Ffn9inRo24J7qw3U0dFfaIfKyFr

### 感谢你右上角的star🌟
[![Stargazers over time](https://starchart.cc/HappyLeslieAlexander/Auto-Email-Weather.svg)](https://starchart.cc/HappyLeslieAlexander/Auto-Email-Weather)
