from flask import Flask
from flask_cors import CORS
from routes.search import search_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(search_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6000)
