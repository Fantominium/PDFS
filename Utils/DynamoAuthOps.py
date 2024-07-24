from fastapi import HTTPException
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from boto3.dynamodb.conditions import Attr
from passlib.context import CryptContext
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb_endpoint = os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:8000')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class DynamoAuthOps:
    def __init__(self, table_name:str, attr_name:str) -> None:
        self.dynamodb = boto3.resource(
                        'dynamodb',
            endpoint_url=dynamodb_endpoint,
            region_name="us-west-2",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy"
        )
        self.table_name=table_name

        try:
            self.table = self.dynamodb.Table(f"{table_name}")
            self.table.load()
        except self.dynamodb.meta.client.exceptions.ResourceNotFoundException:
            try:
                connection = self.dynamodb.create_table(TableName=f"{table_name}", 
                        AttributeDefinitions=[
                            {
                                'AttributeName':f"{attr_name}",
                                'AttributeType':'S'
                            }
                        ],
                        KeySchema=[
                            {
                                'AttributeName': f"{attr_name}",
                                'KeyType': 'HASH'
                            }
                        ],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 10,
                            'WriteCapacityUnits': 10
                        }
                    )
                # Wait until the table exists.
                connection.meta.client.get_waiter('table_exists').wait(TableName=table_name)
                self.table = self.dynamodb.Table(table_name)

            except (NoCredentialsError, PartialCredentialsError) as e:
                print("Credentials not available.", e)
            except ClientError as e:
                print("Unexpected error:", e)

    def verify_password(self, password, hashed_password):
        return pwd_context.verify(password, hashed_password)
    
    def get_pass_hash(self, password):
        return pwd_context.hash(password)

    def db_add_user(self, data: dict, key: str):
        # Build the item dictionary dynamically based on the fields present in the model
        item = {key: str(data.id)}
        
        # Add all fields from the model instance to the item dictionary
        for field, value in data.dict().items():
            if field != 'id':  # Skip the 'id' field as it is already added
                item[field] = value
            if field == 'password':
                item[field] = self.get_pass_hash(value)
        try:
            self.table.put_item(Item=item)
            return item, 200
        except NoCredentialsError as error:
            print(f"Credentials not available: {error}")
        except PartialCredentialsError as error:
            print(f"Partial credentials error: {error}")
        except Exception as error:
            print(f"An error occurred: {error}")

    def db_read(self):
        response = self.table.scan(TableName=f"{self.table_name}")
        return response.get("Items",[]), 200
    
    def db_read_single_user(self, email:str):
        try:
            response = self.table.scan(
                FilterExpression=Attr('email').eq(email)
            )
            items = response.get("Items")
            if items:
                return items[0], 200
            else:
                return {"error": "User not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def db_auth_user (self, email:str, password:str):
        user = self.db_read_single_user(email)
        if user == None:
            return {"error": "User not found"}, 404
        if not self.verify_password(password, user[0].get("password")):
            return {"error": "Username or password does not match"}, 403
        else:
            return user

    def db_update_user(self, id:str, update:dict, key:str):

    # Construct the update expression
        update_expression = "SET"
        update_expression_parts=[]
        expression_attribute_values = {}
        expression_attribute_names = {}

        for attr_name, attr_value in update:
            if attr_value is not None:
                var_name = f"#{attr_name}"
                var_val = f":{attr_value}"
                if isinstance(var_val, str): 
                    var_val = var_val.replace(" ", "_")
                
                update_expression_parts.append(f"{var_name}={var_val}")
                expression_attribute_values[var_val] = attr_value
                expression_attribute_names[var_name] = attr_name


        if not update_expression:
            print("No attributes to update.")
            return False

        update_expression += ", ".join(update_expression_parts)
        
        try:
            response = self.table.update_item(
                Key={f"{key}": id},
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_attribute_values,
                ExpressionAttributeNames=expression_attribute_names,
                ReturnValues="UPDATED_NEW"
        )
            return response.get("Attributes"), 200
        except Exception as e:
            print(f"Error updating item with Record {id}: {e}")
    
    def db_delete_user (self, id:str, key:str):
        try:
            response = self.table.delete_item(
                Key={f"{key}": id}
                )
            # Check the response for successful deletion
            if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200:
                return id, 200
            else:
                raise HTTPException(400, detail=f"There was a problem deleting id: {id}")
        except Exception as e:
            print(f"Error deleting item with record id {id}: {e}")
            return False
            