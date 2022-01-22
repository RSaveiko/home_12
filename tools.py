import json


def json_read(file):
    with open(file, encoding="utf-8") as file:
        json_data = json.load(file)
        return json_data
