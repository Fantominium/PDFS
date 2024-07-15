from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from Booking.Bookings import *
from Auth.AuthFunc import *
from uuid import UUID
from Models.BookingModel import Booking
from Models.UserModel import UserModel
from typing import List

app = FastAPI()

@app.post("/createBooking/")
def create(booking:Booking):
    return create_booking(booking)

@app.post("/registerUser/")
def register(user:UserModel):
    return create_user(user)

@app.get("/getBookings/", response_model=List)
def read():
    return read_bookings()

@app.get("/getUsers/", response_model=List)
def get_users():
    return read_users()

@app.get("/getBooking/<booking_id:UUID>")
def read_booking(booking_id: UUID):
    return read_single_booking(booking_id)

@app.get("/getUser/<email:str>")
def get_single_user(email:str, current_user: UserModel = Depends(auth_handler.get_current_active_user)):
    return read_single_user(email)

@app.patch("/updateBooking/<booking_id:UUID>")
def update(booking_id: UUID, booking_update: Booking):
    return update_booking(booking_id, booking_update)

@app.patch("/updateUser/<user_id:UUID>")
def update_single_user(user_id:UUID, user_update: UserModel):
    return update_user(user_id, user_update)

@app.delete("/deleteBooking/<booking_id:UUID>")
def delete(booking_id:UUID):
    return delete_booking(booking_id)

@app.delete("/deleteUser/<user_id:UUID>")
def delete_single_user(user_id:UUID, current_user: UserModel = Depends(auth_handler.get_current_active_user)):
    return delete_user(user_id)

@app.post("/token")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return auth_handler.db_auth_user(email=form_data.username, password=form_data.password)

# @app.get("getUser/me")
# async def get_user_me(current_user: UserModel = Depends(auth_handler.get_current_active_user)):
#     return auth_handler.get_current_active_user

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)