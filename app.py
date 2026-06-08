from flask import Flask
from routes.main import main_bp
from routes.scheduling import scheduling_bp

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(scheduling_bp)

if __name__ == '__main__':
    app.run(debug=True)