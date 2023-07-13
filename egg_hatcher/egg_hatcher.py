from flask import Flask, flash, render_template, request, url_for, redirect, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from egg_hatcher_classes import *

app = Flask(__name__)
app.secret_key = 'wsuppersecrettkeys'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    """
    Constructor for Users model

    Attributes:
        username (str): username for a user
        layed_egg (bool): track whether a user lays an egg
        score (int): personal best number of eggs hatched by a user
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    layed_egg = db.Column(db.Boolean, default=False, nullable=False)
    score = db.Column(db.Integer)

    def __init__(self, username):
        self.username = username
        self.layed_egg = False
        self.score = 0

#global variables for classes
the_hatcher = Hatcher()
t = Timer(current_time = 60)

@app.route("/", methods=["GET","POST"])
def login():
    """
    Logs in or creates a new user and continues to /egg_hatcher. Adds user to the session

    POST requests
        1. redirects to /egg_hatcher if it's an existing user
        2. creates a new user and redirects to /egg_hatcer if it's a new user
    
    Args:
        None
    
    Returns:
        The required returns by Flask for the specified redirect/file upload
        behavior for POST requests as described above.
    """
    if request.method == "POST":
        user = request.form["username"]
        session["user"] = user
        existing_user = Users.query.filter_by(username=user).first()
        if existing_user:
            return redirect(url_for("egg_hatcher", user = existing_user.username))
        else:
            new_user = Users(user)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("egg_hatcher", user = new_user.username))
    return render_template("rules.html")


@app.route("/_timer", methods=["GET", "POST"])
def timer():
    """
    Provides timer funciton. Resets the timer and layed egg status when it hits zero

    Args:
        None
    
    Returns:
        JSON response
    """
    new_time = t.decrement()
    if new_time == 0:
        t.__set_time__(60)
        for user in Users.query.all():
            user.layed_egg = False
            db.session.commit()
    return jsonify({"result": new_time})


@app.route('/egg_hatcher', methods=["GET", "POST"])
def egg_hatcher():
    """
    Handles '/egg_hatcher' route. Updates count attribute in hatcher object and layed
    egg status if user lays an egg. Redirects to login if query parameter is empty

    POST requests:
        1. Increments egg count by 1, sets layed egg status to true, and redirects
        to /egg_hatcher if user chooses to lay an egg. Flashes message if egg status
        is already true
        2. redirects to /scores if user chooses to hatch the eggs

    Args:
        None
    
    Returns:
        The required returns by Flask for the specified redirect/file upload
        behavior for POST requests as described above.
    """
    query_dict = request.args
    query = query_dict.get("user")

    if query is None:
        flash("Please login")
        return redirect(url_for("login"))
    
    curr_user = Users.query.filter_by(username=query).first()

    if request.method == "POST":
        name = request.form.get('lay')
        if name is not None:
            if curr_user.layed_egg == False:
                the_hatcher.lay_egg()
                curr_user.layed_egg = True
                db.session.commit()
                return render_template("index.html", layed = curr_user.layed_egg)
            else:
                flash("You've already layed an egg within this minute")
        else:
            return redirect(url_for('handle_scores', user = query))
    return render_template("index.html")


@app.route('/scores', methods=["GET", "POST"])
def handle_scores():
    """
    Handles the /scores route, updating all appropriate scores
    and resets egg count. Redirects to login if query parameter is empty

    POST requests:
        1. redirects to /egg_hatcher if user chooses to play again

    Args:
        None

    Returns:
        The required return by Flask so the user is redirected to the approptiate
        URL
    """
    query_dict = request.args
    query = query_dict.get("user")

    if query is None:
        flash("Please login")
        return redirect(url_for("login"))
    
    curr_user = Users.query.filter_by(username=query).first()

    if request.method == "POST":
        return redirect(url_for("egg_hatcher", user = query))

    user_score = the_hatcher.__len_count__()
    the_hatcher.__set_count__(0)

    if user_score > curr_user.score:
        curr_user.score = user_score

    for user in Users.query.all():
        if user.score > the_hatcher.__len_high_count__():
            if user_score > user.score:
                the_hatcher.__set_high_count__(user_score)
            else:
                the_hatcher.__set_high_count__(user.score)
    high = the_hatcher.__len_high_count__()

    curr_user.layed_egg = False
    db.session.commit()

    return render_template(
        "score.html", 
        score = user_score, 
        pb = curr_user.score, 
        high_score = high)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5000, debug=True)