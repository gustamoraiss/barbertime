import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash

scheduling_bp = Blueprint('scheduling', __name__)

CSV_PATH = "data/agendamentos.csv"

DURACAO_SERVICOS = {
    "Corte Tradicional": 40,
    "Barba Completa": 30,
    "Combo Premium": 60,
    "Corte Infantil": 30,
    "Pigmentação": 45,
    "Design de Sobrancelha": 20
}

def ler_agendamentos():
    arquivo = open(CSV_PATH, mode='r')
    linhas = arquivo.readlines()
    arquivo.close()

    if len(linhas) > 1:
        return [linha.strip() for linha in linhas[1:] if linha.strip()]
    return []

def validar_agendamento(servico, data, barbeiro, horario, nome, telefone, agendamentos_salvos):
    if len(data) != 10:
        return False, "Formato de data inválido."

    agora = datetime.datetime.now()
    data_atual = agora.date()
    data_escolhida = datetime.datetime.strptime(data, "%Y-%m-%d").date()
    nome_sem_espacos = nome.replace(" ", "")

    if data_escolhida < data_atual:
        return False, "Não é possível realizar agendamentos em datas passadas."
    
    partes_horario = horario.split(':')
    hora_escolhida = int(partes_horario[0])
    minuto_escolhido = int(partes_horario[1])
    
    inicio_novo = datetime.datetime.combine(data_escolhida, datetime.time(hora_escolhida, minuto_escolhido))

    if data_escolhida == data_atual:
        if inicio_novo.time() < agora.time():
            return False, f"O horário {horario} não está disponível para o dia de hoje."

    if not nome_sem_espacos.isalpha():
        return False, "O nome informado deve conter apenas letras e espaços."

    if len(nome_sem_espacos) < 3:
        return False, "O nome informado deve conter pelo menos 3 caracteres."

    if not telefone.isdigit():
        return False, "O telefone informado deve conter apenas números."

    elif len(telefone) != 11:
        return False, "O telefone informado deve conter 11 dígitos."

    if servico in DURACAO_SERVICOS:
        duracao_novo_minutos = DURACAO_SERVICOS[servico]
        
    fim_novo = inicio_novo + datetime.timedelta(minutes=duracao_novo_minutos)

    for linha in agendamentos_salvos:
        dados_linha = linha.split(',')

        if len(dados_linha) >= 6:
            servico_salvo = dados_linha[0].strip()
            data_salva = dados_linha[1].strip()
            barbeiro_salvo = dados_linha[2].strip()
            horario_salva_str = dados_linha[3].strip()

            if barbeiro_salvo == barbeiro and data_salva == data:
                if servico_salvo in DURACAO_SERVICOS:
                    duracao_salvo_minutos = DURACAO_SERVICOS[servico_salvo]

                partes_salvo = horario_salva_str.split(':')
                inicio_salvo = datetime.datetime.combine(data_escolhida, datetime.time(int(partes_salvo[0]), int(partes_salvo[1])))
                fim_salvo = inicio_salvo + datetime.timedelta(minutes=duracao_salvo_minutos)

                if inicio_novo < fim_salvo and fim_novo > inicio_salvo:
                    return False, f"Este barbeiro estará ocupado das {inicio_salvo.strftime('%H:%M')} até as {fim_salvo.strftime('%H:%M')} atendendo um cliente de '{servico_salvo}'."

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

        valido, mensagem = validar_agendamento(servico, data, barbeiro, horario, nome, telefone, agendamentos_salvos)

        if valido:
            salvar_agendamento(servico, data, barbeiro, horario, nome, telefone)
            flash("Agendamento realizado com sucesso!", "success")
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash(mensagem, "error")
            return render_template('agendamento.html')

    return render_template('agendamento.html')