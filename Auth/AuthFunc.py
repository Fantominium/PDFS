from Utils.DynamoCrudOps import DynamoCrudOps
from Auth.UserModel import UserModel
from uuid import UUID, uuid4

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


handler = DynamoCrudOps(table_name="Users", attr_name="UserId")
key_value = "UserId"

def create_user(user:UserModel):
    user.id = uuid4()
    user_key = "UserId"
    response = handler.db_insert(user, f"{user_key}")
    logger.info(f"{response} from the insert of {user}")
    return response

def read_users():
    return handler.db_read()

def read_single_user(email: str):
    return handler.db_read_single_user(f"{email}")

def update_user(user_id: UUID, user_update: UserModel):
    return handler.db_update(f"{user_id}", user_update, key_value)

def delete_user(user_id:UUID):
    return handler.db_delete(f"{user_id}", key_value)

