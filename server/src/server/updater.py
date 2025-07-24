from datetime import datetime as dt
from datetime import timedelta as td
from flask import request, jsonify

from src.updates import get_records_to_update


def update(self):

    post = request.json

    if post["token"] != "token":
        print("Authentication Error")
        return "Auth Error!"

    if post["instruction"] == "get_records_to_update":
        return jsonify(get_records_to_update.get_records(self.db.cursor))

    if post["instruction"] == "do_updates":
        print("Do Update!")
        return "Do Update!"
