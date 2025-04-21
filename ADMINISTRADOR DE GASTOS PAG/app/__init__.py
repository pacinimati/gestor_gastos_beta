from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)  # Asegúrate de que esto esté presente
    migrate.init_app(app, db)
    login.init_app(app)
    login.login_view = 'login'

    # Definir el user_loader
    from app.models import Usuario
    @login.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Importar rutas y modelos
    with app.app_context():
        from app import routes, models

    return app