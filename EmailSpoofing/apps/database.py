import json
from flask import current_app
import os


class Database:
    def __init__(self):
        self.database_path = os.path.join(current_app.root_path, "database.json")

    def re_build(self):
        data = {
            "account": {
                "email": "",
                "password": "",
                "smtp": "",
                "remember_me": False
            }
        }
        json_data = json.dumps(data, indent=2)
        with open(self.database_path, 'w') as json_file:
            json_file.write(json_data)
            json_file.close()

        return True

    def add_new(self, email, password, smtp, remember_me):
        try:
            with open(self.database_path, 'r+') as json_file:
                try:
                    existing_data = json.load(json_file)
                except json.JSONDecodeError:
                    self.re_build()
                    return self.add_new(email, password, smtp, remember_me)

                new_app = {
                    "email": email,
                    "password": password,
                    "smtp": smtp,
                    "remember_me": remember_me
                }

                existing_data['account'] = new_app

                json_file.seek(0)
                json.dump(existing_data, json_file, indent=2)
                json_file.truncate()

            return True
        except FileNotFoundError:
            return False
        except Exception as e:
            print("An error occurred:", str(e))
            return False

    def get_info(self):
        try:
            with open(self.database_path, 'r+') as json_file:
                existing_data = json.load(json_file)
            json_file.close()
            return existing_data
        except FileNotFoundError:
            return False
        except Exception as e:
            print("An error occurred:", str(e))
            return False
