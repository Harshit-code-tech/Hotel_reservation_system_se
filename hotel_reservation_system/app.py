from flask import Flask, render_template
from pymongo import MongoClient
from config import Config
from hotel_reservation_system.routes import bp
from flask_mail import Mail
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()  # Load environment variables from .env file
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY', '59a4ecd754c57833ffe61c94a568a390')  # Set a unique and secret key

    # Register the blueprint
    app.register_blueprint(bp)
    app.config.from_object(Config)

    # Initialize MongoDB client
    client = MongoClient(app.config['MONGO_URI'])
    app.db = client[app.config['MONGO_DB']]

    # Setup Flask-Mail
    mail = Mail(app)  # Initialize Mail with the app

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
