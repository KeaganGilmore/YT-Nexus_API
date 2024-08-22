from flask import Flask
from flask_cors import CORS
from youtube.routes import youtube_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(youtube_bp, url_prefix='/youtube')

if __name__ == '__main__':
    app.run(debug=True)