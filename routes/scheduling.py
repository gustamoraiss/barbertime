from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

scheduling_bp = Blueprint('scheduling', __name__)

CSV_PATH = "data/agendamentos.csv"

SERVICOS = [
    {"id": 1, "nome": "Corte Tradicional"},
    {"id": 2, "nome": "Barba Completa"},
    {"id": 3, "nome": "Cabelo e Barba"}
]
BARBEIROS = [
    {"id": 1, "nome": "Carlos Silva"},
    {"id": 2, "nome": "Pedro Santos"}
]

def ler_agendamentos():
    linhas = []
    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            linhas_limpas = [linha.strip() for linha in linhas]
            return linhas_limpas
    except FileNotFoundError:
        return []

def validar_agendamento(data, barbeiro, horario, nome, telefone, agendamentos_salvos):
    if not nome or len(nome.strip()) < 3:
        return False, "Por favor, digite um nome válido (mínimo de 3 caracteres)."
        
    if not telefone or len(telefone.strip()) == 0:
        return False, "Por favor, insira um número de telefone."
    
    telefone_analise = telefone.replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
    
    if not telefone_analise.isdigit():
        return False, "O telefone deve conter apenas números (letras não são permitidas)."
        
    if len(telefone_analise) != 11:
        return False, "O número de telefone deve conter 11 dígitos numéricos."

    try:
        agora = datetime.now()
        data_atual = agora.date()
        data_escolhida = datetime.strptime(data, "%Y-%m-%d").date()
        
        if data_escolhida < data_atual:
            return False, "Você não pode selecionar uma data que já passou."
            
        if data_escolhida == data_atual:
            horario_escolhido = datetime.strptime(horario, "%H:%M").time()
            horario_atual = agora.time()
            
            if horario_escolhido < horario_atual:
                return False, f"O horário {horario} não está disponível para o dia de hoje."
                
    except (ValueError, TypeError):
        return False, "Data ou horário inválidos selecionados."

    for linha in agendamentos_salvos:
        if not linha:
            continue
        dados_linha = [d.strip() for d in linha.split(',')]
        
        if len(dados_linha) >= 4:
            data_salva = dados_linha[1]
            barbeiro_salvo = dados_linha[2]
            horario_salvo = dados_linha[3]

            if barbeiro_salvo == barbeiro and data_salva == data and horario_salvo == horario:
                return False, "Este barbeiro já possui um agendamento neste dia e horário."

    return True, "Horário disponível!"

def salvar_agendamento(servico, data, barbeiro, horario, nome, telefone):
    novo_agendamento = f"{servico},{data},{barbeiro},{horario},{nome},{telefone}\n"
    with open(CSV_PATH, mode='a', encoding='utf-8') as arquivo:
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
        
        # CORREÇÃO AQUI: Passando as variáveis 'nome' e 'telefone' que faltavam!
        valido, mensagem = validar_agendamento(data, barbeiro, horario, nome, telefone, agendamentos_salvos)
        
        if valido:
            salvar_agendamento(servico, data, barbeiro, horario, nome, telefone)
            flash("Agendamento realizado com sucesso!", "success")
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash(mensagem, "error")
            return render_template('agendamento.html', servicos=SERVICOS, barbeiros=BARBEIROS)

    return render_template('agendamento.html', servicos=SERVICOS, barbeiros=BARBEIROS)