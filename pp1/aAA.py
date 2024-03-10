from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cars.db"
db = SQLAlchemy(app)


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    car_plate = db.relationship('CarPlate', backref='car', uselist=False)


class CarPlate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reg_number = db.Column(db.String(20), nullable=False, unique=True)
    custom_number = db.Column(db.String(20))
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)


@app.route("/")
def govno():
    return "<a href='http://127.0.0.1:5000/car'>AAAA</a>"


@app.route('/car', methods=['GET'])
def get_car_by_reg_number():
    reg_number = request.args.get('reg_number')
    car_plate = CarPlate.query.filter_by(reg_number=reg_number).first()
    if car_plate:
        car = car_plate.car
        return jsonify({
            'owner': car.owner,
            'brand': car.brand,
            'model': car.model,
            'year': car.year,
            'reg_number': car_plate.reg_number,
            'custom_number': car_plate.custom_number
        })
    else:
        return jsonify({'error': 'Car not found for the given registration number'}), 404


def fill_database():
    car_data = [
        {"owner": "John Doe", "brand": "Toyota", "model": "Camry", "year": 2018,
         "reg_number": "AB1234BA", "custom_number": "ABBOBBA"},
        {"owner": "Will Smith", "brand": "Toyota", "model": "Hilux", "year": 2010,
         "reg_number": "AA0001AA", "custom_number": "WILLKA"},
        {"owner": "Eloh Minsk", "brand": "Cherry", "model": "Tiggo 7 Pro Turbo Max XLS", "year": 2022,
         "reg_number": "EE9182BA", "custom_number": "CHINACAR"}
    ]
    for car_info in car_data:
        car = Car(owner=car_info["owner"],
                  brand=car_info["brand"],
                  model=car_info["model"],
                  year=car_info["year"])

        db.session.add(car)

        car_plate = CarPlate(reg_number=car_info["reg_number"],
                             custom_number=car_info["custom_number"],
                             car=car)
        db.session.add(car_plate)
        db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # fill_database()
    app.run(debug=True)
