from flask import Flask
from youtube.routes import youtube_bp
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(youtube_bp, url_prefix='/youtube')

# Enable CORS
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)