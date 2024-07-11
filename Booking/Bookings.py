from Utils.DynamoCrudOps import DynamoCrudOps
from Booking.BookingModel import Booking
from uuid import UUID, uuid4
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


handler = DynamoCrudOps(table_name="Bookings", attr_name="BookingId")
key_value = "BookingId"

def create_booking(booking:Booking):
    booking.id = uuid4()
    booking_key = "BookingId"
    response = handler.db_insert(booking, f"{booking_key}")
    logger.info(f"{response} from the insert of {booking}")
    return response

def read_bookings():
    return handler.db_read()

def read_single_booking(booking_id: UUID):
    return handler.db_read_single(f"{booking_id}", key_value)

def update_booking(booking_id: UUID, booking_update: Booking):
    return handler.db_update(f"{booking_id}", booking_update, key_value)

def delete_booking(booking_id:UUID):
    return handler.db_delete(f"{booking_id}", key_value)

