from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from routes.main import main_bp
from routes.scheduling import scheduling_bp
from routes.contact import contact_bp
from routes.scheduling_menager import limpar_agendamentos_expirados

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(scheduling_bp)
app.register_blueprint(contact_bp)

scheduler = BackgroundScheduler()

scheduler.add_job(limpar_agendamentos_expirados, 'interval', minutes=10)

scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)