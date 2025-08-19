# wsgi.py — robust entrypoint + ensure DB tables
import traceback

app = None
db = None

try:
    import app as app_module
    if hasattr(app_module, "app"):
        app = app_module.app
    if hasattr(app_module, "db"):
        db = app_module.db
except Exception:
    traceback.print_exc()

if app is None:
    try:
        import app as app_module
        if hasattr(app_module, "application"):
            app = app_module.application
        if hasattr(app_module, "db"):
            db = app_module.db
    except Exception:
        traceback.print_exc()

if app is None:
    try:
        import app as app_module
        if hasattr(app_module, "create_app"):
            app = app_module.create_app()
        if hasattr(app_module, "db"):
            db = app_module.db
    except Exception:
        traceback.print_exc()

# Ensure DB tables on boot when running under gunicorn
if app is not None and db is not None:
    try:
        with app.app_context():
            db.create_all()
    except Exception:
        traceback.print_exc()

if app is None:
    from flask import Flask
    app = Flask(__name__)

    @app.get('/')
    def _boot_error():
        return "WSGI failed to locate your Flask app. Ensure you expose 'app' or 'create_app' in app.py.", 500

# Alias for hosts expecting 'application'
application = app
