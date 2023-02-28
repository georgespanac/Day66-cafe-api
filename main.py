from random import choice

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # Method 1.
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            # Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/all")
def all():
    all = []
    for cafe in Cafe.query.all():
        all.insert(0, cafe.to_dict())
    return jsonify(all)

@app.route("/search")
def search():
    location = request.args.get('location')
    cafe = Cafe.query.filter_by(location=location).first()
    if cafe:
        return jsonify(cafe.to_dict())
    else:
        return jsonify({"Not Found": "Sorry, we dont have that cafe at that location"})

@app.route("/add")
def add():
    new_cafe = Cafe(name=request.form["name"], map_url=request.form["map_url"])
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify({"response": {"sucess":"Succesfully added a new cafe"}})


@app.route("/update_price/<cafe_id>")
def update_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        new_price = request.args.get('new_price')
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"sucess": "Succesfully updated the price"}), 200
    else:
        return jsonify(error={"Not Found": "Cafe with id not found!"}), 404

@app.route("/report_closed/<cafe_id>")
def report_closed(cafe_id):
    if request.args.get('api-key') == "TopSecretAPIKey":
        cafe = Cafe.query.get(cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"sucess": "Succesfully deleted the Cafe"}), 200
        else:
            return jsonify(error={"Not Found": "Cafe with id not found!"}), 404
    else:
        return jsonify(error="That's not allowed, Make sure you have the correct api-key"), 403

@app.route("/random")
def random():
    random_cafe = choice(Cafe.query.all())
    return jsonify(name=random_cafe.name,
                   map_url=random_cafe.map_url,
                   img_url=random_cafe.img_url,
                   location=random_cafe.location,
                   seats=random_cafe.seats,
                   has_toilet=random_cafe.has_toilet,
                   has_wifi=random_cafe.has_wifi,
                   has_sockets=random_cafe.has_sockets,
                   can_take_calls=random_cafe.can_take_calls,
                   coffee_price=random_cafe.coffee_price,
                   id = random_cafe.id
                   )

## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
