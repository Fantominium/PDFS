from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from Booking.Bookings import *
from Auth.AuthFunc import *
from Investors.InvestorService import *
from fastapi.middleware.cors import CORSMiddleware

from uuid import UUID
from Models.BookingModel import Booking
from Models.UserModel import UserModel
from typing import List

app = FastAPI()

origins = [
    "https://localhost:3000",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
def get_single_user(email:str):
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
def delete_single_user(user_id:UUID, current_user: UserModel = Depends(get_current_active_user)):
    return delete_user(user_id)

@app.post("/token")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return auth_user(email=form_data.username, password=form_data.password)

@app.get("/investors")
def get_all_investors():
    return load_csv();

@app.get("/investors/investorList")
def get_investor_names_and_commitments():
    return sort_by_investor_name();

@app.get("/investors/<investor_name:str>")
def get_investor_commitments(investor_name:str):
    return get_investor_commitment_list(investor_name)

@app.post("/investors/commitmentsByClass")
def read_commitments_by_asset_class(asset_class: str, investor_name: str):
    return filter_commitments_by_asset_class(asset_class, investor_name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)