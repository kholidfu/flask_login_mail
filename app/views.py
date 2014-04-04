# author: @sopier

from flask import render_template, request, redirect, send_from_directory
from flask import make_response # untuk sitemap
from app import app
# untuk find_one based on data id => db.freewaredata.find_one({'_id': ObjectId(file_id)})
# atom feed
from werkzeug.contrib.atom import AtomFeed
from bson.objectid import ObjectId
from filters import slugify, splitter, onlychars, get_first_part, get_last_part, formattime, cleanurl
from forms import ContactForm
from flask import flash
import datetime
from flask.ext.mail import Message, Mail

mail = Mail()

@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()

    if request.method == "POST":
        if form.validate() == False:
            flash("All fields are required.")
            return render_template("contact.html", form=form)
        else:
            # all form fields validated
            msg = Message(form.subject.data, sender="sopier@gmail.com", recipients=["kh.fuadi@gmail.com"])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template("contact.html", success=True)
    elif request.method == "GET":
        return render_template("contact.html", form=form)
