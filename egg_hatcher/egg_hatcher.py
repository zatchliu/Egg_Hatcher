from flask import Flask, flash, render_template, request, url_for, redirect, jsonify
from werkzeug.utils import secure_filename

import time

app = Flask(__name__)
app.secret_key = 'wsuppersecrettkeys'

class Timer:
    def __init__(self, current_time):
        self.current_time = current_time

    def decrement(self):
        if self.current_time > 0:
            self.current_time = self.current_time - 1
        #time.sleep(1)
        return self.current_time

    def __get_time__(self):
        return self.current_time


t = Timer(current_time=60)

class Hatcher:

    def __init__(self):
        """
        Constructor for Hatcher class

        Attributes"

            count (int): the current number of eggs in the hatcher
            high_count (int): the highest number of eggs that have been in the hatcher
            layed_egg (bool): boolean to keep track whether player hatched an egg within the minute

        """
        self.count = 0 
        self.high_count = 0
        self.layed_egg = False

    def __len__(self):
        """
        The number of eggs currently in the hatcher

        Returns:
            count (int): number of eggs
        """
        return self.count
    
    def lay_egg(self):
        """
        increases egg count by one

        Returns:
            None
        """
        self.count += 1

the_hatcher = Hatcher()


@app.route("/_timer", methods=["GET", "POST"])
def timer():
    new_time = t.decrement()
    if new_time == 0:
        the_hatcher.layed_egg = False
        t.current_time = 60
    return jsonify({"result": new_time})


@app.route('/', methods=["GET", "POST"])
def home():
    """
    Handles '/' route and updates count attribute in hatcher object if user
    lays an egg

    Args:
        None
    Returns:
        The required return by Flask so the user is redirected to the '/'
        URL
    """
    if request.method == "POST":
        if the_hatcher.layed_egg == False:
            the_hatcher.lay_egg()
            the_hatcher.layed_egg = True
        else:
            flash("You've already layed an egg within this minute")
    return render_template("index.html")


@app.route('/scores')
def handle_scores():
    """
    Handles the /scores route, updating all appropriate scores
    and resets hatcher function

    Args:
        None

    Returns:
        The required return by Flask so the user is redirected to the /scores
        URL
    """
    user_score = the_hatcher.__len__()
    the_hatcher.count = 0
    if user_score > the_hatcher.high_count:
        the_hatcher.high_count = user_score
    high = the_hatcher.high_count
    the_hatcher.layed_egg = False
    t.current_time = 60
    return render_template("score.html", score = str(user_score), high_score = high)


if __name__ == "__main__":
    app.run(port=5000, debug=True)