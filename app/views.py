# author: @sopier
from flask import render_template, request, redirect, send_from_directory
from flask import make_response # untuk sitemap
from flask import flash
from flask.ext.mail import Message, Mail
from app import app
from forms import ContactForm

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
