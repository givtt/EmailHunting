import smtplib
from ..apps.database import Database
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
from email.message import EmailMessage


class EmailService:
    def __init__(self):
        self.server = None
        self.config = {}

    def turnoff(self):
        return self.server.quit()

    def is_login(self):
        try:
            status = self.server.noop()[0]
        except:
            status = -1
        return True if status == 250 else False

    def re_login(self):
        if self.config["account"]["remember_me"] is True:
            app = self.login(
                email=self.config["account"]["email"],
                password=self.config["account"]["password"],
                smtp=self.config["account"]["smtp"],
                remember_me=self.config["account"]["remember_me"]
            )
            if app[0] is True:
                return True
            else:
                return False

    def login(self, email, password, smtp, remember_me):
        if smtp == "gmail":
            self.server = smtplib.SMTP('smtp.gmail.com:587')
            self.server.starttls()
            try:
                self.server.login(email, password)
                Database().add_new(
                    email=email,
                    password=password,
                    smtp=smtp,
                    remember_me=remember_me
                )
                self.load_config()
                return [True, "نجح تسجيل الدخول"]

            except smtplib.SMTPAuthenticationError as e:
                self.turnoff()
                error_message = e.smtp_error.decode('utf-8') if hasattr(e, 'smtp_error') else str(e)
                return [False, error_message]

            except Exception as e:
                return [False, str(e)]

    def load_config(self):
        try:
            data = Database().get_info()["account"]

            if data["email"] != "":
                self.config["account"] = data
            else:
                self.config["account"] = {
                    "email": "",
                    "password": "",
                    "smtp": "",
                    "remember_me": False
                }
        except Exception as e:
            self.config["account"] = {
                "email": "",
                "password": "",
                "smtp": "",
                "remember_me": False
            }
            print(e)
            return False

    def send_message(self, target, subject, _from, _message):
        try:
            message = MIMEMultipart()
            message['From'] = _from
            message['To'] = target
            message['Subject'] = subject
            message.attach(MIMEText(_message, 'plain'))
            self.server.sendmail(self.config["account"]["email"], target, message.as_string())
            return [True, "200"]
        except Exception as e:
            return [False, str(e)]

    def build_indexes(self, _index, _username, _email, _link):
        if _index == "epic_games_1":
            return {
                "payload": str(render_template("indexes/epic_games_rest_password.html", _username=_username, _link=_link)),
                "From": "Epic Games",
                "subject": "Rest Your Password"
            }
        elif _index == "instagram_password_changed":
            return {
                "payload": str(render_template("indexes/instagram_password_changed.html", _username=_username, _link=_link, _email=_email)),
                "From": "Instagram",
                "subject": "Your Instagram password has been changed"
            }
        elif _index == "facebook_password_changed":
            return {
                "payload": str(render_template("indexes/facebook_changed_password.html", _username=_username, _link=_link, _email=_email)),
                "From": "FaceBook",
                "subject": "هل قمت بإعادة تعيين كلمة السر الخاصة بك؟"
            }
        elif _index == "gmail_login_detect":
            return {
                "payload": str(render_template("indexes/gmail_login_detect.html", _link=_link, _email=_email)),
                "From": "Google Security",
                "subject": "تنبيه أمني"
            }
        elif _index == "netflix_changed_password":
            return {
                "payload": str(render_template("indexes/netflix_changed_password.html", _link=_link, _email=_email)),
                "From": "Netflix <info@account.netflix.com>",
                "subject": "لقد تمّ تغيير كلمة المرور الخاصة بك."
            }
        elif _index == "twitter_changed_password":
            return {
                "payload": str(render_template("indexes/twitter_login_detect.html", _link=_link, _email=_email, _username=_username)),
                "From": "Twitter verify@x.com",
                "subject": "New login to Twitter on iPhone"
            }

    def send_html(self, target, subject, _from, _message):
        try:
            Massage = EmailMessage()
            Massage['subject'] = subject
            Massage['from'] = _from
            Massage['to'] = target
            Massage.add_alternative(_message, subtype='html')
            self.server.send_message(Massage)
            return [True, "200"]
        except Exception as e:
            return [False, str(e)]

    def check_email_existence(self, target_email):
        try:
            with smtplib.SMTP("gmail-smtp-in.l.google.com") as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.mail("ValidEmail@all-nettools.com")
                response = server.rcpt(target_email)

                if response[0] == 250:
                    return {"error": False, "exist": True}
                elif response[0] == 550:
                    return {"error": False, "exist": False}
                else:
                    return {"error": True, "exist": False, "message": "something wrong"}

        except smtplib.SMTPException as e:
            return {"error": False, "exist": False, "message": str(e)}