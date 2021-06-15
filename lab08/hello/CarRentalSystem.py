from src.Booking import Booking
import copy
from src.errors import *
from datetime import datetime

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
    
        search_cars = []
        
        if name is None and model is None:          
            return self._cars
            
        for car in self._cars:
            c_name = car.name
            c_model = car.model
            if name is not None and name.lower() == c_name.lower():
                search_cars.append(car)
            elif model is not None and model.lower() == c_model.lower():
                search_cars.append(car)
        return search_cars
            
 
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
    #########################################################
    def _check_booking(self,start,end, start_date, end_date):
        errors = self.check_booking_error(start, end, start_date, end_date)
        if errors:
            raise BookingError(errors)    
    

    def make_booking(self, customer, car, location, start_date, end_date):
      
        try:
            self._check_booking(location.pickup, location.dropoff, start_date, end_date)
        except BookingError as be:
            return be.errors
        #########################        
        else:
            customer = copy.copy(customer)

            new_booking = Booking(customer, car, location)
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
        
    def check_booking_error(self, start, end, start_date,end_date):
        errors = {}

        if start == "":
            errors['start'] = "Specify a valid start location"
        if end == "":
            errors['end'] = "Specify a valid end location"
      
           
            
        date_format = "%Y-%m-%d"    
        
        try:
            datetime.strptime(start_date, date_format)
        except:
            errors['start_date'] = "Specify a valid start date"

        try:
            datetime.strptime(end_date, date_format)
        except:
            errors['end_date'] = "Specify a valid end date"
            
        if "start_date" not in errors and "end_date" not in errors:
        
            
            
            if datetime.strptime(start_date, date_format) > datetime.strptime(end_date, date_format):
                errors['period'] = "Specify a valid booking period"
        return errors


        
        
        
        
        
