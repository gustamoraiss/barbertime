from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from routes.main import main_bp
from routes.scheduling import scheduling_bp
from routes.contact import contact_bp

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(scheduling_bp)
app.register_blueprint(contact_bp)

def rotina_temporaria():
    pass

scheduler = BackgroundScheduler()

scheduler.add_job(rotina_temporaria, 'interval', minutes=15, id='limpeza_csv_job')

scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)