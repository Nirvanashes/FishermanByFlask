from flask import Flask
from app.extensions import init_extensions, db
from config import Config
from app.routes.project_routes import pj_bp
from app.routes.auth_routes import auth_bp

app = Flask(__name__,template_folder="app/templates")
app.config.from_object(Config)
init_extensions(app)
with app.app_context():
    db.create_all()

app.register_blueprint(auth_bp)
app.register_blueprint(pj_bp)

if __name__ == "__main__":
    app.run(debug=True,port=5003)
