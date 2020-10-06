import secrets
from pathlib import Path
from datetime import datetime

from flask import Flask, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import InputRequired


app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)
db_path = Path(__file__).parent / "chatbot.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    replies = db.relationship("Turn", backref="user")


class Turn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    by_user = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)


class ChatForm(FlaskForm):
    reply = TextAreaField("Odpověď:", validators=[InputRequired()])


@app.route("/", methods=("GET", "POST"))
def index():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
    else:
        user = User()
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id

    form = ChatForm()
    if form.validate_on_submit():
        # the user has just submitted the form -> take note of their
        # reply
        reply = form.reply.data
        print(reply)
        if user.name is None:
            user.name = reply
            db.session.add(user)
        turn = Turn(text=reply, user=user, by_user=True)
        db.session.add(turn)
        db.session.commit()
        return redirect(url_for("index"))

    else:
        # the user is waiting for a reaction from the chatbot
        chatbot_turn = Turn(
            text=next_chatbot_turn(user.replies), user=user, by_user=False
        )
        db.session.add(chatbot_turn)
        db.session.commit()
        return render_template(
            "index.html", user=user.name, history=user.replies, form=form
        )


def next_chatbot_turn(history):
    if not history:
        return "Dobrý den, jak se jmenujete?"
    last = history[-1].text
    if len(history) == 2:
        return f"Vy se jmenujete {last}? Těší mě, já jsem Chatbot!"
    if len(last) > 100:
        return "Máte dneska povídavou? :)"
    if "?" in last:
        return "Já na otázky bohužel moc odpovídat neumím..."
    if "!" in last:
        return "Tak tak, sám bych to líp neřekl."
    else:
        return "Těžko říct, je to zapeklitá věc."


if not db_path.is_file():
    db.create_all()
