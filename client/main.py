import requests
import logging

from src.updates import gather_all

# reduce Flask output to command line
logging.getLogger("werkzeug").disabled = True


class Dash:

    def logging(self, *args, **kwargs):
        pass


def main():

    import pprint

    url = "http://192.168.68.105:5000/update"
    _json = {"token": "token", "instruction": "get_records_to_update"}

    g = requests.post(url=url, json=_json)
    pprint.pprint(g.json())

    dash = Dash()
    x = gather_all.gather_threads(dash=dash, all_updates=g.json())
    pprint.pprint(x)


if __name__ == "__main__":
    main()
