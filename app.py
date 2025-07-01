from flask import Flask, render_template
from routes.post_routes import post
from routes.login_routes import login
from config import Config
from extension import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(post)
    app.register_blueprint(login)

    @app.route('/')
    def home():
        return render_template('base.html')

    with app.app_context():
        from models.post import Post
        from models.user import User
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)