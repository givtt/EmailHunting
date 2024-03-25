from flask import Blueprint, render_template, request, jsonify, url_for
from ..app import EmailServer
from ..apps.Helper import Helper

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if EmailServer.is_login():
            return jsonify({
                "error": True,
                "message": "انت مسجل دخول بالفعل !"
            })
        else:
            email = Helper().clean_input(request.json.get("email", False))
            password = Helper().clean_input(request.json.get("password", False))
            save_account = Helper().clean_input(request.json.get("remember_me", False))
            if email and password:
                if "@gmail.com" in email:
                    smtp = "gmail"
                else:
                    return jsonify({"error": True, "message": "يمكنك تسجيل الدخول من حسابات Gmail فقط"})

                app = EmailServer.login(
                    email=email,
                    password=password,
                    smtp=smtp,
                    remember_me=save_account
                )
                if app[0] is False:
                    return jsonify({'error': True, "message": app[1]})
                else:
                    return jsonify({
                        "error": False,
                        "message": app[1],
                        "redirect": url_for("main.home", _external=True)
                    })

            else:
                return jsonify({
                    "error": True,
                    "message": "جميع الحقول مطلوبة!"
                })
    else:
        return render_template("login.html")


