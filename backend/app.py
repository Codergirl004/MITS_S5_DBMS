from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the database (SQLite in this case)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bicycle_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# Define a model for the bookings table
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    college_id = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    bicycle_choice = db.Column(db.String(100), nullable=False)
    #date=db.column(db.Date)
    def __repr__(self):
        return f"<Booking {self.name}, {self.college_id}, {self.email}, {self.bicycle_choice}>"

# Create the database
with app.app_context():
    db.create_all()

# Route to show the booking confirmation form
@app.route('/confirm-booking', methods=['GET', 'POST'])
def confirm_booking():
    if request.method == 'POST':
        name = request.form['name']
        college_id = request.form['college-id']
        email = request.form['email']
        bicycle_choice = request.form['bicycle-choice']

        new_booking = Booking(name=name, college_id=college_id, email=email, bicycle_choice=bicycle_choice)
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('booking_success'))

    return render_template('confirm-booking.html')  # Make sure this file exists in templates folder
@app.route('/')
def homePage():
    return render_template('index.html')

# Route to show a booking success page after form submission
@app.route('/success')
def booking_success():
    return "<h1>Booking Successful!</h1>"
@app.route('/view-bookings')
def view_bookings():
    bookings = Booking.query.all()  # Get all bookings from the database
    return render_template('view_bookings.html', bookings=bookings)

@app.route('/bicycle-selection')
def bicycle_selection():
    return render_template('bicycle-selection.html')
@app.route('/availability')
def availability():
    return render_template('availability.html')

# Start the application
if __name__ == '__main__':
    app.run(debug=True)
