from flask import Flask
from youtube.views import youtube_bp
from database import create_database
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(youtube_bp, url_prefix='/youtube')

# Enable CORS
CORS(app)

if __name__ == '__main__':
    create_database()
    app.run(debug=True)