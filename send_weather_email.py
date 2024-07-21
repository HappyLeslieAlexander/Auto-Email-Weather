import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import os
from datetime import datetime, timezone, timedelta

# 获取环境变量
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))  # 使用端口 587 进行 STARTTLS
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
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        wind_deg = data['wind']['deg']
        sunrise = datetime.fromtimestamp(data['sys']['sunrise'], tz=timezone.utc).astimezone(timezone(timedelta(hours=8))).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(data['sys']['sunset'], tz=timezone.utc).astimezone(timezone(timedelta(hours=8))).strftime('%H:%M:%S')

        wind_direction = convert_deg_to_direction(wind_deg)
        
        weather_report = (
            f"天气: {weather_description}\n"
            f"温度: {temperature}°C\n"
            f"最高温度: {temp_max}°C\n"
            f"最低温度: {temp_min}°C\n"
            f"湿度: {humidity}%\n"
            f"风速: {wind_speed} m/s\n"
            f"风向: {wind_direction} ({wind_deg}°)\n"
            f"日出时间: {sunrise}\n"
            f"日落时间: {sunset}"
        )
        return weather_report
    else:
        return f"获取天气信息失败: {data.get('message', '未知错误')}"

def convert_deg_to_direction(deg):
    """将风向从度数转换为方向"""
    directions = ['北', '北东北', '东北', '东东北', '东', '东东南', '东南', '南东南', '南', '南西南', '西南', '西西南', '西', '西西北', '西北', '北西北']
    ix = round(deg / 22.5) % 16
    return directions[ix]

def send_email(subject, body):
    """通过 SMTP 发送电子邮件"""
    message = MIMEMultipart()
    message['From'] = EMAIL_FROM
    message['To'] = EMAIL_TO
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=ssl.create_default_context())
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(message)

def main():
    # 获取当前 UTC+8 时间
    utc8_now = datetime.now(timezone.utc) + timedelta(hours=8)
    greeting = "早上好！\n\n这是今天的天气报告：\n\n"
    weather_report = get_weather()
    body = greeting + weather_report
    subject = f'每日天气报告 - {utc8_now.strftime("%Y-%m-%d")}'
    send_email(subject, body)

if __name__ == "__main__":
    main()
