from app.extensions import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.routes import main


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # db = SQLAlchemy(app)
    db.init_app(app)

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app

# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=False)
