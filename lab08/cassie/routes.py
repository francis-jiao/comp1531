from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user, login_user

from server import app, system, auth_manager
from datetime import datetime
from src.Location import Location



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Task 1: complete this function
    """

    if request.method == 'POST':
        user = system.validate(request.form["username"], request.form["password"])
        if user == None:
            return render_template('login.html')
            
        else:
           login_user(user)
        

        # Next helps with redirecting the user to their previous page
        redir = request.args.get('next')
        return redirect(redir or url_for('home'))
    
    return render_template('login.html')



@app.route('/login_admin', methods=['POST'])
def login_admin():

    '''
    TASK 4.1 complete this function
    '''

    redir = request.args.get('next')
    return redirect(redir or url_for('home'))



@app.route('/logout')
@login_required
def logout():
    auth_manager.logout()
    return redirect(url_for('home'))



'''
    Dedicated page for "page not found"
'''
@app.route('/404')
@app.errorhandler(404)
def page_not_found(e=None):
    return render_template('404.html'), 404



'''
    Search for Cars
'''
@app.route('/cars')
@login_required
def cars():
    """
    Task 2: At the moment this endpoint does not do anything if a search
    is sent. It should filter the cars depending on the search criteria
    """

    make=request.args.get('make')
    model=request.args.get('model')
    if make=="":
        make=None
        
    if model=="":
        model=None

    cars = system.car_search(make, model)

    return render_template('cars.html', cars = cars)



'''
    Display car details for the car with given rego
'''
@app.route('/cars/<rego>')
@login_required
def car(rego):
    car = system.get_car(rego)

    if not car:
        abort(404)

    return render_template('car_details.html', car=car)



'''
    Make a booking for a car with given rego
'''
@app.route('/cars/book/<rego>', methods=["GET", "POST"])
@auth_manager.customer_required
def book(rego):
    car = system.get_car(rego)

    if not car:
        abort(404)
    
    if request.method == 'POST':
        date_format = "%Y-%m-%d"
        start_date  = datetime.strptime(request.form['start_date'], date_format)
        end_date    = datetime.strptime(request.form['end_date'],   date_format)

        num_days = (end_date - start_date).days + 1
        
        if 'check' in request.form:

            fee = system.check_fee(num_days, car)

            if isinstance(fee, list):
                return render_template('Jinja.html', fee=fee)
                
            else:
                return render_template(
                    'booking_form.html',
                    confirmation=True,
                    form=request.form,
                    car=car,
                    fee=fee
                )

        elif 'confirm' in request.form:
            location = Location(request.form['start'], request.form['end'])
            booking  = system.make_booking(current_user, num_days, car, location)
    
            if isinstance(booking, list):
                return render_template('Jinja.html', booking=booking)
    
            else:
                return render_template('booking_confirm.html', booking=booking)

    return render_template('booking_form.html', car=car)


'''
    Display list of all bookings for the car with given 'rego'
'''
@app.route('/cars/bookings/<rego>')
@login_required
def car_bookings(rego):
    """
    Task 3: This should render a new template that shows a list of all
    the bookings associated with the car represented by 'rego'
    """
    
    car = system.get_car(rego)
    
    return render_template('bookings.html', book=car.bookings)


'''
    View all current bookings
'''
@app.route('/cars/bookings')
@auth_manager.admin_required
def all_bookings():

    '''
    Task 4.2: This should render a list of all current bookings
    on the system
    '''
    return '<h1> Needs to be implemented </h1>'


'''
    Add a new car to the system
'''
from src.CarFactory import CarFactory
@app.route('/add_car', methods=['GET', 'POST'])
@auth_manager.admin_required
def add_car():

    '''
    Task 4.3: This should allow the admin to register
    new cars to the system, using the method provided
    in the CarFactory class.
    
    Provide meaningful message upon success
    '''

    return render_template('car_register_form.html')
