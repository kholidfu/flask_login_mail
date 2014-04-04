# author: @sopier
from flask import render_template, request, redirect, send_from_directory, session, url_for
from flask import make_response # untuk sitemap
from flask import flash
from flask.ext.mail import Message, Mail
from app import app
from forms import ContactForm, SignupForm, SigninForm
import pymongo

c = pymongo.Connection()
db = c['users']


# build mail object
mail = Mail()

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if request.method == "POST":
        if form.validate() == False:
            flash("All fields are required.")
            return render_template("contact.html", form=form)
        else: # all form fields validated
            msg = Message(form.subject.data, sender="sopier@gmail.com", recipients=["kh.fuadi@gmail.com"])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template("contact.html", success=True)
    elif request.method == "GET":
        return render_template("contact.html", form=form)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form  = SignupForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if request.method == "POST":
        if form.validate() == False:
            return render_template("signup.html", form=form)
        else:
            db.user.insert({
                "firsname": form.firstname.data,
                "lastname": form.lastname.data,
                "email": form.email.data,
                "password": form.password.data,
                })
            session['email'] = form.email.data
            return redirect(url_for('profile'))

    elif request.method == "GET":
        return render_template("signup.html", form=form)

@app.route("/profile")
def profile():
    if "email" not in session:
        return redirect(url_for("signin"))

    user = db.user.find_one({"email": session["email"]})

    if user is None:
        return redirect(url_for("signin"))
    else:
        return render_template("profile.html")

@app.route("/signin", methods=["GET", "POST"])
def signin():
    form = SigninForm()

    if 'email' in session:
        return redirect(url_for('profile'))

    if request.method == "POST":
        if form.validate() == False:
            return render_template("signin.html", form=form)
        else:
            session['email'] = form.email.data
            return redirect(url_for('profile'))

    elif request.method == "GET":
        return render_template("signin.html", form=form)

@app.route("/signout")
def signout():
    if "email" not in session:
        return redirect(url_for("signin"))

    session.pop("email", None)
    return redirect(url_for("signup"))
