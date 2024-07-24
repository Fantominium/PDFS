from fastapi import HTTPException, status, Depends
from Utils.DynamoAuthOps import  DynamoAuthOps
from Models.UserModel import UserModel
from uuid import UUID, uuid4
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import os
import jwt
from datetime import datetime, timedelta
from Models.AuthModel import TokenData
from typing import Optional
from Models.UserModel import UserModel
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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

def create_access_token(data:dict, exp_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if exp_delta:
        expires= datetime.now() + exp_delta
    else:
        print(f"{os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")}")
        expires = datetime.now() + timedelta(minutes= 30)

    to_encode.update({"exp": expires})
    jwt_encoded = jwt.encode(to_encode, os.getenv("SECRET_KEY"), os.getenv("ALGORITHM"))

    return jwt_encoded

def auth_user(email:str, password:str):

    user = auth_handler.db_auth_user(email, password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 
                            detail="Credentials not validated", 
                            headers={"WWW-Authenticate":"Bearer"})
    else:
        access_token= create_access_token(data={"sub":email})
        return {"access_token": access_token,
                 "token_type":"Bearer"}

async def get_current_user (token: str = Depends(oauth_2_scheme)):
    cred_exp = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credentials not validated", 
                            headers={"WWW-Authenticate":"Bearer"})

    jwt_payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    if jwt_payload:
        email: str = jwt_payload.get("sub")
        token_data = TokenData(email=email)
        if token_data is None:
            raise cred_exp
        else:
            user = auth_handler.db_read_single_user(email=token_data.email)
            # Final check: to see if user is found in db
            if user:
                return user
            else:
                raise cred_exp
    else:
        raise cred_exp

async def get_current_active_user(current_user: UserModel = Depends(get_current_user)):
    if current_user[0].get("rsvp") != "Not Attending":
        return current_user
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="You are currently not attending")


