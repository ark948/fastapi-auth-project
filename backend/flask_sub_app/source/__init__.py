from flask import Flask

def create_app():
    app = Flask(__name__)

    @app.route('/hello')
    def hello():
        return 'hello world from flask'
    
    @app.route('/register')
    def register():
        return 'register page'
    
    return app