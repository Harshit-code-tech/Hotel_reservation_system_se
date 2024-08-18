from flask import Flask, session, render_template
from pymongo import MongoClient
from config import Config
from hotel_reservation_system.routes import bp

def create_app():
    # Initialize Flask application
    app = Flask(__name__)
    app.secret_key = 'chang'  # Set a unique and secret key

    # Register the blueprint
    app.register_blueprint(bp)
    app.config.from_object(Config)

    # Initialize MongoDB client
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client[app.config['MONGO_DB']]

    # Error handling pages
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)