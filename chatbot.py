import secrets
from pathlib import Path
from datetime import datetime

from flask import Flask, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired


app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)
db_path = Path(__file__).parent / "chatbot.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    turns = db.relationship("Turn", backref="user")


class Turn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    by_user = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)


if not db_path.is_file():
    db.create_all()


class ChatForm(FlaskForm):
    reply = StringField("Odpověď:", validators=[InputRequired()])


@app.route("/", methods=("GET", "POST"))
def index():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
    else:
        user = User()
        db.session.add(user)
        # need to commit here so that the new user gets assigned an id
        db.session.commit()
        session["user_id"] = user.id

    form = ChatForm()
    if form.validate_on_submit():
        # the user has submitted the form -> take note of their reply
        reply = form.reply.data.strip()
        form = ChatForm(formdata=None)
        if user.name is None:
            user.name = reply
            db.session.add(user)
        turn = Turn(text=reply, user=user, by_user=True)
        db.session.add(turn)

    if not user.turns or user.turns[-1].by_user:
        # either the conversation is just starting, or the last turn was
        # by the user -> generate the chatbot's next turn
        chatbot_turn = Turn(
            text=next_chatbot_turn(user.turns), user=user, by_user=False
        )
        db.session.add(chatbot_turn)

    db.session.commit()
    return render_template("index.html", user=user.name, history=user.turns, form=form)


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
    return "Těžko říct, je to zapeklitá věc."


if __name__ == "__main__":
    app.run(debug=True)
