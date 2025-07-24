from flask import Flask, request, session
import threading
import os

# local imports
from src.server.validation import FormValidate
from src.utils.utils import get_local_ip
from src.utils.constants import NETWORK_PATH
from src.server import settings, ui, oauth, updater


class Server:

    def __init__(self, db):

        self.db = db
        self.validacion = FormValidate(db=self.db)
        self.data_lock = threading.Lock()

        # initialize Flask app object, set configuration and define routes
        self.app = Flask(
            __name__,
            template_folder=os.path.join(NETWORK_PATH, "templates"),
            static_folder=os.path.join(NETWORK_PATH, "static"),
        )
        self.session = session

        # set app configurations
        settings.set_config(self)

        # define endpoints
        settings.set_routes(self)

    # starting server
    def run(self):
        print(f" > SERVER RUNNING ON: http://{get_local_ip()}:5000")
        self.app.run(
            debug=False,
            threaded=True,
            port=5000,
            host="0.0.0.0",
        )

    def run_in_background(self):
        flask_thread = threading.Thread(target=self.run, daemon=True)
        flask_thread.start()
        return flask_thread

    # FRONT END ENDPOINTS
    # root endpoint
    def root(self):
        return ui.root(self)

    # login endpoint
    def log(self):
        return ui.log(self)

    # registration endpoints
    def reg(self):
        return ui.reg(self)

    def reg2(self):
        return ui.reg2(self)

    # password recovery endpoints
    def rec(self):
        return ui.rec(self)

    def rec2(self):
        return ui.rec2(self)

    # dashboard endpoints
    def reportes(self):
        return ui.reportes(self)

    # mi cuenta endpoint (NAVBAR)
    def mic(self):
        return ui.mic(self)

    # "acerca de" endpoint (NAVBAR)
    def acerca(self):
        return ui.acerca(self)

    # logout endpoint (NAVBAR)
    def logout(self):
        return ui.logout(self)

    # BACKEND ENDPOINTS
    # receive request to determine records to update and updated records
    def update(self):
        return updater.update(self)

    # redirect endpoint (OAuth)
    def redir(self):
        self.all_params = request.args.to_dict()
        oauth.get_oauth2_token(self)
