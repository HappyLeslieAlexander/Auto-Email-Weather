import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import os
from datetime import datetime

# 获取环境变量
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_FROM = os.getenv('EMAIL_FROM')
EMAIL_TO = os.getenv('EMAIL_TO')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
WEATHER_CITY = os.getenv('WEATHER_CITY')

def get_weather():
    """获取天气信息"""
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric&lang=zh_cn'
    )
    data = response.json()
    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return f'天气: {weather_description}\n温度: {temperature}°C'
    else:
        return f"获取天气信息失败: {data.get('message', '未知错误')}"

def send_email(subject, body):
    """通过 SMTP 发送电子邮件"""
    message = MIMEMultipart()
    message['From'] = EMAIL_FROM
    message['To'] = EMAIL_TO
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(message)

def main():
    greeting = "早上好！\n\n这是今天的天气报告：\n\n"
    weather_report = get_weather()
    body = greeting + weather_report
    subject = f'每日天气报告 - {datetime.now().strftime("%Y-%m-%d")}'
    send_email(subject, body)

if __name__ == "__main__":
    main()
