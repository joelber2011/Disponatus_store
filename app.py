from dotenv import load_dotenv
import os
from app import create_app
from app.auth import auth_bp

load_dotenv()
app = create_app()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)



