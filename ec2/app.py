 import mysql.connector
import boto3

# AWS credentials and region configuration
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
aws_region = 'YOUR_AWS_REGION'

# AWS SNS setup
sns_client = boto3.client(
    'sns',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)
sns_topic_arn = 'YOUR_SNS_TOPIC_ARN'

# Lightsail MySQL Database configuration
db_config = {
    'user': 'YOUR_DB_USER',
    'password': 'YOUR_DB_PASSWORD',
    'host': 'YOUR_DB_HOST',
    'database': 'YOUR_DB_NAME',
}

def register_email(email):
    if email:
        try:
            # Save to Lightsail MySQL database
            db_connection = mysql.connector.connect(**db_config)
            cursor = db_connection.cursor()

            # Insert email into the database
            insert_query = "INSERT INTO EmailSubs (Email) VALUES (%s)"
            cursor.execute(insert_query, (email,))
            db_connection.commit()

            # Subscribe email to AWS SNS topic
            sns_client.subscribe(
                TopicArn=sns_topic_arn,
                Protocol='email',
                Endpoint=email
            )

            cursor.close()
            db_connection.close()
            return f"Email '{email}' registered successfully and subscribed to the SNS topic!"
        except Exception as e:
            return f"Error: {e}"
    else:
        return "Email not provided."

if __name__ == "__main__":
    email_to_register = input("Enter email to register: ")
    result = register_email(email_to_register)
    print(result)
