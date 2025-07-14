from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from .models import db, ParkingLot, ParkingSpot, Reservation , User
from sqlalchemy import or_

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    query = request.args.get('query')
    if query:
        lots = ParkingLot.query.filter(
            or_(
                ParkingLot.location.ilike(f'%{query}%'),
                ParkingLot.pin_code.ilike(f'%{query}%')
            )
        ).all()
    else:
        lots = ParkingLot.query.all()

    return render_template('available_lots.html', lots=lots)




@views.route('/admin/add-lot', methods=['GET', 'POST'])
def add_lot():
    if request.method == 'POST':
        location = request.form.get('location')
        address = request.form.get('address')
        pin_code = request.form.get('pin_code')
        price_per_hour = request.form.get('price_per_hour')
        max_spots = request.form.get('max_spots')

        new_lot = ParkingLot(
            location=location,
            address=address,
            pin_code=pin_code,
            price_per_hour=price_per_hour,
            max_spots=max_spots
        )
        db.session.add(new_lot)
        db.session.commit()
        
        for _ in range(new_lot.max_spots):
            spot = ParkingSpot(lot_id=new_lot.id, status="A")
            db.session.add(spot)


        db.session.commit()
        flash('Successfully added Parking Lot and Spots', 'success')
        return redirect(url_for('views.home'))
        
    return render_template('add_lot.html')
    
        
@views.route('/admin/dashboard')
def dashboard():
    lots = ParkingLot.query.all()
    lots_data = []

    for lot in lots:
        total_spots = lot.max_spots
        available_spots_lot = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
        occupied_spots_lot = total_spots - available_spots_lot

        lots_data.append({
            'id': lot.id,
            'location': lot.location,
            'address': lot.address,
            'pin_code': lot.pin_code,
            'price_per_hour': lot.price_per_hour,
            'total_spots': total_spots,
            'available_spots': available_spots_lot,
            'occupied_spots': occupied_spots_lot
        })

    total_lots = len(lots)
    total_spots = sum(lot.max_spots for lot in lots)
    available_spots = ParkingSpot.query.filter_by(status='A').count()
    occupied_spots = total_spots - available_spots

    return render_template(
        'dashboard.html',
        lots=lots_data,
        total_lots=total_lots,
        total_spots=total_spots,
        available_spots=available_spots,
        occupied_spots=occupied_spots
    )

@views.route('/admin/lot/<int:lot_id>')
def view_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
    return render_template('view.html',lot=lot, spots=spots)

@views.route('/admin/lot/<int:lot_id>/delete')
def delete_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    
    occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
    
    if occupied > 0:
        flash("This lot has active bookings and can't be removed.", "warning")
        return redirect(url_for('views.dashboard'))


    ParkingSpot.query.filter_by(lot_id=lot.id).delete()
    db.session.delete(lot)
    db.session.commit()

    flash("Parking lot deleted successfully.", "success")
    return redirect(url_for('views.dashboard'))

@views.route('user/book/<int:lot_id>')
def book_spot(lot_id):
    if 'user_id' not in session:
        flash("You need to be logged in to book a spot,", "warning")
        return redirect(url_for('auth.login'))
    
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
    if not spot:
        flash("No available spots in this lot.", "warning")
        return redirect(url_for('views.home'))
    
    new_reservation = Reservation(
        user_id=session['user_id'],
        spot_id=spot.id,
    )

    spot.status = 'O'
    db.session.add(new_reservation)
    db.session.commit() 

    flash("Spot booked successfully.", "success")
    return redirect(url_for('views.my_bookings')) 


@views.route('user/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        flash("You need to be logged in to view your bookings.", "warning")
        return redirect(url_for('auth.login'))
    
    bookings = Reservation.query.filter_by(user_id=session['user_id']).all()
    return render_template('bookings.html', bookings=bookings)

@views.route('/user/release/<int:reservation_id>')
def release_spot(reservation_id):
    if 'user_id' not in session:
        flash("Please login to continue.", "warning")
        return redirect(url_for('auth.login'))


    reservation = Reservation.query.get_or_404(reservation_id)

    if reservation.user_id != session['user_id']:
        flash("Unauthorized action.", "danger")
        return redirect(url_for('views.my_bookings'))

    if reservation.out_time is not None:
        flash("Spot already released.", "info")
        return redirect(url_for('views.my_bookings'))
    
    from datetime import datetime
    now = datetime.now()
    reservation.out_time = now
    print("OUT TIME:", reservation.out_time)


    in_time = reservation.in_time
    duration = now - in_time
    hours = int(duration.total_seconds()// 3600) + 1 

    spot = ParkingSpot.query.get(reservation.spot_id)
    lot = ParkingLot.query.get(spot.lot_id)
    print("Price per hour:", lot.price_per_hour)


    print("Lot ID:", reservation.spot.lot_id)
    print("Lot Found", lot)
    print("Price per hour:", lot.price_per_hour if lot else "Lot not found")
    reservation.amount = lot.price_per_hour * hours
    
    reservation.spot.status = 'A'

    db.session.commit()

    flash(f"Spot released successfully. Total Cost: ₹{reservation.amount}", "success")
    return redirect(url_for('views.my_bookings'))


@views.route('/admin/users')
def view_users():
    if session.get('user_role') != 'admin':
        flash("Unauthorized access.", "danger")
        return redirect(url_for('views.home'))
    
    users = User.query.all()
    return render_template('users.html', users=users)

@views.route('/user/available-lots')
def available_lots():
    if 'user_id' not in session:
        flash("Please log in first", "warning")
        return redirect(url_for('auth.login'))

    query = request.args.get('query')
    if query:
        lots = ParkingLot.query.filter(
            or_(
                ParkingLot.location.ilike(f'%{query}%'),
                ParkingLot.pin_code.ilike(f'%{query}%')
            )
        ).all()
    else:
        lots = ParkingLot.query.all()

    return render_template('available_lots.html', lots=lots)
