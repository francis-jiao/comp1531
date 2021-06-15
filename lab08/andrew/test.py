from server import app, system
from src.client import bootstrap_system
from src.Car import *
from src.CarRentalSystem import BookingError
from routes import *
import pytest

def test_correct():
    s_date = "2018-5-13"
    e_date = "2018-5-16"
    start_date = convert_time(s_date, 0)
    end_date = convert_time(e_date, 1)

    car = LargeCar("Mazda", "Falcon", 0)
    assert car != None
    assert isinstance(start_date, BookingError) != True
    assert isinstance(end_date, BookingError) != True
    diff = end_date-start_date
    location = Location("Kingsford", "UNSW")
    booking = system.make_booking(current_user, diff, car, location)
    assert booking != None
    assert car.get_fee(diff.days) == 300

def test_invalid_start_date():
    s_date = "cbsau"

    try:
        start_date = convert_time(s_date, 0)
    except BookingError as err:
        output = err.msg

    assert output == 'Invalid Start Date'

def test_invalid_end_date():

    e_date = ""

    try:
        e_date = convert_time(e_date, 1)
    except BookingError as err:
        output = err.msg

    assert output == 'Invalid End Date'

def test_invalid_period():

    try:
        s_date = "2018-5-16"
        e_date = "2018-5-13"
        start_date = convert_time(s_date, 0)
        end_date = convert_time(e_date, 1)

        car = LargeCar("Mazda", "Falcon", 0)
        assert car != None
        assert isinstance(start_date, BookingError) != True
        assert isinstance(end_date, BookingError) != True
        diff = end_date-start_date
        location = Location("Kingsford", "UNSW")
        booking = system.make_booking(current_user, diff, car, location)

    except BookingError as err:
        output = err.msg
        assert output == 'Specify a valid booking period.'


def test_invalid_pickup():
    try:
        location = Location(None, "Kingsford")
        s_date = "2018-5-13"
        e_date = "2018-5-16"
        start_date = convert_time(s_date, 0)
        end_date = convert_time(e_date, 1)
        diff = end_date-start_date
        car = LargeCar("Mazda", "Falcon", 0)
        dropoff = system.make_booking(current_user, diff, car, location)

    except BookingError as err:
        output = err.msg
        assert output == 'Specity a valid start location.'

def test_invalid_dropoff():
    try:
        location = Location("Kingsford", None)
        s_date = "2018-5-13"
        e_date = "2018-5-16"
        start_date = convert_time(s_date, 0)
        end_date = convert_time(e_date, 1)
        diff = end_date-start_date
        car = LargeCar("Mazda", "Falcon", 0)
        dropoff = system.make_booking(current_user, diff, car, location)
    except BookingError as err:
        output = err.msg
        assert output == 'Specity a valid end location.'
