from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', pagina_ativa='home')

@app.route('/base')
def base():
    return render_template('base.html', pagina_ativa='base')

@app.route('/contato')
def contato():
    return render_template('contato.html', pagina_ativa='contato')

@app.route('/agendamento')
def agendamento():
    return render_template('agendamento.html')

if __name__ == '__main__':
    app.run(debug=True)