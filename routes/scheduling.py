import datetime
from flask import Blueprint, render_template, request, redirect, url_for

scheduling_bp = Blueprint('scheduling', __name__)

CSV_PATH = "data/agendamentos.csv"

def ler_agendamentos():
    linhas = []
    try:
        with open(CSV_PATH, 'r') as arquivo:

            linhas = arquivo.readlines()
            linhas_limpas = [linha.strip() for linha in linhas]
            
            return linhas_limpas
        
    except FileNotFoundError:
        return []

def validar_agendamento(data, barbeiro, horario, agendamentos_salvos):

    data_atual = datetime.date.today()
    data_escolhida = datetime.datetime.strptime(data, "%Y-%m-%d").date()

    if data_escolhida < data_atual:
        return False, "Não é possível realizar agendamentos em datas passadas."

    for linha in agendamentos_salvos:
        dados_linha = linha.split(',')
        
        if len(dados_linha) >= 4:
            data_salva = dados_linha[1]
            barbeiro_salvo = dados_linha[2]
            horario_salvo = dados_linha[3]

            if barbeiro_salvo == barbeiro and data_salva == data and horario_salvo == horario:
                return False, "Este barbeiro já possui um agendamento neste dia e horário."

    return True, "Horário disponível!"

def salvar_agendamento(servico, data, barbeiro, horario, nome, telefone):
    novo_agendamento = f"{servico},{data},{barbeiro},{horario},{nome},{telefone}\n"
    
    with open(CSV_PATH, mode='a') as arquivo:
        arquivo.write(novo_agendamento)

@scheduling_bp.route('/agendar', methods=['GET', 'POST'])
def agendamento():
    if request.method == 'POST':
        
        servico = request.form.get('servico')
        data = request.form.get('data')
        barbeiro = request.form.get('barbeiro')
        horario = request.form.get('horario')
        nome = request.form.get('nome_cliente')
        telefone = request.form.get('telefone_cliente')
        
        agendamentos_salvos = ler_agendamentos()
        
        valido, mensagem = validar_agendamento(data, barbeiro, horario, agendamentos_salvos)
        
        if valido:
            salvar_agendamento(servico, data, barbeiro, horario, nome, telefone)
            return redirect(url_for('main.home'))
        else:
            return render_template('agendamento.html', erro=mensagem)
        
    return render_template('agendamento.html')