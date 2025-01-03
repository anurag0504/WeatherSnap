import requests
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    # AWS credentials and SNS topic details
    aws_access_key = os.getenv('AWS_ACCESS_KEY')
    aws_secret_key = os.getenv('AWS_SECRET_KEY')
    sns_topic_arn = os.getenv('SNS_TOPIC_ARN')

    # OpenWeatherMap API details
    api_key = os.getenv('OPENWEATHER_API_KEY')
    city = os.getenv('CITY', 'Milwaukee')
    language = 'en'

    sns_client = boto3.client(
        'sns',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=os.getenv('AWS_REGION')
    )

    def get_weather():
        base_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang={language}'
        response = requests.get(base_url)
        if response.status_code == 200:
            data = response.json()
            weather = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description']
            }
            return weather
        else:
            return None

    def send_weather_update():
        weather_info = get_weather()
        if weather_info:
            message = (
                f"Weather in {weather_info['city']} - "
                f"Temperature: {weather_info['temperature']}°C, "
                f"Description: {weather_info['description']}"
            )
            sns_client.publish(
                TopicArn=sns_topic_arn,
                Message=message,
                Subject='Weather Update'
            )
            print("Weather update sent successfully to subscribers!")
        else:
            print("Failed to fetch weather information")

    send_weather_update()
 
