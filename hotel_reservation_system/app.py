from flask import Flask
from pymongo import MongoClient
from config import Config

def create_app():
    # Initialize Flask application
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize MongoDB client
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client[app.config['MONGO_DB']]

    # Register blueprints
    from routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
