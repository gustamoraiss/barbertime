from flask import Flask
from routes.main import main_bp
from routes.scheduling import scheduling_bp
from routes.contact import contact_bp

app = Flask(__name__)

app.register_blueprint(main_bp)
app.register_blueprint(scheduling_bp)
app.register_blueprint(contact_bp)

@app.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')

if __name__ == '__main__':
    app.run(debug=True)