from fastapi import HTTPException, status, Depends
from Utils.DynamoAuthOps import  DynamoAuthOps
from Models.UserModel import UserModel
from uuid import UUID, uuid4
import os

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


auth_handler= DynamoAuthOps(table_name="Users", attr_name="UserId")
key_value = "UserId"

def create_user(user:UserModel):
    user.id = uuid4()
    response = auth_handler.db_add_user(user, f"{key_value}")
    logger.info(f"{response} from the insert of {user}")
    return response

def read_users():
    return auth_handler.db_read()

def read_single_user(email: str):
    return auth_handler.db_read_single_user(f"{email}")

def update_user(id:UUID, user_update: UserModel):
    return auth_handler.db_update_user(f"{id}", user_update, key_value)
def delete_user(id:UUID):
    return auth_handler.db_delete_user(f"{id}", key_value)

def auth_user(email:str, password:str):
    user = auth_handler.db_auth_user(email, password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                            detail="Credentials not validated", 
                            headers={"WWW-Authenticate":"Bearer"})
    else:
        access_token= auth_handler.db_create_access_token(data={"sub":user.email})
        return {"access_token": access_token,
                 "token_type":"Bearer"}


