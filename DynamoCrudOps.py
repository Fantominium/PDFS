from fastapi import HTTPException
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from BookingModel import Booking
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb_endpoint = os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:8000')


class DynamoCrudOps:
    def __init__(self, table_name, 
                    region_name="us-west-2",
                    aws_access_key_id="dummy",
                    aws_secret_access_key = "dummy") -> None:
        self.table_name = table_name
        self.dynamodb = boto3.resource(
                        'dynamodb',
            endpoint_url=dynamodb_endpoint,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.table = self.dynamodb.Table(table_name)

        
    def db_insert(self, data: dict):
        item = {
            'BookingId': f"{data.id}",
            'title': data.title,
            'description': data.description,
            'completed': data.completed
        }
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
        response = self.table.scan()
        return response.get("Items",[]), 200
    
    def db_read_single(self, id:str, key:str):
        response_list = self.table.get_item(Key={f"{key}": id})
        response = response_list.get("Item")
        return response, 200
        
    def db_update(self, id:str, update:dict, key:str):

    # Construct the update expression
        update_expression = "SET"
        update_expression_parts=[]
        expression_attribute_values = {}
        expression_attribute_names = {}

        for attr_name, attr_value in update:
            if attr_value is not None:
                var_name = f"#{attr_name}"
                var_val = f":{attr_value}"
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
            print(f"Error updating item with BookingId {id}: {e}")
    
    def db_delete (self, id:str, key:str):
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
            print(f"Error deleting item with BookingId {id}: {e}")
            return False
            




