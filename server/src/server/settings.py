def set_routes(self):

    # user interface routes
    self.app.add_url_rule("/", "root", self.root)
    self.app.add_url_rule("/log", "log", self.log, methods=["GET", "POST"])
    self.app.add_url_rule("/reg", "reg", self.reg, methods=["GET", "POST"])
    self.app.add_url_rule("/reg-2", "reg-2", self.reg2, methods=["GET", "POST"])
    self.app.add_url_rule("/rec", "rec", self.rec, methods=["GET", "POST"])
    self.app.add_url_rule("/rec-2", "rec-2", self.rec2, methods=["GET", "POST"])
    self.app.add_url_rule("/mic", "mic", self.mic, methods=["GET", "POST"])
    self.app.add_url_rule("/acerca", "acerca", self.acerca)
    self.app.add_url_rule("/logout", "logout", self.logout)

    # back end routes
    self.app.add_url_rule("/update", "update", self.update, methods=["POST"])

    # redirect route (OAuth2)
    self.app.add_url_rule("/redir", "redir", self.redir, methods=["POST"])


def set_config(self):
    self.app.config["SECRET_KEY"] = "sdlkfjsdlojf3r49tgf8"
    self.app.config["TEMPLATES_AUTO_RELOAD"] = True
