from src.Booking import Booking
import copy


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
        
        if name==None and model==None:
            return []
        
        cars=[]
        for car in self._cars:
            if name != None and name in car.name:
                cars.append(car)
                
            elif model != None and model in car.model:
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
    

    def validate(self, username, password):
        for customers in self._customers:
            if customers.username == username and customers.validate_password(password):
                return customers
                
            else:
                return None



    '''
    Booking Services
    '''
    def make_booking(self, customer, period, car, location):
        # Prevent the customer from referencing 'current_user';
        # otherwise the customer recorded in each booking will be modified to
        # a different user whenever the current_user changes (i.e. when new user logs-in)

        

        
        BookingError = []
        if location.pickup.isalnum() == False:
            BookingError.append("Specify a valid start location")
            
        if location.dropoff.isalnum() == False:
            BookingError.append("Specify a valid end location")
       
        if BookingError == []:
            customer = copy.copy(customer)
        
            new_booking = Booking(customer, period, car, location)
            self._bookings.append(new_booking)
            car.add_booking(new_booking)

            return new_booking
            
        else:
            return BookingError


    def check_fee(self, period, car):
        error = []
        
        if period < 0:
            error.append("Specify a valid booking period")
            return error

        else:
            return car.get_fee(period)



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
