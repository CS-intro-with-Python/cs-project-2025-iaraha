from flask import Flask


app = Flask(__name__)

@app.route("/")
@app.route("/home")
def hello():
    return "Sup dude"

@app.route("/user/<string:n>")
def f(n):
    return "Sup " + n
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)