import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash

scheduling_bp = Blueprint('scheduling', __name__)

CSV_PATH = "data/agendamentos.csv"

def ler_agendamentos():
    arquivo = open(CSV_PATH, mode='r')
    linhas = arquivo.readlines()
    arquivo.close()

    if len(linhas) > 1:
        return [linha.strip() for linha in linhas[1:] if linha.strip()]
    return []

def validar_agendamento(data, barbeiro, horario, nome, telefone, agendamentos_salvos):

    agora = datetime.datetime.now()
    data_atual = datetime.date.today()
    data_escolhida = datetime.datetime.strptime(data, "%Y-%m-%d").date()
    nome_sem_espacos = nome.replace(" ", "")

    if data_escolhida < data_atual:
        return False, "Não é possível realizar agendamentos em datas passadas."
    
    if data_escolhida == data_atual:
        partes_horario = horario.split(':')
        hora_escolhida = int(partes_horario[0])
        minuto_escolhido = int(partes_horario[1])
        tempo_escolhido = datetime.time(hora_escolhida, minuto_escolhido)
        tempo_atual = agora.time()

        if tempo_escolhido < tempo_atual:
            return False, f"O horário {horario} não está disponível para o dia de hoje."

    if not nome_sem_espacos.isalpha():
        return False, "O nome informado deve conter apenas letras e espaços."

    if len(nome_sem_espacos) < 3:
        return False, "O nome informado deve conter pelo menos 3 caracteres."

    if not telefone.isdigit():
        return False, "O telefone informado deve conter apenas números."

    elif len(telefone) != 11:
        return False, "O telefone informado deve conter 11 dígitos."

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
    arquivo = open(CSV_PATH, mode='a')
    arquivo.write(novo_agendamento)
    arquivo.close()

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

        valido, mensagem = validar_agendamento(data, barbeiro, horario, nome, telefone, agendamentos_salvos)

        if valido:
            salvar_agendamento(servico, data, barbeiro, horario, nome, telefone)
            flash("Agendamento realizado com sucesso!", "success")
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash(mensagem, "error")
            return render_template('agendamento.html')

    return render_template('agendamento.html')