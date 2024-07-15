from fastapi import FastAPI
from Booking.Bookings import *
from Auth.AuthFunc import *
from uuid import UUID
from Booking.BookingModel import Booking
from Auth.UserModel import UserModel
from typing import List

app = FastAPI()

@app.post("/bookings/")
def create(booking:Booking):
    return create_booking(booking)

@app.post("/login/")
def register(user:UserModel):
    return create_user(user)

@app.get("/bookings/", response_model=List)
def read():
    return read_bookings()

@app.get("/getUsers/", response_model=List)
def get_users():
    return read_users()

@app.get("/bookings/<booking_id:UUID>")
def read_booking(booking_id: UUID):
    return read_single_booking(booking_id)

@app.get("/users/<email:str>")
def get_single_user(email:str):
    return read_single_user(email)

@app.patch("/bookings/<booking_id:UUID>")
def update(booking_id: UUID, booking_update: Booking):
    return update_booking(booking_id, booking_update)

@app.patch("/updateUser/<user_id:UUID>")
def update_single_user(user_id:UUID, user_update: UserModel):
    return update_user(user_id, user_update)

@app.delete("/bookings/<booking_id:UUID>")
def delete(booking_id:UUID):
    return delete_booking(booking_id)

@app.delete("/deleteUser/<user_id:UUID>")
def delete_single_user(user_id:UUID):
    return delete_user(user_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)