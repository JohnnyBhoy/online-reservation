from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservation.db'
db = SQLAlchemy(app)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #reservation_date = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)#
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    contact_number = db.Column(db.Integer, default=0)
    number_of_guest = db.Column(db.Integer, default=0)
    address = db.Column(db.String(400), default='')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        #reserve_reservation_date = request.form['reservation_date']
        reserve_first_name = request.form['first_name']
        reserve_last_name = request.form['last_name']
        reserve_contact_number = request.form['contact_number']
        reserve_number_of_guest = request.form['number_of_guest']
        reserve_address = request.form['address']
        new_reserve = Reservation(first_name=reserve_first_name, last_name=reserve_last_name, contact_number=reserve_contact_number, number_of_guest=reserve_number_of_guest, address=reserve_address)

        try:
            db.session.add(new_reserve)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your reservation!'
    else:
        reserves = Reservation.query.order_by(Reservation.date_created).all()
        return render_template('index.html', reserves=reserves)

@app.route('/delete/<int:id>')
def delete(id):
        reserve_to_remove = Reservation.query.get_or_404(id)

        try:
            db.session.delete(reserve_to_remove)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem removing reservation'

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    reserve = Reservation.query.get_or_404(id)

    if request.method == 'POST':
        reserve.first_name = request.form['first_name']
        reserve.last_name = request.form['last_name']
        reserve.contact_number = request.form['contact_number']
        reserve.number_of_guest = request.form['number_of_guest']
        reserve.address = request.form['address']

        try:
            db.session.commit()
            return redirect('/') 
        except:
            return 'There was  a problem updating your reservation'
    else:
        return render_template('update.html', reserve = reserve)   

if __name__ == "__main__":
    app.run(debug=True)