from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://car_fleet_user:edfCorsica@localhost:5432/car_fleet'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Define a simple model to test
class Voiture(db.Model):
    __tablename__ = 'voitures'
    immat = db.Column(db.String(20), primary_key=True)
    propulsion = db.Column(db.String(50), nullable=False)
    nb_places = db.Column(db.Integer, nullable=False)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/test_db')
def test_database():
    try:
        # Attempt to create tables
        db.create_all()

        # Try to add a sample record
        test_voiture = Voiture(
            immat='TEST123',
            propulsion='Électrique',
            nb_places=5
        )
        db.session.add(test_voiture)
        db.session.commit()

        return "Database connection successful! Test record added."
    except Exception as e:
        return f"Database connection failed: {str(e)}"

@app.route('/all_voitures')
def get_all_voitures():
    try:
        voitures = Voiture.query.all()
        if not voitures:
            return "No cars found in the database."

        # Render the template and pass the list of cars
        return render_template('all_voitures.html', voitures=voitures)

    except Exception as e:
        return f"Failed to fetch cars: {str(e)}"
