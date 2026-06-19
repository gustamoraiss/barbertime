from flask import Flask
from routes.main import main_bp
from routes.scheduling import scheduling_bp
from routes.contact import contact_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

app.register_blueprint(main_bp)
app.register_blueprint(scheduling_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(dashboard_bp)

if __name__ == '__main__':
    app.run(debug=True)