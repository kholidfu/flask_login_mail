from flask import Flask
from flask.ext.mail import Mail

mail = Mail()

app = Flask(__name__,
        static_folder="static", # match with your static folder
        static_url_path="/static" # you can change this to anything other than static, its your URL
      )
# set secret key for csrf
app.secret_key = 'development key'

# mail config

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "sopier@gmail.com"
app.config["MAIL_PASSWORD"] = "gm41lv3rt1g0"

mail.init_app(app)


from app import views

# logging tools
# author: https://gist.github.com/mitsuhiko/5659670
# monitor uwsgi access / error :: output di nohup.out

import sys
from logging import Formatter, StreamHandler
handler = StreamHandler(sys.stderr)
handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(handler)
