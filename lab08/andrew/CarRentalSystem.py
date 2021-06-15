from src.Booking import Booking
from datetime import datetime
import copy

class BookingError(Exception):
    def __init__(self, variable, msg = None):
        super().__init__()
        if msg is None:
            self.msg = ""
        else:
            self.msg = msg
        #super().__init__()
        self.variable = variable

class CarRentalSystem:
    def __init__(self, admin_system, auth_manager):
        self._cars = []
        self._customers = []
        self._bookings = []
        self._admin_system = admin_system
        self._auth_manager = auth_manager


    '''
    Query Processing Services
    '''
    def car_search(self, name=None, model=None):
        if name is None and model is None:
            return self._cars
        cars = []

        for car in self._cars:
            c_name = car.name
            c_model = car.model
            if name is not None and name.lower() in c_name.lower():
                cars.append(car)
            elif model is not None and model.lower() in c_model.lower():
                cars.append(car)
        return cars



    def get_user_by_id(self, user_id):
        for c in self._customers:
            if c.get_id() == user_id:
                return c

        return self._admin_system.get_user_by_id(user_id)


    def get_car(self, rego):
        for c in self.cars:
            if c.rego == rego:
                return c
        return None



    '''
    Booking Services
    '''
    def make_booking(self, customer, period, car, location):
        # Prevent the customer from referencing 'current_user';
        # otherwise the customer recorded in each booking will be modified to
        # a different user whenever the current_user changes (i.e. when new user logs-in)
        try:
            if location.pickup == '' or location.pickup == None:
                raise BookingError(car, 'Specify a valid start location.')
            if location.dropoff == '' or location.dropoff == None:
                raise BookingError(car, 'Specify a valid end location.')
            if period.days < 0:
                raise BookingError(car, 'Specify a valid booking period.')

        except BookingError as error:
            return error

        else:
            new_booking = Booking(customer, period, car, location)
            self._bookings.append(new_booking)
            car.add_booking(new_booking)
            return new_booking


    '''
    Registration Services
    '''
    def add_car(self, car):
        self._cars.append(car)


    def add_customer(self, customer):
        self._customers.append(customer)



    '''
    Login Services
    '''

    def login_customer(self, username, password):
        for customer in self._customers:
            if self._auth_manager.login(customer, username, password):
                return True
        return False

    def login_admin(self, username, password):
        return self._admin_system.login(username, password)



    '''
    Properties
    '''
    @property
    def cars(self):
        return self._cars


    @property
    def bookings(self):
        return self._bookings
