import requests
import json
import re
import mysql.connector
from datetime import datetime
import config
import logging

FAILURE_IMAGE_NAME = 'negative.jpeg'
SUCCESS_IMAGE_NAME = 'positive.jpeg'
SERVICE_IMAGE_NAME = 'plate_image.jpg'


class Vehicle:
    def __init__(self, plate_number, access_granted, timestamp):
        self.plate_number = plate_number
        self.access_granted = access_granted
        self.timestamp = timestamp


class ParkingService:
    INSERT_SQL_QUERY = "INSERT INTO incoming_vehicles (plate_number,access_granted,timestamp) VALUES (%s, %s, %s)"
    API_URL = 'https://api.ocr.space/parse/image'
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
    LOGGING_FORMAT = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    LOGGING_DATEFMT = '%Y-%m-%d:%H:%M:%S'
    LOGGING_FILENAME = 'logfile.log'

    def ocr_api(self, filename, overlay=False, api_key=config.api_key, language=config.language):
        payload = {'isOverlayRequired': overlay,
                   'apikey': api_key,
                   'language': language,
                   }
        with open(filename, 'rb') as f:
            response = requests.post(ParkingService.API_URL, files={filename: f}, data=payload)
            err = ParkingService.server_responses_error_handling(self, response.status_code)
            if err:
                if response == 0:
                    logging.error('No response from server')
                    raise Exception('No response from server')
                else:
                    logging.error(response.content.decode())
                    raise Exception(response.content.decode())

        return response.content.decode()

    def server_responses_error_handling(self, status_code=0):
        if 200 <= status_code < 300:
            return False
        return True

    def remove_spaces(self, plate_number):
        plate_number = plate_number.replace(' ', '')
        return plate_number

    def load_json(self, json_text):
        try:
            json_content = json.loads(json_text)
            return json_content
        except ValueError as err:
            logging.error(f'Loading json has failed with error: {ValueError}')
            raise err

    def json_error_handling(self, json_content):
        if json_content['IsErroredOnProcessing']:
            logging.error(json_content['ErrorMessage'])
            raise Exception(json_content['ErrorMessage'])

    def is_access_granted(self, plate_number, timestamp):
        if plate_number == '':
            logging.info(f'Plate number: {plate_number}, Denied: Unreadable / missing plate, Timestamp: {timestamp}')
            return False

        if not re.search(r"[A-Z]", plate_number):
            logging.info(f'Plate number: {plate_number}, Denied: No letter in plate, Timestamp: {timestamp}')
            return False

        if plate_number[-1] in ('6', 'G'):
            logging.info(f'Plate number: {plate_number}, Denied: Public transportation, Timestamp: {timestamp}')
            return False

        if 'L' in plate_number:
            logging.info(f'Plate number: {plate_number}, Denied: Law, Timestamp: {timestamp}')
            return False

        if 'M' in plate_number:
            logging.info(f'Plate number: {plate_number}, Denied: Military, Timestamp: {timestamp}')
            return False

        logging.info(f'Plate number: {plate_number}, Granted, Timestamp: {timestamp}')
        return True

    def insert_to_db(self, vehicle: Vehicle):
        try:
            db_config = mysql.connector.connect(
                host="localhost",
                user=config.user,
                password=config.password,
                database="parking_lot"
            )
            db_cursor = db_config.cursor()
            value_for_db = (vehicle.plate_number, vehicle.access_granted, vehicle.timestamp)
            db_cursor.execute(ParkingService.INSERT_SQL_QUERY, value_for_db)
            db_config.commit()
        # handling DB errors
        except mysql.connector.Error as err:
            logging.error(err)
            raise Exception(err)
        except:
            logging.error("An unknown DB error occurred")
            raise Exception("An unknown DB error occurred")

    def vehicle_enter(self, filename):
        logging.basicConfig(format=ParkingService.LOGGING_FORMAT,
                            datefmt=ParkingService.LOGGING_DATEFMT,
                            filename=ParkingService.LOGGING_FILENAME,
                            level=logging.DEBUG)

        timestamp = datetime.now().strftime(ParkingService.TIMESTAMP_FORMAT)
        json_text = ParkingService.ocr_api(self, filename=filename, language=config.language)
        json_content = ParkingService.load_json(self, json_text)
        ParkingService.json_error_handling(self, json_content)
        plate_number = json_content['ParsedResults'][0]['ParsedText']
        plate_number = ParkingService.remove_spaces(self, plate_number)
        access_granted = ParkingService.is_access_granted(self, plate_number, timestamp)
        vehicle = Vehicle(plate_number, access_granted, timestamp)
        ParkingService.insert_to_db(self, vehicle)


# Client
def main():
    try:
        service = ParkingService()
        service.vehicle_enter(SERVICE_IMAGE_NAME)
    except ValueError as err:
        print(err)


main()

