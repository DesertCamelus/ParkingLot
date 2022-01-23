import unittest
import parking_lot
from datetime import datetime

TEST_TIMESTAMP = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
SERVICE = parking_lot.ParkingService()


class TestParkingLot(unittest.TestCase):
    def test_unreadable_plate(self):
        test_plate_number = ''
        result = SERVICE.is_access_granted(test_plate_number, TEST_TIMESTAMP)
        self.assertFalse(result)

    def test_only_digits_plate(self):
        test_plate_number = '8785492'
        result = SERVICE.is_access_granted(test_plate_number, TEST_TIMESTAMP)
        self.assertFalse(result)

    def test_public_transportation_plate_with_g(self):
        test_plate_number = '878549G'
        result = SERVICE.is_access_granted(test_plate_number, TEST_TIMESTAMP)
        self.assertFalse(result)

    def test_public_transportation_plate_with_6(self):
        test_plate_number = '8785496'
        result = SERVICE.is_access_granted(test_plate_number, TEST_TIMESTAMP)
        self.assertFalse(result)

    def test_digit_and_chars_plate(self):
        test_plate_number = '8-785-49Q'
        result = SERVICE.is_access_granted(test_plate_number, TEST_TIMESTAMP)
        self.assertTrue(result)

    def test_chars_only_plate(self):
        test_plate_number = 'ADGHVCD'
        result = SERVICE.is_access_granted(test_plate_number, TEST_TIMESTAMP)
        self.assertTrue(result)

    def test_law_plate(self):
        test_plate_number = '878L549'
        result = SERVICE.is_access_granted(test_plate_number, TEST_TIMESTAMP)
        self.assertFalse(result)

    def test_military_plate(self):
        test_plate_number = '87M8549'
        result = SERVICE.is_access_granted(test_plate_number, TEST_TIMESTAMP)
        self.assertFalse(result)

    def test_server_response_199(self):
        test_status_code = 199
        result = SERVICE.server_responses_error_handling(test_status_code)
        self.assertTrue(result)

    def test_server_response_200(self):
        test_status_code = 200
        result = SERVICE.server_responses_error_handling(test_status_code)
        self.assertFalse(result)

    def test_server_response_201(self):
        test_status_code = 201
        result = SERVICE.server_responses_error_handling(test_status_code)
        self.assertFalse(result)

    def test_server_response_299(self):
        test_status_code = 299
        result = SERVICE.server_responses_error_handling(test_status_code)
        self.assertFalse(result)

    def test_server_response_300(self):
        test_status_code = 300
        result = SERVICE.server_responses_error_handling(test_status_code)
        self.assertTrue(result)

    def test_server_response_no_response_no_arg(self):
        result = SERVICE.server_responses_error_handling()
        self.assertTrue(result)

    def test_server_response_no_response_0(self):
        test_status_code = 0
        result = SERVICE.server_responses_error_handling(test_status_code)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
