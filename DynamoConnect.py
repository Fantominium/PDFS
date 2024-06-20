import boto3
import logging
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import os


logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb_endpoint = os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:8000')


db = boto3.resource("dynamodb", 
                    endpoint_url=dynamodb_endpoint,
                    region_name="us-west-2",
                    aws_access_key_id="dummy",
                    aws_secret_access_key = "dummy")

try:
    tables = list(db.tables.all())
    print("Tables in DynamoDB:", tables)

    connection = db.create_table(TableName="Bookings", 
                AttributeDefinitions=[
                    {
                        'AttributeName':'BookingId',
                        'AttributeType':'S'
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': 'BookingId',
                        'KeyType': 'HASH'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
    # Wait until the table exists.
    connection.meta.client.get_waiter('table_exists').wait(TableName="Bookings")
    print(f"Table {"Bookings"} created successfully.")

except (NoCredentialsError, PartialCredentialsError) as e:
    print("Credentials not available.", e)


logger.info("Db created table and running")

    