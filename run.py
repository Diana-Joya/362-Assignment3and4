from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", name=user))
    else:
        return render_template("index.html", restaurant_name="Restaurant Services App", page_name="Home Page", state="hm")


@app.route("/<name>")
def user(name):
    return render_template("home.html", restaurant_name=name, page_name="Home Page", state="usr")


@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))


@app.route("/signup")
def signup():
    return render_template("signup.html", restaurant_name="Restaurant Services App", page_name="Sign Up", state="su")


if __name__ == "__main__":
    app.run(debug=True)