import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS

# Import only the simplified eliza blueprint
# Import blueprints
from src.routes.eliza import eliza_bp
from src.routes.user import user_bp
from src.routes.blockchain import blockchain_bp
from src.models.user import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'temp-secret-key-12345')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///xmrt.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Enable CORS for all routes
CORS(app)

# Create tables within app context
with app.app_context():
    db.create_all()

# Register blueprints
app.register_blueprint(eliza_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(blockchain_bp, url_prefix='/api')

@app.route('/')
def health_check():
    return jsonify({
        "status": "Flask Eliza API is running",
        "version": "minimal-v1",
        "endpoints": ["/api/eliza", "/api/eliza/health"]
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
