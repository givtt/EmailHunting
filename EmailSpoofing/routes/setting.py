from flask import Blueprint, request, render_template, url_for
from ..app import EmailServer
from ..apps.before_request import is_user_login
from ..apps.database import Database

setting = Blueprint('setting', __name__)


@setting.route("/", methods=["GET", "POST"])
@is_user_login
def home():
    account_info = EmailServer.config
    if request.method == "POST":
        _type = request.json.get("_type", "")
        if _type != "":
            if _type == "logout":
                Database().re_build()
                EmailServer.config = {}
                EmailServer.load_config()
                EmailServer.turnoff()
                return {
                    "error": False,
                    "redirect": url_for("auth.login")
                }

        else:
            return {
                "error": True,
                "message": ""
            }
    else:
        return render_template("settings.html", account_info=account_info)


@setting.route("/questions/", methods=["GET"])
@setting.route("/questions", methods=["GET"])
def questions():
    return render_template("qs.html")