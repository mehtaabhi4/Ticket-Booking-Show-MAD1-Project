from flask import render_template, request, redirect, url_for, flash
from application.models import *
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from application import app, db


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/user_login_register')
def user_login_register():
    return render_template('user_login_register.html')


@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    all_venue_data = Venue.query.all()
    all_show_data = Show.query.all()
    return render_template('venue_show_management.html', venues=all_venue_data, shows=all_show_data)


@app.route('/venue_insert', methods=['POST'])
@login_required
def venue_insert():
    if request.method == 'POST':
        name = request.form['name']
        place = request.form['place']
        capacity = request.form['capacity']
        no_of_screens = request.form['no_of_screens']

        venue_data = Venue(name, place, capacity, no_of_screens)

        db.session.add(venue_data)
        db.session.commit()

        flash("Venue Inserted Successfully")

        return redirect(url_for('admin_dashboard'))


@app.route('/venue_update', methods=['GET', 'POST'])
@login_required
def venue_update():
    if request.method == 'POST':
        venue_data = Venue.query.get(request.form.get('venue_id'))
        venue_data.venue_name = request.form['name']
        venue_data.place = request.form['place']
        venue_data.capacity = request.form['capacity']
        venue_data.no_of_screens = request.form['no_of_screens']
        db.session.commit()

        flash("Venue Updated Successfully")

        return redirect(url_for('admin_dashboard'))


@app.route('/venue_delete/<venue_id>/', methods=['GET', 'POST'])
@login_required
def venue_delete(venue_id):
    venue_data = Venue.query.get(venue_id)
    shows = Show.query.filter_by(venue_id=venue_id).all()
    for show in shows:
        bookings = Booking.query.filter_by(show_id=show.show_id).all()
        for booking in bookings:
            db.session.delete(booking)
            db.session.commit()
        db.session.delete(show)
        db.session.commit()

    db.session.delete(venue_data)
    db.session.commit()

    flash("Venue Deleted Successfully")

    return redirect(url_for('admin_dashboard'))


@app.route('/show_insert', methods=['POST'])
@login_required
def show_insert():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        show_date = datetime.strptime(request.form['show_date'], '%Y-%m-%d').date()
        show_start_time = datetime.strptime(request.form['show_start_time'], '%H:%M').time()
        show_end_time = datetime.strptime(request.form['show_end_time'], '%H:%M').time()
        rating = request.form['rating']
        tags = request.form['tags']
        ticket_price = request.form['ticket_price']
        venue_id = request.form['venue_id']

        # Validation so that show doesn't overlap
        venue = Venue.query.get(venue_id)

        if not venue:
            flash('Invalid venue')
            return redirect(url_for('admin_dashboard'))

        if show_date < datetime.now().date().today():
            flash('Show cannot happen in past. Recheck Date')
            return redirect(url_for('admin_dashboard'))
        elif show_date == datetime.now().date():
            if show_start_time <= datetime.now().time() or show_end_time <= datetime.now().time():
                flash('Show cannot happen in past. Recheck Time')
                return redirect(url_for('admin_dashboard'))

        already_running_shows = Show.query.filter_by(venue_id=venue_id, show_date=show_date).all()

        for show in already_running_shows:
            if show.show_start_time <= show_end_time <= show.show_end_time:
                flash('Another show is already running on this time.')
                return redirect(url_for('admin_dashboard'))
            if show.show_start_time <= show_start_time <= show.show_start_time:
                flash('Another show is already running on this time.')
                return redirect(url_for('admin_dashboard'))

        show_data = Show(name, description, show_date, show_start_time, show_end_time, rating, tags, ticket_price,
                         venue_id)

        db.session.add(show_data)
        db.session.commit()

        flash("Show Inserted Successfully")

        return redirect(url_for('admin_dashboard'))


@app.route('/show_update', methods=['GET', 'POST'])
@login_required
def show_update():
    if request.method == 'POST':

        show_date = datetime.strptime(request.form['show_date'], '%Y-%m-%d').date()
        show_start_time = datetime.strptime(request.form['show_start_time'], '%H:%M:%S').time()
        show_end_time = datetime.strptime(request.form['show_end_time'], '%H:%M:%S').time()
        venue_id = request.form['venue_id']

        venue = Venue.query.get(venue_id)

        if not venue:
            flash('Invalid venue')
            return redirect(url_for('admin_dashboard'))

        already_running_shows = Show.query.filter_by(venue_id=venue_id, show_date=show_date).all()

        for show in already_running_shows:
            if show_date < datetime.now().date().today():
                flash('Show cannot happen in past. Recheck Date')
                return redirect(url_for('admin_dashboard'))
            if show_date == datetime.now().date().today():
                if show_start_time <= datetime.now().time() or show_end_time <= datetime.now().time():
                    flash('Show cannot happen in past. Recheck Time')
                    return redirect(url_for('admin_dashboard'))

            if show.show_start_time <= show_end_time <= show.show_end_time:
                flash('Another show is already running on this time.')
                return redirect(url_for('admin_dashboard'))
            if show.show_start_time <= show_start_time <= show.show_start_time:
                flash('Another show is already running on this time.')
                return redirect(url_for('admin_dashboard'))

        show_data = Show.query.get(request.form.get('show_id'))
        show_data.show_name = request.form['name']
        show_data.description = request.form['description']
        show_data.show_date = show_date
        show_data.show_start_time = show_start_time
        show_data.show_end_time = show_end_time
        show_data.rating = request.form['rating']
        show_data.tags = request.form['tags']
        show_data.ticket_price = request.form['ticket_price']
        show_data.venue_id = venue_id

        db.session.commit()

        flash("Show Updated Successfully")

        return redirect(url_for('admin_dashboard'))


