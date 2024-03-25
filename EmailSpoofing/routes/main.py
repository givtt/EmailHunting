from flask import Blueprint, render_template, request, jsonify
from ..apps.before_request import is_user_login
from ..app import EmailServer


main = Blueprint("main", __name__)


@main.route('/gmail/password', methods=["GET"])
@main.route('/gmail/password/', methods=["GET"])
def how_get_password():
    return render_template("get_password.html")


@main.route("/", methods=["GET"])
@is_user_login
def home():
    return render_template("home.html")


@main.route("/send/fake_template", methods=["GET", "POST"])
@main.route("/send/fake_template/", methods=["GET", "POST"])
@is_user_login
def send_fake_template():
    email_info = EmailServer.config["account"]
    if request.method == "POST":
        TargetEmail = request.json.get("TargetEmail", False)
        TargetUsername = request.json.get("TargetUsername", False)
        HackLink = request.json.get("HackLink", False)
        Template = request.json.get("Template", False)

        payload = EmailServer.build_indexes(
            _index=Template,
            _email=TargetEmail,
            _username=TargetUsername,
            _link=HackLink
        )

        app = EmailServer.send_html(
            target=TargetEmail,
            subject=payload["subject"],
            _from=payload["From"],
            _message=payload["payload"]
        )

        if app[0]:
            return {"error": False, "message": "تم ارسال الرسالة بنجاح"}
        else:
            return {"error": True, "message": app[1]}
    else:
        return render_template("tools/fake_template.html", email=email_info["email"])


@main.route("/send/fake_template/show", methods=["PUT"])
@main.route("/send/fake_template/show/", methods=["PUT"])
def show_the_fake_template():
    TargetEmail = request.json.get("TargetEmail", False)
    TargetUsername = request.json.get("TargetUsername", False)
    HackLink = request.json.get("HackLink", False)
    Template = request.json.get("Template", False)

    if TargetEmail and TargetUsername and HackLink and Template:
        app = EmailServer.build_indexes(
            _email=TargetEmail,
            _username=TargetUsername,
            _link=HackLink,
            _index=Template
        )
        return {
            "error": False,
            "message": "",
            "template": app["payload"]
        }

    return {"error": True, "message": "method not allowed"}

@main.route("/send/simple", methods=["GET", "POST"])
@main.route("/send/simple/", methods=["GET", "POST"])
@is_user_login
def send_simple_message():
    email_info = EmailServer.config["account"]
    if request.method == "POST":
        FromName = request.json.get("FromName", False)
        TargetEmail = request.json.get("TargetEmail", False)
        Subject = request.json.get("Subject", False)
        Message = request.json.get("Message", False)

        if not FromName:
            FromName = email_info["email"]

        if not TargetEmail:
            return jsonify({
                "error": True,
                "message": "الرجاء ادخال البريد الخاص بالضحية"
            })

        if not Subject:
            Subject = "Message From ", email_info["email"]

        if len(Message.strip()) <= 2:
            return jsonify({
                "error": True,
                "message": "يجب تضمين رسالة لأرسالها"
            })

        send = EmailServer.send_message(
            target=TargetEmail,
            subject=Subject,
            _from=FromName,
            _message=Message
        )

        if send[0] is True:
            return {"error": False, "message": "تم ارسال الرسالة بنجاح"}
        else:
            return {"error": False, "message": send[1]}

    else:
        return render_template("tools/simple_message.html", email=email_info["email"])


@main.route("/email/check", methods=["GET", "POST"])
@main.route("/email/check/", methods=["GET", "POST"])
def email_check():
    if request.method == "POST":
        email = request.json.get("email", "")
        if email != "":
            app = EmailServer.check_email_existence(target_email=email)
            return app
        else:
            return {
                "error": True,
                "message": "empty args"
            }
    else:
        return render_template("tools/emails_check.html")


