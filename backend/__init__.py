import os
from flask import Flask
from dotenv import load_dotenv, find_dotenv
from flask_talisman import Talisman

CONFIG_NAME_MAPPER = {
    "development": "config.DevelopmentConfig",
    "test": "config.TestConfig",
    "production": "config.ProductionConfig"
}


def create_app(flask_env=None):
    app = Flask(
        __name__,
        template_folder="../frontend/dist/html",
        static_folder="../frontend/dist",
        static_url_path="/frontend/dist"
    )

    # WILL FIND A BETTER WAY TO ONLY EXECUTE INLINE SCRIPT FOR /API ENDPOINTS
    SELF = "\'self\'"
    csp = {
        "default-src": [
            SELF,
            "\'unsafe-inline\'"  # ONLY TO SHOW SWAGGER UI INTERFACE
        ],
        "script-src": [
            SELF,
            "\'unsafe-inline\'"  # ONLY TO SHOW SWAGGER UI INTERFACE
        ],
        "connect-src": SELF,
        "style-src": [
            SELF,
            "*.googleapis.com",
            "\'unsafe-inline\'"
        ],
        "font-src": [
            SELF,
            "data:",
            "*.googleapis.com",
            "*.gstatic.com"
        ],
        "img-src": [
            "*",
            "data:"
        ],
        "media-src": [
            "*"
        ],
        "frame-src": "\'none\'",
        "worker-src": "\'none\'"
    }

    Talisman(app, content_security_policy=csp)
    load_dotenv(find_dotenv())

    envvar_flask_env = os.getenv("FLASK_ENV")
    if not envvar_flask_env and flask_env is None:
        raise SystemExit("Either flask_config or environment variable FLASK_ENV are unset.")
    elif flask_env is None:
        flask_env = envvar_flask_env
    else:
        if envvar_flask_env and envvar_flask_env != flask_env:
            raise SystemExit("Flask_env and environment variable FLASK_ENV are different.")

    try:
        app.config.from_object(CONFIG_NAME_MAPPER[flask_env])
    except KeyError:
        raise SystemExit(
            "Invalid flask_config. Create_app argument or set FLASK_ENV environment "
            "variable must be one of the following options: development, test or production."
        )

    from backend.dao.postgres_db import init_db, DBSession
    init_db()

    from backend.controller.auth import login_manager
    login_manager.init_app(app)

    from backend.controller.api import bpapi
    app.register_blueprint(bpapi, url_prefix="/api")

    from backend.controller.auth import bpauth, bplogin
    app.register_blueprint(bpauth, url_prefix="/auth")
    app.register_blueprint(bplogin, url_prefix="/auth")

    from backend.controller.frontend import bpfrontend
    app.register_blueprint(bpfrontend)

    @app.teardown_request
    def teardown_request(e):
        DBSession.remove()

    return app
