from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)


class Styles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primary = db.Column(db.String())


db.create_all()


@app.route("/", methods=["GET"])
def hello_world():
    styles = Styles.query.first()
    if styles is None:
        primary = None
    else:
        primary = styles.primary
    return render_template("index.html", primary=primary)


@app.route("/", methods=["POST"])
def set_colour():
    primary = request.form.get("primary")

    # Query the database & update it
    styles = Styles.query.first()
    if styles is None:  # If first time setting, there will be none
        styles = Styles()

    styles.primary = primary
    db.session.add(styles)
    db.session.commit()
    return render_template("index.html")
