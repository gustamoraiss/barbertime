from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from routes.main import main_bp
from routes.scheduling import scheduling_bp
from routes.contact import contact_bp
from routes.dashboard import dashboard_bp

app = Flask(__name__)
app.secret_key = 'chave_secreta_aqui'

app.register_blueprint(main_bp)
app.register_blueprint(scheduling_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(dashboard_bp)

scheduler = BackgroundScheduler()

scheduler.add_job(limpar_agendamentos_expirados, 'interval', minutes=10)

scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)