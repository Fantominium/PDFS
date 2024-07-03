import unittest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
from pydantic import ValidationError
from BookingModel import Booking
from Bookings import *


# Assuming the necessary imports and class definitions are available

class TestCreateBooking(unittest.TestCase):

    @patch('Bookings.uuid4')
    @patch('Bookings.handler.db_insert')
    def test_successful_booking_creation(self, mock_db_insert, mock_uuid4):
        # Arrange
        booking = Booking(title="Test Booking", description="Test Description", completed=False)
        mock_uuid = UUID('12345678123456781234567812345678')
        mock_uuid4.return_value = mock_uuid
        mock_db_insert.return_value = booking
        
        # Act
        response = create_booking(booking)

        # Assert
        self.assertEqual(response.id, mock_uuid)  # Ensure the ID was assigned correctly
        self.assertEqual(response.title, "Test Booking")
        self.assertEqual(response.description, "Test Description")
        self.assertFalse(response.completed)
        mock_db_insert.assert_called_once_with(booking)  # Ensure db_insert was called once

    def test_missing_title(self):
        # Arrange
        booking_data = {"description": "Test Description", "completed": False}

        # Act & Assert
        with self.assertRaises(ValidationError):
            Booking(**booking_data)

    @patch('Bookings.uuid4')
    @patch('Bookings.handler.db_insert')
    def test_completed_booking(self, mock_db_insert, mock_uuid4):
        # Arrange
        booking = Booking(title="Test Booking", completed=True)
        mock_uuid = UUID('12345678123456781234567812345678')
        mock_uuid4.return_value = mock_uuid
        mock_db_insert.return_value = booking

        # Act
        response = create_booking(booking)

        # Assert
        self.assertEqual(response.id, mock_uuid)  # Ensure the ID was assigned correctly
        self.assertTrue(response.completed)
        mock_db_insert.assert_called_once_with(booking)  # Ensure db_insert was called once

class TestReadSingleBooking(unittest.TestCase):

    @patch('Bookings.handler.db_read_single')
    def test_successful_booking_retrieval(self, mock_db_read_single):
        # Arrange
        booking_id = UUID('12345678123456781234567812345678')
        expected_booking = Booking(id=booking_id, title="Test Booking", description="Test Description", completed=False)
        mock_db_read_single.return_value = expected_booking

        # Act
        result = read_single_booking(booking_id)

        # Assert
        self.assertEqual(result, expected_booking)
        mock_db_read_single.assert_called_once_with(f"{booking_id}")

    @patch('Bookings.handler.db_read_single')
    def test_non_existent_booking(self, mock_db_read_single):
        # Arrange
        booking_id = UUID('12345678123456781234567812345678')
        mock_db_read_single.return_value = None

        # Act
        result = read_single_booking(booking_id)

        # Assert
        self.assertIsNone(result)
        mock_db_read_single.assert_called_once_with(f"{booking_id}")

    def test_invalid_uuid_format(self):
        # Arrange
        invalid_uuid = "invalid-uuid-format"

        # Act & Assert
        with self.assertRaises(ValueError):
            read_single_booking(UUID(invalid_uuid))

if __name__ == '__main__':
    unittest.main()