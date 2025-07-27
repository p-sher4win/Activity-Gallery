from flask import Flask, render_template
from config import Config
from mongoengine import connect
from cloudinary import config as cloud_config
from flask_login import LoginManager
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash


# Initialize Login Manager
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Database connection
    connect(
        db='activity_db',
        host=app.config['MONGO_URI']
    )
    print("connected successfully")

    # Cloudinary API setup
    cloud_config(
        cloud_name=app.config['CLOUD_NAME'],
        api_key=app.config['API_KEY'],
        api_secret=app.config['API_SECRET']
    )

    # Register Blueprint route
    from app.auth import auth
    from app.routes import main
    from app.root import root
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(root, url_prefix='/')

    # Register Admin
    create_admin(app)

    # Setting up Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page!'
    login_manager.login_message_category = 'warning'

    # Import User model
    from .models import User

    # Load User
    @login_manager.user_loader
    def load_user(user_id):
        return User.objects.get(id=ObjectId(user_id))
    
    # Custom Error Pages
    # Not found page
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    # Internal server error page
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template ('500.html'), 500

    return app

# Add Admin User
def create_admin(app):
    with app.app_context():
        from .models import User

        first_user = User.objects.first()

        if first_user:
            if first_user.username != 'admin':
                User.objects.delete() # Delete all users

                admin_user = User(
                    name = 'Admin',
                    username = 'admin',
                    password_hash = generate_password_hash('admin123')
                )
                admin_user.save()
                print("\nAdmin Created!\n")
            else:
                print("\nAdmin Exists!\n")
        else:
            admin_user = User(
                name = 'Admin',
                username = 'admin',
                password_hash = generate_password_hash('admin123')
            )
            admin_user.save()
            print("\nAdmin Created!\n")