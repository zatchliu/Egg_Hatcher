from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(port=5000, debug=True)

"""
class User:
    username
    email
    password
    egg_count

class Hatcher
    current_count

    def lay_egg:

    def hatch_eggs:
"""