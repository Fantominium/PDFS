from fastapi import FastAPI
from Booking.Bookings import *
from uuid import UUID
from Booking.BookingModel import Booking
from typing import List

app = FastAPI()

@app.post("/bookings/")
def create(booking:Booking):
    return create_booking(booking)

@app.get("/bookings/", response_model=List)
def read():
    return read_bookings()

@app.get("/bookings/<booking_id:UUID>")
def read_booking(booking_id: UUID):
    return read_single_booking(booking_id)

@app.patch("/bookings/<booking_id:UUID>")
def update(booking_id: UUID, booking_update: Booking):
    return update_booking(booking_id, booking_update)

@app.delete("/bookings/<booking_id:UUID>")
def delete(booking_id:UUID):
    return delete_booking(booking_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)