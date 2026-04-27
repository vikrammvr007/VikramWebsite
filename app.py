import os
from flask import Flask
from config import SECRET_KEY
from routes.public import public_bp
from routes.admin import admin_bp

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register blueprints
app.register_blueprint(public_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_ENV") != "production"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