@app.route('/show_delete/<show_id>/', methods=['GET', 'POST'])
@login_required
def show_delete(show_id):
    show = Show.query.get(show_id)
    bookings = Booking.query.filter_by(show_id=show_id).all()
    for booking in bookings:
        db.session.delete(booking)
        db.session.commit()

    db.session.delete(show)
    db.session.commit()

    flash("Show Deleted Successfully")

    return redirect(url_for('admin_dashboard'))


def search(shows_list, search_q):
    s_list = []
    for show in shows_list:
        if (search_q in show.show_name or
                search_q in show.description or
                search_q in show.venue_name or
                search_q in show.place or
                str(show.rating) == search_q):
            s_list.append(show)

    # search in shows table for matching tags
    shows = Show.query.filter(Show.tags.ilike(f'%{search_q}%')).all()
    for show in shows:
        if show not in s_list:
            s_list.append(show)

    return s_list


# Ticket Booking Page for Users
@app.route('/ticket_booking_page', methods=['GET', 'POST'])
@login_required
def ticket_booking_page():
    shows_list = db.session.query(Show.show_id, Show.show_name, Show.description, Show.show_date,
                                  Show.show_start_time,
                                  Show.show_end_time, Show.rating, Show.ticket_price, Show.ticket_available,
                                  Venue.venue_name, Venue.place, Venue.no_of_screens). \
        join(Venue, Show.venue_id == Venue.venue_id).all()

    search_q = request.args.get('search_query')
    s_list = []
    if search_q:
        s_list = search(shows_list, search_q)
    return render_template('ticket_booking.html', user=current_user.user_name, shows_list=shows_list,
                           search_list=s_list)


@app.route('/select_venue')
@login_required
def select_venue():
    show_id = int(request.args.get('show_id'))
    venue_list = Venue.query.join(Show).filter(Show.show_id == show_id).all()
    return render_template('select_venue.html', user=current_user, venue_list=venue_list, show_id=show_id)


def calculate_ticket_price(number_of_tickets, ticket_price):
    return number_of_tickets * ticket_price


@app.route('/book_ticket', methods=['GET', 'POST'])
@login_required
def book_ticket():
    if request.method == 'POST':
        user_id = current_user.user_id
        venue_id = int(request.args.get('venue_id'))
        show_id = int(request.args.get('show_id'))
        number_of_tickets = request.form['tickets']
        number_of_tickets = int(number_of_tickets)

        # venue = Venue.query.filter_by(venue_id=venue_id).first()
        show = Show.query.filter_by(show_id=show_id).first()

        ticket_available = int(show.ticket_available)
        if ticket_available == 0:
            flash("This Show is Houseful.")

        elif number_of_tickets > ticket_available:
            flash(f'Cannot book {number_of_tickets}')

        else:
            total_ticket_price = calculate_ticket_price(number_of_tickets, int(show.ticket_price))
            ticket_available = ticket_available - number_of_tickets
            show.ticket_available = str(ticket_available)
            booking = Booking(user_id, show_id, venue_id, number_of_tickets, total_ticket_price)
            db.session.add(booking)
            db.session.commit()
            flash("Booking Done Successfully")

            return redirect(url_for('booking_details'))

    return redirect(url_for('ticket_booking_page'))


@app.route('/booking_details')
@login_required
def booking_details():
    bookings = Booking.query \
        .join(User).join(Show).join(Venue) \
        .filter(Booking.user_id == current_user.user_id) \
        .with_entities(User.user_name, Booking.booking_date, Show.show_name, Show.show_date, Show.show_start_time,
                       Show.show_end_time,
                       Venue.venue_name, Venue.place, Venue.no_of_screens, Booking.number_of_tickets, Show.ticket_price,
                       Booking.total_ticket_price) \
        .order_by(Booking.booking_date.desc()) \
        .all()

    return render_template('booking_details.html', bookings=bookings)


# Login Page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and user.email == "admin@admin.com" and email == "admin@admin.com":
            if password == user.password and password == "admin":

                login_user(user, remember=True)
                flash('Logged in Successfully.')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Incorrect Password.')

        return redirect(url_for('index'))

    return render_template('admin_login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if password == user.password:

                login_user(user, remember=True)
                flash('Logged in Successfully.')
                return redirect(url_for('ticket_booking_page'))
            else:
                flash('Incorrect Password.')
        else:
            flash('User does not exist.')
            return redirect(url_for('register'))

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Password do not match')
            return redirect(url_for('register'))

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists')
            return redirect(url_for('login'))

        new_user = User(user_name=user_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('You are successfully registered')

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("User Logged-Out Successfully")
    return redirect(url_for('home'))


def create_default_user():
    if not User.query.first():
        user = User(user_name='Admin', email='admin@admin.com', password='admin')
        db.session.add(user)
        db.session.commit()
