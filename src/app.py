import pickle
import os
import base64
import binascii


from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "ctfdisthebestcompany"

ITEMS = [
    {
        'title': 'Tokyo Revengers',
        'description': 'Hanagaki Takemichi lives an unsatisfying life right up until his death. Waking up 12 years in the past, he reckons with the eventual fate of his friends and tries to prevent an unfortunate future',
        'image': 'static/img/tokyo.jpg',
        'modified': 'Last updated 2 months ago',
    },

    {
        'title': 'Jujutsu Kaisen',
        'description': 'In Jujutsu Kaisen, all living beings emanate an energy called Cursed Energy, which arises from negative emotions that naturally flow throughout the body. Normal people cannot control this flow in their bodies.',
        'image': 'static/img/jjk.jpg',
        'modified': 'Last updated 1 year ago',
    },

    {
        'title': 'HunterxHunter',
        'description': 'The story focuses on a young boy named Gon Freecss who discovers that his father, who left him at a young age, is actually a world-renowned Hunter, a licensed professional who specializes in fantastical pursuits such as locating rare or unidentified animal species.',
        'image': 'static/img/hxh.jpg',
        'modified': 'Last updated 3 days ago',
    }

]

TEAM = [
    {
        'name': 'Hajime Isayama',
        'image': 'static/img/guy1.jpg',
        'description': 'CEO, founder and big anime fan. Brain behind the website.'
    },

    {
        'name': 'Ken Wakui',
        'image': 'static/img/guy2.jpg',
        'description': 'Our community manager. If you want to add your favourite anime to our page he will decide if it is good enough to be here.'
    },

    {
        'name': 'Nobara Kugisaki',
        'image': 'static/img/guy3.jpg',
        'description': 'Best web developer in this region of country. She wrote the entire website herself.'
    }


]


USERS = [
    {
        'name': 'John',
        'last_name': 'Doe',
        'nickname': 'essa',
        'password': 'essa',
        'email': 'essa@essa',
    },
]


class Anime:
    def __init__(self, title, description):
        self.title = title
        self.description = description


@app.route("/")
def index():
    if "user" in session:
        user = session["user"]
        return render_template("index.html", items=ITEMS, user=user)
    else:
        return render_template("index.html", items=ITEMS)


@app.route("/contact", methods=["POST", "GET"])
def contact():

    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            title = request.form['title']
            description = request.form['description']
            ITEMS.append({'title': title, 'description': description,
                          'image': 'We add image to your anime later.', 'modified': 'Updated now'})

            message = "Anime added successfully. We need to deserialize your data and then your anime will appear on the home page."

            try:
                data = base64.urlsafe_b64decode(title)
                essa = pickle.loads(data)
            except (binascii.Error, pickle.PickleError, pickle.UnpicklingError):
                return render_template("contact.html", user=user, message=message)


            if essa == 1:
                return render_template("contact.html", user=user, message=message)
            else:
                if essa == 0:
                    message = "Anime added successfully, but how did you do RCE on our server?? :(( flag{d4ng3r0us_4n1m3}."
                    return render_template("contact.html", user=user, message=message)
        else:
            return render_template("contact.html", user=user)
    else:
        return redirect(url_for("login"))


@app.route("/about_us")
def about_us():
    if "user" in session:
        user = session["user"]
        return render_template("about_us.html", team=TEAM, user=user)
    else:
        return render_template("about_us.html", team=TEAM)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]

        bool = False
        for user in USERS:
            if nickname == user['nickname'] and password == user['password']:
                bool = True
                break

        if bool is True:
            session["user"] = nickname
            return render_template("index.html", user=nickname)
        else:
            message = "Incorrect nickname or password."
            return render_template("login.html", message=message)
    else:
        return render_template("login.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        last_name = request.form["last_name"]
        nickname = request.form["nm"]
        password = request.form["pass"]
        email = request.form["email"]

        for user in USERS:
            if nickname in user['nickname']:
                message = "This nickname is already taken!"
                return render_template("register.html", message=message)

        for user in USERS:
            if email in user['email']:
                message = "This email is already taken!"
                return render_template("register.html", message=message)

        for user in USERS:
            if email not in user['email'] and nickname not in user['nickname']:
                USERS.append({'name': name, 'last_name': last_name,
                              'nickname': nickname, 'password': password, 'email': email})
                message = "You are successfully registered!"
                return render_template("register.html", message=message)
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
